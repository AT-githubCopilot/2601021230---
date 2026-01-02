#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
宫格合成模块
负责将提取的关键帧合成为宫格图
"""

import os
from PIL import Image, ImageDraw, ImageFont
import math


class GridSynthesizer:
    """宫格合成器类"""
    
    def __init__(self):
        """初始化"""
        pass
    
    def calculate_grid_layout(self, num_images):
        """
        计算最优宫格布局
        
        Args:
            num_images (int): 图片数量
            
        Returns:
            tuple: (行数, 列数)
        """
        if num_images <= 0:
            return (0, 0)
        
        # 计算最接近的矩形
        cols = math.ceil(math.sqrt(num_images))
        rows = math.ceil(num_images / cols)
        
        # 优化为更接近正方形的布局
        while cols > 1 and (rows * (cols - 1) >= num_images):
            cols -= 1
            rows = math.ceil(num_images / cols)
        
        return (rows, cols)
    
    def synthesize_grid(self, image_paths, output_path, layout=None, spacing=5, border=1, border_color=(200, 200, 200), 
                       output_size=None, fit_mode='center_crop'):
        """
        合成宫格图
        
        Args:
            image_paths (list): 图片路径列表
            output_path (str): 输出路径
            layout (tuple): 自定义布局 (rows, cols)，None则自动计算
            spacing (int): 图片间距（像素）
            border (int): 边框宽度（像素）
            border_color (tuple): 边框颜色 (R, G, B)
            output_size (tuple): 输出尺寸 (width, height)，None则根据原始图片计算
            fit_mode (str): 图片适配模式，'center_crop'或'keep_aspect'
            
        Returns:
            str: 合成的宫格图路径
        """
        if not image_paths:
            return None
        
        num_images = len(image_paths)
        
        # 计算布局
        if layout is None:
            rows, cols = self.calculate_grid_layout(num_images)
        else:
            rows, cols = layout
        
        # 加载第一张图片获取基础尺寸
        with Image.open(image_paths[0]) as first_img:
            img_width, img_height = first_img.size
        
        # 计算每个格子的尺寸
        if output_size is None:
            # 如果没有指定输出尺寸，使用原始图片尺寸
            cell_width = img_width
            cell_height = img_height
            output_width = cols * cell_width + (cols - 1) * spacing + 2 * border
            output_height = rows * cell_height + (rows - 1) * spacing + 2 * border
        else:
            # 根据指定输出尺寸计算每个格子的尺寸
            output_width, output_height = output_size
            # 减去边框和间距
            available_width = output_width - 2 * border - (cols - 1) * spacing
            available_height = output_height - 2 * border - (rows - 1) * spacing
            cell_width = available_width // cols
            cell_height = available_height // rows
        
        # 创建空白画布
        grid_image = Image.new('RGB', (output_width, output_height), (255, 255, 255))
        draw = ImageDraw.Draw(grid_image)
        
        # 遍历所有图片位置
        for i in range(rows):
            for j in range(cols):
                index = i * cols + j
                if index >= num_images:
                    break
                
                # 计算当前图片在画布上的位置
                x = border + j * (cell_width + spacing)
                y = border + i * (cell_height + spacing)
                
                # 加载并处理图片
                with Image.open(image_paths[index]) as img:
                    # 调整图片尺寸以适应格子
                    if fit_mode == 'center_crop':
                        # 中心裁剪
                        img = self.center_crop(img, cell_width, cell_height)
                    else:
                        # 保持纵横比，可能有黑边
                        img = self.keep_aspect_ratio(img, cell_width, cell_height)
                    
                    # 绘制边框
                    if border > 0:
                        draw.rectangle([x - border, y - border, x + cell_width + border, y + cell_height + border], 
                                     fill=border_color)
                    
                    # 粘贴图片到画布
                    grid_image.paste(img, (x, y))
        
        # 保存合成图片
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        grid_image.save(output_path)
        
        return output_path
    
    def center_crop(self, img, target_width, target_height):
        """
        中心裁剪图片
        
        Args:
            img (Image): PIL Image对象
            target_width (int): 目标宽度
            target_height (int): 目标高度
            
        Returns:
            Image: 裁剪后的Image对象
        """
        img_width, img_height = img.size
        
        # 计算缩放比例
        scale = max(target_width / img_width, target_height / img_height)
        
        # 缩放图片
        scaled_width = int(img_width * scale)
        scaled_height = int(img_height * scale)
        img = img.resize((scaled_width, scaled_height), Image.LANCZOS)
        
        # 计算裁剪区域
        left = (scaled_width - target_width) // 2
        top = (scaled_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        
        # 裁剪
        return img.crop((left, top, right, bottom))
    
    def keep_aspect_ratio(self, img, target_width, target_height):
        """
        保持纵横比缩放图片
        
        Args:
            img (Image): PIL Image对象
            target_width (int): 目标宽度
            target_height (int): 目标高度
            
        Returns:
            Image: 缩放后的Image对象
        """
        img_width, img_height = img.size
        
        # 计算缩放比例
        scale = min(target_width / img_width, target_height / img_height)
        
        # 缩放图片
        scaled_width = int(img_width * scale)
        scaled_height = int(img_height * scale)
        img = img.resize((scaled_width, scaled_height), Image.LANCZOS)
        
        # 创建空白图片并居中粘贴
        result = Image.new('RGB', (target_width, target_height), (0, 0, 0))
        left = (target_width - scaled_width) // 2
        top = (target_height - scaled_height) // 2
        result.paste(img, (left, top))
        
        return result
    
    def add_title(self, image_path, title, output_path, font_path=None, font_size=24, font_color=(0, 0, 0), 
                 alignment='center', margin=20):
        """
        为宫格图添加标题
        
        Args:
            image_path (str): 原始图片路径
            title (str): 标题文本
            output_path (str): 输出路径
            font_path (str): 字体路径，None则使用默认字体
            font_size (int): 字体大小
            font_color (tuple): 字体颜色 (R, G, B)
            alignment (str): 对齐方式，'left', 'center', 'right'
            margin (int): 标题与图片的间距
            
        Returns:
            str: 添加标题后的图片路径
        """
        with Image.open(image_path) as img:
            # 创建新画布，预留标题空间
            img_width, img_height = img.size
            new_height = img_height + font_size + margin
            result = Image.new('RGB', (img_width, new_height), (255, 255, 255))
            
            # 粘贴原始图片到下方
            result.paste(img, (0, font_size + margin))
            
            # 绘制标题
            draw = ImageDraw.Draw(result)
            
            # 加载字体
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                font = ImageFont.load_default()
            
            # 计算标题位置
            text_bbox = draw.textbbox((0, 0), title, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            if alignment == 'left':
                text_x = margin
            elif alignment == 'center':
                text_x = (img_width - text_width) // 2
            else:  # right
                text_x = img_width - text_width - margin
            
            text_y = (font_size - text_height) // 2
            
            # 绘制文字
            draw.text((text_x, text_y), title, font=font, fill=font_color)
            
            # 保存结果
            result.save(output_path)
            
        return output_path
