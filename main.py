#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
视频关键帧提取与宫格合成工具
入口文件
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("视频关键帧提取与宫格合成工具")
    
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
