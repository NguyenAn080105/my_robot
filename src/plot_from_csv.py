#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import argparse
import sys
import os

def main():
    # --- CẤU HÌNH ĐẦU VÀO ---
    parser = argparse.ArgumentParser(description="Vẽ lại biểu đồ ROS từ file CSV")
    parser.add_argument('csv_file', type=str, help="Đường dẫn đến file CSV (ví dụ: nav03.csv)")
    args = parser.parse_args()

    if not os.path.exists(args.csv_file):
        print(f"Lỗi: Không tìm thấy file '{args.csv_file}'")
        sys.exit(1)

    print(f"Đang đọc dữ liệu từ: {args.csv_file} ...")
    
    # Đọc file CSV
    df = pd.read_csv(args.csv_file)

    # --- CẤU HÌNH CÁC MỐC THỜI GIAN CẦN VẼ ---
    # Bạn có thể thêm sửa các mốc thời gian khác tại đây
    manual_markers = [
        (0, "Start"),
        (37.28, "Start Moving")
    ]

    # --- TỰ ĐỘNG PHÁT HIỆN TÊN NODE ---
    node_list = []
    for col in df.columns:
        if col.endswith('_CPU') and col != 'Total_CPU' and col != 'Time':
            node_name = col.replace('_CPU', '')
            node_list.append(node_name)
    
    print(f"Phát hiện các node: {node_list}")

    # --- VẼ BIỂU ĐỒ ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # Cấu hình trục
    tick_spacing = 10
    
    ax1.tick_params(labelbottom=True) 
    ax2.tick_params(labelbottom=True)

    ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing)) 
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    # --- HÀM VẼ VẠCH KẺ ---
    def draw_markers(ax):
        trans = ax.get_xaxis_transform() 
        colors = ['#2ca02c', '#d62728', '#1f77b4'] 
        
        for i, (t, label) in enumerate(manual_markers):
            if t > df['Time'].max(): continue
            
            c = colors[i % len(colors)]
            ax.axvline(x=t, color=c, linestyle='--', alpha=0.7, linewidth=1.5)
            ax.text(t, -0.12, label, transform=trans, color=c, 
                    ha='center', va='top', fontweight='bold', fontsize=9, 
                    bbox=dict(facecolor='white', alpha=0.9, edgecolor='none'))

    # --- Plot 1: CPU ---
    for node in node_list:
        if f'{node}_CPU' in df.columns:
            ax1.plot(df['Time'], df[f'{node}_CPU'], label=node, alpha=0.7, linewidth=1.5, linestyle='-')
    
    if 'Total_CPU' in df.columns:
        ax1.plot(df['Time'], df['Total_CPU'], label='TOTAL', color='black', linewidth=2.5)
    
    draw_markers(ax1)
    
    max_cpu_val = df['Total_CPU'].max() if 'Total_CPU' in df.columns else 100
    top_ylim = max(105, max_cpu_val + 10)
    ax1.set_ylim(0, top_ylim)
    
    ax1.set_ylabel('CPU Usage (%)')
    ax1.set_title(f'CPU Performance')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3, which='both')

    # --- Plot 2: RAM ---
    for node in node_list:
        if f'{node}_RAM' in df.columns:
            ax2.plot(df['Time'], df[f'{node}_RAM'], label=node, linewidth=2, linestyle='-')
    
    # [ĐÃ BỔ SUNG] Vẽ đường TOTAL RAM màu đen đậm
    if 'Total_RAM' in df.columns:
        ax2.plot(df['Time'], df['Total_RAM'], label='TOTAL', color='black', linewidth=2.5)
    
    draw_markers(ax2)
    
    ax2.set_ylim(bottom=0)
    ax2.set_ylabel('RAM (MB)')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_title('Memory Usage')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3, which='both')

    plt.subplots_adjust(left=0.06, right=0.95, top=0.95, bottom=0.12, hspace=0.25)
    
    output_img = args.csv_file.replace('.csv', '.png')
    plt.savefig(output_img)
    print(f"\nDone! Đã lưu biểu đồ tại: {output_img}")

if __name__ == "__main__":
    main()