# Autonomous Mobile Robot Project (ROS Melodic)

![ROS Melodic](https://img.shields.io/badge/ROS-Melodic-orange)
![Gazebo](https://img.shields.io/badge/Simulator-Gazebo-blue)
![C++](https://img.shields.io/badge/Language-C%2B%2B%20%7C%20Python-blue)
![Build](https://img.shields.io/badge/Build-Catkin-green)

## 📖 Project Overview

This project focuses on designing, simulating, and navigating a **differential drive mobile robot** within the **Robot Operating System (ROS)** framework. The primary goal is to demonstrate a complete autonomous navigation pipeline, ranging from chassis modeling to path planning in a dynamic environment.

The system is simulated in **Gazebo**, utilizing sensor fusion (Lidar & IMU) to perform Simultaneous Localization and Mapping (**SLAM**) and autonomous navigation using the ROS Navigation Stack.

## 🚀 Key Technical Features

### 1. Robot Modeling (URDF & Xacro)
* **Chassis Design:** Developed a custom differential drive robot using **URDF** (Unified Robot Description Format) and **Xacro** for modular code structure.
* **Physics Simulation:** Configured inertia matrices, collision boundaries, and friction coefficients to ensure realistic kinematic behavior in the Gazebo physics engine.
* **Sensor Integration:**
    * **Lidar (S2E):** Integrated for 2D obstacle detection and mapping.
    * **RGB-D Camera:** Integrated for visual feedback and depth perception.

### 2. SLAM (Simultaneous Localization and Mapping)
* Implemented the **gmapping** package (based on the FastSLAM algorithm) to generate a high-resolution 2D occupancy grid map of unknown environments.
* Optimized laser scan matching parameters to reduce map drifting and enhance loop closure accuracy.

### 3. Autonomous Navigation System
* **Localization (AMCL):** Utilized the Adaptive Monte Carlo Localization (particle filter) to track the robot's pose within a known map with high accuracy.
* **Path Planning (Move Base):**
    * **Global Planner:** Implemented Dijkstra/A* algorithms for calculating the optimal path from start to goal.
    * **Local Planner:** Tuned the Dynamic Window Approach (DWA) controller to execute smooth velocity commands and avoid dynamic obstacles in real-time.
    * **Costmaps:** Configured global and local costmap layers (inflation, obstacle) to define safe navigation zones.

### 4. Simulation Environment
* Designed a custom Gazebo world featuring complex geometries, narrow corridors, and obstacles to rigorously test the robot's navigation capabilities.

---

## 🛠 Technology Stack

| Component | Technology / Library |
| :--- | :--- |
| **OS** | Ubuntu 18.04 (Bionic) |
| **Middleware** | ROS Melodic |
| **Simulation** | Gazebo, RViz |
| **Languages** | C++, Python, XML (Launch/URDF) |
| **Build System** | Catkin |
| **Key Packages** | `gmapping`, `amcl`, `move_base`, `xacro`, `gazebo_ros` |

---

## 📂 Project Structure

```bash
my_robot/
├── launch/             # Launch files (world, amcl, mapping)
├── meshes/             # 3D assets (dae/stl files) for the robot
├── urdf/               # Robot description files (.xacro)
├── world/              # Custom simulation environments (.world)
├── maps/               # Generated maps (.pgm and .yaml)
├── config/             # Navigation parameter files (costmaps, planners)
└── CMakeLists.txt      # Build configuration
```

### Building from Source
1.  Navigate to your Catkin workspace's `src` directory:
    ```bash
    cd ~/catkin_ws/src/
    ```

2.  Clone this repository:
    ```bash
    git clone [https://github.com/NguyenAn080105/my_robot.git](https://github.com/NguyenAn080105/my_robot.git)
    ```

3.  Navigate back to the workspace root and build:
    ```bash
    cd ~/catkin_ws/
    catkin_make
    ```

4.  Source the workspace to update your environment:
    ```bash
    source ~/catkin_ws/devel/setup.bash
    ```
    *Note: You must do this in every new terminal you open.*

## Usage

**Important:** Always remember to source your workspace in every new terminal before running ROS commands:

```bash
source ~/catkin_ws/devel/setup.bash
