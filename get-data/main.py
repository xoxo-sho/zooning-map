from crawler.crawler import webdriver_setup, web_crawler
from unzip.unzip import unzip_del_zip

from pathlib import Path

# ダウンロードファイルのフォルダを作成(カレントディレクトリに「data-set」フォルダを作成)
data_dir_path = Path(Path.cwd(), 'data-set')
data_dir_path.mkdir(exist_ok=True, parents=True) # make directry

# 対象のURL
html = 'https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-A29.html'


def main():
    # web driverのセットアップ
    driver = webdriver_setup(data_dir_path, html)

    # クローラー実行
    web_crawler(driver)

    # zipファイルのpathを取得
    dl_zips = data_dir_path.glob('*.zip')

    # zipファイルを展開してzipファイルを削除
    unzip_del_zip(dl_zips, data_dir_path)



    print('Done')



if __name__ == '__main__':
    main()