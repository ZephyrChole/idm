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
        start_time = time.time()
        self.download(url, name, dir_)
        full_path = os.path.join(dir_, name)
        while timeout is None or time.time() - start_time < timeout:
            if os.path.exists(full_path):
                return True
            else:
                time.sleep(1)
        return False

    def restart_idm(self):
        self.process.kill()
        self.process = sp.Popen([self.idm_path])
