Autonomous Mobile Robot (AMR) Implementation with ROS Melodic

Project Abstract

This project involves the design, simulation, and deployment of an autonomous differential drive robot using the Robot Operating System (ROS Melodic). The system is engineered to perform Simultaneous Localization and Mapping (SLAM) and autonomous navigation in both simulated environments (Gazebo) and real-world scenarios.

The primary objective was to bridge the gap between simulation and hardware implementation, demonstrating proficiency in robot modeling, sensor integration, and motion planning algorithms.

Key Technical Achievements

1. Robot Modeling & Simulation

URDF/Xacro Design: Designed a custom Unified Robot Description Format (URDF) model for a differential drive robot, incorporating physical properties (inertia, collision) and visual geometry.

Gazebo Environment: Developed custom simulation worlds in Gazebo 9 to stress-test the robot's navigation capabilities.

Sensor Simulation: Integrated virtual sensor plugins (Lidar, IMU, Encoders) to replicate real-world data streams within the simulation.

2. Autonomous Navigation & Path Planning

ROS Navigation Stack: Successfully implemented the move_base package for global and local path planning.

Costmap Tuning: Configured and tuned local_costmap and global_costmap parameters (inflation radius, obstacle marking) to optimize obstacle avoidance in dynamic environments.

Localization: Deployed Adaptive Monte Carlo Localization (AMCL) to accurately estimate the robot's pose within a known map.

3. Hardware Integration

Lidar Interfacing: Integrated the RPLidar S2E sensor effectively, handling driver configuration and frame transformations (TF) to align hardware data with the simulation model.

SLAM Implementation: Utilized gmapping (FastSLAM algorithm) to generate 2D occupancy grid maps of unknown environments for future navigation tasks.

System Architecture

The package is structured according to standard ROS development practices:

/urdf: Contains the robot's physical description and kinematic model.

/config: Holds critical parameter files for the navigation stack (planners, costmaps) and controller settings.

/launch: Orchestration scripts for bringing up simulation, hardware drivers, and navigation nodes simultaneously.

/maps: Stores generated .pgm and .yaml map files used by the map server.

/worlds: Custom environment files for Gazebo simulation.

Technical Specifications & Prerequisites

Operating System: Ubuntu 18.04 (Bionic Beaver)

Middleware: ROS Melodic Morenia

Simulation: Gazebo 9, RViz

Hardware: Differential Drive Chassis, RPLidar S2E

Languages: C++, Python, XML (Launch/URDF)

Quick Start Guide

1. Installation

Ensure ROS Melodic and the Navigation Stack are installed.

# Clone the repository
cd ~/catkin_ws/src/
git clone [https://github.com/NguyenAn080105/my_robot.git](https://github.com/NguyenAn080105/my_robot.git)

# Install dependencies and build
cd ~/catkin_ws/
catkin_make
source devel/setup.bash


2. Running Simulation

Launch the robot in the Gazebo simulation environment:

roslaunch my_robot world.launch


3. Running Autonomous Navigation

Initiate the navigation stack with AMCL and Move Base:

roslaunch my_robot amcl.launch


Use RViz to set a "2D Nav Goal" and observe the robot's autonomous path planning.

4. Hardware Deployment (RPLidar)

Launch the driver for the physical Lidar sensor:

roslaunch my_robot rplidar.launch


Author: Nguyen An
Repository: github.com/NguyenAn080105/my_robot
