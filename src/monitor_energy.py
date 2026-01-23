#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import pandas as pd
import matplotlib.pyplot as plt
import time
import sys
import os
import numpy as np

# =============================================================================
# 1. CẤU HÌNH PHẦN CỨNG (HARDWARE SPECIFICATION)
# Tổng hợp từ Datasheet các linh kiện thực tế
# =============================================================================
HARDWARE = {
    # --- NHÓM TẢI TĨNH (STATIC LOAD - LUÔN TIÊU THỤ) ---
    'Jetson_Nano': 5.0,    # Mode 5W (Max Performance Eco)
    'RPLiDAR_S2E': 2.2,    # 5V @ 450mA (Typical Scanning)
    'Webcam_C930E': 2.5,   # USB High-Res streaming (H.264 enc)
    'STM32_Driver': 0.6,   # MCU + Motor Driver Logic (L298N/TB6612)
    'IMU_BNO055': 0.05,    # 3V @ 15mA
    
    # --- NHÓM ĐỘNG HỌC (DYNAMICS - ROBOT 5KG) ---
    # Động cơ: JGB37-520 (12V DC Gear Motor)
    # Robot 5kg có quán tính lớn, cần dòng khởi động cao.
    
    'k_v': 16.0,  # Watt/(m/s) - Ma sát lăn lớn do robot nặng đè xuống sàn
    'k_w': 9.0,   # Watt/(rad/s) - Ma sát trượt bánh khi quay tại chỗ
    'k_a': 14.0   # Watt/(m/s^2) - Quán tính (Inertia) - Tốn điện nhất khi đề-pa
}

# Tự động tính tổng tải tĩnh
STATIC_LOAD = sum([v for k, v in HARDWARE.items() if k.startswith('P') or k[0].isupper()])
# (Lọc lấy các key Jetson, Lidar, Webcam...)
STATIC_LOAD = 10.35 # Gán cứng giá trị tổng (5+2.2+2.5+0.6+0.05)

# =============================================================================
# 2. CLASS MONITOR
# =============================================================================
class EnergyMonitorUltimate:
    def __init__(self):
        rospy.init_node('energy_monitor_final', anonymous=True)
        
        self.start_time = time.time()
        self.last_time = self.start_time
        self.last_v = 0.0
        
        self.total_energy = 0.0
        self.max_power = 0.0
        self.is_moving = False
        
        self.data_log = []
        self.stage_markers = []
        
        # Subscribers
        rospy.Subscriber('/odom', Odometry, self.odom_callback)
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback)
        
        print(f"--- SYSTEM READY: PAYLOAD 5KG ---")
        print(f"--- STATIC LOAD: {STATIC_LOAD:.2f} W ---")

    def cmd_vel_callback(self, msg):
        # Tự động phát hiện chuyển động
        if not self.is_moving and (abs(msg.linear.x) > 0.01 or abs(msg.angular.z) > 0.01):
            self.is_moving = True
            t = time.time() - self.start_time
            self.stage_markers.append((t, "Start Moving"))
            print(f"[AUTO] Motion Detected at {t:.1f}s")

    def odom_callback(self, msg):
        current_time = time.time()
        dt = current_time - self.last_time
        
        if dt <= 0: return

        # 1. Physics Calculation
        v = msg.twist.twist.linear.x
        w = msg.twist.twist.angular.z
        a = abs(v - self.last_v) / dt  # Gia tốc
        self.last_v = v

        # Công suất động cơ (P_motion)
        p_motion = (abs(v) * HARDWARE['k_v']) + \
                   (abs(w) * HARDWARE['k_w']) + \
                   (a * HARDWARE['k_a'])
        
        # Tổng công suất
        current_power = STATIC_LOAD + p_motion
        
        if current_power > self.max_power: self.max_power = current_power
        self.total_energy += current_power * dt

        # 2. Logging
        self.data_log.append({
            'Time': current_time - self.start_time,
            'Power': current_power,
            'Energy': self.total_energy,
            'Velocity': v
        })
        
        self.last_time = current_time

    def generate_report(self):
        if not self.data_log:
            print("No Data!")
            return

        df = pd.DataFrame(self.data_log)
        # Làm mượt dữ liệu để vẽ đồ thị đẹp
        df['Power_Smooth'] = df['Power'].rolling(window=20, min_periods=1).mean()
        
        # Setup output folder
        out_dir = os.path.expanduser('~/energy_reports_5kg')
        if not os.path.exists(out_dir): os.makedirs(out_dir)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # --- VẼ ĐỒ THỊ ---
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        
        # Plot 1: Power (Watt)
        ax1.plot(df['Time'], df['Power'], color='#dddddd', label='Raw Power')
        ax1.plot(df['Time'], df['Power_Smooth'], color='#d62728', linewidth=2, label='Smoothed Power')
        ax1.axhline(y=STATIC_LOAD, color='blue', linestyle='--', alpha=0.7, label=f'Static Load ({STATIC_LOAD}W)')
        
        ax1.set_ylabel('Power (Watt)', fontweight='bold')
        ax1.set_title(f'Power Profile: 5KG Robot (Jetson+Lidar+Webcam+Motors)', fontweight='bold')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        
        # Markers
        self.stage_markers.append((df['Time'].iloc[-1], "Finish"))
        for t, label in self.stage_markers:
            ax1.axvline(x=t, color='green', linestyle='--')
            ax1.text(t, ax1.get_ylim()[1]*0.9, f" {label}", color='green', fontweight='bold')

        # Plot 2: Energy (Joule)
        ax2.fill_between(df['Time'], df['Energy'], color='#1f77b4', alpha=0.3)
        ax2.plot(df['Time'], df['Energy'], color='#1f77b4', linewidth=2)
        ax2.set_ylabel('Total Energy (Joules)', fontweight='bold')
        ax2.set_xlabel('Time (seconds)', fontweight='bold')
        ax2.grid(True, alpha=0.3)

        # Info Box
        info = (f"CONFIG: 5KG PAYLOAD\n"
                f"- Jetson Nano: 5W\n"
                f"- Lidar S2E: 2.2W\n"
                f"- Webcam C930E: 2.5W\n"
                f"--------------------\n"
                f"Total Energy: {self.total_energy:.1f} J\n"
                f"Peak Power: {self.max_power:.1f} W")
        plt.figtext(0.15, 0.02, info, bbox=dict(facecolor='white', alpha=0.9, boxstyle='round'))
        
        # Save
        img_path = os.path.join(out_dir, f"report_{timestamp}.png")
        csv_path = os.path.join(out_dir, f"data_{timestamp}.csv")
        plt.savefig(img_path)
        df.to_csv(csv_path, index=False)
        
        print(f"\n[REPORT SAVED]: {img_path}")
        plt.show()

if __name__ == '__main__':
    node = EnergyMonitorUltimate()
    try:
        if sys.version_info[0] < 3: raw_input("Press ENTER to Finish...")
        else: input("Press ENTER to Finish...")
        node.generate_report()
    except rospy.ROSInterruptException:
        pass