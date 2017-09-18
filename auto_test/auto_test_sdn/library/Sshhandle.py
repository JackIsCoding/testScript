import paramiko
from time import sleep

class Sshhandle():
    def __init__(self):
        self.port = 22
        self.username = 'root1'

    def sshConnect(self,hostname,password):
        try:
            self.ssh_fd = paramiko.SSHClient()
            self.ssh_fd.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
            self.ssh_fd.connect( hostname=hostname, port=self.port,username = self.username, password = password )
        except Exception, e:
            print( 'ssh %s@%s: %s' % (self.username, hostname, e) )
            exit()
        return self.ssh_fd

    def sshExecute(self, ssh_fd, cmd):
        return self.ssh_fd.exec_command(cmd)


    def sshClose(self, ssh_fd):
        self.ssh_fd.close()


    def restart(self,hostname,password):
        cmd = 'cd /usr/local/sandai/xcloud_scheduler/sbin/;./scheduler.unified_gateway restart'
        sshd = self.sshConnect(hostname,password)
        stdin, stdout, stderr = self.sshExecute(sshd, cmd)
        err_list = stderr.readlines()

        if len(err_list) > 0:
            print 'ERROR:' + err_list[0]
            exit()

        for item in stdout.readlines():
            print item,
        self.sshClose(sshd)


    def uploadFile(self,inpath,outpath):
        sshd = self.sshConnect()
        ftp = sshd.open_sftp()
        ftp.put(inpath,outpath)
        print inpath
        ftp.close()
        print outpath

if __name__ == "__main__":
    test = Sshhandle()
    fd = test.sshConnect('10.10.67.103','c22hx5A81Vho')
    cmd = "iptables -A INPUT -p tcp --dport 1935 -j DROP"
    test.sshExecute(fd, cmd)
