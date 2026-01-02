#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
关键帧提取模块
负责从视频中提取关键帧
"""

import os
import cv2
from PIL import Image
import numpy as np
from src.video_processor import VideoProcessor


class FrameExtractor:
    """关键帧提取器类"""
    
    def __init__(self, video_path):
        """
        初始化
        
        Args:
            video_path (str): 视频文件路径
        """
        self.video_path = video_path
        self.video_processor = VideoProcessor()
        self.video_info = {}
    
    def initialize(self):
        """
        初始化视频处理器
        
        Returns:
            bool: 是否初始化成功
        """
        if not self.video_processor.load_video(self.video_path):
            return False
        
        self.video_info = self.video_processor.get_video_info()
        return len(self.video_info) > 0
    
    def extract_uniform_frames(self, num_frames=5, output_format='jpg', quality=95):
        """
        均匀间隔模式提取关键帧
        
        Args:
            num_frames (int): 提取的帧数，默认为5
            output_format (str): 输出图片格式，jpg或png
            quality (int): 图片质量，0-100，仅对jpg有效
            
        Returns:
            list: 提取的帧图像路径列表
        """
        if not self.video_processor.cap or not self.video_processor.cap.isOpened():
            return []
        
        if num_frames < 2:
            num_frames = 2
        
        # 计算间隔帧数
        total_frames = self.video_info['total_frames']
        interval = total_frames // (num_frames - 1)
        
        extracted_frames = []
        
        for i in range(num_frames):
            # 计算当前帧位置
            frame_pos = i * interval
            if frame_pos >= total_frames:
                frame_pos = total_frames - 1
            
            # 设置帧位置
            self.video_processor.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            
            # 读取帧
            ret, frame = self.video_processor.cap.read()
            if ret:
                # 将BGR转换为RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                extracted_frames.append(frame_rgb)
        
        return extracted_frames
    
    def save_frames(self, frames, output_dir, output_format='jpg', quality=95):
        """
        保存提取的帧图像
        
        Args:
            frames (list): 帧图像列表
            output_dir (str): 输出目录
            output_format (str): 输出图片格式，jpg或png
            quality (int): 图片质量，0-100，仅对jpg有效
            
        Returns:
            list: 保存的图片路径列表
        """
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        saved_paths = []
        
        # 获取视频文件名（不含扩展名）
        video_name = os.path.splitext(os.path.basename(self.video_path))[0]
        
        for i, frame in enumerate(frames):
            # 生成文件名
            filename = f"{video_name}_{i+1:03d}.{output_format}"
            output_path = os.path.join(output_dir, filename)
            
            # 保存图片
            img = Image.fromarray(frame)
            if output_format.lower() == 'jpg':
                img.save(output_path, 'JPEG', quality=quality)
            else:
                img.save(output_path, 'PNG')
            
            saved_paths.append(output_path)
        
        return saved_paths
    
    def release(self):
        """释放资源"""
        self.video_processor.release()
    
    def __del__(self):
        """析构函数"""
        self.release()
