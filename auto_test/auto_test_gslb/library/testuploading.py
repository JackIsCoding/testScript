#coding=utf-8

import paramiko

def connect(host):
    'this is use the paramiko connect the host,return conn'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
#        ssh.connect(host,username='root',allow_agent=True,look_for_keys=True)
        ssh.connect(host,username='root1',password='awl9w5O1WIgs',allow_agent=True)
        return ssh
    except:
        return None

def copy_moddule(conn,inpath,outpath):
    'this is copy the module to the remote server'
    ftp = conn.open_sftp()
    ftp.put(inpath,outpath)
    ftp.close()
    return outpath




#建立一个加密的管道
scp=paramiko.Transport(('10.10.67.109',22))
#建立连接
scp.connect(username='root1',password='awl9w5O1WIgs')
#建立一个sftp客户端对象，通过ssh transport操作远程文件
sftp=paramiko.SFTPClient.from_transport(scp)
#Copy a remote file (remotepath) from the SFTP server to the local host
#sftp.get('/root/testfile','/tmp/361way')
#Copy a local file (localpath) to the SFTP server as remotepath
sftp.put('./uploadfile.txt','/usr/local/sandai/xcloud_scheduler/conf/uploadfile.txt')
scp.close()


if __name__ == '__main__':
    pass
    #copy_moddule("10.10.67.109",'uploadfile.txt','/usr/local/sandai/xcloud_scheduler/conf')
