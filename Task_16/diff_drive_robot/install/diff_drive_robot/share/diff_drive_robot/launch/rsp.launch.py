import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'diff_drive_robot'

    use_sim_time = LaunchConfiguration('use_sim_time')
    urdf = LaunchConfiguration('urdf')

    default_urdf_path = os.path.join(
        get_package_share_directory(package_name), 'urdf', 'robot.urdf.xacro')

    declare_use_sim_time = DeclareLaunchArgument(
        name='use_sim_time', default_value='true',
        description='Use simulation (Gazebo) clock if true')

    declare_urdf = DeclareLaunchArgument(
        name='urdf', default_value=default_urdf_path,
        description='Full path to the robot xacro/urdf file')

    # xacro is processed at launch time so any xacro:property / xacro:include works
    robot_description = Command(['xacro ', urdf])

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': use_sim_time,
        }]
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_urdf,
        robot_state_publisher_node,
    ])
