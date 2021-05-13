from django.shortcuts import render
from TestWebapp.models import People
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dwebsocket import require_websocket
import threading
import os
import sys
import dwebsocket
import json
import time
import webbrowser
import requests
import urllib
import re
import mimetypes
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
pypath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../TestWebProject')
sys.path.append(pypath)
from BaiduFile import BaiduPan
# Create your views here.
pan = BaiduPan()
username = ''
download_time =[]
isloginBaidu = 0#没有登录百度
def jump_register(request):
    return render(request, 'register.html', context={'word':'请填写您要注册的账号密码'})
@csrf_exempt
def register(request):
    if request.method == 'POST':
        if request.POST.get('Password')!=request.POST.get('Password1'):
            return render(request, 'newlogin.html',context={'word_register':"密码与确认密码不相同",'word_login':'注册失败'})
        if request.POST.get('invite')!='jljqbd':
            return render(request, 'newlogin.html',context={'word_register':"邀请码错误请尽快与管理员联系",'word_login':'注册失败'})
        #sql = "slect Pno from testwebapp_people where Pno='" + request.POST.get('Pno') + "'"
        Pno = request.POST.get('Pno')
        result = People.objects.filter(Pno = Pno)
        if result.count()==0:#该账号可以进行注册
            #word = '您的注册信息为：Pno'+ request.POST.get('Pno') + ',Password:'+ request.POST.get('Password') + ',Page:' + request.POST.get('Page') + ',Psex:'+ request.POST.get('Psex')
            Db_write = People(Pno=request.POST.get('Pno'),Password=request.POST.get('Password'),Page=request.POST.get('Page'),Psex=request.POST.get('Psex'))
            Db_write.save()
            os.mkdir("../static/text/" + Pno)
            os.mkdir("../static/video/" + Pno)
        else:#该账号不能进行注册，跳转register重新输入账号
            word = '错误数据库中存在相同ID请修改名称'
            return render(request, 'newlogin.html',context={'word_register':word,'word_login':'注册失败'})
    #context = {'Pno':Db_write.Pno,'Password':Db_write.Password,'Page':Db_write.Page,'Psex':Db_write.Psex}
    #return render(request, 'login.html',context={'word':'注册成功'})#注册成功后register跳转到login
    return render(request, 'newlogin.html', context={'word_login': '注册成功','word_register':''})
def index(request):#首页
    return render(request, 'newlogin.html',context={'word_login':'请填写您的账号密码','word_register':''})
def readfile(filePath,flag):#返回仅仅是文件，没有路径
    #flag 1是视频文件 0是文本文件
    Sn = ['.mp4','.avi','.wmv','.mpg','.mpeg','.swf','.flv']
    Tn = [".pdf",".html","txt",".ppt",".pptx",".pptm",".ppsx",".ppsm",".potx",".xls",".xlsx",".xlsm",".xltx",".xltm",".xlsb",".xlam",".doc",".docx",".docm",".dotx",".dotm",".mdb",".htm"]
    Temp = Sn if flag==1 else Tn
    filelist=[]
    allfilename = os.listdir(filePath)
    for files in allfilename:
        if  os.path.splitext(files)[1] in  Temp:
            filelist.append(files)
    return filelist
@csrf_exempt
def login(request):
    global username
    Pno = request.POST.get('username')
    username  = Pno
    Password = request.POST.get('password')
    result = People.objects.filter(Pno=Pno, Password=Password)
    if result.count()==1:#账号密码正确
        for i in result:
            context={'username':i.Pno}
        return render(request, 'main.html',context=context)
    else:
        return render(request, 'newlogin.html',context={'word_login':'密码错误 or 数据库中无该账号请去注册','word_register':''})
def videolist(request):
    username = request.GET['username']
    filepath = os.getcwd() + '/static/video/' + username
    filevideolist = readfile(filepath,1)
    context = {'username':username}
    context['filevideolist'] = filevideolist
    print(filevideolist)
    context['isempty'] = 0
    files = request.GET['files']#从主页跳转赋默认值（0），即第一个文件名称
    if not filevideolist:
        context['isempty'] = 1#空文件
        return HttpResponse("该账号无视音频文件")
    if files=='0':
        files = filevideolist[0]
    videofilepath = '../static/video/' + username + '/' + files
    videotype = os.path.splitext(files)[1]
    videotype = videotype[1:]
    context['word'] = videofilepath
    context['type'] = videotype
    return render(request, 'videolist.html',context=context)
def textlist(request):
    username = request.GET['username']
    filepath = os.getcwd() + '/static/text/' + username
    textlist = readfile(filepath,0)
    context = {'username':username}
    context['textlist'] = textlist
    return render(request, 'textlist.html',context=context)
@csrf_exempt
def upload_file(request):
    # 请求方法为POST时，进行处理
    if request.method == "POST":
        username = request.POST.get('username')
        # 获取上传的文件，如果没有文件，则默认为None
        File = request.FILES.get("fileToUpload", None)
        #print('username:'+username)
        if File is None or username is None:
            return HttpResponse("没有需要上传的文件")
        else:
            flag = int(request.POST.get('type'))
            #print("flag:"+ str(flag))
            filepath = "E:/VSC py/TestWebProject/static/"+("video/" if flag else "text/") + username
            #print(filepath)
            #打开特定的文件进行二进制的写操作
            #print(os.path.exists('/temp_file/'))
            if File.name in readfile(filepath,flag):
                return HttpResponse('文件库中已有该文件，请上传其他文件')
            else:
                with open("./static/%s/%s/%s" % ("video" if flag else "text", username, File.name), 'wb+') as f:
                    #分块写入文件
                    for chunk in  File.chunks():
                        f.write(chunk)
                #print(("video" if flag else "text") + "UPload over! Save in:" + "/static/%s/%s/%s" % ("video" if flag else "text", username, File.name))
                return HttpResponse(("video" if flag else "text") + "UPload over! Save in:" + "/static/%s/%s/%s" % ("video" if flag else "text", username, File.name))     
    else:
        return  render(request, "upload.html")
def jump_upload(request):
    return  render(request, "viewupload.html")
def viewtext(request):
    username = request.GET['username']
    files = request.GET['files']
    filepath = '../../text/' + username + '/' + files
    #return render(request, 'viewer.html?file='+filepath)
    flag = -1
    file_type = files.split(".")[1]
    if file_type == "pdf":
        flag = 1
    if file_type in ["ppt","pptx","pptm","ppsx","ppsm","potx","xls","xlsx","xlsm","xltx","xltm","xlsb","xlam","doc","docx","docm","dotx","dotm","mdb","htm"]:
        filepath = "2886a3s359.qicp.vip:51998/static/text/" + username +"/" + files
        flag = 0
    if flag == -1:
        error_str = "Sorry, the online browsing function of this type of file has not been opened, please contact the administrator if you need"
        return HttpResponse(error_str)
    return render(request, 'viewtext.html',context={'path':filepath, "flag":flag})
def Baidu_login(request):
    global pan,isloginBaidu
    #print("isloginBaidu:"+str(isloginBaidu))
    if isloginBaidu==1:#上次已导入网盘文件，未下载完毕
        context = {'file_list':json.dumps(pan.filename)}
        return render(request,'panfileload.html',context=context)
    pan.get_code_url()
    #return render(request,pan.code_url)
    return HttpResponseRedirect(pan.code_url)
def pandownload(pan, download_path):
        global download_time
        flag = 1
        for index in range(len(pan.download_url)):#正式使用时将index=0去掉，将下载/video下所有文件
            path = download_path + pan.filename[index]
            url = pan.download_url[index] + "&access_token=" + pan.access_token
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
                        bar =  str(round(float(size/content_size)*100,2)) + "%"#第几个文件进度如何
                        if flag==1:
                            download_time.append(bar)#到了一个新的文件
                            flag = 0
                        else:
                            download_time[index] = bar#还在老文件中
            end = time.time()
            download_time[index] = str(end-start)#记录文件完成下载的时间
            #print(download_time)
            flag = 1
            #print(self.filename[index] + "总耗时:"+str(end-start)+"秒")
        isloginBaidu = 0#下载完成没有文件要下载
@require_websocket
def websocket(request):
    global download_time
    #print('请求的download_time:'+str(download_time))
    while 1:
        time.sleep(1)
        request.websocket.send(" ".join(download_time))
def redirect_url(request):
    global pan,username,isloginBaidu
    pan.code  = request.GET['code']
    pan.login()
    pan.file_list(parent_path='/Video')#下载前要判断本地路径没有同名文件
    allfilename_video = os.listdir("E:/VSC py/TestWebProject/static/video/" + username)
    allfilename_text = os.listdir("E:/VSC py/TestWebProject/static/text/" + username)
    flag = 0
    for files in pan.filename:
        if files in allfilename_video and files in allfilename_text:
            flag = 1
            break
    if flag == 1:
        #print('在这错误了')
        return HttpResponse("error:文件重名 filename:" + files)
    pan.get_download_url()
    download_path = "E:/VSC py/TestWebProject/static/video/" + username + '/'
    '''
    allfilename = os.listdir(download_path)
    d_list = []
    d_url_list = []
    #print("filename len:"+str(len(pan.filename)))
    for i in range(len(pan.filename)):#去除重名文件
        print("i:"+str(i))
        if pan.filename[i] not in allfilename:
            d_list.append(pan.filename[i])
            d_url_list.append(pan.download_url[i])
    pan.filename = d_list
    pan.download_url = d_url_list
    '''
    p1 = threading.Thread(target=pandownload,args=(pan,download_path,))
    p1.start()
    isloginBaidu = 1#已经登录百度账号，下次无需登录
    #print('已经登陆百度帐号了')
    #pan.pandownload(download_path = "E:/VSC py/TestWebProject/static/video/")
    context = {'file_list':json.dumps(pan.filename)}
    return render(request,'panfileload.html',context=context)
def deletefile(request):
    filetype = request.GET['type']
    username = request.GET['username']
    files = request.GET['files']
    filepath = os.getcwd() + "/static/" + filetype + "/" + username + '/' + files
    os.remove(filepath)
    return HttpResponse(files + "删除成功")
def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data
def stream_video(request):
    """将视频文件以流媒体的方式响应"""
    username = request.GET['username']
    filename = request.GET['files']
    path = os.getcwd() + "/static/video" + "/" + username + '/' + filename
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = first_byte + 1024 * 1024 * 8       # 8M 每片,响应体最大体积
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        # 不是以视频流方式的获取时，以生成器方式返回整个文件，节省内存
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp
def BingPicture(request):
    Picture_file_list = os.listdir("static/BingPicture")
    f = open("static/BingText.txt", 'rb')
    response_list = []
    i = 0
    for line in f:
        response_list.append((Picture_file_list[i], line))
        i += 1
    f.close()
    context = {'firstimage': response_list[0][0], 'firstimagetext': response_list[0][1], 'files': response_list}
    return render(request, 'BingPicture.html', context = context)


