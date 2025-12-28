import sys
import os

sys.path.append(os.path.dirname(__file__))

from datetime import datetime
import logging

def init_logger(name, log_level='DEBUG', log_type='general'):
    """
    初始化日志记录器
    
    Args:
        name: logger 名称
        log_level: 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
        log_type: 日志类型，用于文件名前缀
    
    Returns:
        logger: 配置好的 logger 实例
    """
    # 获取 logger 实例
    logger = logging.getLogger(name)
    
    # ✅ 避免重复添加 handler（如果已经配置过，直接返回）
    if logger.handlers:
        return logger
    
    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')

    # 创建日志文件夹
    log_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs', current_date))
    os.makedirs(log_dir, exist_ok=True)

    # ✅ 使用日期+PID命名，避免文件过多
    log_name = f"{log_type}_{datetime.now().strftime('%Y%m%d')}_{os.getpid()}.log"

    # 拼接日志文件路径
    log_file = os.path.join(log_dir, log_name)

    # 设置日志输出格式
    log_format = "%(asctime)s %(levelname)s %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, date_format)

    # 创建日志记录器
    logger.setLevel(log_level)

    # 创建文件处理器
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # 将文件处理器添加到日志记录器
    logger.addHandler(file_handler)

    # ✅ 不再添加控制台处理器（用户已有 output_formatter 用于终端输出）
    # 日志仅写入文件，终端输出由 output_formatter 统一管理

    return logger

#  调用日志打印函数
#logger = init_logger()
#logger.error("This is an error message.")
#logger.warning("This is a warning message.")
#logger.info("This is an info message.")
#logger.debug("This is a debug message.")