from django.shortcuts import render
from django.views.generic import View
from .models import Upload
from django.http import HttpResponsePermanentRedirect, HttpResponse
import random
import string
import datetime
import json
from django.db.models import Q


# Create your views here.

#定义一个HomeView类,收到get请求就返回
class HomeView(View):
    def get(self, request):
        return render(request, 'base.html', {})

    def post(self, request):
        if request.FILES: #如果post有文件
            file = request.FILES.get('file') #获取文件
            name = file.name
            size = int(file.size)
            with open('static/file/' + name, 'wb') as f: #写入文件
                f.write(file.read())
            code = ''.join(random.sample(string.digits, 8)) #生成随机八位的code
            u = Upload(
                path = 'static/file/' + name,
                name = name,
                Filesize = size,
                code = code,
                PCIP = str(request.META['REMOTE_ADDR']),#上传文件的用户ip
            )
            u.save()
            return HttpResponsePermanentRedirect("/s/" + code)#重定向到展示文件的页面



class DisplayView(View): #展示文件
    def get(self, request, code):
        u = Upload.objects.filter(code=str(code)) #查找
        if u:
            for i in u:
                i.DownloadDocount += 1 #访问次数+1
                i.save()
        return render(request, 'content.html', {"content": u})


class MyView(View):
    def get(self, request):
        IP = request.META['REMOTE_ADDR'] #获取用户IP
        u = Upload.objects.filter(PCIP=str(IP)) #查找数据
        for i in u:
            i.DownloadDocount += 1
            i.save()
        return render(request, 'content.html', {"content": u})


class SearchView(View):
    def get(self, request):
        code = request.GET.get("kw") #获取get请求中的kw值,即搜索的内容
        u = Upload.objects.filter(Q(name__icontains=str(code)))
        data = {} # 存放查询结果
        if u:
            for i in range(len(u)): #将结果放入data
                u[i].DownloadDocount += 1
                u[i].save()
                data[i] = {}
                data[i]['download'] = u[i].DownloadDocount
                data[i]['filename'] = u[i].name
                data[i]['id'] = u[i].id
                data[i]['ip'] = str(u[i].PCIP)
                data[i]['size'] = u[i].Filesize
                data[i]['time'] = str(u[i].Datatime.strftime('%Y-%m-%d %H:%M'))
                #时间格式化
                data[i]['key'] = u[i].code
        return HttpResponse(json.dumps(data), content_type="application/json") #返回json格式
