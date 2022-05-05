from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request

from .models import Venue, Member, VisitingRecord
from .permissions import HasEnterPermission, HasExitPermission, \
    HasViewVisitingRecordsPermission

# hku_id, end_time, start_time
TRACE_VENUE_SQL = """
SELECT DISTINCT sve.id, sve.code, sve.capacity, sve.location
FROM studysafe_venue sve
         JOIN studysafe_visitingrecord svr on sve.id = svr.venue_id
         JOIN studysafe_member sm on sm.id = svr.member_id
WHERE sm.hku_id = %s
  AND svr.entry_datetime <= %s
  AND svr.exit_datetime >= %s
ORDER BY sve.code ASC
"""

# hku_id, end_time, start_time
TRACE_CONTACTS_SQL = """
SELECT DISTINCT sm.id, sm.hku_id, sm.name
FROM studysafe_member sm
         JOIN studysafe_visitingrecord svr on sm.id = svr.member_id
         JOIN
     (
         SELECT svr.venue_id, svr.entry_datetime, svr.exit_datetime
         FROM studysafe_venue sve
                  JOIN studysafe_visitingrecord svr on sve.id = svr.venue_id
                  JOIN studysafe_member sm on sm.id = svr.member_id
         WHERE sm.hku_id = %s
           AND svr.entry_datetime <= %s
           AND svr.exit_datetime >= %s
     ) tvr ON svr.venue_id = tvr.venue_id
WHERE svr.entry_datetime <= tvr.exit_datetime
  AND svr.exit_datetime >= tvr.entry_datetime
"""


class VenueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'code', 'location', 'capacity']


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'hku_id', 'name']


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class VisitingRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VisitingRecord
        fields = ['id', 'venue', 'member', 'entry_datetime', 'exit_datetime']


class VisitingRecordViewSet(viewsets.ModelViewSet):
    queryset = VisitingRecord.objects.all()
    serializer_class = VisitingRecordSerializer


class EnterExitSerializer(serializers.Serializer):
    hku_id = serializers.CharField()
    venue_code = serializers.CharField()


class TraceSerializer(serializers.Serializer):
    hku_id = serializers.CharField()
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()


# noinspection DuplicatedCode
@extend_schema(
    request=EnterExitSerializer,
    responses={204: None},
)
@api_view(['POST'])
@permission_classes([HasEnterPermission])
def enter(request):
    serializer = EnterExitSerializer(data=request.data)

    if not serializer.is_valid():
        return HttpResponse(status=400)

    hku_id = serializer.data['hku_id']
    venue_code = serializer.data['venue_code']

    member = Member.objects.get(hku_id=hku_id)
    venue = Venue.objects.get(code=venue_code)

    existing_non_exited_records = VisitingRecord.objects.filter(
        member=member,
        venue=venue,
        entry_datetime__isnull=False,
        exit_datetime__isnull=True,
    )

    current_datetime = timezone.now()

    for record in existing_non_exited_records:
        if record.entry_datetime + VisitingRecord.DEFAULT_DURATION < current_datetime:
            record.exit_datetime = record.entry_datetime + VisitingRecord.DEFAULT_DURATION
        else:
            record.exit_datetime = current_datetime
        record.save()

    # Finished cleaning, now create the new entry
    VisitingRecord.objects.create(
        venue=venue,
        member=member,
        entry_datetime=timezone.now(),
        exit_datetime=None,
    )

    return HttpResponse(status=204)


# noinspection DuplicatedCode
@extend_schema(
    request=EnterExitSerializer,
    responses={204: None},
)
@api_view(['POST'])
@permission_classes([HasExitPermission])
def exit(request):
    serializer = EnterExitSerializer(data=request.data)

    if not serializer.is_valid():
        return HttpResponse(status=400)

    hku_id = serializer.data['hku_id']
    venue_code = serializer.data['venue_code']

    member = Member.objects.get(hku_id=hku_id)
    venue = Venue.objects.get(code=venue_code)

    existing_non_exited_records = VisitingRecord.objects.filter(
        member=member,
        venue=venue,
        entry_datetime__isnull=False,
        exit_datetime__isnull=True,
    )

    if len(existing_non_exited_records) == 0:
        # No exisiting records, we assume the enter time is two hours before
        VisitingRecord.objects.create(
            venue=venue,
            member=member,
            entry_datetime=timezone.now() - VisitingRecord.DEFAULT_DURATION,
            exit_datetime=timezone.now(),
        )
    else:
        for record in existing_non_exited_records:
            record.exit_datetime = timezone.now()
            record.save()

    return HttpResponse(status=204)


# noinspection DuplicatedCode
@extend_schema(
    parameters=[
        OpenApiParameter(
            name='hku_id',
            type=str,
            required=True,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name='start_datetime',
            type=OpenApiTypes.DATETIME,
            required=True,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name='end_datetime',
            type=OpenApiTypes.DATETIME,
            required=True,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses=VenueSerializer(many=True)
)
@api_view(['GET'])
@permission_classes([HasViewVisitingRecordsPermission])
def trace_venue(request: Request):
    hku_id = request.query_params['hku_id']
    start_datetime = request.query_params['start_datetime']
    end_datetime = request.query_params['end_datetime']

    if hku_id is None or start_datetime is None or end_datetime is None:
        return HttpResponse(status=400)

    venues_arrived = Venue.objects.raw(TRACE_VENUE_SQL,
                                       [hku_id, end_datetime, start_datetime])

    serializer = VenueSerializer(venues_arrived, many=True)

    return JsonResponse(serializer.data, safe=False)


# noinspection DuplicatedCode
@extend_schema(
    parameters=[
        OpenApiParameter(
            name='hku_id',
            type=str,
            required=True,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name='start_datetime',
            type=OpenApiTypes.DATETIME,
            required=True,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name='end_datetime',
            type=OpenApiTypes.DATETIME,
            required=True,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses=MemberSerializer(many=True)
)
@api_view(['GET'])
@permission_classes([HasViewVisitingRecordsPermission])
def trace_contacts(request: Request):
    hku_id = request.query_params['hku_id']
    start_datetime = request.query_params['start_datetime']
    end_datetime = request.query_params['end_datetime']

    if hku_id is None or start_datetime is None or end_datetime is None:
        return HttpResponse(status=400)

    members_arrived = Venue.objects.raw(TRACE_CONTACTS_SQL,
                                        [hku_id, end_datetime, start_datetime])

    serializer = MemberSerializer(members_arrived, many=True)

    return JsonResponse(serializer.data, safe=False)
