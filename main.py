import os
import sys
import uuid
import api

# 提示文本
text1 = '{}  实际成绩：{:<7}/{:<7} 卷面成绩：{:<7}/{:<7} 班级排名：{:<3} 学校排名：{:<5} 全市排名：{:<6}'
text2 = '考生数  班级：{:<7} 学校：{:<7} 全市：{:<7}\n最高分  班级：{:<7} 学校：{:<7} 全市：{:<7}\n平均分  班级：{:<7} 学校：{:<7} 全市：{:<7}'
text3 = '题量  简单题：{:<7} 中等题：{:<7} 难题：{:<7}\n分值  简单题：{:<7} 中等题：{:<7} 难题：{:<7}\n丢分  简单题：{:<7} 中等题：{:<7} 难题：{:<7}\n得分  简单题：{:<7} 中等题：{:<7} 难题：{:<7}'
text4 = '{:<8} 得分：{:<5}/{:<5} 班得分率：{:<7} 校得分率：{:<7} 市得分率：{:<7}'
csv1 = '科目,实际成绩,卷面成绩,班级排名,学校排名,全市排名'
csv2 = "{},'{}/{},'{}/{},{},{},{}"
csv3 = '数据,班级,学校,全市'
csv4 = '考生数,{},{},{}\n最高分,{},{},{}\n平均分,{},{},{}'
csv5 = '数据,简单题,中等题,难题'
csv6 = '题量,{},{},{}\n分值,{},{},{}\n丢分,{},{},{}\n得分,{},{},{}'
csv7 = '题目,得分,班得分率,校得分率,市得分率'
csv8 = "'{},'{}/{},{},{},{}"

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
exam_list = ycj.get_exam_list()
# 整理并显示考试列表
exams = []
for i in exam_list:
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
exam_detail_total = ycj.get_exam_detail_total(sel_exam['id'])
# 整理并保存考试详情
if sel_exam_num == len(exams)+1:
    sel_exam['desc'] = '{} {} {}'.format(exam_detail_total['studentname'],exam_detail_total['examTypeStr'],exam_detail_total['examName'])
output = [sel_exam['desc'],'全科','成绩单']
csv_content = [sel_exam['desc'],'全科','成绩单',csv1]
for i in exam_detail_total['stuOrder']['subjects']:
    output.append(text1.format(i['name'],i['score'],i['fullScore'],i['paperScore'],i['fullScore'],i['classOrder'],i['schoolOrder'],i['unionOrder']))
    csv_content.append(csv2.format(i['name'],i['score'],i['fullScore'],i['paperScore'],i['fullScore'],i['classOrder'],i['schoolOrder'],i['unionOrder']))
scoreGap = exam_detail_total['stuOrder']['scoreGap']
output.append('分数差距')
csv_content.append('分数差距')
output.append(text2.format(scoreGap['classNum'],scoreGap['schoolNum'],scoreGap['unionNum'],scoreGap['classTop'],scoreGap['schoolTop'],scoreGap['unionTop'],scoreGap['classAvg'],scoreGap['schoolAvg'],scoreGap['unionAvg']))
csv_content.append(csv3)
csv_content.append(csv4.format(scoreGap['classNum'],scoreGap['schoolNum'],scoreGap['unionNum'],scoreGap['classTop'],scoreGap['schoolTop'],scoreGap['unionTop'],scoreGap['classAvg'],scoreGap['schoolAvg'],scoreGap['unionAvg']))
output.append('')
csv_content.append('')

# 获取科目列表
print('获取科目列表中')
subject_list = ycj.get_subject_list(sel_exam['id'])
for i in subject_list:
    print('获取 {} 单科详情中'.format(i['name']))
    output.append(i['name'])
    csv_content.append(i['name'])
    # 获取数据
    subject_data = ycj.get_exam_detail_subject(sel_exam['id'],i['id'])
    questions_data = ycj.get_exam_detail_subject_questions(sel_exam['id'],i['id'])
    # 综合数据
    output.append('分数差距')
    csv_content.append('分数差距')
    scoreGap = subject_data['stuOrder']['scoreGap']
    csv_content.append(csv3)
    output.append(text2.format(scoreGap['classNum'],scoreGap['schoolNum'],scoreGap['unionNum'],scoreGap['classTop'],scoreGap['schoolTop'],scoreGap['unionTop'],scoreGap['classAvg'],scoreGap['schoolAvg'],scoreGap['unionAvg']))
    csv_content.append(csv4.format(scoreGap['classNum'],scoreGap['schoolNum'],scoreGap['unionNum'],scoreGap['classTop'],scoreGap['schoolTop'],scoreGap['unionTop'],scoreGap['classAvg'],scoreGap['schoolAvg'],scoreGap['unionAvg']))
    output.append('难度失分分析')
    csv_content.append('难度失分分析')
    output.append(text3.format(subject_data['loseScoreCount1'],subject_data['loseScoreCount2'],subject_data['loseScoreCount3'],subject_data['loseTotalScore1'],subject_data['loseTotalScore2'],subject_data['loseTotalScore3'],subject_data['loseScore1'],subject_data['loseScore2'],subject_data['loseScore3'],subject_data['loseTotalRateScore1'],subject_data['loseTotalRateScore2'],subject_data['loseTotalRateScore3']))
    csv_content.append(csv5)
    csv_content.append(csv6.format(subject_data['loseScoreCount1'],subject_data['loseScoreCount2'],subject_data['loseScoreCount3'],subject_data['loseTotalScore1'],subject_data['loseTotalScore2'],subject_data['loseTotalScore3'],subject_data['loseScore1'],subject_data['loseScore2'],subject_data['loseScore3'],subject_data['loseTotalRateScore1'],subject_data['loseTotalRateScore2'],subject_data['loseTotalRateScore3']))
    # 小分查询
    output.append('小分情况')
    csv_content.append('小分情况')
    csv_content.append(csv7)
    for j in range(len(subject_data['questRates'])):
        output.append(text4.format(subject_data['questRates'][j]['title'],questions_data[j]['score'],questions_data[j]['totalScore'],subject_data['questRates'][j]['classScoreRate'],subject_data['questRates'][j]['schoolScoreRate'],subject_data['questRates'][j]['unionScoreRate']))
        csv_content.append(csv8.format(subject_data['questRates'][j]['title'],questions_data[j]['score'],questions_data[j]['totalScore'],subject_data['questRates'][j]['classScoreRate'],subject_data['questRates'][j]['schoolScoreRate'],subject_data['questRates'][j]['unionScoreRate']))
    output.append('')
    csv_content.append('')

# 写入文件
if not os.path.exists('output'):
    os.mkdir('output')
with open('output/{}.txt'.format(sel_exam['desc']),'w+',encoding='utf-8') as f:
    f.write('\n'.join(output))
with open('output/{}.csv'.format(sel_exam['desc']),'w+',encoding='gbk') as f:
    f.write('\n'.join(csv_content))
print('结果已保存')

# 登出
logout()