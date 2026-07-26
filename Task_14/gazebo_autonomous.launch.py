import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable
from launch_ros.actions import Node

def generate_launch_description():
    world_path = '/home/omar-abdallah/Tasks/Task_14/world.sdf'

    set_env = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value='/opt/ros/jazzy/share/turtlebot3_gazebo/models:/opt/ros/jazzy/share'
    )

    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_path],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',    
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'  
        ],
        output='screen'
    )

    autonomous_mover = Node(
        package='task_14_pkg',
        executable='autonomous_mover',
        output='screen'
    )

    return LaunchDescription([
        set_env,
        gazebo,
        bridge,
        autonomous_mover
    ])
    