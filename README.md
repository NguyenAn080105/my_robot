<div align="center">

🤖 Autonomous Mobile Robot (AMR)

ROS Melodic Implementation on Differential Drive Robot

<!-- BẠN HÃY THAY LINK ẢNH DƯỚI ĐÂY BẰNG ẢNH ROBOT THẬT HOẶC ẢNH GAZEBO CỦA BẠN -->

<!-- Nếu chưa có ảnh, hãy xóa dòng này hoặc để tạm một ảnh placeholder -->

<img src="https://www.google.com/search?q=https://raw.githubusercontent.com/ros-planning/navigation/noetic-devel/navigation_stage/images/stage_rviz.png" width="800" alt="Robot Simulation Preview">

</div>

📖 Overview

This project implements a full-stack navigation solution for a custom differential drive robot. It bridges the gap between simulation (Gazebo) and real-world hardware (RPLidar S2E), demonstrating advanced capabilities in mapping, localization, and autonomous path planning.

The system is engineered to handle dynamic environments using the ROS Navigation Stack, optimized costmaps, and adaptive localization algorithms.

✨ Key Features

Feature

Description

Status

SLAM

Real-time mapping using gmapping (FastSLAM) & Lidar data.

✅

Localization

Robust pose estimation using AMCL (Adaptive Monte Carlo).

✅

Navigation

Autonomous path planning with move_base (Global/Local Planners).

✅

Simulation

High-fidelity URDF modeling and Gazebo physics environment.

✅

Hardware

Seamless integration with RPLidar S2E and motor controllers.

✅

📂 Project Structure

my_robot/
├── config/             # Navigation parameters (costmaps, planners)
├── launch/             # Launch files (Simulation, Drivers, AMCL)
├── maps/               # Occupancy Grid Maps (.pgm, .yaml)
├── meshes/             # 3D assets for the robot
├── urdf/               # Robot Description (Xacro/URDF)
├── worlds/             # Custom Gazebo environments
├── src/                # Source code for nodes
└── CMakeLists.txt      # Build configuration


🛠️ Tech Stack & Hardware

Middleware: ROS Melodic Morenia

OS: Ubuntu 18.04 Bionic

Languages: C++, Python, XML

Sensors: RPLidar S2E (Laser Scan), IMU, Wheel Encoders

Simulation: Gazebo 9, RViz

🚀 Getting Started

1. Prerequisites

Ensure you have the standard ROS Melodic navigation packages installed:

sudo apt-get install ros-melodic-navigation \
                     ros-melodic-map-server \
                     ros-melodic-move-base \
                     ros-melodic-amcl \
                     ros-melodic-rplidar-ros


2. Installation

Clone the repository directly into your catkin workspace:

cd ~/catkin_ws/src
git clone [https://github.com/NguyenAn080105/my_robot.git](https://github.com/NguyenAn080105/my_robot.git)

# Build the project
cd ~/catkin_ws
catkin_make
source devel/setup.bash


3. Usage Guide

🏗️ Simulation Mode

Launch the robot in the custom Gazebo world:

roslaunch my_robot world.launch


🧭 Autonomous Navigation

Start the navigation stack (AMCL + Move Base) with a pre-built map:

roslaunch my_robot amcl.launch


Tip: Open RViz and use the "2D Nav Goal" tool to instruct the robot to move to a specific coordinate.

🗺️ SLAM (Mapping)

To generate a map of a new environment:

roslaunch my_robot gmapping.launch


🔌 Hardware Driver

To start the physical robot sensors:

roslaunch my_robot rplidar.launch


<div align="center">

Developed by Nguyen An





GitHub Profile

</div>
