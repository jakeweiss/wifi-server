from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from server.models import *

import json
from django.utils import timezone
from datetime import timedelta

# Create your views here.

def index(request):
    metrics = Metric.objects.all()
    rssi_values = [metric.rssi for metric in metrics]
    rssi_min = min(rssi_values)
    rssi_max = max(rssi_values)
    rssi_avg = sum(rssi_values)/len(rssi_values)
    context = {'metrics_len': len(metrics), 'min': rssi_min, 'max': rssi_max,
    'avg':rssi_avg}
    return render(request, 'server/index.html', context)


@csrf_exempt
def post_metric(request):
    try:
        print("Test:", request.body)
        d = json.loads(request.body.decode('utf8'))
        print("Incoming Post Request:", d)
        for row in d:
            lat = row.get("lat")
            lon = row.get("lon")
            location = Location(latitude = lat, longitude = lon)
            location.save()
            ssid = row.get("ssid")
            security = row.get("security")
            network = Network(ssid = ssid, security = security)
            network.save()
            mac = row.get("mac")
            router = Router(network=network, mac = mac)
            router.save()
            rssi = row.get("rssi")
            metric = Metric(location=location,router=router,rssi=rssi)
            metric.save()
        return HttpResponse("Thanks!")
    except Exception as e:
        print(e)
        return HttpResponseBadRequest("Woops! {}".format(e))

def get_metrics(request):
    query_dict = request.GET
    first = query_dict.get("first")
    if first=='true':
        metrics = Metric.objects.all()
    else:
        time_threshold = timezone.now() - timedelta(seconds=30)
        metrics = Metric.objects.filter(datetime__gt=time_threshold)
    data = []
    for metric in metrics:
        row = {}
        row['latitude'] = metric.location.latitude
        row['longitude'] = metric.location.longitude
        row['network'] = metric.router.network.ssid
        row['rssi'] = metric.rssi
        data.append(row)
    return HttpResponse(json.dumps(data))
