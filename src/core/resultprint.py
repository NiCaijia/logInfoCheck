import sys
import os
import traceback

sys.path.append(os.path.dirname(__file__))

from src.utils import ArgumentParser
import csv

def result_print_txt(regex_list,data_l30_list,data_l20_list):
    
    try:
        # 如果参数为空，将其设为一个空列表
        if regex_list is None:
            regex_list = []
        if data_l30_list is None:
            data_l30_list = []
        if data_l20_list is None:
            data_l20_list = []

        c = 0
        newpath = ArgumentParser.args.savename + ".txt"
        
        # 使用 with 语句自动管理文件，确保文件正确关闭
        with open(newpath, "w", encoding='utf-8') as f1:
            f1.write('C3字段匹配结果' + '\n')
            for l in data_l30_list:
                f1.write(str(l) + '\n')
                c = c+1

            f1.write('\n' + 'C2字段匹配结果' + '\n')
            for l in data_l20_list:
                f1.write(str(l) + '\n')
                c = c+1

            f1.write('\n' + 'C3C2正则字段匹配结果' + '\n')
            for l in regex_list:
                f1.write(str(l) + '\n')
                c = c+1

        return c

    except Exception as e:
        traceback.print_exc()


def result_print_csv(regex_list,data_l30_list,data_l20_list):

    try:
        # 如果参数为空，将其设为一个空列表
        if regex_list is None:
            regex_list = []
        if data_l30_list is None:
            data_l30_list = []
        if data_l20_list is None:
            data_l20_list = []

        newpath = ArgumentParser.args.savename + ".csv" 

        with open(newpath,"w",newline='',encoding='utf-8') as f1:

            writer = csv.writer(f1)

            # 写入表头
            writer.writerow(['敏感数据类型','配置文件匹配字段','疑似敏感信息','文件名称','检出行数'])

            # 写入C3无正则字段匹配结果
            for l in data_l30_list:
                writer.writerow(['C3字段匹配结果',l[0]]+l[1:])

            # 写入C2无正则字段匹配结果
            for l in data_l20_list:
                writer.writerow(['C2字段匹配结果',l[0]]+l[1:])

            # 写入C3C2正则字段匹配结果
            for l in regex_list:
                writer.writerow(['C3C2正则字段匹配结果','None']+l)
    except Exception as e:
        traceback.print_exc()

