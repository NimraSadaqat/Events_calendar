from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
import calendar
from .models import Event
from .utils import Calendar
from .week import WeekCalendar

# Create your views here.
def index(request):
    return render(request, 'calendar_app/main.html')

def get_date(req_day):
    if req_day:
        if isinstance(req_day, str):
            year, month = (int(x) for x in req_day.split('-'))
            return date(year, month, day=1)
        if isinstance(req_day, datetime.date):
            year = req_day.year
            month = req_day.month
            day= 1
    return datetime.today()

def get_date_week(req_day):
    if req_day:
        print("req_day")
        print(req_day)
        year, month, day = (int(x) for x in req_day.split('-'))
        print(date(year, month, day))
        return date(year, month, day)
    return datetime.today()

def get_week(req_day):
    weekday = req_day.isoweekday()
    print('weekday',weekday)
    # The start of the week
    if weekday==7:
        start = req_day
    else:
        start = req_day - timedelta(days=weekday-1)
    # build a simple range
    dates = [start + timedelta(days=d) for d in range(7)]
    # print(dates)
    return dates

def prev_week(req_day):
    start = req_day - timedelta(days=7)
    dates = [start + timedelta(days=d) for d in range(7)]
    date = 'date=' + str(dates[0].year) + '-' + str(dates[0].month)+ '-' + str(dates[0].day)
    return date
    # return dates[0]

def next_week(req_day):
    start = req_day + timedelta(days=1)
    dates = [start + timedelta(days=d) for d in range(7)]
    date = 'date=' + str(dates[0].year) + '-' + str(dates[0].month)+ '-' + str(dates[0].day)
    return date
    # return dates[0]

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar_app/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

class WeekView(generic.ListView):
    model = Event
    template_name = 'calendar_app/week_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("get_context_data")
        print(self.request.GET.get('date', None))
        d = get_date_week(self.request.GET.get('date', None))
        print("d")
        print(d)
        # d_week = d.isocalendar()[1]
        dates = get_week(d)

        print("dates6",dates[6])
        cal = WeekCalendar(dates[0].year, dates[0].month, dates[0].day)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_week'] = prev_week(dates[0])
        context['next_week'] = next_week(dates[6])
        return context

class AgendaListView(generic.ListView):
    model = Event
    template_name = 'calendar_app/agenda.html'

    def get_queryset(self):
        agenda = Event.objects.filter(start_time__gte = datetime.today()).order_by('start_time')
        return agenda
