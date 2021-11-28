import os
import requests
from resources.User_agent_list import User_agent_list

requests.packages.urllib3.disable_warnings()

# https://arxiv.org/pdf/xxx
# arXiv:2111.12067


def arxiv_download(serial, cache, DIR='./references/pdf/'):
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    if DIR[-1] != '/':
        DIR += '/'

    url = generate_pdf_url(serial)
    flag = download_pdf(url, DIR)
    if flag == 1:
        cache[serial] = url
    else:
        cache[serial] = None
    return flag


def download_pdf(url, DIR, user_agent=User_agent_list[0], proxies=None):
    try:
        pdfname = url.split('/')[-1] + '.pdf'
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
        print("Download error (arxiv): ", e)
    return 0


def generate_pdf_url(serial):
    try:
        serial = serial.split(':')
        if len(serial) != 2:
            print("serial错误")
            return None
    except:
        pass
    url = 'https://arxiv.org/pdf/' + serial[-1]
    return url
