import sys
import os

sys.path.append(os.path.dirname(__file__))

from src.core import resultprint
from src.core import infocheck
from src.utils import ArgumentParser
from src.utils import logging_utils
from src.utils import unzip
import shutil
from datetime import datetime

if sys.version_info < (3, 2):
    sys.stdout.write("日志检查工具不支持python2版本，请使用python3.2以上版本运行。")
    sys.exit(1)


class Program(object):

    logger = logging_utils.init_logger("log_logger")

    def __init__(self):
        self.c = None

        # 检查哪个参数被设置了，然后执行相应的操作
        if ArgumentParser.args.filename:
            start = datetime.now()
            print("扫描中...")

            if ArgumentParser.args.extract_gz:
                
                print("[" + datetime.now().strftime("%H:%M:%S") + "] 正在解压gz文件...")

                new_filename = unzip.extract_and_delete_gz_files(ArgumentParser.args.filename)
                ArgumentParser.args.filename = new_filename

                print("[" + datetime.now().strftime("%H:%M:%S") + "] 解压完成")

            #regex_list（正则敏感信息）data_l30_list（C3敏感信息）data_l20_list（C2敏感信息）
            regex_list,data_l30_list,data_l20_list = infocheck.infoCheck_file(ArgumentParser.args.filename)

            #将文件检查结果写入txt
            self.c = resultprint.result_print_txt(regex_list,data_l30_list,data_l20_list)

            #将文件检查结果写入csv
            resultprint.result_print_csv(regex_list,data_l30_list,data_l20_list)

            print("\n")
            print("共扫描出日志疑似敏感数据" + str(self.c) + "条，详情见" + ArgumentParser.args.savename + ".txt及info_check.csv")
            end = datetime.now()
            print("\n扫描用时"+str(end-start))

        elif ArgumentParser.args.zipname:

            start = datetime.now()
            print("扫描中...")

            #[regex_list（正则敏感信息）data_l30_list（C3敏感信息）data_l20_list（C2敏感信息）]
            regex_list,data_l30_list,data_l20_list,temp_dir = infocheck.infoCheck_zip(os.path.normpath(ArgumentParser.args.zipname))
            
            #将文件检查结果写入txt
            self.c = resultprint.result_print_txt(regex_list,data_l30_list,data_l20_list)

            #将文件检查结果写入csv
            resultprint.result_print_csv(regex_list,data_l30_list,data_l20_list)

            # 删除临时文件夹
            shutil.rmtree(temp_dir)
            
            print("\n")
            print("共扫描出日志疑似敏感数据" + str(self.c) + "条，详情见" + ArgumentParser.args.savename + ".txt及info_check.csv")
            end = datetime.now()
            print("\n扫描用时"+str(end-start))

        elif ArgumentParser.args.directory:

            start = datetime.now()
            print("扫描中...")

            if ArgumentParser.args.extract_gz:

                print("[" + datetime.now().strftime("%H:%M:%S") + "] 正在解压gz文件...")

                unzip.extract_and_delete_gz_files(ArgumentParser.args.directory)

                print("[" + datetime.now().strftime("%H:%M:%S") + "] 解压完成！")

            #[regex_list（正则敏感信息）data_l30_list（C3敏感信息）data_l20_list（C2敏感信息）]
            regex_list,data_l30_list,data_l20_list = infocheck.infoCheck_directory((ArgumentParser.args.directory))
            
            #将文件检查结果写入txt
            self.c = resultprint.result_print_txt(regex_list,data_l30_list,data_l20_list)

            #将文件检查结果写入csv
            resultprint.result_print_csv(regex_list,data_l30_list,data_l20_list)

            print("\n")
            print("共扫描出日志疑似敏感数据" + str(self.c) + "条，详情见" + ArgumentParser.args.savename + ".txt及info_check.csv")
            end = datetime.now()
            print("\n扫描用时"+str(end-start))

        else:
            print('Neither f nor z was chosen.')
            # 这里是没有任何参数被设置时的操作


if __name__ == "__main__":

    main = Program()
