from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
# from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

from ipyleaflet import Map, Polygon, basemaps, LegendControl
from lxml import etree
import zipfile

# ダウンロードファイルのフォルダを作成(カレントディレクトリに「data-set」フォルダを作成)
data_dir_path = Path(Path.cwd(), 'data-set')
data_dir_path.mkdir(exist_ok=True, parents=True) # make directry

# 対象のURL
html = 'https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-A29.html'

# webdriverにオプションを追加
chrome_options = Options()
prefs = {"download.default_directory": str(data_dir_path)} # ダウンロード先のディレクトリ指定
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option("detach", True) # ディタッチモード（実行完了後もドライバーが終了しない）

# Google Cromeで対象のページを開く
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10) # xpathが見つかるまで10秒待機
driver.get(html)

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

dl_zips = data_dir_path.glob('*.zip')

for dl_zip in dl_zips:
    
    extract_file_name = dl_zip.stem # 拡張子を除いたファイル名を取得
    extract_folder = Path(data_dir_path, extract_file_name) # zipファイル名のフォルダを作成
    
    with zipfile.ZipFile(dl_zip) as zip_file:
        zip_file.extractall(extract_folder) # zipファイルを指定のフォルダに展開

    dl_zip.unlink(missing_ok=True) # 展開したzipファイルを削除
    

# 用途地域の色を指定（マップに塗りつぶす色）
color_dic = {
    "第一種低層住居専用地域": "#440154",
    "第二種低層住居専用地域": "#481f70", 
    "第一種中高層住居専用地域": "#443983", 
    "第二種中高層住居専用地域": "#3b528b", 
    "第一種住居地域": "#31688e", 
    "第二種住居地域": "#287c8e", 
    "準住居地域": "#21918c", 
    "近隣商業地域": "#20a486", 
    "商業地域": "#35b779", 
    "準工業地域": "#5ec962", 
    "工業地域": "#90d743", 
    "工業専用地域": "#c8e020", 
    "不明": "#fde725", 
}

def main():
    print('Done')

if __name__ == '__main__':
    main()