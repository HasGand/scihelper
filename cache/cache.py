import os
import json


class Cache(object):
    '''
    添加成功下载条目键值对
    方便下次下载从中读取信息
    '''

    def __init__(self, dir='./references/', filename='cache_log.json'):
        self.cache = {}
        self._cache_dir = dir + filename
        if os.path.exists(dir):
            if os.path.exists(self._cache_dir):
                if os.path.getsize(self._cache_dir):
                    with open(self._cache_dir, 'r', encoding='utf-8') as f:
                        self.cache = json.load(f)
            else:
                with open(self._cache_dir, 'w', encoding='utf-8'):
                    pass
        else:
            os.mkdir(dir)
            with open(self._cache_dir, 'w', encoding='utf-8'):
                pass
        """添加一个自动删除不需要的log 功能"""

    def __setitem__(self, key, value):
        self.cache[key] = value
        with open(self._cache_dir, 'w+', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2)

    def read_cache(self):
        if os.path.getsize(self._cache_dir):
            with open(self._cache_dir, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
