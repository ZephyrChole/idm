import os.path
import subprocess as sp
import time


class Downloader:
    def __init__(self, idm_path):
        self.idm_path = idm_path
        self.process = sp.Popen([idm_path])

    def download(self, url, name, dir_):
        retry = 0
        while True:
            try:
                sp.run([self.idm_path, '/d', url, '/p', dir_, '/f', name, '/s', '/n'], timeout=5, stdout=sp.DEVNULL,
                       stderr=sp.DEVNULL)
                break
            except sp.TimeoutExpired:
                self.restart_idm()
                retry += 1
            if retry == 3:
                print(f'max retry {name}')
                break

    def download_wait4file(self, url, name, dir_, timeout=None):
        def check_exist(d, n):
            for i in os.listdir(d):
                if n in i:
                    return True
            return False

        start_time = time.time()
        if check_exist(dir_, name):
            return True
        self.download(url, name, dir_)
        while timeout is None or time.time() - start_time < timeout:
            if check_exist(dir_, name):
                return True
            else:
                time.sleep(1)
        return False

    def restart_idm(self):
        self.process.kill()
        self.process = sp.Popen([self.idm_path])
