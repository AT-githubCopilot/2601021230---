#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
视频处理核心模块
负责视频导入和信息解析
"""

import os
import cv2
import ffmpeg


class VideoProcessor:
    """视频处理器类"""
    
    def __init__(self):
        """初始化"""
        self.video_path = None
        self.cap = None
        self.video_info = {}
    
    def load_video(self, video_path):
        """
        加载视频文件
        
        Args:
            video_path (str): 视频文件路径
            
        Returns:
            bool: 是否加载成功
        """
        if not os.path.exists(video_path):
            return False
        
        # 验证文件是否为MP4格式
        if not video_path.lower().endswith('.mp4'):
            return False
        
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        
        if not self.cap.isOpened():
            return False
        
        return True
    
    def get_video_info(self):
        """
        获取视频信息
        
        Returns:
            dict: 视频信息字典
        """
        if not self.cap or not self.cap.isOpened():
            return {}
        
        # 使用OpenCV获取基本信息
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # 计算时长（秒）
        duration = total_frames / fps if fps > 0 else 0
        
        # 使用ffmpeg获取更详细的信息
        try:
            probe = ffmpeg.probe(self.video_path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            if video_stream:
                # 从ffmpeg获取文件大小
                file_size = os.path.getsize(self.video_path)
                
                self.video_info = {
                    'filename': os.path.basename(self.video_path),
                    'file_path': self.video_path,
                    'file_size': file_size,
                    'duration': duration,
                    'fps': fps,
                    'width': width,
                    'height': height,
                    'total_frames': total_frames,
                    'resolution': f"{width}×{height}",
                    'codec': video_stream.get('codec_name', 'unknown')
                }
        except Exception as e:
            # 如果ffmpeg获取失败，使用OpenCV的基本信息
            self.video_info = {
                'filename': os.path.basename(self.video_path),
                'file_path': self.video_path,
                'file_size': os.path.getsize(self.video_path),
                'duration': duration,
                'fps': fps,
                'width': width,
                'height': height,
                'total_frames': total_frames,
                'resolution': f"{width}×{height}",
                'codec': 'unknown'
            }
        
        return self.video_info
    
    def get_frame_at_time(self, time_seconds):
        """
        获取指定时间点的帧
        
        Args:
            time_seconds (float): 时间点（秒）
            
        Returns:
            numpy.ndarray: 帧图像
        """
        if not self.cap or not self.cap.isOpened():
            return None
        
        # 设置帧位置
        fps = self.video_info.get('fps', 0)
        if fps == 0:
            return None
        
        frame_pos = int(time_seconds * fps)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
        
        ret, frame = self.cap.read()
        if ret:
            return frame
        return None
    
    def release(self):
        """释放资源"""
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None
    
    def __del__(self):
        """析构函数"""
        self.release()
