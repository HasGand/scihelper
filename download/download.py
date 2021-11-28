from download.download_from_arxiv import arxiv_download
from download.download_from_scihub import scihub_download
from get_info.arxiv_getinfo import get_serial_by_doi
from cache.cache import Cache
import time


def download_by_file(dfile):
    start_time = time.time()

    cache = Cache()
    cache_old_keys = cache.read_cache().keys()
    with open(dfile, 'r') as f:

        for ditem in f.readlines():
            ditem = ditem.strip()
            if ditem in cache_old_keys:
                print(f"Already downloaded: {ditem}")
                continue
            print("\n", ditem)
            try:
                if ditem.split(':')[0] == 'arXiv':
                    arxiv_download(ditem, cache)
                else:
                    if not scihub_download(ditem, cache):
                        serial = get_serial_by_doi(ditem)
                        if serial in cache_old_keys:
                            print(f"Already downloaded: {serial}")
                            return None
                        arxiv_download(serial, cache)
            except:
                pass

    print("\ntotal time: {:.2f} s".format(time.time() - start_time))


def download_by_doiorserial(ditem):
    start_time = time.time()

    cache = Cache()
    cache_old_keys = cache.read_cache().keys()
    if ditem in cache_old_keys:
        print(f"Already downloaded: {ditem}")
        return None

    try:
        if ditem.split(':')[0] == 'arXiv':
            arxiv_download(ditem, cache)
        else:
            if not scihub_download(ditem, cache):
                serial = get_serial_by_doi(ditem)
                if serial in cache_old_keys:
                    print(f"Already downloaded: {serial}")
                    return None
                arxiv_download(serial, cache)
    except:
        pass

    print("\ntotal time: {:.2f} s".format(time.time() - start_time))


if __name__ == "__main__":
    # 10.1021/acs.chemmater.1c02683 scihub无 arxiv有
    # 10.1016/j.physleta.2021.12770 都没有
    download_by_file('./test')
    download_by_file('./resources/dois&serials.txt')
