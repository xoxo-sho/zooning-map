from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

import time

def webdriver_setup(data_dir_path, html):
    
    chrome_options = Options() # webdriverにオプションを追加
    prefs = {"download.default_directory": str(data_dir_path)} # ダウンロード先のディレクトリ指定
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("detach", True) # ディタッチモード（実行完了後もドライバーが終了しない）

    # Google Cromeで対象のページを開く
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Remote(command_executor="http://selenium:4444/wd/hub",options=chrome_options)
    driver.implicitly_wait(10) # xpathが見つかるまで10秒待機
    driver.get(html)

    return driver

def web_crawler(driver):
    # ダウンロードボタンを取得
    elements = driver.find_elements(by=By.ID, value='menu-button')

    for element in elements:
        # ダウンロードボタン押下
        element.click()

        # try:
        #     # アンケートのスキップボタンが出たきたらクリック
        #     driver.find_element(by=By.XPATH, value='//div[text()="スキップする"]').click()
        # except:
        #     pass

        # アンケートのスキップボタンが出たきたらクリック
        if EC.alert_is_present()(driver):

            alert = driver.switch_to.alert
            print(alert.text)
            alert.accept()
            time.sleep(1)

        elif len(driver.find_elements(by=By.XPATH, value='//div[text()="スキップする"]')) > 0:

            driver.find_element(by=By.XPATH, value='//div[text()="スキップする"]').click()

            # ダウンロードに移るアラート処理
            wait = WebDriverWait(driver,20)

            wait.until(EC.alert_is_present()) # Javascriptのアラートがでてくるまで待つ
            Alert(driver).accept()
            # time.sleep(10) # ダウンロード時間を確保

        else:
            pass

    driver.quit()

if __name__ == '__main__':
    import sys
    print(sys.path)