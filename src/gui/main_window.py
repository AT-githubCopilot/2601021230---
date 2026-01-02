#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主窗口界面
"""

import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QFileDialog, QSpinBox, 
                            QComboBox, QGroupBox, QGridLayout, QProgressBar, 
                            QTextEdit, QFrame, QSplitter, QScrollArea, 
                            QMessageBox)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import numpy as np
from src.frame_extractor import FrameExtractor
from src.grid_synthesizer import GridSynthesizer


class ExtractionThread(QThread):
    """
    关键帧提取线程
    """
    progress_updated = pyqtSignal(int)
    extraction_done = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, video_path, num_frames, output_format, quality, output_dir):
        super().__init__()
        self.video_path = video_path
        self.num_frames = num_frames
        self.output_format = output_format
        self.quality = quality
        self.output_dir = output_dir
    
    def run(self):
        """
        执行关键帧提取
        """
        try:
            extractor = FrameExtractor(self.video_path)
            if not extractor.initialize():
                self.error_occurred.emit("无法加载视频文件")
                return
            
            # 提取关键帧
            frames = extractor.extract_uniform_frames(
                num_frames=self.num_frames,
                output_format=self.output_format,
                quality=self.quality
            )
            
            # 保存帧
            saved_paths = extractor.save_frames(
                frames, 
                self.output_dir, 
                output_format=self.output_format,
                quality=self.quality
            )
            
            extractor.release()
            self.extraction_done.emit(saved_paths)
        except Exception as e:
            self.error_occurred.emit(str(e))


class GridSynthesisThread(QThread):
    """
    宫格合成线程
    """
    synthesis_done = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, image_paths, output_path, layout, spacing, border, border_color, output_size, fit_mode):
        super().__init__()
        self.image_paths = image_paths
        self.output_path = output_path
        self.layout = layout
        self.spacing = spacing
        self.border = border
        self.border_color = border_color
        self.output_size = output_size
        self.fit_mode = fit_mode
    
    def run(self):
        """
        执行宫格合成
        """
        try:
            synthesizer = GridSynthesizer()
            result_path = synthesizer.synthesize_grid(
                self.image_paths,
                self.output_path,
                layout=self.layout,
                spacing=self.spacing,
                border=self.border,
                border_color=self.border_color,
                output_size=self.output_size,
                fit_mode=self.fit_mode
            )
            self.synthesis_done.emit(result_path)
        except Exception as e:
            self.error_occurred.emit(str(e))


class MainWindow(QMainWindow):
    """
    主窗口类
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.extracted_frame_paths = []
    
    def init_ui(self):
        """
        初始化用户界面
        """
        # 设置窗口标题和大小
        self.setWindowTitle("视频关键帧提取与宫格合成工具")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建顶部控件区
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        
        # 视频导入按钮
        self.btn_import = QPushButton("导入视频")
        self.btn_import.clicked.connect(self.import_video)
        top_layout.addWidget(self.btn_import)
        
        # 视频信息显示
        self.lbl_video_info = QLabel("未导入视频")
        self.lbl_video_info.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.lbl_video_info.setMinimumHeight(40)
        self.lbl_video_info.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.lbl_video_info, 1)
        
        main_layout.addWidget(top_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧控制面板
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # 关键帧提取设置
        extraction_group = QGroupBox("关键帧提取设置")
        extraction_layout = QGridLayout(extraction_group)
        
        # 提取数量
        extraction_layout.addWidget(QLabel("提取数量："), 0, 0)
        self.spin_num_frames = QSpinBox()
        self.spin_num_frames.setRange(2, 100)
        self.spin_num_frames.setValue(5)
        extraction_layout.addWidget(self.spin_num_frames, 0, 1)
        
        # 图片格式
        extraction_layout.addWidget(QLabel("图片格式："), 0, 2)
        self.combo_format = QComboBox()
        self.combo_format.addItems(["jpg", "png"])
        extraction_layout.addWidget(self.combo_format, 0, 3)
        
        # 图片质量
        extraction_layout.addWidget(QLabel("图片质量："), 1, 0)
        self.spin_quality = QSpinBox()
        self.spin_quality.setRange(1, 100)
        self.spin_quality.setValue(95)
        extraction_layout.addWidget(self.spin_quality, 1, 1)
        
        # 保存路径
        extraction_layout.addWidget(QLabel("保存路径："), 1, 2)
        path_layout = QHBoxLayout()
        self.lbl_save_path = QLabel("选择保存路径")
        path_layout.addWidget(self.lbl_save_path, 1)
        self.btn_browse = QPushButton("浏览")
        self.btn_browse.clicked.connect(self.browse_save_path)
        path_layout.addWidget(self.btn_browse)
        extraction_layout.addLayout(path_layout, 1, 3)
        
        # 提取按钮
        self.btn_extract = QPushButton("提取关键帧")
        self.btn_extract.clicked.connect(self.extract_frames)
        self.btn_extract.setEnabled(False)
        extraction_layout.addWidget(self.btn_extract, 2, 0, 1, 4)
        
        left_layout.addWidget(extraction_group)
        
        # 宫格合成设置
        grid_group = QGroupBox("宫格合成设置")
        grid_layout = QGridLayout(grid_group)
        
        # 布局选择
        grid_layout.addWidget(QLabel("宫格布局："), 0, 0)
        self.combo_layout = QComboBox()
        self.combo_layout.addItems(["自动计算", "2×2", "3×3", "4×4"])
        grid_layout.addWidget(self.combo_layout, 0, 1)
        
        # 图片间距
        grid_layout.addWidget(QLabel("图片间距："), 0, 2)
        self.spin_spacing = QSpinBox()
        self.spin_spacing.setRange(0, 20)
        self.spin_spacing.setValue(5)
        grid_layout.addWidget(self.spin_spacing, 0, 3)
        
        # 边框宽度
        grid_layout.addWidget(QLabel("边框宽度："), 1, 0)
        self.spin_border = QSpinBox()
        self.spin_border.setRange(0, 10)
        self.spin_border.setValue(1)
        grid_layout.addWidget(self.spin_border, 1, 1)
        
        # 合成按钮
        self.btn_synthesize = QPushButton("合成宫格图")
        self.btn_synthesize.clicked.connect(self.synthesize_grid)
        self.btn_synthesize.setEnabled(False)
        grid_layout.addWidget(self.btn_synthesize, 2, 0, 1, 4)
        
        left_layout.addWidget(grid_group)
        
        # 进度条
        self.progress_bar = QProgressBar()
        left_layout.addWidget(self.progress_bar)
        
        # 日志输出
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMinimumHeight(100)
        left_layout.addWidget(QLabel("操作日志："))
        left_layout.addWidget(self.log_output)
        
        splitter.addWidget(left_panel)
        
        # 右侧预览区
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # 预览标题
        self.lbl_preview_title = QLabel("预览区")
        right_layout.addWidget(self.lbl_preview_title)
        
        # 预览图片容器
        self.preview_container = QWidget()
        self.preview_layout = QGridLayout(self.preview_container)
        
        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.preview_container)
        scroll_area.setWidgetResizable(True)
        right_layout.addWidget(scroll_area, 1)
        
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(1, 3)  # 右侧预览区占3份
        
        main_layout.addWidget(splitter, 1)
        
        # 初始化保存路径
        self.save_path = os.path.join(os.path.expanduser("~"), "视频关键帧")
        self.lbl_save_path.setText(self.save_path)
    
    def import_video(self):
        """
        导入视频文件
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择MP4视频文件", "", "MP4视频 (*.mp4)"
        )
        
        if file_path:
            self.video_path = file_path
            self.update_video_info()
            self.btn_extract.setEnabled(True)
            self.log_output.append(f"已导入视频：{os.path.basename(file_path)}")
    
    def update_video_info(self):
        """
        更新视频信息显示
        """
        try:
            extractor = FrameExtractor(self.video_path)
            if extractor.initialize():
                info = extractor.video_info
                info_text = f"{info['filename']} | 分辨率：{info['resolution']} | 时长：{info['duration']:.2f}秒 | 帧率：{info['fps']:.2f}fps"
                self.lbl_video_info.setText(info_text)
                extractor.release()
        except Exception as e:
            self.lbl_video_info.setText(f"无法获取视频信息：{str(e)}")
    
    def browse_save_path(self):
        """
        浏览保存路径
        """
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择保存目录", self.save_path
        )
        if dir_path:
            self.save_path = dir_path
            self.lbl_save_path.setText(self.save_path)
    
    def extract_frames(self):
        """
        提取关键帧
        """
        if not hasattr(self, 'video_path'):
            QMessageBox.warning(self, "警告", "请先导入视频文件")
            return
        
        num_frames = self.spin_num_frames.value()
        output_format = self.combo_format.currentText()
        quality = self.spin_quality.value()
        
        # 创建提取线程
        self.extraction_thread = ExtractionThread(
            self.video_path,
            num_frames,
            output_format,
            quality,
            self.save_path
        )
        
        # 连接信号槽
        self.extraction_thread.extraction_done.connect(self.on_extraction_done)
        self.extraction_thread.error_occurred.connect(self.on_error)
        
        # 禁用按钮
        self.btn_extract.setEnabled(False)
        self.btn_synthesize.setEnabled(False)
        
        # 开始提取
        self.log_output.append("开始提取关键帧...")
        self.extraction_thread.start()
    
    def on_extraction_done(self, saved_paths):
        """
        关键帧提取完成回调
        """
        self.extracted_frame_paths = saved_paths
        self.log_output.append(f"关键帧提取完成，共提取 {len(saved_paths)} 张图片")
        
        # 显示预览
        self.show_frame_preview(saved_paths)
        
        # 启用合成按钮
        self.btn_synthesize.setEnabled(True)
        self.btn_extract.setEnabled(True)
    
    def on_error(self, error_msg):
        """
        错误处理
        """
        self.log_output.append(f"错误：{error_msg}")
        QMessageBox.critical(self, "错误", error_msg)
        self.btn_extract.setEnabled(True)
        if self.extracted_frame_paths:
            self.btn_synthesize.setEnabled(True)
    
    def show_frame_preview(self, frame_paths):
        """
        显示关键帧预览
        """
        # 清空现有预览
        for i in reversed(range(self.preview_layout.count())):
            self.preview_layout.itemAt(i).widget().deleteLater()
        
        # 计算布局
        num_frames = len(frame_paths)
        cols = min(num_frames, 3)
        rows = (num_frames + cols - 1) // cols
        
        # 显示预览图片
        for i, path in enumerate(frame_paths):
            row = i // cols
            col = i % cols
            
            # 创建预览项
            preview_item = QWidget()
            preview_item_layout = QVBoxLayout(preview_item)
            
            # 图片标签
            img_label = QLabel()
            img_label.setFixedSize(200, 150)
            img_label.setScaledContents(True)
            
            # 加载图片
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                img_label.setPixmap(pixmap)
            
            preview_item_layout.addWidget(img_label)
            
            # 图片名称
            name_label = QLabel(os.path.basename(path))
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setWordWrap(True)
            preview_item_layout.addWidget(name_label)
            
            self.preview_layout.addWidget(preview_item, row, col)
    
    def synthesize_grid(self):
        """
        合成宫格图
        """
        if not self.extracted_frame_paths:
            QMessageBox.warning(self, "警告", "请先提取关键帧")
            return
        
        # 解析布局
        layout_str = self.combo_layout.currentText()
        if layout_str == "自动计算":
            layout = None
        else:
            rows, cols = map(int, layout_str.split("×"))
            layout = (rows, cols)
        
        # 获取其他参数
        spacing = self.spin_spacing.value()
        border = self.spin_border.value()
        
        # 生成输出路径
        output_dir = self.save_path
        base_name = os.path.splitext(os.path.basename(self.video_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}_宫格图.jpg")
        
        # 创建合成线程
        self.synthesis_thread = GridSynthesisThread(
            self.extracted_frame_paths,
            output_path,
            layout,
            spacing,
            border,
            (200, 200, 200),  # 边框颜色
            None,  # 输出尺寸
            "center_crop"  # 适配模式
        )
        
        # 连接信号槽
        self.synthesis_thread.synthesis_done.connect(self.on_synthesis_done)
        self.synthesis_thread.error_occurred.connect(self.on_error)
        
        # 禁用按钮
        self.btn_synthesize.setEnabled(False)
        self.btn_extract.setEnabled(False)
        
        # 开始合成
        self.log_output.append("开始合成宫格图...")
        self.synthesis_thread.start()
    
    def on_synthesis_done(self, grid_path):
        """
        宫格合成完成回调
        """
        self.log_output.append(f"宫格图合成完成：{grid_path}")
        QMessageBox.information(self, "完成", f"宫格图已保存至：\n{grid_path}")
        
        # 显示宫格图预览
        self.show_grid_preview(grid_path)
        
        # 启用按钮
        self.btn_synthesize.setEnabled(True)
        self.btn_extract.setEnabled(True)
    
    def show_grid_preview(self, grid_path):
        """
        显示宫格图预览
        """
        # 清空现有预览
        for i in reversed(range(self.preview_layout.count())):
            self.preview_layout.itemAt(i).widget().deleteLater()
        
        # 创建预览项
        preview_item = QWidget()
        preview_item_layout = QVBoxLayout(preview_item)
        
        # 图片标签
        img_label = QLabel()
        img_label.setAlignment(Qt.AlignCenter)
        
        # 加载图片
        pixmap = QPixmap(grid_path)
        if not pixmap.isNull():
            # 缩放图片以适应预览区
            img_label.setPixmap(pixmap.scaled(
                800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        
        preview_item_layout.addWidget(img_label)
        
        # 图片名称
        name_label = QLabel(os.path.basename(grid_path))
        name_label.setAlignment(Qt.AlignCenter)
        preview_item_layout.addWidget(name_label)
        
        self.preview_layout.addWidget(preview_item, 0, 0)
    
    def log(self, message):
        """
        记录日志
        """
        self.log_output.append(message)
        self.log_output.ensureCursorVisible()
