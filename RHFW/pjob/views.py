from django.shortcuts import render
from .models import Job
import requests
import time
from urllib.parse import urlencode
from .forms import JobForm
import json
from pyecharts import Pie
import math
# Create your views here.


def paChong(request):
    if request.method == "GET":
        position = request.GET["position"]
        city = request.GET["city"]
        laGou(position, city)
        html_url = "pjob/{}_{}.html".format(city, position)
        return render(request, html_url)
    return render(request, "search.html", {"forms": JobForm()})

def laGou(position, city):
    start_url = "https://www.lagou.com/jobs/positionAjax.json?{}&needAddtionalResult=false"
    start_url = start_url.format(urlencode({"city": city}))
    refere_url = "https://www.lagou.com/jobs/list_{}?{}&cl=false&fromSearch=true&labelWords=&suginput=".format(
            urlencode({"position": position}).split("=")[-1], urlencode({"city": city}))
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": refere_url,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    }
    # proxy = {
    #     'http': 'http://119.179.148.196:8060',
    # }
    s = requests.Session()
    # s.get(refere_url, headers=headers, timeout=10, proxies=proxy)  # 请求首页获取cookies
    s.get(refere_url, headers=headers, timeout=10)  # 请求首页获取cookies
    cookie = s.cookies  # 为此次获取的cookies
    districts = dict()
    data = {
        "first": "true",
        "pn": "1",
        "kd": position
    }
    # rsp = s.post(url=start_url, headers=headers, data=data, proxies=proxy, cookies=cookie)
    rsp = s.post(url=start_url, headers=headers, data=data, cookies=cookie)
    districts = lagou_parse_json(rsp.text, districts)
    j = json.loads(rsp.text)
    totalCount = 0
    try:
        totalCount = int(j["content"]["positionResult"]["totalCount"])
    except:
        totalCount = 30
    pages = math.ceil(int(totalCount)/15)
    for i in range(2, int(pages+1)):
        data = {
            "first": "false",
            "pn": str(i),
            "kd": position
        }
        #rsp = s.post(url=start_url, headers=headers, data=data, proxies=proxy, cookies=cookie)
        rsp = s.post(url=start_url, headers=headers, data=data, cookies=cookie)
        districts = lagou_parse_json(rsp.text, districts)
        time.sleep(0.02)

    pie = Pie("职位信息统计", "{}{}职位行政区分布".format(city, position), title_pos='center', width=1300)
    columns = districts.keys()
    data = districts.values()
    # 加入数据，设置坐标位置为【75，50】，上方的colums选项取消显示，显示label标签
    pie.add(
        "统计",
        columns,
        data,
        center=[50, 60],
        is_legend_show=False,
        is_label_show=True)
    # 保存图表
    pie.render("/home/itianeru/PycharmProjects/RHFW/RHFW/pjob/templates/pjob/{}_{}.html".format(city, position))

def lagou_parse_json(text, districts):
    j = json.loads(text)
    try:
        jobList = j["content"]["positionResult"]["result"]
        for i in jobList:
            district = i["district"]
            if district not in districts.keys():
                districts[district] = 1
            else:
                districts[district] = districts[district] + 1
    except:
        pass
    return districts

def qianChengWuYou(position, city):
    pass


def zhiLian(position, city):
    pass