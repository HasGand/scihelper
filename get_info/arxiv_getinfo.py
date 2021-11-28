from download.download_from_scihub import get_html
from get_info.checkpath import checkpath
from math import ceil
from csv import writer
import re


def arxiv_getinfo_by_title(title, DIR='./references/'):
    fditemspath, finfopath = checkpath(title, DIR)

    search_url = generate_search_url(title)
    # 仅返回去除start=0的部分
    html = get_html(search_url)
    pages = get_pages(html)
    # 通过总页数 运算得到数组
    search_urls = generate_search_url(title, pages=pages)
    # 返回包含start部分，数组
    infolist = get_infolist(html)
    count = len(infolist[0])
    print(search_url)
    write_info(infolist, fditemspath=fditemspath, finfopath=finfopath)

    if isinstance(search_urls, list):
        for url in search_urls[1:]:
            html = get_html(url)
            infolist = get_infolist(html)
            count += len(infolist[0])
            print(url)
            write_info(infolist, fditemspath=fditemspath, finfopath=finfopath)
    print("{} items have been written.".format(count))
    # 写入ditems.txt & 写入标题 作者 年份(Submitted) serial 摘要(full)

    return fditemspath


def write_info(infolist, fditemspath, finfopath):

    infolist[3][-1] += '\n'
    with open(fditemspath, 'a+') as f:
        f.write('\n'.join(infolist[3]))

    infolist = zip(*infolist)

    with open(finfopath, 'a+', encoding='utf-8', newline='') as f:
        writer_csv = writer(f)
        writer_csv.writerows(infolist)


def get_infolist(html):
    """
    获取每个网页上的所有信息
    title author year serial abstract
    返回一个数组
    """
    pattern_sub = re.compile('<span.*?>')

    # 后的正则表达式不需要编译，只是用了一次
    pattern_title = re.compile('<p class="title.*?>(.*?)</p>', re.S)
    titles = pattern_title.findall(html)
    titles_list = []

    pattern_authors = re.compile(
        '<span class=".*?Authors.*?span>(.*?)</p>', re.S)
    authors = pattern_authors.findall(html)
    pattern_author_per = re.compile('<a href.*?>(.*?)</a>', re.S)
    authors_list = []

    serials_list = []

    pattern_abstract = re.compile(
        '<span class="abstract-full.*?id="(.*?[0-9].*?)-abstract-full.*?>(.*?)<a class', re.S)
    abstracts = pattern_abstract.findall(html)
    abstracts_list = []

    pattern_year = re.compile('>Submitted<.*?([0-9].*?[0-9]);', re.S)
    years_list = pattern_year.findall(html)

    for i in range(len(titles)):
        try:
            title = titles[i].strip().replace('</span>', '')
            title = pattern_sub.sub('', title)
            titles_list.append(title)

            author = pattern_author_per.findall(authors[i])
            authors_list.append(author)

            serial = 'arXiv:' + abstracts[i][0]
            serials_list.append(serial)

            abstract = abstracts[i][1].strip()
            abstracts_list.append(abstract)
        except Exception as e:
            print("get_infolist() error: ", e)
    return titles_list, authors_list, years_list, serials_list, abstracts_list


def generate_search_url(title, pages=[0]):

    title = title.replace(' ', '+')

    url = f'https://arxiv.org/search/?query={title}&searchtype=title&abstracts=show&order=-announced_date_first&size=200'

    if len(pages) == 1:
        return url

    urls = []
    for page in pages:
        urls.append(url + f'&start={page}')
    return urls


def get_pages(html, num_per_page=200):
    # pattern = '.*Showing [0-9].*[0-9] of ([0-9]{1,}.*[0-9]) results for .*'
    pattern = '.*Showing 1.*?of ([0-9].*?) results.*'
    rep = re.match(pattern, html, re.S)
    num = int(rep.group(1).replace(',', ''))
    if num > 10000:
        num = 10000
    maxpage = ceil(num/num_per_page)
    pages = []
    for page in range(maxpage):
        pages.append(page * num_per_page)
    return pages


def get_serial_by_doi(doi):
    doir = doi.replace('/', '%2F')
    url = 'https://arxiv.org/search/?query={}&searchtype=doi&abstracts=show&order=-announced_date_first&size=50'.format(
        doir)
    html = get_html(url)
    pattern = '.*Showing 1.*?of ([0-9].*?) results.*'
    try:
        resp = re.match(pattern, html, re.S)
        if int(resp.group(1)) == 1:
            serial = get_infolist(html)[3][0]
            print("从arxiv下载: {}".format(doi))
            return serial
    except:
        print("arxiv also don't has: {}".format(doi))
        pass
    return None


if __name__ == "__main__":

    arxiv_getinfo_by_title('PtTe2 monolayer')
    arxiv_getinfo_by_title('phase field')
    arxiv_getinfo_by_title('QKD')  # 部分 arXiv 不同
    arxiv_getinfo_by_title('rayleigh')

    search_url = generate_search_url('rayleigh')
    search_url = 'https://arxiv.org/search/?query=Heat+transfer+mechanisms&searchtype=title&abstracts=show&order=-announced_date_first&size=200'
    html = get_html(search_url)
    pages = get_pages(html)
    info = get_infolist(html)

    doi = '10.1021/acs.chemmater.1c02683'
    get_serial_by_doi(doi)
