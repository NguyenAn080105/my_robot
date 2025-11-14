A ROS (Robot Operating System) package for simulating and navigating a custom differential drive robot. This package includes configurations for Gazebo simulation, the ROS Navigation Stack (move_base), and hardware integration for an RPLidar S2E.

## 📦 Package Structure

This package follows standard ROS conventions:

* **/config**: Contains all configuration files (`.yaml`) for:
    * ROS Navigation Stack (planners, costmaps, recovery behaviors).
    * Robot controllers (`ros_control`, PID gains).
    * RViz configurations (`.rviz`).
* **/include**: C++ header files.
* **/launch**: Launch files (`.launch`) to start simulations, navigation, and hardware drivers.
* **/maps**: Pre-generated maps (`.pgm`, `.yaml`) for autonomous navigation.
* **/src**: C++ source code (nodes).
* **/urdf**: Robot model definition files (`.urdf`) for simulation and visualization.
* **/worlds**: Custom Gazebo world files (`.world`).

## 🛠️ Installation

### Prerequisites

* ROS (Noetic recommended)
* Gazebo (usually included with ROS Desktop-Full)
* ROS Navigation Stack:
    ```bash
    sudo apt-get install ros-noetic-navigation
    ```
* ROS Control:
    ```bash
    sudo apt-get install ros-noetic-ros-control ros-noetic-ros-controllers
    ```
* RPLidar ROS:
    ```bash
    sudo apt-get install ros-noetic-rplidar-ros
    ```

### Building from Source

1.  Navigate to your Catkin workspace's `src` directory:
    ```bash
    cd ~/catkin_ws/src/
    ```

2.  Clone this repository (hãy thay `YOUR_USERNAME` bằng tên của bạn):
    ```bash
    git clone [https://github.com/YOUR_USERNAME/my_robot.git](https://github.com/YOUR_USERNAME/my_robot.git)
    ```

3.  Navigate back to the workspace root and build:
    ```bash
    cd ~/catkin_ws/
    catkin_make
    ```

4.  Source the workspace to update your environment:
    ```bash
    source devel/setup.bash
    ```
    *(**Note**: Bạn nên thêm lệnh này vào `~/.bashrc` để chạy tự động)*

## 🚀 Usage

Ensure you have sourced your workspace (`source devel/setup.bash`) in every new terminal.

### 1. Launching Simulation (Gazebo + RViz)

This starts the Gazebo simulation with the robot model and opens RViz for visualization.

```bash
roslaunch my_robot sim.launch
