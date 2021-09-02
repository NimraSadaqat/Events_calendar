from calendar import HTMLCalendar
import calendar
from .models import Event
from dateutil import parser
from datetime import timedelta, datetime
from djongo.models import Q
from dateutil import parser
class WeekCalendar(HTMLCalendar):
    start_date = None
    year2 = None
    month2 = None
    dates = None
    def __init__(self, year1=None, month1=None, day=None):
        self.year1 = year1
        self.month1 = month1
        self.day = day

        self.start_date = str(self.year1)+" "+str(self.month1)+" "+str(self.day)
        self.start_date = parser.parse(self.start_date)
        self.dates = [self.start_date + timedelta(days=d) for d in range(7)]
        compare_month = self.dates[0].month
        compare_year = self.dates[0].year
        for d in range(1,7):
            if self.dates[d].month != compare_month:
                self.month2 = self.dates[d].month

                if self.dates[d].year != compare_year:
                    self.year2 = self.dates[d].year

                break
        super(WeekCalendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        # str_day = str(day)
        if len(str(day))==1:
            str_day = "0"+str(day)
        else:
            str_day = str(day)
        events_per_day = events.filter(day=str_day)
        d = ''
        for event in events_per_day:
            d += f'<div class="event mb-1 p-1"> {event.title} </div>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, dates, events):
        week = ''
        for d in dates:
            week += self.formatday(d.day, events)
        return f'<tr> {week} </tr>'

    def month_with_zero(self, month):
        if len(str(self.month))==1:
            month = "0"+str(self.month)
        else:
            month = str(self.month)
        return month
    # # formats a month as a table
    # # filter events by year and month
    def formatmonth(self, withyear=True):
        cal = '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        if len(str(self.month1))==1:
            month1 = "0"+str(self.month1)
        else:
            month1 = str(self.month1)
        if self.month2 == None:
            events = Event.objects.filter(year=str(self.year1),month=month1)
            cal += f'{self.formatmonthname(self.year1, self.month1, withyear=withyear)}\n'
        else:
            if len(str(self.month2))==1:
                month2 = "0"+str(self.month2)
            else:
                month2 = str(self.month2)
            if self.year2 == None:
                events = Event.objects.filter(Q(year=str(self.year1),month=month1)|Q(year=str(self.year1),month=month2))
            else:
                events = Event.objects.filter(Q(year=str(self.year1),month=month1)|Q(year=str(self.year2),month=month2))
            cal += f'{self.formatmonthname(self.year1, self.month1, withyear=withyear)}'
            if self.year2 == None:
                cal += f'{self.formatmonthname(self.year1, self.month2, withyear=withyear)}\n'
            else:
                cal += f'-{self.formatmonthname(self.year2, self.month2, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        # for week in self.monthdays2calendar(self.year, self.month):
        cal += f'{self.formatweek(self.dates, events)}\n'
        return cal
