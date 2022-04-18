from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import Venue, Member, VisitingRecord


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
