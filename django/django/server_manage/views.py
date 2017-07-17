#coding:utf-8
import datetime
from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from requests import Response

from AnsibleCreateCheck import *
from models import *
import forms
from adhoc import *
import json
import commands




# Create your views here.

def login(request):
    ret = {'error':'','form':''}
    reg = forms.User()
    ret['form'] = reg
    if request.method == "POST":
        form = forms.User(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            count = User.objects.filter(username=data['username'],password=data['password']).count()
            if count == 1:
                request.session['is_login'] = {'user':data['username']}
                return redirect('/index/')
            else:
                ret['error'] = '用户名密码错误'
                return render_to_response('account/login.html', ret)
        else:
            ret['error'] = form.errors.as_data().values()[0][0].messages[0]
            ret['form'] = form
            return render_to_response('account/login.html',ret)
    else:
        return render_to_response('account/login.html',ret)
def logout(request):
    del request.session['is_login']
    return redirect('/login/')


def required_login(fun):
    def _deco(request,*args,**kwargs):
        if request.session.get('is_login'):
            return fun(request,*args,**kwargs)
        else:
            return redirect('/login/')
    return _deco

@required_login
def index(request):
    user = request.session.get('is_login')['user']
    ret = {'data': '','error':'','user':user}
    message = ServerList.objects.all().values('ServerId', 'Name','Address')
    ret['data'] = message
    return render_to_response('index/index.html',ret)

def start(request):
    if request.method == "POST":

        data = {'code':200,'msg':[]}
        ser_id = request.POST.getlist('id')

        for i in range(len(ser_id)):
            print ser_id[i]
        html = []
        ip=["192.168.1.7","192.168.1.139"]
        dir="/"
        #et = Order_Run(host=ip,module_name="shell",module_args="chdir=%s forever list | grep admin | awk '{print $6}' | awk -F '\'{print $1}' "%dir)

        #print ret


        data['msg'] = html
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('Cannot GET /start/')

@required_login
def create(request):
    user = request.session.get('is_login')['user']
    ret = {'data': '', 'error': '', 'user': user}

    return render_to_response('index/create.html',ret)







def eventsource(request):
    if request.method == "POST":
        global wlan_ip_port
        global lan_ip
        global ser_name
        global ser_id
        global game_mysql_addr
        global game_mysql_user
        global game_mysql_passwd
        global game_mysql_db
        global port_list
        ser_id = request.POST.getlist('ser_id')
        ser_name = request.POST.getlist('ser_name')
        port_range = request.POST.getlist('port_range')
        lan_ip = request.POST.getlist('lan_ip')
        wlan_ip_port = request.POST.getlist('wlan_ip_port')
        game_mysql_addr = request.POST.getlist('game_mysql_addr')
        game_mysql_user = request.POST.getlist('game_mysql_user')
        game_mysql_passwd = request.POST.getlist('game_mysql_passwd')
        game_mysql_db = request.POST.getlist('game_mysql_db')


        # check service id
        if ser_id[0]:
            if ser_id_check(ser_id) != 1:
                data = '输入的ID必须在20000-29999范围之内'
                return HttpResponse(data, status=400)
        else:
            data='服务器ID不能为空'
            return HttpResponse(data,status=400)

        # check service name
        if ser_name[0] and '\u' not in unicode(ser_name):
            if game_name_check(ser_name) != 1:
                data = '服务器名称格式错误'
                return HttpResponse(data, status=400)
        else:
            data='服务器名称不能为空'
            return HttpResponse(data,status=400)

        # check private ip
        if lan_ip[0]:
            private_ip_result = private_ip_check(lan_ip)
            if private_ip_result == 2:
                data='服务器内网IP必须是私有地址'
                return HttpResponse(data,status=400)
            elif private_ip_result == 3:
                data = '服务器内网IP格式错误'
                return HttpResponse(data, status=400)
        else:
            data='服务器内网IP不能为空'
            return HttpResponse(data,status=400)

        # check port range
        if port_range[0]:
            if port_check(lan_ip, ser_name[0], port_range) != 1:
                data = '选择的端口范围已存在'
                return HttpResponse(data, status=400)



        # check public ip
        if wlan_ip_port[0]:
            public_ip_result = public_ip_check(wlan_ip_port)
            if public_ip_result == 2:
                data = '服务器外网IP必须是公有地址'
                return HttpResponse(data, status=400)
            elif public_ip_result == 3:
                data = '外网端口必须在8000-8999范围之内'
                return HttpResponse(data, status=400)
            elif public_ip_result == 4:
                data = '公网IP端口输入格式->ip:port'
                return HttpResponse(data, status=400)
        else:
            data = '服务器外网IP不能为空'
            return HttpResponse(data, status=400)

        # check mysql info
        for i in [game_mysql_addr,
                game_mysql_user,
                game_mysql_passwd,
                game_mysql_db
                  ]:
            if not i[0]:
                data = '数据库信息必须填写'
                return HttpResponse(data, status=400)

        # check game mysql connect
        mysql_result = mysql_check(lan_ip,game_mysql_addr,game_mysql_user,game_mysql_passwd,game_mysql_db)
        if mysql_result != 1:
            data = "MySQL: ",mysql_result.values()[0]
            return HttpResponse(data, status=400)



        print 'updatemysql'
        # update mysql
        acc_sql_addr="192.168.1.139"
        acc_sql_user="game02"
        acc_sql_passwd="game0"
        acc_sql_db="02Acc"
        TIME = datetime.datetime.now()
        ser_conf_sql = r"{\"mysql\":{\"host\":\"%s\",\"port\":3306,\"user\":\"%s\",\"password\":\"%s\",\"database\":\"%s\",\"connectionLimit\":32}}" % (
            game_mysql_addr[0], game_mysql_user[0], game_mysql_passwd[0], game_mysql_db[0])
        ser_stat_sql = r"{\"tag\":1,\"status\":0,\"version\":\"0.0.0.0\",\"order\":4,\"pkgversion\":0}"
        stat,msg=commands.getstatusoutput("""mysql -h %s -u %s -p%s -e 'insert into %s.GameService (Id,CreateTime,Name,Address,ServerConfig,Status)values(%s,"%s","%s","%s","%s","%s")'""" % (\
                               acc_sql_addr,acc_sql_user,acc_sql_passwd,acc_sql_db, \
                               ser_id[0], TIME, ser_name[0], wlan_ip_port[0], ser_conf_sql, ser_stat_sql))


        if stat != 0:
            print msg
            data = msg
            return HttpResponse(data, status=400)
        # copy files
        global FILE_DIR
        FILE_DIR='/git/GameService/'
        if not os.path.exists(FILE_DIR):

        # for k,v in copy_result.items():
        #     if v and k != 'success':
                data = '拷贝文件出错:源目录不存在'
                return HttpResponse(data, status=400)


        # check nginx config
        global  nginx_config_file
        nginx_config_file = "/usr/local/nginx/conf/nginx.conf"
        port_list = port_range[0].split(',')
        result = Order_Run(host=lan_ip, module_name="shell",
                           module_args="sed -i '/gameservice begin/i@\tupstream %s {' %s" %(ser_name[0],nginx_config_file))
        for k, v in result.items():
            if v and k != 'success':
                data = v.values()
                return HttpResponse(data, status=400)


        data = 'ok'
        return HttpResponse(data)
    elif  request.method == "GET":
        response = StreamingHttpResponse(stream_generator(), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response

def copy_file():
    Order_Run(host=lan_ip, module_name="copy", module_args="src=%s dest=/gameService/work/"%FILE_DIR)
    return 'OK'

def config_nginx():
    nginx_reload = "/usr/local/nginx/sbin/nginx -s reload"
    flag = 1
    for port in port_list:
        if flag <= 2:
            Order_Run(host=lan_ip, module_name="shell",
                      module_args="sed -i '/gameservice begin/i@\t\tserver %s:%s;' %s" % (
                          lan_ip[0], port,nginx_config_file))
        else:
            Order_Run(host=lan_ip, module_name="shell",
                      module_args="sed -i '/gameservice begin/i@\t\t#server %s:%s;' %s" % (
                          lan_ip[0], port,nginx_config_file))
        flag += 1

    wlan_port = wlan_ip_port[0].split(':')[1]
    order_list = [
        "sed -i '/gameservice begin/i@\t}'",
        "sed -i '/gameservice end/i@\tserver {'",
        "sed -i '/gameservice end/i@\t\tlisten %s;'"%wlan_port,
        "sed -i '/gameservice end/i@\t\tlocation / {'",
        "sed -i '/gameservice end/i@\t\t\tproxy_pass http://%s;'"%ser_name[0],
        "sed -i '/gameservice end/i@\t\t\tproxy_set_header U-Remote-Endpoint $remote_addr:$remote_port;'",
        "sed -i '/gameservice end/i@\t\t\tproxy_set_header Host $http_host;'",
        "sed -i '/gameservice end/i@\t\t\tproxy_set_header Connection \"\";'",
        "sed -i '/gameservice end/i@\t\t}'",
        "sed -i '/gameservice end/i@\t}'",
        "sed -i 's/^@/ /'"
    ]
    a = 1
    for order in order_list:
        if a == 2:
            a += 1
            err = Order_Run(host=lan_ip, module_name="shell", module_args="%s %s"%(order,nginx_config_file))
            print err
        else:
            Order_Run(host=lan_ip, module_name="shell", module_args="%s %s" % (order, nginx_config_file))
    Order_Run(host=lan_ip,module_name="shell",module_args="%s"%nginx_reload)
    return 'OK'

def config_game():
    DATE = datetime.datetime.date(datetime.datetime.now())
    order_list = [
        "sed -i '2i\"host\": \"%s\",'"%lan_ip[0],
        "sed -ri 's/(\"gameServiceId\":)(.*)/\\1 %s/'"%ser_id[0],
        "sed -ri 's/(\"ServerOpenTime\":\")(.*)(00:00:.*)/\\1%s \\3/'"%DATE,
    ]
    Order_Run(host=lan_ip, module_name="shell", module_args="cp /gameService/work/gameService.conf{.tmpl,}")
    for order in order_list:
        Order_Run(host=lan_ip, module_name="shell", module_args="%s /gameService/work/gameService.conf"% order)
    return 'OK'

def start_game():
    flag = 1
    global run_port
    run_port = []
    for port in port_list:
        order_list = [
            "mkdir -p /gameService/%s/%s" % (ser_name[0], port),
            "cp -r /gameService/work/* /gameService/%s/%s" % (ser_name[0], port),
            "sed -ri '3s/(\"port\":)(.*)/\\1 %s,/' /gameService/%s/%s/gameService.conf" % (port, ser_name[0], port),
            "cd /gameService/%s/%s && node gameService updatedb &>/dev/null" % (ser_name[0], port),
            "cd /gameService/%s/%s && forever start gameService %s_%s &>/dev/null" % (ser_name[0], port, ser_name[0], port)
        ]
        if flag <= 2:
            flag += 1
            run_port.append(port)
            for order in order_list:
                Order_Run(host=lan_ip, module_name="shell", module_args="%s"%order)
        else:
            for order in order_list[:3]:
                Order_Run(host=lan_ip, module_name="shell", module_args="%s" % order)
    return 'OK'

def check_game():
    for port in run_port:
        result = Order_Run(host=lan_ip, module_name="shell", module_args="forever list --no-colors | grep %s_%s | grep -i stopped"%(ser_name[0],port))
        if result['success']:
            return 'FAILD'
    return 'OK'


def stream_generator():
    stat = 404
    data = {'msg': ""}
    order_list = ["copy_file","config_nginx","config_game","start_game","check_game"]
    order_dict = {"copy_file":copy_file,
                  "config_nginx":config_nginx,
                  "config_game":config_game,
                  "start_game":start_game,
                  "check_game":check_game
                  }
    flag = 1
    for order in order_list:
        if flag == 1:
            flag += 1
            data['msg']=''
            yield u'data: %s\n\n' % data['msg']
        status = order_dict[order]()
        data['msg'] = order + ' :%s'%status
        yield u'data: %s\n\n' % data['msg']
    else:
        yield u'data: %s\n\n' % stat





