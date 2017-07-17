# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect

from models import *
import json
# Create your views here.

def required_login(fun):
    def _deco(request,*args,**kwargs):
        if request.session.get('is_login'):
            return fun(request,*args,**kwargs)
        else:
            return redirect('/login/')
    return _deco

@required_login
def data_view(request):
    if request.method == "POST":
        get_date = request.POST.getlist('get_date')
        print get_date[0]
        ret = {"DiskUse":"","MemUse":"","RedisUse":""}
        disk = []
        mem = []
        redis =[]
        all_data = ServerView.objects.filter(Date=get_date[0])
        for i in  all_data.values("Address","DiskUse","MemUse","RedisUse"):
            print i
            disk.append({i["Address"]:map(lambda x:float(x),i["DiskUse"].split(','))})
            mem.append({i["Address"]:map(lambda x:float(x),i["MemUse"].split(','))})
            redis.append({i["Address"]:map(lambda x:float(x),i["RedisUse"].split(','))})

        ret["DiskUse"] = disk
        ret["MemUse"] = mem
        ret["RedisUse"] = redis
        return HttpResponse(json.dumps(ret))
    user = request.session.get('is_login')['user']
    ret = {'data': '', 'error': '', 'user': user}

    return render_to_response('view/graph.html',ret)






