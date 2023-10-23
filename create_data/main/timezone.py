# coding=utf-8
'''
Created on 2018年4月26日
@author: Administrator
'''
import os
import paramiko


class SftpUtils(object):
    def __init__(self, host, port, user, password):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self.SFTP = self._connect()

    def _connect(self):
        u"""
 链接SFTP
        """
        try:
            transport = paramiko.Transport((self._host, self._port))
            transport.connect(username=self._user, password=self._password)
            SFTP = paramiko.SFTPClient.from_transport(transport)
            print(u"链接成功...")
            return SFTP
        except Exception as e:
            print( u"连接失败..%s" % e)

    def _makeRemotePath(self, target):
        u"""
 创建目标路径
 说明: 目标路径不存在则依次创建路径目录
        """
        # 切换根目录
        self.SFTP.chdir('/')
        # 分割目标目录为目录单元集合
        target.strip('/')
        data = target.split('/')
        # 进入目标目录, 目录不存在则创建
        for item in data:
            try:
                self.SFTP.chdir(item)
                print( u'要上传的目录已经存在，选择性进入合并：' + item)
            except:
                self.SFTP.mkdir(item)
                self.SFTP.chdir(item)
                print(u'要上传的目录不存在，创建目录：' + item)

    def _makeLocalPath(self, target_dir):
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)

    def upload_file(self, localfile, remotedir):
        u"""
 传输单个文件
        """
        self._makeRemotePath(remotedir)
        filename = localfile.split('/')[-1]
        # 上传文件
        try:
            self.SFTP.put(localfile, filename)
            print(u'%s 上传成功:' % filename)
        except Exception as e:
            print(u'%s 上传失败:%s' % (filename, str(e)))

    def download_file(self, remotefile, localdir):
        u"""
 下载单个文件
        """
        filename = remotefile.split('/')[-1]
        self._makeLocalPath(localdir)
        # 下载文件
        try:
            self.SFTP.get(remotefile, os.path.join(localdir, filename))
        except Exception as e:
            print(u'%s 下载失败:%s' % (filename, str(e)))
    def upload_dir(self, localdir, remotedir):
        for filename in os.listdir(localdir):
            localfile = os.path.join(localdir, filename)
            self.upload_file(localfile, remotedir)

    def download_dir(self, remotedir, localdir):
        self.SFTP.chdir(remotedir)
        for remote_file in self.SFTP.listdir(remotedir):
            self.download_file(remote_file, localdir)

    def close(self):
        self.SFTP.close()


if __name__ == '__main__':
    sftp = SftpUtils("175.25.49.73",23229,"WLSJTest@175.25.49.73","puan0314")
    sftp.upload_file("/WLSJ01/return/50/202309/20230921/WLSJ01_20230816095822_10_001.pdf", "/home/bohai/remote_file/hdye.pdf")
    sftp.close()