from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    safety_zone = LaunchConfiguration("safety_zone")

    r1_x = LaunchConfiguration("r1_x")
    r1_y = LaunchConfiguration("r1_y")
    r1_prio = LaunchConfiguration("r1_prio")

    r2_x = LaunchConfiguration("r2_x")
    r2_y = LaunchConfiguration("r2_y")
    r2_prio = LaunchConfiguration("r2_prio")

    return LaunchDescription([

        DeclareLaunchArgument(
            "safety_zone",
            default_value="2.0"
        ),

        DeclareLaunchArgument(
            "r1_x",
            default_value="0.0"
        ),
        DeclareLaunchArgument(
            "r1_y",
            default_value="0.0"
        ),
        DeclareLaunchArgument(
            "r1_prio",
            default_value="1"
        ),

        DeclareLaunchArgument(
            "r2_x",
            default_value="3.0"
        ),
        DeclareLaunchArgument(
            "r2_y",
            default_value="0.0"
        ),
        DeclareLaunchArgument(
            "r2_prio",
            default_value="2"
        ),

        Node(
            package="autonomous_traffic_manager",
            executable="traffic_manager",
            name="traffic_manager",
            output="screen",
            emulate_tty=True,
            parameters=[
                {
                    "safety_zone": safety_zone
                }
            ]
        ),

        Node(
            package="autonomous_traffic_manager",
            executable="fleet_emulator",
            namespace="robot1",
            name="fleet_emulator",
            output="screen",
            emulate_tty=True,
            parameters=[
                {
                    "x": r1_x,
                    "y": r1_y,
                    "priority": r1_prio
                }
            ]
        ),

        Node(
            package="autonomous_traffic_manager",
            executable="fleet_emulator",
            namespace="robot2",
            name="fleet_emulator",
            output="screen",
            emulate_tty=True,
            parameters=[
                {
                    "x": r2_x,
                    "y": r2_y,
                    "priority": r2_prio
                }
            ]
        ),
    ])