import json
from django.shortcuts import render
import math
import requests
from django.views.generic import View
   
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
# Create your views here.
name = []
stars = []
date = []
count = []
def index(request):
    if request.method == "GET" :
        data = requests.get('https://api.github.com/orgs/amfoss/repos?sort=stars&per_page=10')
        data = json.loads(data.text)
        return render(request,'plot/index.html')

    elif request.method == "POST" :
        orgname  = request.POST['orgname']
        reponame = request.POST['reponame']
        timeFrom = request.POST['timeFrom']
        timeUntil = request.POST['timeUntil']

        if(orgname):
            data = requests.get('https://api.github.com/search/repositories?q=org:'+orgname+'&sort=stars&order=desc')
            data = json.loads(data.text)
            global name
            global stars
            global date
            global count
            name = []
            stars = []
            print(len(data))
            try:
                if(data["errors"]):
                    return Response("No repo found")
            except:
                if(len(data)>2):
                    for i in range(len(data["items"])):
                        if(len(name)<10):
                            print(data["items"][i]["name"])
                            name.append(data["items"][i]["name"])
                            stars.append(data["items"][i]["stargazers_count"])

        if(orgname and reponame and timeFrom and timeUntil):
            comData = requests.get('https://api.github.com/repos/'+ orgname + '/' + reponame + '/commits?until='+timeUntil+'&per_page=100')
            comData = json.loads(comData.text)
            print(comData)
            print(len(comData))
            date = []
            count = []
            try:
                if(comData["errors"]):
                    return Response("No repo found")
            except:
                if(len(comData)>2):
                    for i in range(len(comData)):
                        d = comData[i]["commit"]["author"]["date"]
                        d = d[0:10]
                        print(d)
                        if(d>=timeFrom):
                            date.append(d[0:10])
                my_dict = {i:date.count(i) for i in date}
                print(my_dict)
                date = my_dict.keys()
                count = my_dict.values()
        return render( request,'plot/index.html', {'script' : stars , 'div' : name} )

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'plot/index.html')

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
    global name
    global stars
    global date
    global count
    def get(self, request, format = None):
        labels = name
        chartLabel = "Stars"
        chartdata = stars
        linelabel = "Commits"
        lineLabels= date
        linedata = count
        data ={
                    "labels":labels,
                    "chartLabel":chartLabel,
                    "chartdata":chartdata,
                    "linedata":linedata,
                    "linelabel":linelabel,
                    "lineLabels":lineLabels,
             }
        return Response(data)

class RepoData(APIView):

    def post(self, request, format = None):
        print(request.data["orgname"])
        orgname  = request.data["orgname"]
        data = requests.get('https://api.github.com/search/repositories?q=org:'+orgname+'&sort=stars&order=desc')
        data = json.loads(data.text)
        name = []
        stars = []
        print(data)
        try:
            if(data["errors"]):
                return Response("No repo found")
        except:
            if(len(data)>2):
                for i in range(len(data["items"])):
                    if(len(name)<10):
                        name.append(data["items"][i]["name"])
                        stars.append(data["items"][i]["stargazers_count"])
            my_dict = []
            for i in range(len(name)):
                my_dict.append({"name":name[i],"stars":stars[i]})
            return Response(my_dict)