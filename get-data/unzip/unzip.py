from pathlib import Path
import zipfile

def unzip_del_zip(dl_zips, data_dir_path):
    for dl_zip in dl_zips:
        
        extract_file_name = dl_zip.stem # 拡張子を除いたファイル名を取得
        extract_folder = Path(data_dir_path, extract_file_name) # zipファイル名のフォルダを作成
        
        with zipfile.ZipFile(dl_zip) as zip_file:
            zip_file.extractall(extract_folder) # zipファイルを指定のフォルダに展開
            print('展開完了')

        dl_zip.unlink(missing_ok=True) # 展開したzipファイルを削除

if __name__ == '__main__':
    unzip_del_zip()