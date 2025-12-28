import sys
import os

sys.path.append(os.path.dirname(__file__))

from src.core import resultprint
from src.core import infocheck
from src.utils import ArgumentParser
from src.utils import logging_utils
from src.utils import unzip
from src.utils import output_formatter
from src.utils import banner
import shutil
from datetime import datetime


if sys.version_info < (3, 7):
    sys.stdout.write(
        "日志检查工具需要 Python 3.7 或更高版本运行。\n"
        "当前 Python 版本: {}.{}.{}\n"
        "请升级 Python 版本后重试。\n".format(
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro
        )
    )
    sys.exit(1)



class Program(object):

    logger = logging_utils.init_logger("log_logger")

    def __init__(self):
        self.c = None
        
        # 显示启动 Logo
        self._print_logo()
        
        # 根据命令行参数设置是否启用彩色输出
        if hasattr(ArgumentParser.args, 'no_color') and ArgumentParser.args.no_color:
            output_formatter.set_color_enabled(False)
        
        # Level 2 交互式确认
        self._confirm_level2_if_needed()
        
        # 记录扫描参数
        self._log_scan_parameters()

        # 检查哪个参数被设置了，然后执行相应的操作
        if ArgumentParser.args.filename:
            start = datetime.now()
            self._print_scan_config("日志文件")

            if ArgumentParser.args.extract_gz:
                output_formatter.print_info("正在解压 .gz 文件...")

                new_filename = unzip.extract_and_delete_gz_files(ArgumentParser.args.filename)
                ArgumentParser.args.filename = new_filename

                output_formatter.print_success("解压完成")

            #regex_list（正则敏感信息）data_l30_list（C3敏感信息）data_l20_list（C2敏感信息）
            regex_list,data_l30_list,data_l20_list = infocheck.infoCheck_file(ArgumentParser.args.filename)

            #将文件检查结果写入txt
            self.c = resultprint.result_print_txt(regex_list,data_l30_list,data_l20_list)

            #将文件检查结果写入csv
            resultprint.result_print_csv(regex_list,data_l30_list,data_l20_list)

            # 输出扫描结果和日志
            end = datetime.now()
            self._log_scan_results('文件', ArgumentParser.args.filename, self.c, start, end)
            self._print_scan_results(self.c, end - start)

        elif ArgumentParser.args.zipname:

            start = datetime.now()
            self._print_scan_config("压缩包")

            #[regex_list（正则敏感信息）data_l30_list（C3敏感信息）data_l20_list（C2敏感信息）]
            regex_list,data_l30_list,data_l20_list,temp_dir = infocheck.infoCheck_zip(os.path.normpath(ArgumentParser.args.zipname))
            
            #将文件检查结果写入txt
            self.c = resultprint.result_print_txt(regex_list,data_l30_list,data_l20_list)

            #将文件检查结果写入csv
            resultprint.result_print_csv(regex_list,data_l30_list,data_l20_list)

            # 删除临时文件夹
            shutil.rmtree(temp_dir)
            
            # 输出扫描结果和日志
            end = datetime.now()
            self._log_scan_results('压缩包', ArgumentParser.args.zipname, self.c, start, end)
            self._print_scan_results(self.c, end - start)

        elif ArgumentParser.args.directory:

            start = datetime.now()
            self._print_scan_config("文件夹")

            if ArgumentParser.args.extract_gz:
                output_formatter.print_info("正在解压 .gz 文件...")

                unzip.extract_and_delete_gz_files(ArgumentParser.args.directory)

                output_formatter.print_success("解压完成")

            #[regex_list（正则敏感信息）data_l30_list（C3敏感信息）data_l20_list（C2敏感信息）]
            regex_list,data_l30_list,data_l20_list = infocheck.infoCheck_directory((ArgumentParser.args.directory))
            
            #将文件检查结果写入txt
            self.c = resultprint.result_print_txt(regex_list,data_l30_list,data_l20_list)

            #将文件检查结果写入csv
            resultprint.result_print_csv(regex_list,data_l30_list,data_l20_list)

            # 输出扫描结果和日志
            end = datetime.now()
            self._log_scan_results('目录', ArgumentParser.args.directory, self.c, start, end)
            self._print_scan_results(self.c, end - start)

        else:
            print('Neither f nor z was chosen.')
    
    def _print_logo(self):
        """打印启动 Logo"""
        # 检查是否禁用彩色输出
        color_enabled = not (hasattr(ArgumentParser.args, 'no_color') and ArgumentParser.args.no_color)
        
        # 使用 minimal 风格（简洁美观）
        banner.Banner.print_banner(style='simple', color_enabled=color_enabled)
    
    def _confirm_level2_if_needed(self):
        """Level 2 模式交互式确认"""
        if ArgumentParser.args.level == "2":
            output_formatter.print_warning("═" * 70)
            output_formatter.print_warning("⚠️  您已选择 Level 2 深度扫描模式")
            output_formatter.print_info("   • 正则规则数: 800+ 条 (Level 1 仅 13 条)")
            output_formatter.print_info("   • 预计耗时: 比 Level 1 慢 15-20 倍")
            output_formatter.print_info("   • 适用场景: 需要检测完整银行卡BIN码库时使用")
            output_formatter.print_warning("═" * 70)
            
            while True:
                try:
                    # 使用格式化输出显示提示
                    output_formatter.print_warning("是否继续使用 Level 2 深度扫描? (Y=继续 / N=切换到Level 1)")
                    # 接收用户输入（不带提示文本）
                    user_input = input("请输入选择: ").strip().lower()
                    if user_input == 'y':
                        output_formatter.print_success("确认使用 Level 2 深度扫描模式")
                        break
                    elif user_input == 'n':
                        ArgumentParser.args.level = "1"
                        output_formatter.print_success("已切换到 Level 1 标准扫描模式")
                        break
                    else:
                        output_formatter.print_error("无效输入，请输入 Y 或 N")
                except (KeyboardInterrupt, EOFError):
                    output_formatter.print_error("\n用户取消操作")
                    sys.exit(0)
    
    def _print_scan_config(self, scan_type):
        """打印扫描配置信息"""
        output_formatter.print_info(f"开始扫描{scan_type}...")
        
        level = ArgumentParser.args.level
        if level == "1":
            output_formatter.print_info("扫描级别: Level 1 (标准模式)")
            output_formatter.print_info("正则规则: 13 条 | 字段匹配: C3+C2")
        elif level == "2":
            output_formatter.print_warning("扫描级别: Level 2 (深度模式 - 完整银行卡库)")
            output_formatter.print_warning("正则规则: 800+ 条 (基础 13 条 + 扩展 800+ 条)")
            output_formatter.print_warning("⚠️  深度模式扫描时间较长，请耐心等待...")
    
    def _print_scan_results(self, count, elapsed_time):
        """打印扫描结果统计"""
        # 输出扫描结果
        if count > 0:
            output_formatter.print_warning(f"发现 {count:,} 条疑似敏感数据")
        else:
            output_formatter.print_success("未发现敏感数据")
        
        output_formatter.print_info(f"详细报告: {ArgumentParser.args.savename}.txt, info_check.csv")
        
        level = ArgumentParser.args.level
        level_name = "Level 1 (标准)" if level == "1" else "Level 2 (深度)"
        regex_count = "13" if level == "1" else "800+"
        
        output_formatter.print_info(f"扫描级别: {level_name} | 用时: {elapsed_time} | 规则数: {regex_count}")
        
        # Level 2 完成后的提示
        if level == "2":
            output_formatter.print_info("💡 提示: Level 1 标准模式扫描更快 (约 15-20 倍)，适合日常检查")
    
    def _log_scan_parameters(self):
        """记录扫描参数到日志"""
        self.logger.info("="*60)
        self.logger.info("开始新的扫描任务")
        self.logger.info(f"扫描级别: Level {ArgumentParser.args.level}")
        
        if ArgumentParser.args.filename:
            self.logger.info(f"扫描模式: 单文件扫描")
            self.logger.info(f"目标文件: {ArgumentParser.args.filename}")
        elif ArgumentParser.args.zipname:
            self.logger.info(f"扫描模式: 压缩包扫描")
            self.logger.info(f"目标压缩包: {ArgumentParser.args.zipname}")
        elif ArgumentParser.args.directory:
            self.logger.info(f"扫描模式: 目录扫描")
            self.logger.info(f"目标目录: {ArgumentParser.args.directory}")
        
        self.logger.info(f"输出路径: {ArgumentParser.args.savename}")
        self.logger.info(f"是否解压 .gz: {ArgumentParser.args.extract_gz}")
        self.logger.info(f"彩色输出: {not ArgumentParser.args.no_color}")
        self.logger.info(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("="*60)
    
    def _log_scan_results(self, scan_type, target_path, found_count, start_time, end_time):
        """记录扫描结果和性能指标到日志"""
        elapsed_time = end_time - start_time
        elapsed_seconds = elapsed_time.total_seconds()
        
        self.logger.info("-"*60)
        self.logger.info("扫描完成")
        self.logger.info(f"扫描类型: {scan_type}")
        self.logger.info(f"目标路径: {target_path}")
        self.logger.info(f"发现敏感数据: {found_count} 条")
        self.logger.info(f"扫描耗时: {elapsed_time}")
        self.logger.info(f"扫描速度: {elapsed_seconds:.2f} 秒")
        
        # 计算文件/目录大小
        try:
            if os.path.isfile(target_path):
                file_size = os.path.getsize(target_path)
                self.logger.info(f"文件大小: {file_size:,} 字节 ({file_size/1024/1024:.2f} MB)")
                if elapsed_seconds > 0:
                    speed_mb_s = (file_size / 1024 / 1024) / elapsed_seconds
                    self.logger.info(f"处理速度: {speed_mb_s:.2f} MB/s")
            elif os.path.isdir(target_path):
                # 计算目录下所有文件总大小
                total_size = 0
                file_count = 0
                for root, dirs, files in os.walk(target_path):
                    for f in files:
                        fp = os.path.join(root, f)
                        if os.path.isfile(fp):
                            total_size += os.path.getsize(fp)
                            file_count += 1
                self.logger.info(f"目录大小: {total_size:,} 字节 ({total_size/1024/1024:.2f} MB)")
                self.logger.info(f"文件数量: {file_count} 个")
                if elapsed_seconds > 0:
                    speed_mb_s = (total_size / 1024 / 1024) / elapsed_seconds
                    speed_files_s = file_count / elapsed_seconds
                    self.logger.info(f"处理速度: {speed_mb_s:.2f} MB/s, {speed_files_s:.2f} 文件/秒")
        except Exception as e:
            self.logger.warning(f"无法计算文件大小: {e}")
        
        self.logger.info(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("="*60)
            # 这里是没有任何参数被设置时的操作


if __name__ == "__main__":

    main = Program()
