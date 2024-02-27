import sys
import os

sys.path.append(os.path.dirname(__file__))

from src.utils import unzip
from src.utils import readconfigs
from src.utils import logging_utils
from src.utils import ArgumentParser
from datetime import datetime
import codecs
import traceback
import re

# 设置日志
logger = logging_utils.init_logger("log_logger")

def info_check_regex(x,file_path):

    retry_count = 0
    max_retries = 2  # 最多尝试转码的次数

    try:
        with open(file_path,mode='r',encoding='utf-8') as file:
            list = []
            r = [
                #银行卡磁道数据-磁道2
                r'[\"\'><\[\]{}&=\uff1a\u4E00-\u9FA5]\s*\d{19}=\d{17,19}\s*[\"\'><\[\]{}&=\uff1a\u4E00-\u9FA5]',
                #银行卡磁道数据-磁道3
                r'(99)\d{19}(=1561560000000000000003000000)\d{1,}',
                #信用卡验证码
                #r'[\"|\'|\:](\d{3})[\"|\']',
                #卡片有效期
                #r'(0[1-9]|1[0-2])\/[0-9]{2}',
                #银行卡账号（自行添加你需要的银行卡段）
                r'(621096|621098|622150|622151|622181|622188|622199|955100|621095|620062|621285|621798|621799|621797|620529|621622|621599|621674|623218|623219)\d{13}',
                r'(62215049|62215050|62215051|62218850|62218851|62218849)\d{11}',
                r'(622812|622810|622811|628310|625919)\d{10}',
                #支付密码
                #r'[\"|\'|\:](\d{6})[\"|\']',
                #用于身份鉴别生物识别信息
                r'([a-zA-Z0-9+/]{1000,})',
                #证件号码
                r'[\"\'><\[\]{}&=\uff1a\u4E00-\u9FA5]\s*[1-9]\d{5}(19|20|(3\d))\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]\s*[\"\'><\[\]{}&=\uff1a\u4E00-\u9FA5]',
                #手机号码
                r'[\"\'><\[\]{}&=\uff1a\u4E00-\u9FA5]\s*1(3\d|4[5-9]|5[0-35-9]|6[2567]|7[0-8]|8\d|9[0-35-9])\d{8}\s*[\"\'><\[\]{}&=\uff1a\u4E00-\u9FA5]',
                #家庭地址
                r'[\"\'><\[\]{}&=\uff1a\u4E00-\u9FA5A-Za-z0-9_]\s*([\u4E00-\u9FA5A-Za-z0-9_]+(省|市|区|县|道|路|街|号)){2,}\s*[\"\'><\[\]{}&=\uff1a\u4E00-\u9FA5A-Za-z0-9_]'
            ]
            
            # 获取文件名
            file_name = os.path.basename(file_path)
            logger.info(f'正则表达式匹配正在处理文件: {file_name}')  # 记录日志：正在处理的文件名

            try:
                #执行level1的扫描
                if ArgumentParser.args.level == "1":
                    data_lines = file.readlines()
                    for i, line in enumerate(data_lines, 1):
                        for rs in r:
                            pattern = re.compile(rs)
                            search_result = re.search(pattern, line)
                            if search_result is not None:
                                match_str = search_result.group()
                                if match_str not in list:
                                    # 将匹配的字符串，文件名，行号添加到结果列表中
                                    list.append([match_str, file_name, i])

                # 执行level2的扫描
                elif ArgumentParser.args.level == "2":
                    # 遍历文件的每一行
                    for i, line in enumerate(file.readlines(), 1):
                        # 对于每个正则表达式
                        for rs in r:
                            # 编译正则表达式
                            pattern = re.compile(rs)
                            # 在当前行中找到正则表达式的所有匹配项
                            matches = re.finditer(pattern, line)
                            # 遍历匹配项
                            for match in matches:
                                # 获取匹配的字符串
                                matched_str = match.group()
                                if matched_str not in list:
                                    # 将匹配的字符串，文件名，行号添加到结果列表中
                                    list.append([matched_str, file_name, i])
                else:
                    print("【Error】扫描等级输入有误，请输入1或2确定扫描等级。")
                    sys.exit()

            # 如果文件打开报错，则自动尝试将文件从gb2312编码转换为UTF-8编码。
            except UnicodeDecodeError:
                while retry_count < max_retries:
                    try:

                        # 以GB2312编码读取文件
                        with codecs.open(file_path, 'r', encoding='gb2312', errors='ignore') as file_content:
                            content = file_content.read()

                        # 以UTF-8编码写入文件
                        with codecs.open(file_path, 'w', encoding='utf-8') as utf8_file:
                            utf8_file.write(content)

                        # 调用处理文件的函数，对刚刚转换过的文件进行处理
                        info_check_regex(None,file_path)
                        
                        break  # 成功转码，退出内部循环

                    except UnicodeDecodeError:
                        retry_count += 1
                else:
                    # 达到最大尝试次数，放弃并继续下一个文件
                    str_print = f'&#8203;``【oaicite:0】``&#8203;文件 {file_path} 自动转码失败。请尝试UTF-8编码方式手动编码后再进行尝试。'
                    print("\033[0;31;40m" + str_print + "\033[0m")
                    logger.error(f'文件 {file_name} 自动转码失败。', exc_info=True)
                retry_count = 0  # 重置尝试计数器

        logger.info(f'正则表达式匹配完成文件处理: {file_path}')  # 记录日志：完成的文件处理

        # 返回结果 return:字符串，文件名，行号
        return list

    except Exception as e:
        # 如果出现错误，打印回溯并记录错误
        traceback.print_exc()
        logger.error(f'正则表达式匹配处理文件时出错: {file_path}', exc_info=True)

def info_check_data(r,file_path):
    
    retry_count = 0
    max_retries = 2  # 最多尝试转码的次数

    try:
        # 初始化一个空列表来存储结果
        list = []

        # 获取文件名
        file_name = os.path.basename(file_path)
        logger.info(f'字段名称匹配正在处理文件: {file_name}')  # 记录日志：正在处理的文件名

        # 以读取模式打开文件
        with open(file_path,mode='r',encoding='utf-8') as file:
            
            # 生成正则表达式列表
            regex_patterns = [re.compile("(" + re.escape(keyword) + ")" + r"(.{18})") for keyword in r]

            try:
                #执行level1的扫描
                if ArgumentParser.args.level == "1":
                    for i, line in enumerate(file.readlines(), 1):
                        # 对于每个正则表达式
                        for pattern in regex_patterns:
                            search_result = re.search(pattern, line)
                            if search_result is not None:
                                match_str = search_result.group(1) # keyword
                                match_val = search_result.group(2)  # 后面的10个字符
                                if [match_str, match_val] not in list:
                                    # 将匹配的字符串，取值结果，文件名，行号添加到结果列表中
                                    list.append([match_str, match_val, file_name, i])

                #执行level2的扫描
                elif ArgumentParser.args.level == "2":
                    # 遍历文件的每一行
                    for i, line in enumerate(file.readlines(), 1):
                        # 对于每个正则表达式
                        for pattern in regex_patterns:
                            # 在当前行中找到正则表达式的所有匹配项
                            matches = pattern.finditer(line)

                            # 遍历匹配项
                            for match in matches:
                                # 获取匹配的字符串以及向后取10个字符的结果
                                matched_str = match.group(1)  # keyword
                                matched_val = match.group(2)  # 后面的10个字符
                                
                                if [matched_str, matched_val] not in list:
                                    # 将匹配的字符串，取值结果，文件名，行号添加到结果列表中
                                    list.append([matched_str, matched_val, file_name, i])

                else:
                    print("【Error】扫描等级输入有误，请输入1或2确定扫描等级。")
                    sys.exit()

            # 如果文件打开报错，则自动尝试将文件从gb2312编码转换为UTF-8编码。
            except UnicodeDecodeError:
                while retry_count < max_retries:
                    try:

                        # 以GB2312编码读取文件
                        with codecs.open(file_path, 'r', encoding='gb2312', errors='ignore') as file_content:
                            content = file_content.read()
                        
                        # 以UTF-8编码写入文件
                        with codecs.open(file_path, 'w', encoding='utf-8') as utf8_file:
                            utf8_file.write(content)

                        # 调用处理文件的函数，对刚刚转换过的文件进行处理
                        info_check_data(r,file_path)

                        break  # 成功转码，退出内部循环
                    except UnicodeDecodeError:
                        retry_count += 1
                else:
                    # 达到最大尝试次数，放弃并继续下一个文件
                    str_print = f'&#8203;``【oaicite:0】``&#8203;文件 {file_path} 自动转码失败。请尝试UTF-8编码方式手动编码后再进行尝试。'
                    print("\033[0;31;40m" + str_print + "\033[0m")
                    logger.error(f'文件 {file_name} 自动转码失败。', exc_info=True)

                retry_count = 0  # 重置尝试计数器

        logger.info(f'字段名称匹配完成文件处理: {file_path}')  # 记录日志：完成的文件处理
        # return: [将匹配的字符串，取值结果，文件名，行号]
        return list

    except Exception as e:
        traceback.print_exc()
        logger.error(f'字段名称匹配处理文件时出错: {file_path}', exc_info=True)

        

#检查单个文件中的敏感信息 return：单个文件的敏感信息list，regex_list（正则敏感信息）data_l30_list（C3敏感信息）data_l20_list（C2敏感信息）
def infoCheck_file(file_path):       
    try:       
        # 获取配置文件中的date
        r30,r31,r20,r21 = readconfigs.readConfigs() #目前正则表达式是写在程序中的，没有从配置文件获取，故只需要使用r30、r20两个参数即可。
        
        # 调用正则表达检查敏感信息
        regex_list = info_check_regex("1",file_path)
        # 调用文本检查敏感信息
        data_l30_list = info_check_data(r30,file_path)
        data_l20_list = info_check_data(r20,file_path)

        return regex_list,data_l30_list,data_l20_list; #regex_list（正则敏感信息）data_l30_list（C3敏感信息）data_l20_list（C2敏感信息）

    except Exception as e:
        traceback.print_exc()
        logger.error(f'处理文件时出错: {file_path}', exc_info=True)   



#检查单个文件中的敏感信息 return：单个文件的敏感信息list，regex_list（正则敏感信息）data_l30_list（C3敏感信息）data_l20_list（C2敏感信息）
def infoCheck_zip(zip_path):       
    try:     
        # 获取配置文件中的date
        r30,r31,r20,r21 = readconfigs.readConfigs() #目前正则表达式是写在程序中的，没有从配置文件获取，故只需要使用r30、r20两个参数即可。
        
        # 获取zip中所有日志的绝对路径
        zip_path_list,temp_dir = unzip.zip_path_list(zip_path) 

        # 创建收集敏感信息list的列表
        regex_list = []
        data_l30_list = []
        data_l20_list = []

        # 遍历解压后的文件路径
        for file_path in zip_path_list:
            # 获取当前时间
            now = datetime.now()
            print("[" + now.strftime("%H:%M:%S") + "] 正在扫描文件：" + file_path)

            # 调用正则表达检查敏感信息
            regex_list_new = info_check_regex("1",file_path)
            if regex_list_new is not None:
                regex_list.extend(regex_list_new)
            # 调用文本检查敏感信息
            data_l30_list_new = info_check_data(r30,file_path)
            if regex_list_new is not None:
                data_l30_list.extend(data_l30_list_new)
            data_l20_list_new = info_check_data(r20,file_path)
            if regex_list_new is not None:
                data_l20_list.extend(data_l20_list_new)


        return regex_list,data_l30_list,data_l20_list,temp_dir; #regex_list（正则敏感信息）data_l30_list（C3敏感信息）data_l20_list（C2敏感信息）临时文件夹绝对路径
    except Exception as e:
        traceback.print_exc()
        logger.error(f'处理文件时出错: {traceback.print_exc()}', exc_info=True) 
        

#检查整个文件夹中的敏感信息 return：整个文件夹的敏感信息list，regex_list（正则敏感信息）data_l30_list（C3敏感信息）data_l20_list（C2敏感信息）
def infoCheck_directory(directory):       
    try:     
        # 获取配置文件中的date
        r30,r31,r20,r21 = readconfigs.readConfigs() #目前正则表达式是写在程序中的，没有从配置文件获取，故只需要使用r30、r20两个参数即可。
        
        # 获取zip中所有日志的绝对路径
        file_path_list = unzip.directory_list(directory) 

        # 创建收集敏感信息list的列表
        regex_list = []
        data_l30_list = []
        data_l20_list = []

        # 遍历解压后的文件路径
        for file_path in file_path_list:
            # 获取当前时间
            now = datetime.now()
            message = "[" + now.strftime("%H:%M:%S") + "] 正在扫描文件：" + file_path

            # 使用\r回车符覆盖上一行的输出
            sys.stdout.write('\r' + message)
            sys.stdout.flush()

            # 调用正则表达检查敏感信息
            regex_list_new = info_check_regex("1",file_path)
            if regex_list_new is not None:
                regex_list.extend(regex_list_new)
            # 调用文本检查敏感信息
            data_l30_list_new = info_check_data(r30,file_path)
            if regex_list_new is not None:
                data_l30_list.extend(data_l30_list_new)
            data_l20_list_new = info_check_data(r20,file_path)
            if regex_list_new is not None:
                data_l20_list.extend(data_l20_list_new)


        return regex_list,data_l30_list,data_l20_list; #regex_list（正则敏感信息）data_l30_list（C3敏感信息）data_l20_list（C2敏感信息）临时文件夹绝对路径
    except Exception as e:
        traceback.print_exc()
        logger.error(f'处理文件时出错: {traceback.print_exc()}', exc_info=True) 