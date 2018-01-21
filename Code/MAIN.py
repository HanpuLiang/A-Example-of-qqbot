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
            ComAdd = '添加口令格式：\n Command Add!\n 口令&你的口令&\n 回复&你的回复内容&\n 【如】\n Command Add!\n 口令&吃了么&\n 回复&吃啦吃啦，可香呢&'
            ComDel = '删除口令格式：\n Command Delete!\n 口令&要删除的口令&\n 【如】\n Command Delete!\n 口令&吃了么&'
            yiliyaFunc = '伊莉雅目前有三大功能:\n1)指定词回复。对于某些特定的词可以予以回复。\n2)签到系统。通过【签到】【打卡】【冒泡】这三个语句可以进行签到并获得积分。\n3)抢劫系统。抢走某人的积分。如：抢劫@张三\n4)天气查询系统。查询方式：天气检测 城市\n就这么多啦！'
            otherSenList = {'不喜欢你':['为嘛不喜欢我呀'], 
                            '士郎':['士郎可是我亲爱的欧尼酱!'], 
                            '凉扑扑':['叫我的Master干嘛？'], 
                            '不高兴':['乖~不高兴那就吃东西', '摸摸头~开心了没呀~'],
                            '不开心':['乖~不开心那就吃东西'],
                            '高兴':['高兴个mmp呦'],
                            '开心':['在开心什么呀？'],
                            '晚安':['大家晚安呦~~~'], 
                            '果冻冻':['果冻冻不是我家的小可爱嘛？'], 
                            '汤圆圆':['汤圆圆是我家的二可爱！'], 
                            '矿大':['悄咪咪地给你说，我可是出生在矿大的呢'], 
                            '早安':['大家早安呀，睡得舒服不？'], 
                            '天气':['今天天气？好的不得了呀哈哈哈'], 
                            '我喜欢你':['我也喜欢你噢么么哒~'], 
                            '卧槽':['讲文明讲礼貌！'], 
                            '傻逼':['不许骂人！！'], 
                            '想问下':['嗯嗯，有什么可以帮助你么？'], 
                            '可爱':['可爱可爱，特别可爱！(OS: 没我可爱咯)'], 
                            '什么情况':['没啥情况，就是这样子的咯'], 
                            '扎心':['没事没事么么哒'], 
                            '机器人':['郑重声明，本群机器人我最萌！'], 
                            '枪毙':['嘤嘤嘤，不要枪毙我'], 
                            '复杂':['人家的心里也很复杂的呢~'], 
                            '苟':['唱诗班！预备，唱！', '富贵！勿相忘！', '全姓名于乱世！'], 
                            '太行之阳':['莘莘学子救国种老公~'], 
                            '妈耶':['妈耶，吓了我一大跳'], 
                            '妈呀':['抱歉，我没有当妈业务。。'], 
                            '好的':['好的好的，就知道说好的'], 
                            '添加口令':[ComAdd], 
                            '删除口令':[ComDel], 
                            '全体成员':['叫伊莉雅干什么呀？'], 
                            '哈哈':['笑笑笑，成天就知道笑', '笑什么笑，作业写完了么！'], 
                            '秀':['秀秀秀，陈独秀的蒂花之秀,我能摸摸你的奖杯嘛?'], 
                            '厉害':['厉害厉害'], 
                            '复习':['复个啥习起来嗨'], 
                            '程娟娟':['欸呦呦，程娟娟不是大美铝嘛？', '最喜欢程娟娟了！', '略略略'], 
                            '知道':['你知道个p'], 
                            '现代科技论文':['现代科技论文发邮箱82185184@qq.com里呦'],
                            '泷泽萝拉':['你在说神马？我听不懂欸(嘿嘿嘿？)'], 
                            '汉普':['叫我主人干嘛?'], 
                            '作业':['没有作业没有作业！！'], 
                            '物理':['一时学物理，终身学物理！'], 
                            '屁':['屁屁屁，就知道屎尿屁！'], 
                            '喵':['汪汪汪！！！汪汪汪！！！', '叽叽叽！叽叽叽！', '咩咩咩~咩咩咩~','呱'], 
                            '什么鬼':['饿死鬼', '饱死鬼', '牡丹花下龟'], 
                            '嘤':['嘤嘤嘤，我要锤爆你的小胸胸！', '要抱抱！', '要亲亲！'], 
                            '抱':['抱抱~么么哒！', '给你一个大熊抱！', '左三圈右三圈'], 
                            '亲':['么么哒！', '么么哒!!x2', '么么哒!!!x3'], 
                            '想你':['么么，我也想你啦！', '想我就快亲亲我！', '想我就快抱抱我！'], 
                            '重复':['我没有重复！是你看错了！', '我是不会重复说话滴！'], 
                            'http':['什么po网址，我都看不了', '天呐，这里有个人竟然发网址！'], 
                            '明天':'明日复明日，明日何其多', 
                            '投票':['拒绝qq上转发微信投票！', '已投', '投票有奖励嘛?', '我是投给小红好呢？还是给小丽好呢？'], 
                            'exm':['事实就如此！不用怀疑！'], 
                            '伊莉雅的功能':[yiliyaFunc], 
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
