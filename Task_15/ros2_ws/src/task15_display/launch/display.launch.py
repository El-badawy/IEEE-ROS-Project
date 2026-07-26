from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    robot_description = Command([
        "cat ",
        PathJoinSubstitution([
            FindPackageShare("task15_display"),
            "urdf",
            "robot.urdf"
        ])
    ])

    return LaunchDescription([

        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[{
                "robot_description": robot_description
            }]
        ),

        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui"
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            output="screen"
        ),
    ])
