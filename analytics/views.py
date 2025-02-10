from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Avg, F
from user_agents import parse
from .models import Visit
from datetime import timedelta


def get_visits_data(start_date, end_date):
    visits = Visit.objects.filter(entered_at__gte=start_date, entered_at__lte=end_date)

    daily_data = visits.extra({'day': "strftime('%%Y-%%m-%%d', entered_at)"}).values('day').annotate(count=Count('id'))
    chart_labels = [item['day'] for item in daily_data]
    chart_data = [item['count'] for item in daily_data]

    country_visits = visits.values('country').annotate(visit_count=Count('id'))
    country_names = [item['country'] if item['country'] else "Unknown" for item in country_visits]
    visit_data = [item['visit_count'] for item in country_visits]

    visitor_details = visits.values('ip', 'country', 'entered_at').order_by('-entered_at')

    device_stats = {"computer": 0, "mobile": 0}
    for visit in visitor_details:
        user_agent = parse(visit.get('user_agent', "Unknown"))
        if user_agent.is_mobile:
            device_stats["mobile"] += 1
        else:
            device_stats["computer"] += 1

    unique_visits = visits.values('ip').distinct().count()
    average_view_time = visits.filter(left_at__isnull=False).annotate(
        view_time=F('left_at') - F('entered_at')
    ).aggregate(Avg('view_time'))['view_time__avg']

    minutes, seconds = (0, 0)
    if average_view_time:
        total_seconds = average_view_time.total_seconds()
        minutes, seconds = divmod(int(total_seconds), 60)

    return chart_labels, chart_data, visit_data, country_names, unique_visits, minutes, seconds, visitor_details, device_stats


@login_required
def dashboard(request):
    today = timezone.now()
    start_of_day = today - timedelta(days=7)
    end_of_day = today

    data = get_visits_data(start_of_day, end_of_day)
    chart_labels, chart_data, visit_data, country_names, unique_visits, minutes, seconds, visitor_details, device_stats = data

    context = {
        'total_visits': sum(visit_data),
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'visit_data': visit_data,
        'country_names': country_names,
        'unique_visits': unique_visits,
        'average_view_time_minutes': minutes,
        'average_view_time_seconds': seconds,
        'start_date': start_of_day.strftime('%Y-%m-%d'),
        'end_date': end_of_day.strftime('%Y-%m-%d'),
        'visitor_details': visitor_details,
        'device_stats': device_stats,
    }
    return render(request, 'dashboard.html', context)

def get_data_by_date(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not start_date or not end_date:
            return JsonResponse({'error': 'Invalid dates'}, status=400)

        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d')

        data = get_visits_data(start_date, end_date)
        chart_labels, chart_data, visit_data, country_names, unique_visits, minutes, seconds, visitor_details, device_stats = data

        visitor_details_list = [
            {'ip': v['ip'], 'country': v['country'] or "Unknown", 'entered_at': v['entered_at'].strftime('%Y-%m-%d %H:%M:%S')}
            for v in visitor_details
        ]

        return JsonResponse({
            'chart_labels': chart_labels,
            'chart_data': chart_data,
            'visitor_details': visitor_details_list,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
