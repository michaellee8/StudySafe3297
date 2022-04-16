from django.db import models
from datetime import timedelta


class Venue(models.Model):
    VENUE_TYPES = (
        ("LT", "Lecture Theatre"),
        ("CR", "Classroom"),
        ("TR", "Tutorial Room"),
    )
    code = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=150)
    capacity = models.IntegerField()


class Member(models.Model):
    hku_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=150)


# It would be hard to query whether the member is in the venue for
# the particular time if we put entry and exit timestamp in second rows.
# To prevent dual entry issues, if the user enters the same venue twice
# without exiting within the same two hours, the later entry time will be
# used for the exit time of the previous unclosed entry as well. If the user
# enter a with previous unclosed entry, the exit time of the previous entry
# will be taken as 2 hours after the previous entry time. If the user exits
# the venue without previously entering it, we will take the duration of the visit
# to be two hours as well.
class VisitingRecord(models.Model):
    DEFAULT_DURATION = timedelta(hours=2)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    entry_datetime = models.DateTimeField(null=True)
    exit_datetime = models.DateTimeField(null=True)
