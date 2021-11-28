import re
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains


def get_wos_searchurl_by_title(title):
    wos_url = 'http://apps.webofknowledge.com'
    url = 'http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=GeneralSearch&parentQid=&qid=1&SID={}&&update_back2search_link_param=yes&page=1'

    '''
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: ()= > undefined
        })
      """
    })
    '''
    driver = webdriver.Chrome()
    driver.get(wos_url)
    driver.get(wos_url)

    driver.find_element_by_xpath(
        '//*[@id="value(input1)"]').send_keys(title)
    search_button = driver.find_element_by_xpath(
        '//*[@id="searchCell1"]/span[1]/button')
    ActionChains(driver).click(search_button).perform()

    SID = re.match('.*SID=(.*?)&.*', driver.current_url).group(1)
    url = url.format(SID)

    driver.close()

    return title, url


if __name__ == "__main__":
    get_wos_searchurl_by_title('PtTe2 monolayer')
