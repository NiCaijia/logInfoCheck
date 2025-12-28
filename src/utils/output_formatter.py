#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输出格式化模块 - SQLMap 风格的终端输出
提供彩色输出、符号前缀、进度显示等功能
"""

import sys
import os
from datetime import datetime


class Colors:
    """ANSI 颜色代码定义"""
    # 基础颜色
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # 前景色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # 高亮前景色
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


class OutputFormatter:
    """输出格式化类"""
    
    def __init__(self, enable_color=True):
        """
        初始化输出格式化器
        
        Args:
            enable_color: 是否启用彩色输出，默认为 True
        """
        # 检测是否应该启用颜色
        self.enable_color = enable_color and self._supports_color()
    
    def _supports_color(self):
        """
        检测终端是否支持颜色输出
        
        Returns:
            bool: 如果支持颜色返回 True，否则返回 False
        """
        # 如果输出被重定向到文件或管道，禁用颜色
        if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
            return False
        
        # Windows 系统特殊处理
        if sys.platform == 'win32':
            # Windows 10 及以上版本支持 ANSI 颜色
            try:
                import platform
                version = platform.version()
                major_version = int(version.split('.')[0])
                if major_version >= 10:
                    # 启用 Windows 控制台的 ANSI 支持
                    import ctypes
                    kernel32 = ctypes.windll.kernel32
                    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                    return True
            except:
                pass
            return False
        
        # Unix-like 系统通常都支持
        return True
    
    def colored(self, text, color_code):
        """
        为文本添加颜色
        
        Args:
            text: 要着色的文本
            color_code: 颜色代码
            
        Returns:
            str: 着色后的文本
        """
        if not self.enable_color:
            return text
        return f"{color_code}{text}{Colors.RESET}"
    
    def print_info(self, message):
        """
        打印信息消息（蓝色 [*] 前缀）
        
        Args:
            message: 消息内容
        """
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        prefix = self.colored("[*]", Colors.BRIGHT_BLUE)
        print(f"{timestamp} {prefix} {message}", flush=True)
    
    def print_success(self, message):
        """
        打印成功消息（绿色 [+] 前缀）
        
        Args:
            message: 消息内容
        """
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        prefix = self.colored("[+]", Colors.BRIGHT_GREEN)
        print(f"{timestamp} {prefix} {message}", flush=True)
    
    def print_warning(self, message):
        """
        打印警告消息（黄色 [!] 前缀）
        
        Args:
            message: 消息内容
        """
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        prefix = self.colored("[!]", Colors.BRIGHT_YELLOW)
        print(f"{timestamp} {prefix} {message}", flush=True)
    
    def print_error(self, message):
        """
        打印错误消息（红色 [-] 前缀）
        
        Args:
            message: 消息内容
        """
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        prefix = self.colored("[-]", Colors.BRIGHT_RED)
        print(f"{timestamp} {prefix} {message}", flush=True)
    
    def print_critical(self, message):
        """
        打印严重错误消息（红色高亮 [!!] 前缀）
        
        Args:
            message: 消息内容
        """
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        prefix = self.colored("[!!]", Colors.BOLD + Colors.BRIGHT_RED)
        print(f"{timestamp} {prefix} {message}", flush=True)
    
    def print_progress(self, current, total, message, clear_line=True):
        """
        打印进度信息（带计数的蓝色 [*] 前缀）
        
        Args:
            current: 当前进度
            total: 总数
            message: 消息内容
            clear_line: 是否清除当前行（用于动态刷新）
        """
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        prefix = self.colored("[*]", Colors.BRIGHT_BLUE)
        counter = self.colored(f"[{current}/{total}]", Colors.CYAN)
        
        # 构建完整消息
        full_message = f"{timestamp} {prefix} {counter} {message}"
        
        if clear_line:
            # 使用 \r 回车符实现同行刷新
            # 添加额外空格以覆盖之前可能更长的内容
            sys.stdout.write(f"\r{full_message}" + " " * 20)
            sys.stdout.flush()
        else:
            print(full_message, flush=True)
    
    def clear_line(self):
        """清除当前行"""
        sys.stdout.write('\r' + ' ' * 120 + '\r')
        sys.stdout.flush()
    
    def print_divider(self, char='-', length=60):
        """
        打印分割线
        
        Args:
            char: 分割线字符
            length: 分割线长度
        """
        print(self.colored(char * length, Colors.CYAN), flush=True)


# 创建全局默认实例
_default_formatter = OutputFormatter(enable_color=True)


# 便捷函数，直接使用默认实例
def set_color_enabled(enabled):
    """设置是否启用颜色"""
    global _default_formatter
    _default_formatter = OutputFormatter(enable_color=enabled)


def colored(text, color_code):
    """为文本添加颜色"""
    return _default_formatter.colored(text, color_code)


def print_info(message):
    """打印信息消息"""
    _default_formatter.print_info(message)


def print_success(message):
    """打印成功消息"""
    _default_formatter.print_success(message)


def print_warning(message):
    """打印警告消息"""
    _default_formatter.print_warning(message)


def print_error(message):
    """打印错误消息"""
    _default_formatter.print_error(message)


def print_critical(message):
    """打印严重错误消息"""
    _default_formatter.print_critical(message)


def print_progress(current, total, message, clear_line=True):
    """打印进度信息"""
    _default_formatter.print_progress(current, total, message, clear_line)


def clear_line():
    """清除当前行"""
    _default_formatter.clear_line()


def print_divider(char='-', length=60):
    """打印分割线"""
    _default_formatter.print_divider(char, length)
