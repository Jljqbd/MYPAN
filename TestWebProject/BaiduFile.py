# coding=utf-8
import webbrowser
import json
import requests
import urllib
import time
#API_KEY = 'qjlph5x8KL3DxVqK98D1G6ul'
#SECRET_KEY = 'UW6Zj5k6dBvydosDkTG0aNZIt54IAg3E'


class BaiduPan:
    def __init__(self):
        self.login_status = False
        self.API_KEY = 'qjlph5x8KL3DxVqK98D1G6ul'
        self.SECRET_KEY = 'UW6Zj5k6dBvydosDkTG0aNZIt54IAg3E'
        self.code = ''
    def get_code_url(self):
        code_url = f'https://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={self.API_KEY}&redirect_uri=http://127.0.0.1:8000/redirect_url&scope=basic,netdisk&display=tv&qrcode=1&force_login=1'
        self.code_url = code_url
    def login(self):
        #code_url = f'https://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={self.API_KEY}&redirect_uri=oob&scope=basic,netdisk&display=tv&qrcode=1&force_login=1'
        #self.code_url = code_url
        #webbrowser.open(code_url)
        #code = input('输入授权码（浏览器扫码登录）：')
        access_token_url = f'https://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code&code={self.code}&client_id={self.API_KEY}&client_secret={self.SECRET_KEY}&redirect_uri=http://127.0.0.1:8000/redirect_url'
        #print(access_token_url)
        self.access_token = requests.get(access_token_url).json()['access_token']
        self.get_user_info()

    def get_user_info(self):
        info = requests.get('https://pan.baidu.com/rest/2.0/xpan/nas?method=uinfo',
                            params={'access_token': self.access_token}).json()
        self.login_status = info['errno'] == 0
        if self.login_status:
            #print('-' * 10, info['baidu_name'], '-' * 10)
            #print('欢迎【', info['netdisk_name'], '】')
            vip = '普通用户'
            if info['vip_type'] == 1:
                vip = '普通会员'
            elif info['vip_type'] == 2:
                vip = '超级会员'
            #print('等级：', vip)
        #else:
            #print('登录失败！')
    def file_list(self, parent_path='/'):
        files = 'https://pan.baidu.com/rest/2.0/xpan/file?method=videolist'
        get_data = requests.get(files, params={'access_token': self.access_token, 'parent_path': parent_path, 'order': 'name', 'desc': '0'})
        data_json = json.loads(get_data.text)
        #print(data_json) 
        Video_fsid_array = []
        Video_file_name = []
        for index in range(len(data_json['info'])):
            Video_fsid_array.append(data_json['info'][index]['fs_id'])
            Video_file_name.append(data_json['info'][index]['server_filename'])
        #print(Video_fsid_array)
        #print(Video_file_path)
        self.fsid = Video_fsid_array
        self.filename = Video_file_name
    def get_download_url(self):
        url = "https://pan.baidu.com/rest/2.0/xpan/multimedia?method=filemetas"
        get_data = requests.get(url, params={'access_token': self.access_token, 'fsids': json.dumps(self.fsid[0:99]), 'dlink': 1})
        file_json = json.loads(get_data.text)
        #print(file_json)
        download_url = []
        for index in range(len(file_json['list'])):
            download_url.append(file_json['list'][index]['dlink'])
        #print(download_url)
        self.download_url = download_url
    def pandownload(self, download_path):
        for index in range(len(self.download_url)):#正式使用时将index=0去掉，将下载/video下所有文件
            index =0
            path = download_path + self.filename[index]
            url = self.download_url[index] + "&access_token=" + self.access_token
            #urllib.request.urlretrieve(self.download_url[index] + "&access_token=" + self.access_token, download_path + self.filename[index]) 
            start = time.time()
            size = 0
            response = requests.get(url,stream = True)#stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载
            chunk_size = 1024#每次块大小为1024
            content_size = int(response.headers['content-length'])#返回的response的headers中获取文件大小信息
            #print("文件大小："+str(round(float(content_size/chunk_size/1024),4))+"[MB]")
            with open(path,'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):#每次只获取一个chunk_size大小
                        file.write(data)#每次只写入data大小
                        size = len(data)+size        #'r'每次重新从开始输出，end = ""是不换行
                        #print('\r'+"已经下载："+int(size/content_size*100)*"█"+" 【"+str(round(size/chunk_size/1024,2))+"MB】"+"【"+str(round(float(size/content_size)*100,2))+"%"+"】",end="")
                        
            end = time.time()
            print(self.filename[index] + "总耗时:"+str(end-start)+"秒")

'''if __name__ == '__main__':
    pan = BaiduPan()
    pan.login()
    pan.file_list(parent_path='/Video')
    pan.get_download_url()
    pan.pandownload(download_path = "D:/")
'''