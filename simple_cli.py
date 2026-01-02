#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单命令行工具 - 视频关键帧提取与宫格合成
适合新手使用，操作简单直观
"""

import os
import sys
from src.frame_extractor import FrameExtractor
from src.grid_synthesizer import GridSynthesizer


def print_welcome():
    """
    打印欢迎信息
    """
    print("=" * 60)
    print("📹 视频关键帧提取与宫格合成工具")
    print("=" * 60)
    print("欢迎使用！这个工具可以帮你从视频中提取关键帧，并合成为美观的宫格图。")
    print("\n操作流程：")
    print("1. 选择视频文件")
    print("2. 设置提取参数")
    print("3. 提取关键帧")
    print("4. 合成宫格图")
    print("=" * 60)


def get_video_path():
    """
    获取视频文件路径
    """
    # 先检查测试视频目录
    test_video_dir = os.path.join(os.getcwd(), "测试视频")
    if os.path.exists(test_video_dir):
        video_files = [f for f in os.listdir(test_video_dir) if f.endswith('.mp4')]
        if video_files:
            print(f"\n在 '测试视频' 目录中找到以下视频文件：")
            for i, file in enumerate(video_files):
                print(f"{i+1}. {file}")
            
            choice = input(f"\n请选择要处理的视频（1-{len(video_files)}），或输入完整路径：")
            try:
                index = int(choice) - 1
                if 0 <= index < len(video_files):
                    return os.path.join(test_video_dir, video_files[index])
            except ValueError:
                pass
    
    # 让用户输入视频路径
    video_path = input("\n请输入视频文件路径（MP4格式）：").strip()
    
    # 处理引号
    if (video_path.startswith('"') and video_path.endswith('"')) or \
       (video_path.startswith("'") and video_path.endswith("'")):
        video_path = video_path[1:-1]
    
    return video_path


def get_extraction_params():
    """
    获取提取参数
    """
    # 默认值设置
    default_num_frames = 5
    default_format = "jpg"
    default_quality = 95
    default_save_dir = os.path.join(os.getcwd(), "output")
    
    print(f"\n🔧 提取参数设置（按回车使用默认值）")
    print("-" * 30)
    
    # 提取数量
    try:
        num_frames = input(f"提取帧数（默认：{default_num_frames}，≥2）：").strip()
        num_frames = int(num_frames) if num_frames else default_num_frames
        if num_frames < 2:
            num_frames = 2
    except ValueError:
        num_frames = default_num_frames
    
    # 图片格式
    img_format = input(f"图片格式（默认：{default_format}，可选：jpg/png）：").strip().lower()
    if img_format not in ["jpg", "png"]:
        img_format = default_format
    
    # 图片质量（仅jpg有效）
    quality = default_quality
    if img_format == "jpg":
        try:
            quality_input = input(f"图片质量（默认：{default_quality}，0-100）：").strip()
            quality = int(quality_input) if quality_input else default_quality
            quality = max(0, min(100, quality))
        except ValueError:
            quality = default_quality
    
    # 保存目录
    save_dir = input(f"保存目录（默认：{default_save_dir}）：").strip()
    save_dir = save_dir if save_dir else default_save_dir
    
    return num_frames, img_format, quality, save_dir


def get_grid_params():
    """
    获取宫格合成参数
    """
    print(f"\n🎨 宫格合成设置（按回车使用默认值）")
    print("-" * 30)
    
    # 布局选择
    layout_options = ["自动计算", "2×2", "3×3", "4×4"]
    print("可用布局模板：")
    for i, option in enumerate(layout_options):
        print(f"{i+1}. {option}")
    
    layout = None
    try:
        choice = input(f"请选择布局（1-{len(layout_options)}）：").strip()
        if choice:
            index = int(choice) - 1
            if 0 <= index < len(layout_options):
                if index == 0:
                    layout = None
                else:
                    rows, cols = map(int, layout_options[index].split("×"))
                    layout = (rows, cols)
    except ValueError:
        pass
    
    # 间距
    spacing = 5
    try:
        spacing_input = input(f"图片间距（默认：{spacing} 像素）：").strip()
        spacing = int(spacing_input) if spacing_input else spacing
        spacing = max(0, min(20, spacing))
    except ValueError:
        pass
    
    return layout, spacing


def main():
    """
    主函数
    """
    print_welcome()
    
    # 1. 获取视频路径
    video_path = get_video_path()
    
    if not os.path.exists(video_path):
        print(f"❌ 错误：找不到文件 '{video_path}'")
        return 1
    
    if not video_path.lower().endswith('.mp4'):
        print(f"❌ 错误：只支持MP4格式视频")
        return 1
    
    # 2. 获取提取参数
    num_frames, img_format, quality, save_dir = get_extraction_params()
    
    # 3. 初始化提取器
    print(f"\n🔍 正在加载视频...")
    extractor = FrameExtractor(video_path)
    if not extractor.initialize():
        print(f"❌ 错误：无法加载视频 '{video_path}'")
        return 1
    
    # 显示视频信息
    print(f"\n📊 视频信息：")
    for key, value in extractor.video_info.items():
        print(f"  {key}: {value}")
    
    # 4. 提取关键帧
    print(f"\n🎬 正在提取 {num_frames} 张关键帧...")
    frames = extractor.extract_uniform_frames(num_frames=num_frames)
    if not frames:
        print(f"❌ 错误：提取关键帧失败")
        return 1
    
    print(f"✅ 成功提取 {len(frames)} 张关键帧")
    
    # 5. 保存关键帧
    print(f"\n💾 正在保存关键帧到 '{save_dir}'...")
    saved_paths = extractor.save_frames(frames, save_dir, output_format=img_format, quality=quality)
    if not saved_paths:
        print(f"❌ 错误：保存关键帧失败")
        return 1
    
    print(f"✅ 成功保存 {len(saved_paths)} 张图片")
    for path in saved_paths:
        print(f"  - {os.path.basename(path)}")
    
    # 6. 询问是否合成宫格图
    make_grid = input(f"\n🔗 是否要将这些关键帧合成为宫格图？（y/n）：").strip().lower()
    if make_grid not in ["y", "yes", "是", ""]:
        print(f"\n🎉 操作完成！")
        print(f"📁 关键帧已保存到：{save_dir}")
        return 0
    
    # 7. 获取宫格参数
    layout, spacing = get_grid_params()
    
    # 8. 合成宫格图
    print(f"\n🖼️  正在合成宫格图...")
    synthesizer = GridSynthesizer()
    
    # 生成输出路径
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    grid_output_path = os.path.join(save_dir, f"{video_name}_宫格图.{img_format}")
    
    result_path = synthesizer.synthesize_grid(
        saved_paths, 
        grid_output_path, 
        layout=layout,
        spacing=spacing,
        border=1,
        border_color=(200, 200, 200)
    )
    
    if result_path:
        print(f"✅ 成功合成宫格图！")
        print(f"📄 宫格图保存路径：{result_path}")
    else:
        print(f"❌ 错误：合成宫格图失败")
        return 1
    
    # 9. 完成提示
    print(f"\n🎉 所有操作完成！")
    print(f"📁 输出目录：{save_dir}")
    print(f"📖 你可以在该目录中查看提取的关键帧和合成的宫格图")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
