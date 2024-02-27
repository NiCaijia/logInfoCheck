import sys
import os

sys.path.append(os.path.dirname(__file__))

import zipfile
import chardet
import codecs
import tempfile
import rarfile
import traceback
import gzip
import shutil
from src.utils import logging_utils

logger = logging_utils.init_logger("log_logger")

def extract_compressed_files(filename):
    try:
        # 获取当前项目的目录
        project_dir = os.path.dirname(os.path.abspath(__file__))
        # 获取当前项目的上两层路径
        parent_dir = os.path.abspath(os.path.join(project_dir, "../../temp"))
    
        # 创建保存文件夹


        # 创建临时文件夹
        temp_dir = tempfile.mkdtemp(dir=parent_dir)

        # 获取文件后缀名
        file_extension = os.path.splitext(filename)[1]

        # 根据文件后缀名选择相应的解压缩库
        if file_extension == ".zip":
            extract_zip_files(filename, temp_dir)
        elif file_extension == ".rar":
            extract_rar_files(filename, temp_dir)
        else:
            print("当前版本仅支持'.zip'，'.rar'两种压缩格式文件。请更换压缩格式重新尝试。")
            return
        
        # 返回本次调用解压后的临时文件夹目录
        return temp_dir
    
    except Exception as e:
        traceback.print_exc()

#获取传入zip文件中所有日志文件在解压到临时文件夹中绝对路径的集合 return：zip中所有日志的绝对路径
def zip_path_list(filename):
    try:
        # 解压zip文件到临时文件夹并获取临时文件夹路径
        temp_dir = extract_compressed_files(filename)

        zip_path_list = []
        # 遍历文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(temp_dir):
            # 遍历当前文件夹中的文件
            for file_name in files:
                # 获取文件的绝对路径
                file_path = os.path.join(root, file_name)
                zip_path_list.append(file_path)

        return zip_path_list, temp_dir

    except Exception as e:
        traceback.print_exc()


#获取传入文件夹中所有日志文件的绝对路径集合 return：文件夹中所有日志的绝对路径
def directory_list(directory):
    try:
        file_path_list = []
        # 遍历文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(directory):
            # 遍历当前文件夹中的文件
            for file_name in files:
                # 获取文件的绝对路径
                file_path = os.path.join(root, file_name)
                file_path_list.append(file_path)

        return file_path_list

    except Exception as e:
        traceback.print_exc()



def extract_zip_files(filename, temp_dir):
    try:
        # 打开ZIP压缩文件
        zip_file = zipfile.ZipFile(os.path.normpath(filename), "r")
        logger.info("打开zip压缩文件" + str(zip_file) + "。")
        # 递归遍历当前ZIP压缩文件中的所有文件和文件夹
        for file_name in zip_file.namelist():

            # 检查是否为文件夹
            if file_name.endswith('/'):
                # 创建对应的文件夹
                folder_path = os.path.join(temp_dir, file_name)
                os.makedirs(folder_path, exist_ok=True)
            else:
                try:
                    # 读取文件内容
                    file_content = zip_file.read(file_name)

                    # 使用 chardet 模块自动检测文件的编码方式
                    detection = chardet.detect(file_content)
                    encoding = detection["encoding"]

                    # 如果无法检测到编码，将其设置为utf-8
                    if encoding is None:
                        encoding = "utf-8"

                    # 使用 codecs 模块将文件内容从检测到的编码方式解码为字符串
                    file_content_str = codecs.decode(file_content, encoding, "ignore")

                    # 将字符串编码为 utf-8
                    file_content_utf8 = file_content_str.encode('utf-8')

                    # 将文件内容写入临时文件夹中
                    file_path = os.path.join(temp_dir, file_name)
                    with open(file_path, "wb") as f:
                        f.write(file_content_utf8)

                except UnicodeDecodeError:
                    str_print = f'【Error】解压缩文件 {file_name} 自动转码失败。请尝试UTF-8编码方式手动编码后再进行尝试。'
                    print("\033[0;31;40m" + str_print + "\033[0m")
                    logger.error(f'解压缩文件 {file_name} 自动转码失败。', exc_info=True)

        # 关闭ZIP压缩文件
        zip_file.close()

    except Exception as e:
        traceback.print_exc()

def extract_rar_files(filename, temp_dir):
    try:
        # 打开RAR压缩文件
        rar_file = rarfile.RarFile(filename)

        # 递归遍历当前RAR压缩文件中的所有文件和文件夹
        for file_info in rar_file.infolist():
            
            # 修复文件路径，确保使用正确的斜线
            corrected_filename = file_info.filename.replace('/', os.sep)
            
            # 检查是否为文件夹
            if file_info.isdir():
                # 创建对应的文件夹
                folder_path = os.path.join(temp_dir, corrected_filename)
                os.makedirs(folder_path, exist_ok=True)
            else:
                try:
                    # 读取文件内容
                    file_content = rar_file.read(file_info.filename)
                    # 使用 chardet 模块自动检测文件的编码方式
                    detection = chardet.detect(file_content)
                    encoding = detection["encoding"]
                    # 使用 codecs 模块将文件内容从检测到的编码方式转换为 utf-8 编码
                    file_content = codecs.decode(file_content, encoding, "ignore")
                    file_content = codecs.encode(file_content, "utf-8")

                    # 将文件内容写入临时文件夹中
                    file_path = os.path.join(temp_dir, corrected_filename)
                    with open(file_path, "wb") as f:
                        f.write(file_content)

                except UnicodeDecodeError:
                    str_print = f'【Error】解压缩文件 {file_info.filename} 自动转码失败。请尝试UTF-8编码方式手动编码后再进行尝试。'
                    print("\033[0;31;40m" + str_print + "\033[0m")
                    logger.error(f'解压缩文件 {file_info.filename} 自动转码失败。', exc_info=True)

        # 关闭RAR压缩文件
        rar_file.close()

    except Exception as e:
        traceback.print_exc()
               
#批量解压gz  调用函数，传入你想要解压的目录
def extract_and_delete_gz_files(path):
    if os.path.isfile(path):
        if path.endswith(".gz"):
            with gzip.open(path, 'rb') as f_in:
                new_filename = path[:-3]  # 新文件名，去除 .gz 扩展名
                with open(new_filename, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(path)
            return new_filename
        else:
            print(f"Skipping non-gzipped file: {path}")
    elif os.path.isdir(path):
        # 如果传入的是文件夹，找到文件夹中的.gz文件并解压
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".gz"):
                    file_path = os.path.join(root, file)
                    with gzip.open(file_path, 'rb') as f_in:
                        with open(file_path[:-3], 'wb') as f_out:  # 移除 .gz 扩展名
                            shutil.copyfileobj(f_in, f_out)
                    os.remove(file_path)
    else:
        print(f"Invalid path: {path}")