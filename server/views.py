from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from server.models import *

import json
# Create your views here.

def index(request):
    metrics = Metric.objects.all()

    context = {'metrics': metrics}
    print(metrics)
    return render(request, 'server/index.html', context)


@csrf_exempt
def post_metric(request):
    try:
        d = json.loads(request.body.decode('utf8'))
        lat = d.get("lat")
        lon = d.get("lon")
        location = Location(latitude = lat, longitude = lon)
        location.save()
        ssid = d.get("ssid")
        security = d.get("security")
        network = Network(ssid = ssid, security = security)
        network.save()
        mac = d.get("mac")
        router = Router(network=network, mac = mac)
        router.save()
        rssi = d.get("rssi")
        snr = d.get("snr")
        metric = Metric(location=location,router=router,rssi=rssi,snr=snr)
        metric.save()
        return HttpResponse("Thanks!")
    except Exception as e:
        return HttpResponseBadRequest("Woops! {}".format(e))

def get_metrics(request):
    metrics = Metric.objects.all()
    data = []
    for metric in metrics:
        row = {}
        row['latitude'] = metric.location.latitude
        row['longitude'] = metric.location.longitude
        row['network'] = metric.router.network.ssid
        row['rssi'] = metric.rssi
        data.append(row)
    return HttpResponse(json.dumps(data))
