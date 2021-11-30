import os
import re
import requests
from resources.User_agent_list import User_agent_list

requests.packages.urllib3.disable_warnings()


def scihub_download(doi, cache, DIR='./references/pdf/'):
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    if DIR[-1] != '/':
        DIR += '/'

    html_url = generate_html_url(doi)
    html = get_html(html_url)
    url = get_pdf_url(html)
    flag = download_pdf(url, DIR)
    if flag == 1:
        cache[doi] = url
    else:
        cache[doi] = None
    return flag


def download_pdf(url, DIR, user_agent=User_agent_list[0], proxies=None):

    try:
        pdfname = url.split('/')[-1]
    except Exception as e:
        print("pdf_url error: ", e)

    headers = {'User-Agent': user_agent}
    try:
        print("Downloading: ", url)
        # 这一步get请求需要的时间最久
        response = requests.get(url, headers=headers,
                                proxies=proxies, verify=False)
        if response.status_code == 200:
            with open(DIR + pdfname, 'wb') as f:
                f.write(response.content)
            print("Download complete.")
            return 1
        else:
            print("Download error (arxiv): ")
    except requests.exceptions.RequestException as e:
        print("Download error (scihub): ", e)
    return 0


def get_pdf_url(html):
    """
    使用正则表达式获取pdf url
    此处可能需要维护
    """
    # pattern = '.*<embed type="application/pdf" src=".*(//.*?pdf).*id = "pdf">.*'
    pattern = '.*http.*?//(.*?sci-hub.*?pdf).*?(download=true).*'
    try:
        res = re.match(pattern, html, re.S)
        pdf_url = 'https://' + res.group(1)
    except Exception as e:
        print("get_pdf_url error(): ", e)
        pdf_url = None
    return pdf_url


def get_html(url, user_agent=User_agent_list[0], proxies=None, num_retries=2):
    """
    获取Sci-Hub的(doi)html源码
    """
    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(url, headers=headers,
                                proxies=proxies, verify=False)
        html = response.text
        if response.status_code >= 400:
            print('Download html error: ', response.status_code)
            html = None
            if num_retries and 500 <= response.status_code < 600:
                return get_html(url, user_agent, proxies, num_retries - 1)
    except requests.exceptions.RequestException as e:
        print('Download html error: ', e)
        return None
    return html


def generate_html_url(doi, start_url='sci-hub.se/'):
    if len(doi.split('/')) < 2:
        print("doi error")
        return None
    url = 'https://' + start_url + doi
    return url


if __name__ == "__main__":
    doi = '10.1021/acsami.9b21838'
    doi = '10.1038/s41699-018-0085-z'
    doi = '10.1016/j.cpc.2021.108180'  # 不存在
    doi = '10.1016/j.physe.2021.114925'
    html_url = generate_html_url(doi)
    html = get_html(html_url)
    pdf_url = get_pdf_url(html)
    print(pdf_url)

    with open('temp.txt', 'w', encoding='utf-8') as f:
        f.write(html)
