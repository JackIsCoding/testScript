import paramiko
from time import sleep

class Sshhandle():
    def __init__(self):
        # self.hostname = '10.10.67.109'
        self.port = 22
        self.username = 'root1'
        # self.password = 'awl9w5O1WIgs'

    def ssh_connect(self,hostname,password):
        try:
            self.ssh_fd = paramiko.SSHClient()
            self.ssh_fd.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
            self.ssh_fd.connect( hostname=hostname, port=self.port,username = self.username, password = password )
        except Exception, e:
            print( 'ssh %s@%s: %s' % (self.username, hostname, e) )
            exit()
        return self.ssh_fd

    def ssh_exec_cmd( self,ssh_fd, cmd ):
        return self.ssh_fd.exec_command( cmd )


    def ssh_close( self,ssh_fd ):
        self.ssh_fd.close()


    def restartSch(self,hostname,password):
        cmd = 'cd /usr/local/sandai/xcloud_scheduler/sbin/;./scheduler.unified_gateway restart'
        sshd = self.ssh_connect(hostname,password)
        stdin, stdout, stderr = self.ssh_exec_cmd(sshd, cmd)
        err_list = stderr.readlines()

        if len(err_list) > 0:
            print 'ERROR:' + err_list[0]
            exit()

        for item in stdout.readlines():
            print item,
        self.ssh_close(sshd)


    def uoloadFile(self,inpath,outpath):
        sshd = self.ssh_connect()
        ftp = sshd.open_sftp()
        ftp.put(inpath,outpath)
        print inpath
        ftp.close()
        print outpath

if __name__ == "__main__":
    test = Sshhandle()
    test.restartSch('10.10.67.109','awl9w5O1WIgs')
