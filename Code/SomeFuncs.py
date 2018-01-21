import time
import json



def ShowAll(bot, contact, member, content, sentence1, sentence2, otherSenList):
    '''!-------展示所有口令-------!'''
    flag = 0
    outStr = '全部口令为：\n'
    outStr = outStr + '【可修改"全字"口令】\n'
    for item in sentence2:
        outStr = outStr + item + '-))' + sentence2[item] + '\n'
    outStr = outStr + '【不可修改"全字"口令】\n'
    for item in sentence1:
        outStr = outStr + item + '-))' + sentence1[item] + '\n'
    outStr = outStr + '【不可修改"存在字"口令】\n'
    for item in otherSenList:
        outStr = outStr + item + '-))' + otherSenList[item] + '\n'
    bot.SendTo(contact, outStr)
    
def CannotTouch(bot, contact, member, content, key, sentence):
    '''!-------不可修改口令禁令-------!'''
    flag = 0
    if sentence.__contains__(key):
        bot.SendTo(contact, '抱歉噢，这个指令不能够被修改的呢~')
        flag = 1
    return flag

def MasterCommands(bot, contact, member, content):
    '''!-------不反应或者反应-------!'''
    masterFlagFile_name = 'C:\\Users\\vento\\Documents\\QQBotSentence\\MasterFlag.txt'
    if member != None:
        if member.qq == '798258079':
            if content == '闭嘴吧！伊莉雅':
                bot.SendTo(contact, '好的好的，我闭嘴:(')
                with open(masterFlagFile_name, 'w') as file_obj:
                    json.dump('0', file_obj)
                    print('已修改为0')
            elif content == '说话吧，伊莉雅':
                bot.SendTo(contact, '我又能说话啦')
                with open(masterFlagFile_name, 'w') as file_obj:
                    json.dump('1', file_obj)
                    print('已修改为1')
    with open(masterFlagFile_name) as file_obj:
        flag = json.load(file_obj)
        print('已读取', flag)
    return flag
