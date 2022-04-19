from django.http import HttpResponse
from django.utils import timezone
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view, permission_classes

from .models import Venue, Member, VisitingRecord
from .permissions import HasEnterPermission, HasExitPermission, HasViewVisitingRecordsPermission


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


@api_view(['GET'])
@permission_classes([HasViewVisitingRecordsPermission])
def trace_venue(request):
    serializer = TraceSerializer(data=request.data)

    if not serializer.is_valid():
        return HttpResponse(status=400)

    hku_id = serializer.data['hku_id']
    start_datetime = serializer.data['start_datetime']
    end_datetime = serializer.data['end_datetime']

    venues_arrived = Venue.objects.filter()
