# my_robot

A ROS (Robot Operating System) package for simulating and navigating a custom differential drive robot. This package is configured for **ROS Melodic Morenia** on **Ubuntu 18.04**.

It includes configurations for Gazebo simulation, the ROS Navigation Stack (move_base), and hardware integration for an RPLidar S2E.

## 📦 Package Structure

This package follows standard ROS conventions:

* **/config**: All `.yaml` configurations for `move_base` (planners, costmaps), robot controllers, and `.rviz` files.
* **/include**: C++ header files.
* **/launch**: `.launch` files to start simulations, navigation, and hardware drivers.
* **/maps**: Pre-generated maps (`.pgm`, `.yaml`) for autonomous navigation.
* **/src**: C++ source code (nodes).
* **/urdf**: Robot model definition files (`.urdf`) for simulation and visualization.
* **/worlds**: Custom Gazebo world files (`.world`).

## 🛠️ Installation

### Prerequisites

* Ubuntu 18.04
* ROS Melodic Morenia
* Gazebo 9
* ROS Navigation Stack:
    ```bash
    sudo apt-get install ros-melodic-navigation
    ```
* ROS Control:
    ```bash
    sudo apt-get install ros-melodic-ros-control ros-melodic-ros-controllers
    ```
* RPLidar ROS:
    ```bash
    sudo apt-get install ros-melodic-rplidar-ros
    ```

### Building from Source

1.  Navigate to your Catkin workspace's `src` directory:
    ```bash
    cd ~/catkin_ws/src/
    ```

2.  Clone this repository:
    ```bash
    git clone [https://github.com/NguyenAn080105/my_robot.git](https://github.com/NguyenAn080105/my_robot.git)
    ```

3.  Navigate back to the workspace root and build:
    ```bash
    cd ~/catkin_ws/
    catkin_make
    ```

4.  Source the workspace to update your environment (làm điều này ở mọi terminal mới):
    ```bash
    source devel/setup.bash
    ```

## 🚀 Usage:
    ```bash
    source ~/catkin_ws/devel/setup.bash
    ```
### 1. Launching Simulation (Gazebo + RViz)
```bash
roslaunch my_robot sim.launch
