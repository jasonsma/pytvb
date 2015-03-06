from django.shortcuts import render
from django.http import HttpResponseRedirect
from tvb.models import Forum81Item

# Create your views here.

def index(request):
    return HttpResponseRedirect('/admin/tvb/forum81item/')

def clicked(request, obj_id):
    item = Forum81Item.objects.get(id=obj_id)
    if item.subscribe:
        Forum81Item.objects.filter(id=obj_id).update(subscribe=False)
    else:
        Forum81Item.objects.filter(id=obj_id).update(subscribe=True)
    return HttpResponseRedirect('/admin/tvb/forum81item/')

