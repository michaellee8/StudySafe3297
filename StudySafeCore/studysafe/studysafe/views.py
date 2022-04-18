from django.http import HttpResponse
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import Venue, Member, VisitingRecord
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime


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


@api_view(['POST'])
def enter(request):
    if not (request.user.has_perm('studysafe.can_enter_venue')):
        return HttpResponse(status=403)

    serializer = EnterExitSerializer(data=request.data)

    member = Member.objects.get(hku_id=serializer.hku_id)
    venue = Venue.objects.get(code=serializer.venue_code)

    existing_non_exited_records = VisitingRecord.objects.filter(
        member=member,
        venue=venue,
        entry_datetime__isnull=False,
        exit_datetime__isnull=True,
    )

    current_datetime = datetime.now()

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
        entry_datetime=datetime.now(),
        exit_datetime=None,
    )

    return HttpResponse(status=204)


@api_view(['POST'])
def exit(request):
    if not (request.user.has_perm('studysafe.can_exit_venue')):
        return HttpResponse(status=403)

    serializer = EnterExitSerializer(data=request.data)

    member = Member.objects.get(hku_id=serializer.hku_id)
    venue = Venue.objects.get(code=serializer.venue_code)

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
            entry_datetime=datetime.now() - VisitingRecord.DEFAULT_DURATION,
            exit_datetime=datetime.now(),
        )
    else:
        for record in existing_non_exited_records:
            record.exit_datetime = datetime.now()
            record.save()

    return HttpResponse(status=204)
