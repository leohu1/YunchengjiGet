import requests


class YunchengjiAPI:
    def __init__(self,session_id):
        # URL
        self.login_url_1 = "https://www.yunchengji.net/app/login?j_username={}&j_password={}"
        self.login_url_2 = "https://www.yunchengji.net/app/student/login"
        self.index_url = "https://www.yunchengji.net/app/student/index"
        self.total_url = "https://www.yunchengji.net/app/student/cj/report-total?seid={}"
        self.subject_list_url = "https://www.yunchengji.net/app/student/cj/subject-list?seid={}"
        self.subject_url = "https://www.yunchengji.net/app/student/cj/report-subject?seid={}&subjectid={}"
        self.question_list_url = "https://www.yunchengji.net/app/student/cj/question-list?seid={}&subjectid={}"
        self.logout_url_1 = "https://www.yunchengji.net/app/logout"
        self.logout_url_2 = "https://www.yunchengji.net/app/student/session/sessionout"
        # Headers
        self.user_agent_1 = "ycj/5.7.0(Android;12)<okhttp>(<okhttp/3.10.0>)<brand_HONOR,model_SDY-AN00,maker_HONOR,device_Sandy>"
        self.user_agent_2 = "Mozilla/5.0 (Linux; Android 12; SDY-AN00 Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046295 Mobile Safari/537.36"
        self.headers1 = {
            'User-Agent': self.user_agent_1,
            'Accept-Encoding': "gzip"
        }
        self.headers2: dict[str, str] = {
            'User-Agent': self.user_agent_2,
            'Accept': "application/json, text/plain, */*",
            'pragma': "no-cache",
            'cache-control': "no-cache",
            'x-requested-with': "com.wish.ycj",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.yunchengji.net/app/student/report/html/report.html",
            'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        self.session = requests.Session()
        self.session.cookies = requests.utils.dict_from_cookiejar({"SESSIONID": session_id})


    def login(self,username,password):
        """
        登录系统
        :param username: 用户名
        :param password: 密码
        :return: None
        """
        
        response1 = self.session.post(self.login_url_1.format(username,password), headers={**self.headers1, 'content-length': "0"})
        if response1.url == 'sessionout':
            return -1
        return 0

    def get_exam_list(self):
        """
        获取考试列表
        :return:exams
        """
        response = self.session.post(self.index_url, headers={**self.headers1, 'httpcache': "index", 'content-length': "0"})
        if response.json()['result'] == 'sessionout':
            print('用户名或密码错误')
            return -1
        result = response.json()['desc']['selist']
        return result

    def get_exam_detail_total(self,exam_id):
        """
        获取考试详情
        :param exam_id: 考试id
        :return: exam_detail
        """
        
        response = self.session.get(self.total_url.format(exam_id), headers=self.headers2)
        result = response.json()['desc']
        return result

    def get_subject_list(self,exam_id):
        """
        获取科目列表
        :param exam_id: 考试id
        :return: subject_list
        """
    
        response = self.session.get(self.subject_list_url.format(exam_id), headers=self.headers2)
        result = response.json()['desc']
        return result

    def get_exam_detail_subject(self,exam_id,subject_id):
        """
        获取单科数据
        :param exam_id: 考试id
        :param subject_id: 科目id
        :return:单科数据
        """
        response = self.session.get(self.subject_url.format(exam_id,subject_id), headers=self.headers2)
        result = response.json()['desc']
        return result

    def get_exam_detail_subject_questions(self,exam_id,subject_id):
        """
        获取单科小分
        :param exam_id:考试id
        :param subject_id:科目id
        :return:单科小分数据
        """
        response = self.session.get(self.question_list_url.format(exam_id,subject_id), headers=self.headers2)
        result = response.json()['desc']['questions']
        return result

    def logout(self) -> str | None:
        """
        登出
        :return: session_id
        """
        self.session.post(self.logout_url_1, headers={**self.headers1, 'content-length': "0"})
        response = self.session.get(self.logout_url_2, headers=self.headers1)
        return response.cookies.get('SESSIONID')