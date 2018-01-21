from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re

def GetWeather(bot, contact, member, content, city):
    
    print(content[4:])
    city_name = content[4:].strip(' ')

    if city.__contains__(city_name):
        city_code = city[city_name]
        resp=urlopen('http://www.weather.com.cn/weather/'+city_code+'.shtml')
        soup=BeautifulSoup(resp,'html.parser')
        #第一个包含class="tem"的p标签即为存放今天天气数据的标签
        tagToday=soup.find('p',class_="tem")  
        try:
            #有时候这个最高温度是不显示的，此时利用第二天的最高温度代替。
            temperatureHigh=tagToday.span.string  
        except AttributeError as e:
            #获取第二天的最高温度代替
            temperatureHigh=tagToday.find_next('p',class_="tem").span.string  
        #获取最低温度
        temperatureLow=tagToday.i.string  
        #获取天气
        weather=soup.find('p',class_="wea").string 

        reqStr = city_name+'的天气为:'+weather+'\n 温度区间为:'+temperatureHigh+'~'+temperatureLow+'\n 欢迎下次光临~'

        bot.SendTo(contact, reqStr)
    else:
        bot.SendTo(contact, '查个毛，只能查国内城市！')

