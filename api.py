import uuid

import requests


class YunchengjiAPI:
    def __init__(self,session_id):
        # URL
        self.login_url_1 = "https://www.yunchengji.net/app/login?j_username={}&j_password={}"
        self.login_url_2 = "https://www.yunchengji.net/app/student/login"
        self.index_url = "https://www.yunchengji.net/app/student/index"
        self.total_url = "https://www.yunchengji.net/app/student/cj/report-total?seid={}"
        self.logout_url_1 = "https://www.yunchengji.net/app/logout"
        self.logout_url_2 = "https://www.yunchengji.net/app/student/session/sessionout"
        # Headers
        self.user_agent_1 = "ycj/5.7.0(Android;12)<okhttp>(<okhttp/3.10.0>)<brand_HONOR,model_SDY-AN00,maker_HONOR,device_Sandy>"
        self.user_agent_2 = "Mozilla/5.0 (Linux; Android 12; SDY-AN00 Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046295 Mobile Safari/537.36"
        self.cookies = "SESSIONID={}"
        # sessionID
        if session_id == "":
            self.session_id = str(uuid.uuid4())
        else:
            self.session_id = session_id

    def login(self,username,password):
        '''
        登录系统
        :return: None
        '''
        headers1 = {
            'User-Agent': self.user_agent_1,
            'Accept-Encoding': "gzip",
            'content-length': "0",
            'Cookie': self.cookies.format(self.session_id)
        }
        response1 = requests.post(self.login_url_1.format(username,password), headers=headers1, allow_redirects=False)
        self.session_id = response1.cookies.get("SESSIONID")
        headers2 = {
            'User-Agent': self.user_agent_1,
            'Accept-Encoding': "gzip",
            'Cookie': self.cookies.format(self.session_id)
        }
        requests.get(self.login_url_2, headers=headers2)

    def get_exam_list(self):
        '''
        获取考试列表
        :return:
        '''
        headers = {
            'User-Agent': self.user_agent_1,
            'Accept-Encoding': "gzip",
            'httpcache': "index",
            'content-length': "0",
            'Cookie': self.cookies.format(self.session_id)
        }
        response = requests.post(self.index_url, headers=headers)