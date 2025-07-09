import os
import sys
import uuid
import api

# 初始session_id生成或获取
session_id = ''
if not os.path.exists("session_id.txt"):
    session_id = uuid.uuid4()
else:
    with open("session_id.txt", "r", encoding='utf-8') as f:
        session_id = f.read()

# API对象
ycj = api.YunchengjiAPI(session_id)

def logout():
    """
    登出系统
    :return: None
    """
    print('登出中')
    content = ycj.logout()
    with open('session_id.txt', 'w+', encoding='utf-8') as f:
        f.write(content)

# 获取用户名密码
user = input("输入手机号/用户名(按Enter键确认)：")
pw = input("输入密码(按Enter键确认)：")

# 登录
print('登录中')
login_result = ycj.login(user,pw)
if login_result == -1:
    print('用户名或密码错误')
    sys.exit(1)

# 获取考试列表
print('获取考试列表中')
result1 = ycj.get_exam_list()
# 整理并显示考试列表
exams = []
for i in result1:
    exams.append({'desc':'{} {} {} {} {}'.format(i['studentname'],i['date'],i['examdesc'],i['examtypestr'],i['name']),'id':i['id']})
print('考试列表：')
for i in range(len(exams)):
    print('[{}] {}'.format(i+1,exams[i]['desc']))
print('[{}] 手动输入考试ID'.format(len(exams)+1))
# 选择考试
sel_exam = {}
try:
    sel_exam_num = int(input('请输入要获取的考试的序号(按Enter键确认)：'))
    if sel_exam_num == len(exams)+1:
        sel_exam['id'] = int(input('请输入要获取的考试的考试ID(按Enter键确认)：'))
    else:
        sel_exam = exams[sel_exam_num-1]
except ValueError:
    print('输入数据不合规')
    logout()
    sys.exit(1)
except IndexError:
    print('不存在该考试')
    logout()
    sys.exit(1)

# 获取考试详情
print('获取考试详情中')
result2 = ycj.get_exam_detail_total(sel_exam['id'])
# 整理并保存考试详情
if sel_exam_num == len(exams)+1:
    sel_exam['desc'] = '{} {} {}'.format(result2['studentname'],result2['examTypeStr'],result2['examName'])
text1 = '{}  实际成绩：{:<7} 卷面成绩：{:<7} 班级排名：{:<3} 学校排名：{:<5} 全市排名：{:<6}'
output = [sel_exam['desc']]
for i in result2['stuOrder']['subjects']:
    output.append(text1.format(i['name'],i['score'],i['paperScore'],i['classOrder'],i['schoolOrder'],i['unionOrder']))
scoreGap = result2['stuOrder']['scoreGap']
text2 = '总人数  班级：{:<7}  学校：{:<7}  全市：{:<7}\n最高分  班级：{:<7}  学校：{:<7}  全市：{:<7}\n平均分  班级：{:<7}  学校：{:<7}  全市：{:<7}'.format(scoreGap['classNum'],scoreGap['schoolNum'],scoreGap['unionNum'],scoreGap['classTop'],scoreGap['schoolTop'],scoreGap['unionTop'],scoreGap['classAvg'],scoreGap['schoolAvg'],scoreGap['unionAvg'])
output.append(text2)
# 写入文件
if not os.path.exists('output'):
    os.mkdir('output')
with open('output/{}.txt'.format(sel_exam['desc']),'w+',encoding='utf-8') as f:
    f.write('\n'.join(output))
print('结果已保存')

# 登出
logout()