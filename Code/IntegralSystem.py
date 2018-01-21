import time
import json
import random

int_file = 'C:\\Users\\vento\\Documents\\QQBotSentence\\Integral_users.txt'
def IntSignIn(bot, contact, member):
    if member != None:
        with open(int_file) as file_obj:
            #字典，值为列表[今天打卡状态1215, 积分总值]
            integral_users = json.load(file_obj)
        
        #记录今天时间
        time_today = str(time.localtime(time.time()).tm_mon)+str(time.localtime(time.time()).tm_mday)
        integral_users['today'] = time_today

        if integral_users.__contains__(member.qq) == False:
            integral_users[member.qq] = ['0', 0]
        state_users = integral_users[member.qq]
        state_today = integral_users['today']

        #如果打卡时间不是今天，则打卡
        if state_users[0] != state_today:
            score = random.randint(1, 30)
            state_users[0] = state_today
            state_users[1] += score
            users_str = '恭喜'+member.name+'打卡成功！获得积分'+str(score)+'\n目前拥有积分'+str(state_users[1])+'\n请再接再厉！'
            bot.SendTo(contact, users_str, resendOn1202=False)
        else:
            score = random.randint(1, 15)
            state_users[1] -= score
            users_str = member.name+',你今天都打过卡了你还打卡,扣你'+str(score)+'分\n目前拥有积分'+str(state_users[1])+'\n下次注意点！'
            bot.SendTo(contact, users_str, resendOn1202=False)
        integral_users[member.qq] = state_users

        with open(int_file, 'w') as file_obj:
            json.dump(integral_users, file_obj)
            print('已写入积分系统')
    return True

def IntegralRob(bot, contact, member, content):
    '''-------积分抢劫-------'''
    if member != None:
        #更新名字
        update = bot.List('group', contact.name)
        if update:
            up = update[0]
            bot.Update(up)
        #得到抢劫者与被抢劫者的名字与qq
        robber = member.qq
        beRobbeder_name = content.strip('抢劫@')
        beRobbeder_name = beRobbeder_name.strip(' ')
        if random.random() < 0.3:
            #没能抢劫成功
            bot.SendTo(contact, member.name+'，你被'+beRobbeder_name+'一下子给打翻在地，没能抢劫成功。')
        else:
            #抢劫成功
            beRobbeder_qq = ''
            liveFlag = True
            gList = bot.List('group', contact.name)[0]
            for item in bot.List(gList):
                if item.name == beRobbeder_name:
                    beRobbeder_qq = item.qq
                    break
            else:
                liveFlag = False
                bot.SendTo(contact, member.name+', '+beRobbeder_name+'都不在这个群里你还要抢劫Ta')
            if liveFlag:
                #得到每个人的积分
                int_file = 'C:\\Users\\vento\\Documents\\QQBotSentence\\Integral_users.txt'
                with open(int_file) as file_obj:
                    integral_users = json.load(file_obj)
                
                #判断两人是否存在积分库中
                if integral_users.__contains__(robber) == False:
                    integral_users[robber] = ['0', 10] 
                if integral_users.__contains__(beRobbeder_qq) == False:
                    integral_users[beRobbeder_qq] = ['0', 10] 
                
                #抢劫得到的积分
                range_high = int(int(integral_users[beRobbeder_qq][1])/4*0.08)
                range_low = 1
                
                #判断被抢劫者有没有积分
                if int(integral_users[beRobbeder_qq][1]) <= 0:
                    bot.SendTo(contact, member.name+'，'+beRobbeder_name+'人家都没积分了你还抢劫！')
                else:
                    if range_high < range_low:
                        range_high, range_low = range_low, range_high
                    score_rob = random.randint(range_low, range_high)
                    integral_users[robber][1] += score_rob
                    integral_users[beRobbeder_qq][1] -= score_rob
                    bot.SendTo(contact, member.name+'，'+beRobbeder_name+'被你从后面扇了一个大耳瓜子，从口袋里里掉出了'+str(score_rob)+'点积分，你屁颠屁颠的跑了')
                    with open(int_file, 'w') as file_obj:
                        json.dump(integral_users, file_obj)
                        print('抢劫完成')
    else:
        bot.SendTo(contact, '老哥，只有群里才能抢劫的')


def InquireIntegral(bot ,contact, member, content):
    '''-------查询积分-------'''
    with open(int_file) as file_obj:
        integral_users = json.load(file_obj)
    if contact.ctype == 'buddy':
         man_qq = contact.qq
         man_name = contact.name
    else:
        man_qq = member.qq
        man_name = member.name
    man_integral = integral_users[man_qq][1]
    bot.SendTo(contact, man_name+', 你的积分现在有'+str(man_integral)+', 真是好厉害啊！')