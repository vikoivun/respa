from .models import Day, Resource, Period, Unit, ResourceType
from psycopg2.extras import DateTimeTZRange, DateRange, NumericRange
import datetime
import arrow
from collections import namedtuple
import django.db.models as djdbm
from django.utils import timezone
import pytz

OpenHours = namedtuple("OpenHours", ['opens', 'closes'])


class TimeWarp(object):

    def __init__(self, daytime=None, day=None, original_timezone=None):
        """
        Converts given daytime or day into UTC date time object
        and saves this and the original time zone object
        into object's fields

        :type daytime: datetime.datetime | None
        :type day: datetime.day | None
        :type original_timezone: basestring
        :rtype: None
        """
        if daytime:
            # Incoming datetetime
            if daytime.tzinfo:
                self._dt = pytz.utc.normalize(daytime)
                self._orig_zone = daytime.tzinfo
            else:
                if original_timezone:
                    zone = pytz.timezone(original_timezone)
                else:
                    zone = timezone.get_current_timezone()
                self._dt = zone.normalize(daytime)
                self._orig_zone = zone
        elif day:
            self._dt = pytz.utc.normalize(
                datetime.datetime.combine(day, datetime.time(0, 0)))
            self._orig_zone = pytz.utc
        else:
            # Now dates, well be the moment of creation
            self._dt = pytz.utc.normalize(datetime.datetime.now())
            self._orig_zone = pytz.utc


def get_opening_hours(begin, end, resources=None):
    """
    :type begin:datetime.date
    :type end:datetime.date
    :type resources: Resource | None
    :rtype: dict[datetime, dict[Resource, list[OpenHours]]]

    Find opening hours for all resources on a given time period.

    If resources is None, finds opening hours for all resources.

    This version goes through all regular periods and then all
    exception periods that are found overlapping the given
    time range. It builds a dict of days that has dict of
    resources with their active hours.

    TODO: There is couple optimization avenues worth exploring
    with prefetch or select_related for Periods'
    relational fields Unit, Resource and Day. This way all
    relevant information could be requested with one or two
    queries from the db.
    """
    if not resources:
        resources = Resource.objects.all()

    if not begin < end:
        end = begin + datetime.timedelta(days=1)

    d_range = DateRange(begin, end)

    periods = Period.objects.filter(
        djdbm.Q(resource__in=resources) | djdbm.Q(unit__in=resources.values("unit__pk")),
        duration__overlap=d_range).order_by('exception')

    begin_dt = datetime.datetime.combine(begin, datetime.time(0, 0))
    end_dt = datetime.datetime.combine(end, datetime.time(0, 0))

    # Generates a dict of time range's days as keys and values as active period's days

    # all requested dates are assumed closed
    dates = {r.date() : False for r in arrow.Arrow.range('day', begin_dt, end_dt)}

    for period in periods:

        if period.start < begin:
            start = begin_dt
        else:
            start = arrow.get(period.start)
        if period.end > end:
            end = end_dt
        else:
            end = arrow.get(period.end)

        if period.resource:
            period_resources = [period.resource]
        else:
            period_resources = period.unit.resources.filter(pk__in=resources)

        for res in period_resources:

            for r in arrow.Arrow.range('day', start, end):
                for day in period.days.all():
                    if day.weekday is r.weekday():
                        if not dates.get(r.date(), None):
                            dates[r.date] = {}
                        dates[r.date()].setdefault(
                                res, []).append(
                            OpenHours(day.opens, day.closes))

    return dates


def set():
    u1 = Unit.objects.create(name='Unit 1', id='unit_1')
    rt = ResourceType.objects.create(name='Type 1', id='type_1', main_type='space')
    Resource.objects.create(name='Resource 1a', id='r1a', unit=u1, type=rt)
    Resource.objects.create(name='Resource 1b', id='r1b', unit=u1, type=rt)
    Resource.objects.create(name='Resource 2a', id='r2a', unit=u1, type=rt)
    Resource.objects.create(name='Resource 2b', id='r2b', unit=u1, type=rt)

    # Regular hours for one week
    p1 = Period.objects.create(start=datetime.date(2015, 8, 3), end=datetime.date(2015, 8, 9),
                               unit=u1, name='regular hours')
    Day.objects.create(period=p1, weekday=0, opens=datetime.time(8, 0), closes=datetime.time(18, 0))
    Day.objects.create(period=p1, weekday=1, opens=datetime.time(8, 0), closes=datetime.time(18, 0))
    Day.objects.create(period=p1, weekday=2, opens=datetime.time(8, 0), closes=datetime.time(18, 0))
    Day.objects.create(period=p1, weekday=3, opens=datetime.time(8, 0), closes=datetime.time(18, 0))
    Day.objects.create(period=p1, weekday=4, opens=datetime.time(8, 0), closes=datetime.time(18, 0))
    Day.objects.create(period=p1, weekday=5, opens=datetime.time(12, 0), closes=datetime.time(16, 0))
    Day.objects.create(period=p1, weekday=6, opens=datetime.time(12, 0), closes=datetime.time(14, 0))

    # Two shorter days as exception
    exp1 = Period.objects.create(start=datetime.date(2015, 8, 6), end=datetime.date(2015, 8, 7),
                                 unit=u1, name='exceptionally short days', exception=True,
                                 parent=p1)
    Day.objects.create(period=exp1, weekday=3,
                       opens=datetime.time(12, 0), closes=datetime.time(14, 0))
    Day.objects.create(period=exp1, weekday=4,
                       opens=datetime.time(12, 0), closes=datetime.time(14, 0))

    # Weekend is closed as an exception
    exp2 = Period.objects.create(start=datetime.date(2015, 8, 8), end=datetime.date(2015, 8, 9),
                                 unit=u1, name='weekend is closed', closed=True, exception=True,
                                 parent=p1)
