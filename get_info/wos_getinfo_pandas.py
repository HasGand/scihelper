from download.download_from_scihub import get_html
from get_info.checkpath import checkpath
from pandas import DataFrame
import re


def wos_getinfo_by_searchurl(title, search_url, DIR='./references/'):
    """
    判断存在文件
    根据title得到搜索界面url
    获取最大page num
    获取所有搜索页面的urls
    获取每个搜索页面存在的文献urls_per_page
    获取每个文献页面的info
    将每个文献页面的info写入文件
    """
    fditemspath, finfopath = checkpath(title, DIR)

    if search_url[-1] != '1':
        urls = [search_url]
    else:
        html = get_html(search_url)
        maxpage = get_maxpage(html)
        urls = generate_page_urls(maxpage, start_url=search_url[:-1])

    for url in urls:
        html = get_html(url)
        urls_per_page = get_urls_per_page(html)
        infolist = []
        for url_per in urls_per_page:
            html_per = get_html(url_per)
            print(url_per)
            info = get_info(html_per)
            infolist.append(info)
        write_info(infolist, fditemspath=fditemspath, finfopath=finfopath)
    # 写入ditems.txt & 写入标题 作者 年份 doi 摘要(full)

    return fditemspath


def input_search_url(search_url=''):
    search_url = input("请输入搜索页面链接: ")
    return search_url


def write_info(infolist, fditemspath, finfopath):

    data = DataFrame(infolist)
    # data.columns = ['title', 'author', 'year', 'doi', 'abstract']

    data.to_csv(finfopath, index=False, header=False,
                mode='a', encoding="utf_8_sig")

    doilist = data[3].tolist()
    doilist[-1] += '\n'
    with open(fditemspath, 'a+') as f:
        f.write('\n'.join(doilist))


def generate_page_urls(maxpage, start_url):
    urls = []
    for i in range(1, maxpage+1):
        urls.append(start_url + str(i))
    return urls


def get_maxpage(html):
    pattern = '.*pageCount.top.*?([0-9]{1,})</span.*'
    resp = re.match(pattern, html, re.S)
    return int(resp.group(1))


def get_urls_per_page(html):
    pattern = '<a class=.*?full-record" href="(/full_record.*?amp.*?page.*?doc=[0-9]{1,})">'
    resp = re.findall(pattern, html, re.S)
    urls = []
    for url in resp:
        url = url.replace('amp;', '')
        urls.append('https://apps.webofknowledge.com' + url)
    return urls


def get_info(html):
    return get_title(html), get_author(html), get_year(html), get_doi(html), get_abstract(html)


def get_title(html):
    pattern = '.*<div.*?class="title">.*?value>(.*?)</value>.*'
    resp = re.match(pattern, html, re.S).group(1).replace('</span>', '')
    return re.sub('<span.*?>', '', resp)


def get_author(html):
    pattern = 'alt=.*?by this author.*?</a> \((.*?)\)<sup>'
    resp = re.findall(pattern, html)
    return resp


def get_year(html):
    pattern = '<value>([A-Z]{3} [0-9]{4})</value>'
    # 读中间无数
    resp = re.findall(pattern, html, re.S)

    if len(resp) == 0:
        pattern = '<value>([A-Z]{3} [0-9]{1,} [0-9]{4})</value>'
        # 读中间有数
        resp = re.findall(pattern, html, re.S)
    return resp[0]


def get_doi(html):
    pattern = '.*DOI.*?>([0-9].*?)<.*'
    resp = re.match(pattern, html, re.S)
    return resp.group(1)


def get_abstract(html):
    pattern = '.*Abstract.*?FR_field">(.*?)</p>'
    resp = re.match(pattern, html, re.S).group(1).replace('</span>', '')
    return re.sub('<span.*?>', '', resp).strip()


if __name__ == "__main__":
    doi = '10.1038/s41699-018-0085-z'
    url = 'http://apps.webofknowledge.com/full_record.do?product=UA&search_mode=GeneralSearch&qid=1&SID=F4p93Hv3gl5ggRcwi1m&page=1&doc=1'
    html = get_html(url)
    get_year(html)

    wos_getinfo_by_searchurl('PtTe2 monolayer')
    html = get_html(
        'https://apps.webofknowledge.com/full_record.do?product=UA&search_mode=GeneralSearch&qid=2&SID=7A4DuoqnQM8PIFB1OyY&page=1&doc=3')
    with open('temp-sci.txt', 'w', encoding='utf-8') as f:
        f.write(html)

    sigle_url = 'https://apps.webofknowledge.com/Search.do?product=UA&SID=7A4DuoqnQM8PIFB1OyY&search_mode=GeneralSearch&prID=f782baeb-84cc-494a-8a42-76d7237ab423'
    sigle_url = 'https://apps.webofknowledge.com/Search.do?product=UA&SID=7A4DuoqnQM8PIFB1OyY&search_mode=GeneralSearch&prID=7b152cd1-2391-465c-b92b-39bad654f541'
    url = 'https://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=GeneralSearch&parentQid=&qid=2&SID=7A4DuoqnQM8PIFB1OyY&&update_back2search_link_param=yes&page=1'
    url = 'https://apps.webofknowledge.com/Search.do?product=UA&SID=7A4DuoqnQM8PIFB1OyY&search_mode=GeneralSearch&prID=cce8906d-3910-487f-bab1-616ba38da8ef'
    url = 'https://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=GeneralSearch&parentQid=&qid=40&SID=7A4DuoqnQM8PIFB1OyY&&update_back2search_link_param=yes&page=1'

    # wos给出的url是临时生成的，有时效 ??? 主要是 SID
