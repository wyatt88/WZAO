__author__ = 'wenwen'
import paramiko


class WZAOSSHClient:

    def __init__(self):

        paramiko.util.log_to_file('syslogin.log')

    @staticmethod
    def myconnect(host,user,passwd,command):
        ssh1=paramiko.SSHClient()
        ssh1.load_system_host_keys()
        ssh1.connect(hostname=host,username=user,password=passwd)
        stdin,stdout,stderr=ssh1.exec_command(command)
        return stdout.read()

    def myclose(self):
        ssh1.close()

if __name__=='__main__':
    ssh1=WZAOSSHClient()
#    ssh1.myconnect('192.168.4.128','root','adccadcc','')


