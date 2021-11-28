from get_info.arxiv_getinfo import arxiv_getinfo_by_title
from get_info.wos_getinfo import wos_getinfo_by_searchurl
from get_info.get_wos_searchurl_by_title import get_wos_searchurl_by_title
from download.download import download_by_file
from download.download import download_by_doiorserial
from sys import argv
from os.path import isfile

"""
WOS 访问旧版网站，爬取信息前先用浏览器打开一次该网站，以便访问。
"""


def helpinfo():
    helpstr = '''
        scihelper -h 帮助信息
        scihelper --help 帮助信息
        scihelper [doi/serial] 根据传入的doi/serial下载文献
        scihelper --arxiv [topic] 从arxiv获取相关主题的文献信息
        scihelper --arxiv -d [topic] 从arxiv获取相关主题的文献信息并下载所有文献
        scihelper --wos -link [topic] [link] 自行输入从webofscience获得的搜索页面的网址
        scihelper --wos -link -d [topic] [link] 自行输入从webofscience获得的搜索页面的网址并下载所有文献
        scihelper --wos [topic] 从webofscience获取相关主题的文献信息并下载所有文献
        scihelper --wos -d [topic] 从webofscience获取相关主题的文献信息并下载所有文献
        scihelper -d <ditems file> 从规定格式的文件(参考ditems目录下文件)中批量下载文献pdf
        scihelper <ditems file> 从规定格式的文件(参考ditems目录下文件)中批量下载文献pdf
    '''
    print(helpstr)


if len(argv) == 1:
    helpinfo()
    raise ValueError('empty input.')


if not isfile(argv[1]) and ('/' in argv[1] or argv[1][0:6] == 'arXiv:'):
    download_by_doiorserial(argv[1])

elif argv[1] == '--arxiv' and argv[2] != '-d':
    arxiv_getinfo_by_title(' '.join(argv[2:]))
elif argv[1] == '--arxiv' and argv[2] == '-d':
    ditemspath_arxiv = arxiv_getinfo_by_title(' '.join(argv[3:]))
    download_by_file(ditemspath_arxiv)

elif argv[1] == '--wos' and argv[2] == '-link' and argv[3] != '-d':
    wos_getinfo_by_searchurl(' '.join(argv[3:-1]), argv[-1])
elif argv[1] == '--wos' and argv[2] == '-link' and argv[3] == '-d':
    ditemspath_wos = wos_getinfo_by_searchurl(' '.join(argv[4:-1]), argv[-1])
    download_by_file(ditemspath_wos)

elif argv[1] == '--wos' and argv[2] != '-d':
    title, search_url = get_wos_searchurl_by_title(' '.join(argv[2:]))
    wos_getinfo_by_searchurl(title, search_url)
elif argv[1] == '--wos' and argv[2] == '-d':
    title, search_url = get_wos_searchurl_by_title(' '.join(argv[3:]))
    ditemspath_wos = wos_getinfo_by_searchurl(title, search_url)
    download_by_file(ditemspath_wos)

elif isfile(argv[1]) and len(argv) == 2:
    # print("download_by_file from ", argv[1])
    download_by_file(argv[1])

elif argv[1] == '-d' and isfile(argv[2]):
    try:
        download_by_file(argv[2])
    except:
        pass

elif argv[1] == '-h' or argv[1] == '--help':
    helpinfo()

else:
    helpinfo()
    raise ValueError('argument error.')


'''
if __name__ == "__main__":
    # arxiv_getinfo_by_title('QKD')
    # ditemspath = arxiv_getinfo_by_title('rayleigh')
    ditemspath_arxiv = arxiv_getinfo_by_title('PtTe2 monolayer')
    download_by_file(ditemspath_arxiv)

    title, search_url = get_wos_searchurl_by_title('PtTe2 monolayer')
    ditemspath_wos = wos_getinfo_by_searchurl(title, search_url)
    download_by_file(ditemspath_wos)
'''
