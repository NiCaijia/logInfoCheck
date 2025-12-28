#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Banner module for displaying application logo and information
"""

import sys


class Banner:
    """Application banner and logo"""
    
    VERSION = "0.7.0"
    
    # ASCII Art Logo
    LOGO = r"""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║     _                ___        __        ____ _               _      ║
║    | |    ___   __ _|_ _|_ __  / _| ___  / ___| |__   ___  ___| | __  ║
║    | |   / _ \ / _` || || '_ \| |_ / _ \| |   | '_ \ / _ \/ __| |/ /  ║
║    | |__| (_) | (_| || || | | |  _| (_) | |___| | | |  __/ (__|   <   ║
║    |_____\___/ \__, |___|_| |_|_|  \___/ \____|_| |_|\___|\___|_|\_\  ║
║                |___/                                                  ║
║                                                                       ║
║              日志敏感数据检查工具 - Log Info Check Tool               ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
"""

    LOGO_SIMPLE = r"""
┌─────────────────────────────────────────────────────────────────────┐
│  _                ___        __        ____ _               _       │
│ | |    ___   __ _|_ _|_ __  / _| ___  / ___| |__   ___  ___| | __   │
│ | |   / _ \ / _` || || '_ \| |_ / _ \| |   | '_ \ / _ \/ __| |/ /   │
│ | |__| (_) | (_| || || | | |  _| (_) | |___| | | |  __/ (__|   <    │
│ |_____\___/ \__, |___|_| |_|_|  \___/ \____|_| |_|\___|\___|_|\_\   │
│             |___/                                                   │
│             日志敏感数据检查工具 - Log Info Check Tool              │
└─────────────────────────────────────────────────────────────────────┘
"""

    LOGO_MINIMAL = """
╔═══════════════════════════════════════════════════════════════════════╗
║                  LogInfoCheck - 日志敏感数据检查工具                     ║
╚═══════════════════════════════════════════════════════════════════════╝
"""
    
    @staticmethod
    def print_banner(style='full', color_enabled=True):
        """
        Print application banner
        
        Args:
            style: 'full', 'simple', or 'minimal'
            color_enabled: Whether to use colored output
        """
        # Select logo style
        if style == 'full':
            logo = Banner.LOGO
        elif style == 'simple':
            logo = Banner.LOGO_SIMPLE
        else:
            logo = Banner.LOGO_MINIMAL
        
        # Print logo
        if color_enabled:
            # Print with color
            print(f"\033[96m{logo}\033[0m")  # Cyan color
        else:
            print(logo)
        
        # Print version and info
        info_lines = [
            f"版本 (Version): {Banner.VERSION}",
            "用途 (Purpose): 检测日志文件中的 C2/C3 敏感信息",
            "支持 (Support): 正则匹配 + 字段匹配",
            ""
        ]
        
        for line in info_lines:
            print(f"  {line}")
        
        print()  # Empty line for spacing


def main():
    """Test the banner"""
    print("\n=== Full Banner (Colored) ===")
    Banner.print_banner(style='full', color_enabled=True)
    
    print("\n=== Simple Banner (No Color) ===")
    Banner.print_banner(style='simple', color_enabled=False)
    
    print("\n=== Minimal Banner ===")
    Banner.print_banner(style='minimal', color_enabled=True)


if __name__ == "__main__":
    main()
