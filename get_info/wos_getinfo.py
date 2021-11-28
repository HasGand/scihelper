from download.download_from_scihub import get_html
from get_info.checkpath import checkpath
from csv import writer
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

    html = get_html(search_url)
    maxpage = get_maxpage(html)
    if maxpage == 1:
        urls = [search_url]
    else:
        if not re.match('.*(page=[0-9]).*', search_url):
            search_url = correct_search_url(search_url)
        urls = generate_page_urls(search_url[:-1], maxpage)

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


def correct_search_url(search_url):
    url = 'http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=GeneralSearch&parentQid=&qid=1&SID={}&&update_back2search_link_param=yes&page=1'
    SID = re.match('.*SID=(.*?)&.*', search_url).group(1)
    url = url.format(SID)
    return url


def write_info(infolist, fditemspath, finfopath):

    with open(finfopath, 'a+', newline='', encoding='utf-8') as f:
        writer_csv = writer(f)
        writer_csv.writerows(infolist)

    doilist = []
    for info in infolist:
        doilist.append(info[3])
    doilist[-1] += '\n'
    with open(fditemspath, 'a+') as f:
        f.write('\n'.join(doilist))


def generate_page_urls(start_url, maxpage):
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
    try:
        pattern = '.*<div.*?class="title">.*?value>(.*?)</value>.*'
        resp = re.match(pattern, html, re.S).group(1).replace('</span>', '')
        return re.sub('<span.*?>', '', resp).strip()
    except:
        pass
    return ' '


def get_author(html):
    try:
        pattern = 'alt=.*?by this author.*?</a> \((.*?)\)<sup>'
        resp = re.findall(pattern, html)
        return resp
    except:
        pass
    return ' '


def get_year(html):
    try:
        pattern = '<value>([A-Z]{3} [0-9]{4})</value>'
        # 读中间无数
        resp = re.findall(pattern, html, re.S)

        if len(resp) == 0:
            pattern = '<value>([A-Z]{3} [0-9]{1,} [0-9]{4})</value>'
            # 读中间有数
            resp = re.findall(pattern, html, re.S)
        return resp[0].strip()
    except:
        pass
    return ' '


def get_doi(html):
    try:
        pattern = '.*DOI.*?>([0-9].*?)<.*'
        resp = re.match(pattern, html, re.S)
        return resp.group(1).strip()
    except:
        pass
    return ' '


def get_abstract(html):
    try:
        pattern = '.*Abstract.*?FR_field">(.*?)</p>'
        resp = re.match(pattern, html, re.S).group(1).replace('</span>', '')
        return re.sub('<span.*?>', '', resp).strip()
    except:
        pass
    return ' '


if __name__ == "__main__":
    doi = '10.1038/s41699-018-0085-z'
    url = 'https://apps.webofknowledge.com/Search.do?product=UA&SID=F4KRVd4MyGCWNVheOhG&search_mode=GeneralSearch&prID=f9b261e8-eba4-4654-afa2-37546caf5e08'
    url = 'https://apps.webofknowledge.com/Search.do?product=UA&SID=&search_mode=GeneralSearch&prID=de086a2f-a24a-41a6-9b48-acd5df8c2962'
    url = 'http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=GeneralSearch&parentQid=&qid=1&SID=F4KRVd4MyGCWNVheOhG&&update_back2search_link_param=yes&page=1'
    url = 'https://apps.webofknowledge.com/Search.do?product=UA&SID=F4KRVd4MyGCWNVheOhG&search_mode=GeneralSearch&prID=42c7aba0-a8a4-4e0f-8782-1c9de8065f75'
    html = get_html(url)
    get_maxpage(html)
    urls_per_page = get_urls_per_page(html)

    infolist = []
    for url_per in urls_per_page:
        html_per = get_html(url_per)
        print(url_per)
        info = get_info(html_per)
        infolist.append(info)

    wos_getinfo_by_searchurl('PtTe2 monolayer', url)

    with open('temp-sci.txt', 'w', encoding='utf-8') as f:
        f.write(html)

    # wos给出的url是临时生成的，有时效 ??? 主要是 SID
