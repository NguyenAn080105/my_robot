#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
import argparse
import sys
import threading
from datetime import datetime

# Import ROS libraries
import rospy
from geometry_msgs.msg import Twist

# --- BIẾN TOÀN CỤC ---
current_stage = "Stage 1: Idle"
stage_markers = [] 
is_moving = False
start_time_global = 0

def cmd_vel_callback(msg):
    global current_stage, is_moving, stage_markers, start_time_global
    if not is_moving and (abs(msg.linear.x) > 0.01 or abs(msg.angular.z) > 0.01):
        is_moving = True
        switch_time = time.time() - start_time_global
        current_stage = "Stage 2: Moving"
        stage_markers.append((switch_time, "Start Moving"))
        print(f"\n\n[AUTO] Motion Detected! -> Stage 2 ({switch_time:.1f}s)")

def manual_input_listener():
    global current_stage, stage_markers, start_time_global
    try:
        if sys.version_info[0] < 3: raw_input()
        else: input()
        
        switch_time = time.time() - start_time_global
        current_stage = "Stage 3: Return"
        stage_markers.append((switch_time, "Stage 3"))
        print(f"\n\n[MANUAL] Type Enter! -> Stage 3 ({switch_time:.1f}s)")
    except EOFError: pass

def get_process_stats(node_names):
    stats = {}
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline:
                cmd_str = ' '.join(cmdline)
                for target_node in node_names:
                    if f"__name:={target_node}" in cmd_str or (target_node in cmd_str and "python" not in proc.info['name']):
                        cpu = proc.cpu_percent(interval=None) 
                        mem = proc.memory_info().rss / (1024 * 1024) # MB
                        
                        if target_node not in stats: stats[target_node] = {'cpu': 0, 'ram': 0}
                        stats[target_node]['cpu'] += cpu
                        stats[target_node]['ram'] += mem
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): pass
    return stats

def main():
    global start_time_global, current_stage
    
    rospy.init_node('performance_monitor_v7', anonymous=True)
    rospy.Subscriber("/cmd_vel", Twist, cmd_vel_callback)

    parser = argparse.ArgumentParser()
    parser.add_argument('--nodes', nargs='+', required=True, help="List of nodes to monitor")
    args = parser.parse_args()

    print(f"--- ROS System Monitor V7 (Full Axis & Solid Lines) ---")
    print(f"Monitoring: {args.nodes}")
    print("Status: Waiting... (Press ENTER to finish Stage 3)")

    input_thread = threading.Thread(target=manual_input_listener)
    input_thread.daemon = True
    input_thread.start()

    data_log = []
    start_time_global = time.time()
    stage_markers.append((0, "Start"))

    try:
        rate = rospy.Rate(1) 
        while not rospy.is_shutdown():
            current_time = time.time() - start_time_global
            node_stats = get_process_stats(args.nodes)
            
            row = {'Time': current_time}
            total_system_cpu = 0
            total_system_ram = 0

            for node in args.nodes:
                val = node_stats.get(node, {'cpu': 0, 'ram': 0})
                row[f'{node}_CPU'] = val['cpu']
                row[f'{node}_RAM'] = val['ram']
                total_system_cpu += val['cpu']
                total_system_ram += val['ram']

            row['Total_CPU'] = total_system_cpu
            row['Total_RAM'] = total_system_ram
            
            data_log.append(row)
            
            msg = f"\rT={current_time:03.0f}s | {current_stage} | TOTAL CPU: {total_system_cpu:5.1f}% | TOTAL RAM: {total_system_ram:5.0f} MB     "
            sys.stdout.write(msg)
            sys.stdout.flush()
            rate.sleep()

    except KeyboardInterrupt:
        print("\nStopping...")

    if not data_log: return

    # --- SAVE DATA ---
    df = pd.DataFrame(data_log)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    df.to_csv(f"ros_benchmark_nav_{timestamp}.csv", index=False)

    # --- SMOOTHING ---
    window_size = 4
    for node in args.nodes:
        df[f'{node}_CPU_Smooth'] = df[f'{node}_CPU'].rolling(window=window_size, min_periods=1).mean()
        df[f'{node}_RAM_Smooth'] = df[f'{node}_RAM'].rolling(window=window_size, min_periods=1).mean()
    
    df['Total_CPU_Smooth'] = df['Total_CPU'].rolling(window=window_size, min_periods=1).mean()

    # --- PLOTTING ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # X-Axis Settings
    tick_spacing = 10
    ax1.tick_params(labelbottom=True) 
    ax2.tick_params(labelbottom=True)

    ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    ax2.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    def draw_markers(ax):
        trans = ax.get_xaxis_transform() 
        colors = ['#2ca02c', '#d62728', '#1f77b4'] 
        for i, (t, label) in enumerate(stage_markers):
            if t > df['Time'].max(): continue
            c = colors[i % len(colors)]
            ax.axvline(x=t, color=c, linestyle='--', alpha=0.7, linewidth=1.5)
            ax.text(t, -0.12, label, transform=trans, color=c, 
                    ha='center', va='top', fontweight='bold', fontsize=9, 
                    bbox=dict(facecolor='white', alpha=0.9, edgecolor='none'))

    # --- Plot 1: CPU ---
    for node in args.nodes:
        ax1.plot(df['Time'], df[f'{node}_CPU_Smooth'], label=node, alpha=0.7, linewidth=1.5, linestyle='-')
    
    ax1.plot(df['Time'], df['Total_CPU_Smooth'], label='TOTAL', color='black', linewidth=2.5)
    
    draw_markers(ax1)
    max_cpu_val = df['Total_CPU_Smooth'].max()
    top_ylim = max(105, max_cpu_val + 10)
    ax1.set_ylim(0, top_ylim)
    
    ax1.set_ylabel('CPU Usage (%)')
    ax1.set_title(f'CPU Performance')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3, which='both')

    # --- Plot 2: RAM ---
    for node in args.nodes:
        # [SỬA] Nét liền cho RAM
        ax2.plot(df['Time'], df[f'{node}_RAM_Smooth'], label=node, linewidth=2, linestyle='-')
    
    draw_markers(ax2)
    
    # [SỬA] Set trục Y bắt đầu từ 0
    ax2.set_ylim(bottom=0)
    
    ax2.set_ylabel('RAM (MB)')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_title('Memory Usage')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3, which='both')
    plt.subplots_adjust(left=0.06, right=0.95, top=0.95, bottom=0.12, hspace=0.25)
    
    plt.savefig(f"benchmark_nav_{timestamp}.png")
    print(f"\n[Done] Chart saved at: benchmark_full_{timestamp}.png")
    plt.show()

if __name__ == "__main__":
    main()