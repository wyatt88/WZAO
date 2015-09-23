###~*-coding:utf-8-*~###
from flask import Flask,render_template,request
import MySQLdb as mysql
import sys
import socket
from WZAOSSH import WZAOSSHClient
import json

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

con = mysql.connect(user='root',\
					passwd='root',\
					db='WZAO',\
					host='10.44.147.52')
con.autocommit(True)
cur = con.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servermanager')
def servermanager():
    return render_template('/manage/servermanager.html')

@app.route('/serverlist')
def serverlist():
    init_str=''
    query_sql='select * from t_servers'
    cur.execute(query_sql)
    for c in cur.fetchall():
        init_str=init_str+ '''<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>
                        <button data-id=%s class="btn btn-danger server-delete">删除</button>
                        <button data-id=%s class="btn btn-warning server-modify" data-toggle="modal" data-target="#exampleModal">变更</button>
                        <button data-id=%s class="btn btn-default ssh" data-toggle="modal">SSH</button>
                        <button data-id=%s class="btn btn-default scan-port" data-toggle="modal">端口扫描</button>
                        </td></tr>''' % (c[0],c[1],c[2],c[3],c[4],c[0],c[0],c[0],c[2])
    return init_str

@app.route('/addserver')
def addserver():
    server=request.args.get('server')
    ip=request.args.get('ip')
    mac=request.args.get('mac')
    op=request.args.get('op')
    user=request.args.get('user')
    passwd=request.args.get('pass')
    try:
        sql="insert into t_servers (servername,ip,mac,op,hostuser,hostpass) values ('%s','%s','%s','%s','%s','%s')" % (server,ip,mac,op,user,passwd)
        print sql
        cur.execute(sql)
        # con.commit()
        str_alert='ok'
    except mysql.Error, e:
        str_alert="Error %d:%s" % (e.args[0], e.args[1])
    return str_alert

@app.route('/queryserver')
def queryserver():
    serverid=request.args.get('serverid')
    query_sql='select * from t_servers where id=%s' % serverid
    cur.execute(query_sql)
    data=cur.fetchone()
    return data[2]+','+data[5]+','+data[6]

@app.route('/deleteserver')
def deleteserver():
    serverid=request.args.get('serverid')
    sql='delete from t_servers where id=%s' % serverid
    cur.execute(sql)
    return 'ok'

@app.route('/sshclient')
def sshclient():
    ip=request.args.get('ip')
    user=request.args.get('user')
    passwd=request.args.get('pass')
    command=request.args.get('cmd')
    str_result=WZAOSSHClient.myconnect(ip,user,passwd,command)
    return str_result

@app.route('/scanport')
def scanp():
    ip=request.args.get('ip')
    try:
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setblocking(False)
    except socket.error,sock_msg:
        print sock_msg.args[0]
    result_str=''
    for port in range(20,50):
        try:
            print port
            sock.connect((str(ip),port))

        except socket.error,e:
            print e.args[0],e.args[1]
            sock.close()
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.setblocking(False)
        else:
            result_str= result_str + '端口 '+str(port)+' 打开\n'
            sock.close()
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.setblocking(False)
    return result_str

@app.route('/getDiskusage')
def getDiskusage():
    d={
        'unuse':110000,
        'use':1200
    }
    return json.dumps(d)

@app.route('/getCountbyNET')
def getCountbyNET():
    query_sql='select count(*) from t_servers where ip like "192.168.4.%"'
    cur.execute(query_sql)
    net4=cur.fetchone()
    print net4
    query_sql="select count(*) from t_servers where ip like '192.168.1.%'"
    cur.execute(query_sql)
    net1=cur.fetchone()
    print net1
    d={
        'net4':net4,
        'net1':net1
    }
    return json.dumps(d)
@app.route('/help')
def help():
    return "我爱大橙子"
    
@app.route('/map')
def servermap():
    return render_template('/manage/map.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
