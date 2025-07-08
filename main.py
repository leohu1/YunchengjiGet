import os
import sys

import requests, uuid

user = input("输入手机号/用户名(按Enter键确认)：")
pw = input("输入密码(按Enter键确认)：")

# URL
login_url_1 = f"https://www.yunchengji.net/app/login?j_username={user}&j_password={pw}"
login_url_2 = "https://www.yunchengji.net/app/student/login"
index_url = "https://www.yunchengji.net/app/student/index"
total_url = "https://www.yunchengji.net/app/student/cj/report-total?seid={}"
logout_url_1 = "https://www.yunchengji.net/app/logout"
logout_url_2 = "https://www.yunchengji.net/app/student/session/sessionout"

# Headers
user_agent_1 = "ycj/5.7.0(Android;12)<okhttp>(<okhttp/3.10.0>)<brand_HONOR,model_SDY-AN00,maker_HONOR,device_Sandy>"
user_agent_2 = "Mozilla/5.0 (Linux; Android 12; SDY-AN00 Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046295 Mobile Safari/537.36"
cookies = "SESSIONID={}"

# 初始uuid生成
uuid_s = ''
if not os.path.exists("uuid.txt"):
    uuid_s = uuid.uuid4()
else:
    with open("uuid.txt","r",encoding='utf-8') as f:
        uuid_s = f.read()

# 登录
print('Login Stage 1')
response1 = requests.post(login_url_1, headers= {
    'User-Agent': user_agent_1,
    'Accept-Encoding': "gzip",
    'content-length': "0",
    'Cookie': cookies.format(uuid_s)
},allow_redirects=False)
uuid_s =  response1.cookies.get("SESSIONID")
print('uuid:{} Login Stage 2'.format(uuid_s))
response2 = requests.get(login_url_2, headers={
    'User-Agent': user_agent_1,
    'Accept-Encoding': "gzip",
    'Cookie':  cookies.format(uuid_s)
})

# 获取考试列表
print('Getting Exam List')
headers = {
    'User-Agent': user_agent_1,
    'Accept-Encoding': "gzip",
    'httpcache': "index",
    'content-length': "0",
    'Cookie': cookies.format(uuid_s)
}
response = requests.post(index_url, headers=headers)
if response.json()['result'] == 'sessionout':
    print('用户名或密码错误')
    sys.exit(1)
result = response.json()['desc']['selist']
exams = []
for i in result:
    exams.append({'desc':'{} {} {} {} {}'.format(i['studentname'],i['date'],i['examdesc'],i['examtypestr'],i['name']),'id':i['id']})
print('考试列表：')
for i in range(len(exams)):
    print('[{}] {}'.format(i+1,exams[i]['desc']))
print('[{}] 手动输入考试ID'.format(len(exams)+1))
sel_exam = {}
try:
    sel_exam_num = int(input('请输入要获取的考试的序号(按Enter键确认)：'))
    if sel_exam_num == len(exams)+1:
        sel_exam['id'] = int(input('请输入要获取的考试的考试ID(按Enter键确认)：'))
    else:
        sel_exam = exams[sel_exam_num-1]
except ValueError:
    print('输入数据不合规')
    sys.exit(1)
except IndexError:
    print('不存在该考试')
    sys.exit(1)

# 考试详情
print('Getting Exam Details')
response3 = requests.get(total_url.format(sel_exam['id']), headers= {
    'User-Agent': user_agent_2,
    'Accept': "application/json, text/plain, */*",
    'pragma': "no-cache",
    'cache-control': "no-cache",
    'x-requested-with': "com.wish.ycj",
    'sec-fetch-site': "same-origin",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://www.yunchengji.net/app/student/report/html/report.html",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'Cookie':  cookies.format(uuid_s)
})
result2 = response3.json()['desc']
if sel_exam_num == len(exams)+1:
    sel_exam['desc'] = '{} {} {}'.format(result2['studentname'],result2['examTypeStr'],result2['examName'])
# print('姓名  {}'.format(result2['studentname']))
text1 = '{}  实际成绩：{}  卷面成绩：{}  班级排名：{}  学校排名：{}  全市排名：{}'
output = [sel_exam['desc']]
for i in result2['stuOrder']['subjects']:
    # print(text1.format(i['name'],i['score'],i['paperScore'],i['classOrder'],i['schoolOrder'],i['unionOrder']))
    output.append(text1.format(i['name'],i['score'],i['paperScore'],i['classOrder'],i['schoolOrder'],i['unionOrder']))
scoreGap = result2['stuOrder']['scoreGap']
text2 = '参与考试的人数  班级：{}  学校：{}  全市：{}\n最高分  班级：{}  学校：{}  全市：{}\n平均分  班级：{}  学校：{}  全市：{}'.format(scoreGap['classNum'],scoreGap['schoolNum'],scoreGap['unionNum'],scoreGap['classTop'],scoreGap['schoolTop'],scoreGap['unionTop'],scoreGap['classAvg'],scoreGap['schoolAvg'],scoreGap['unionAvg'])
# print(text2)
output.append(text2)
# 写入文件
if not os.path.exists('output'):
    os.mkdir('output')
with open('output/{}.txt'.format(sel_exam['desc']),'w+',encoding='utf-8') as f:
    f.write('\n'.join(output))
print('结果已保存')

# 登出
print('Logout Stage 1')
headers2 = {
  'User-Agent': user_agent_1,
  'Accept-Encoding': "gzip",
  'content-length': "0",
  'Cookie': cookies.format(uuid_s)
}
requests.post(logout_url_1, headers=headers2)
print('Logout Stage 2')
headers3 = {
  'User-Agent': user_agent_1,
  'Accept-Encoding': "gzip"
}
response3 = requests.get(logout_url_2, headers=headers3)
with open('uuid.txt','w+',encoding='utf-8') as f:
    f.write(response3.cookies.get('SESSIONID'))