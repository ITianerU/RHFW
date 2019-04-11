from django.shortcuts import render
import requests
import time
from urllib.parse import urlencode, quote
from .forms import JobForm
import json
from pyecharts import Pie
import math
from lxml import etree
# Create your views here.


def paChong(request):
    if request.method == "GET":
        position = request.GET["position"]
        city = request.GET["city"]
        # laGou(position, city)
        # qianChengWuYou(position, city)
        zhiLian(position, city)
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
    start_url = "https://search.51job.com/list/{},000000,0000,00,9,99,{},2,{}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
    city_code = {
        "北京": "010000", "上海": "020000", "广州": "030200", "深圳": "040000", "武汉": "180200",
        "西安": "200200", "杭州": "080200", "南京": "070200", "成都": "090200", "重庆": "060000",
        "东莞": "030800", "大连": "230300", "沈阳": "230200", "苏州": "070300", "昆明": "250200",
        "长沙": "190200", "合肥": "150200", "宁波": "080300", "郑州": "170200", "天津": "050000",
        "青岛": "120300", "济南": "120200", "哈尔滨": "220200", "长春": "240200", "福州": "110200"
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Host": "search.51job.com",
        "Referer": start_url.format(quote(city_code[city]), quote(position), 1),
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    }
    rsp = requests.get(start_url.format(quote(city_code[city]), quote(position), 1), headers=headers)
    html = etree.HTML(rsp.content)
    pages = html.xpath('//*[@id="resultList"]/div[2]/div[5]/text()')[1].replace(" / ", "")
    districts = dict()
    districts = qianChengWuYou_parse_html(html, districts)
    for i in range(2, int(pages)):
        headers["Referer"] = start_url.format(quote(city_code[city]), quote(position), i)
        rsp = requests.get(start_url.format(quote(city_code[city]), quote(position), 1), headers=headers)
        html = etree.HTML(rsp.content)
        districts = qianChengWuYou_parse_html(html, districts)
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

def qianChengWuYou_parse_html(html, districts):
    districts_list = html.xpath('//*[@id="resultList"]/div[@class="el"]/span[2]/text()')
    for district in districts_list:
        # district = district.encode("ISO-8859-1").decode('gb2312')
        if district not in districts.keys():
            districts[district] = 1
        else:
            districts[district] = districts[district] + 1
    return districts

def zhiLian(position, city):
    start_url = "https://fe-api.zhaopin.com/c/i/sou?"
    city_code = {
        "北京": "530", "上海": "538", "广州": "763", "深圳": "765", "武汉": "736",
        "西安": "854", "杭州": "653", "南京": "635", "成都": "801", "重庆": "551",
        "东莞": "779", "大连": "600", "沈阳": "599", "苏州": "639", "昆明": "831",
        "长沙": "749", "合肥": "664", "宁波": "654", "郑州": "719", "天津": "531",
        "青岛": "703", "济南": "702", "哈尔滨": "622", "长春": "613", "福州": "681",
        "无锡": "636", "厦门": "682", "石家庄": "565", "惠州": "773"
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Host": "fe-api.zhaopin.com",
        "Origin": "https://sou.zhaopin.com",
        "Referer": "https://sou.zhaopin.com/?jl={}&kw={}&kt=3&sf=0&st=0".format(city_code[city], quote(position)),
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    }
    data = {
        "pageSize": 90,
        "cityId": city_code[city],
        "workExperience": -1,
        "education": -1,
        "companyType": -1,
        "employmentType": -1,
        "jobWelfareTag": -1,
        "kw": position,
        "kt": 3,
        "userCode": 718661104,
    }
    rsp = requests.get(start_url, headers=headers, params=data)
    pages = math.ceil(int(json.loads(rsp.text)["data"]["numFound"]) / 90)
    districts = dict()
    if pages > 100:
        pages == 100
    for i in range(2, int(pages)):
        data["start"] = i * 90,
        rsp = requests.get(start_url, headers=headers, params=data)
        districts = zhiLian_parse_json(rsp.text, districts)
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

def zhiLian_parse_json(text, districts):
    j = json.loads(text)
    try:
        jobList = j["data"]["results"]
        for i in jobList:
            district = i["city"]["display"]
            if district not in districts.keys():
                districts[district] = 1
            else:
                districts[district] = districts[district] + 1
    except:
        pass
    return districts