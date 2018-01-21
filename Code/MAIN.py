import json
from qqbotLHP import * 
import random
from QQBotWeather import *
import time
from IntegralSystem import *
import numpy as np

file_name1 = 'C:\\Users\\vento\\Documents\\QQBotSentence\\sentence.txt'
file_name2 = 'C:\\Users\\vento\\Documents\\QQBotSentence\\sentence_users.txt'

'''!-------不可修改口令-------!'''
with open(file_name1) as file_obj:
    sentence1 = json.load(file_obj)
    print('已读取', sentence1)

'''!-------可修改口令-------!'''
with open(file_name2) as file_obj:
    sentence2 = json.load(file_obj)
    print('已读取', sentence2)

'''!-------天气数据-------!'''
city_file = 'C:\\Users\\vento\\Documents\\QQBotSentence\\CityCodes.txt'
with open(city_file) as file_obj:
    city = json.load(file_obj)
    print('已写入天气')

'''!-------------测试区域开始---------------!'''
    
'''!-------------测试区域截止---------------!'''


def CommandAdd(bot, contact, member, content, sentence1):
    '''!-------添加口令-------!'''
    flag = 0
    key = ''
    val = ''
    for item in content:
        if item == '&' and flag == 0:
            flag = 1
            continue
        else: flag
        key = key + item if flag == 1 and item != '&' else key
        TouchFlag = CannotTouch(bot, contact, member, content, key, sentence1)
        if TouchFlag == 1: break
        if item == '&' and flag == 1:
            flag = 2
            continue
        else: flag
        if item == '&' and flag == 2:
            flag = 3
            continue
        else: flag
        val = val + item if flag == 3 and item != '&' else val
        flag = 4 if item == '&' and flag == 3 else flag
        if flag == 4:
            sentence2[key] = val
            bot.SendTo(contact, '添加成功~现在就可以试试啦！',  resendOn1202=False)
            break
    else:
        bot.SendTo(contact, '我好像没有收到正确格式噢', resendOn1202=False)

def CommandDelete(bot, contact, member, content, sentence1):
    '''!-------删除口令-------!'''
    flag = 0
    key = ''
    for item in content:
        if item == '&' and flag == 0:
            flag = 1
            continue
        else: flag
        key = key + item if flag == 1 and item != '&' else key
        TouchFlag = CannotTouch(bot, contact, member, content, key, sentence1)
        if TouchFlag == 1: break
        flag = 2 if item == '&' and flag == 1 else flag
        if flag == 2:
            sentence2.pop(key)
            bot.SendTo(contact, '删除成功~', resendOn1202=False)
            break
    else:
        bot.SendTo(contact, '我好像没有收到正确格式噢', resendOn1202=False)

def onQQMessage(bot, contact, member, content):
    #优先级一
    '''!-------识别是否是自己的话-------!'''
    if bot.isMe(contact, member):
        print('自己的命令')
    else: 
        #优先级二
        masterFlag = MasterCommands(bot, contact, member, content)
        if masterFlag == '1':
            '''!-------添加口令-------!'''
            if 'Command Add' in content:
                CommandAdd(bot, contact, member, content, sentence1)
            
            '''!-------删除口令-------!'''
            if 'Command Delete' in content:
                CommandDelete(bot, contact, member, content, sentence1)
            
            '''!-------字词识别指令字典存储-------!'''
            otherSenList = {'http':['什么po网址，我都看不了', '天呐，这里有个人竟然发网址！'], 
                            '明天':'明日复明日，明日何其多', 
                            '投票':['拒绝qq上转发微信投票！', '已投', '投票有奖励嘛?', '我是投给小红好呢？还是给小丽好呢？'], 
                            '伊莉雅':['叫我干嘛？'], 
                            }


            '''-------签到-------'''
            #优先级三
            if content == '签到' or content == '打卡' or content == '冒泡':
                intFlag = IntSignIn(bot, contact, member)
            else:
                #优先级四
                '''-------非签到-------'''
                if '@ME' in content:
                    '''-------艾特识别-------'''
                    outStr = member.name+', 叫我干嘛呀'
                    bot.SendTo(contact, outStr, resendOn1202=False)
                elif content[0:4] == '天气检测':
                    #优先级五
                    '''-------天气检测功能-------'''
                    GetWeather(bot, contact, member, content, city)
                else:
                    #优先级六
                    '''!-------抢劫系统-------!'''
                    if '抢劫' == content[0:2]:
                        IntegralRob(bot, contact, member, content)
                    elif '我的积分' == content:
                        #优先级七
                        InquireIntegral(bot ,contact, member, content)
                    else:
                        #优先级八
                        '''!-------不识别全程句子识别-------!'''
                        for item in otherSenList:
                            if item in content:
                                bot.SendTo(contact, random.choice(otherSenList[item]), resendOn1202=False)
                                break
                        else:
                            #优先级九
                            '''!-------全称句子识别-------!'''
                            if sentence1.__contains__(content):
                                bot.SendTo(contact, sentence1[content], resendOn1202=False)
                            if sentence2.__contains__(content):
                                bot.SendTo(contact, sentence2[content], resendOn1202=False)
                        
                        

                '''!-------全称句子存储-------!'''
                with open(file_name2, 'w')as file_obj:
                    json.dump(sentence2, file_obj)
            
            '''-------暂停三秒钟-------'''
            time.sleep(3)
