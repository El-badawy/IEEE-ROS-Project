import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


PACKAGE_NAME = "Mapping_Robot"


def _launch_setup(context, *args, **kwargs):

    use_sim_time = LaunchConfiguration("use_sim_time").perform(context)
    world_path = LaunchConfiguration("world").perform(context)
    world_name = LaunchConfiguration("world_name").perform(context)
    robot_path = LaunchConfiguration("robot_model").perform(context)
    entity_name = LaunchConfiguration("entity_name").perform(context)
    slam_params_path = LaunchConfiguration("slam_params_file").perform(context)
    rviz_config_path = LaunchConfiguration("rviz_config_file").perform(context)

    spawn_x = LaunchConfiguration("x").perform(context)
    spawn_y = LaunchConfiguration("y").perform(context)
    spawn_z = LaunchConfiguration("z").perform(context)
    spawn_yaw = LaunchConfiguration("yaw").perform(context)

    if not os.path.isfile(world_path):
        raise FileNotFoundError(
            f"Gazebo world file was not found: {world_path}\n"
            "Pass another file with: world:=/absolute/path/to/world.sdf"
        )

    if not os.path.isfile(robot_path):
        raise FileNotFoundError(
            f"Robot URDF file was not found: {robot_path}\n"
            "Expected urdf/robot.urdf inside the package."
        )

    if not os.path.isfile(slam_params_path):
        raise FileNotFoundError(
            f"SLAM Toolbox parameter file was not found: {slam_params_path}"
        )

    with open(robot_path, "r", encoding="utf-8") as urdf_file:
        robot_description = urdf_file.read()

    # Start Gazebo Sim and load the selected world.
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py",
            )
        ),
        launch_arguments={
            "gz_args": f'-r -v 4 "{world_path}"',
            "on_exit_shutdown": "true",
        }.items(),
    )

    # Publish the URDF and the robot TF tree.
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": use_sim_time.lower() == "true",
            }
        ],
    )

    # Spawn the standalone combined URDF in Gazebo.
    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        name="spawn_diff_drive_robot",
        output="screen",
        arguments=[
            "--world", "sumo_maze_world",
            "--file", robot_path,
            "--name", "diff_drive_robot",
            "-x", "0.0",
            "-y", "0.0",
            "-z", "1.0",
            "-Y", "0.0",
        ],
    )

    # Bridge the Gazebo Transport topics used by the robot and SLAM.
    # '[' means Gazebo -> ROS 2, and ']' means ROS 2 -> Gazebo.
    gazebo_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="gazebo_bridge",
        output="screen",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
            "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
            "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
            "/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V",
            "/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model",
            "/imu@sensor_msgs/msg/Imu[gz.msgs.IMU",
            "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
        ],
        parameters=[
            {
                "qos_overrides./scan.publisher.reliability": "best_effort",
            }
        ],
    )

    # Start SLAM Toolbox in online asynchronous mapping mode.
    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("slam_toolbox"),
                "launch",
                "online_async_launch.py",
            )
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "slam_params_file": slam_params_path,
            "autostart": "true",
        }.items(),
    )

    # Start RViz with a configuration suitable for SLAM Toolbox.
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_path],
        parameters=[{"use_sim_time": use_sim_time.lower() == "true"}],
        condition=IfCondition(LaunchConfiguration("launch_rviz")),
    )

    # Gazebo needs a short startup period before the robot is inserted.
    return [
        gazebo,
        robot_state_publisher,
        gazebo_bridge,
        TimerAction(period=3.0, actions=[spawn_robot]),
        TimerAction(period=5.0, actions=[slam_toolbox]),
        TimerAction(period=6.0, actions=[rviz]),
    ]


def generate_launch_description() -> LaunchDescription:
    package_share = get_package_share_directory(PACKAGE_NAME)
    slam_toolbox_share = get_package_share_directory("slam_toolbox")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
                description="Use Gazebo simulation time.",
            ),
            DeclareLaunchArgument(
                "world",
                default_value=os.path.join(
                    package_share,
                    "worlds",
                    "sumo_maze_world.sdf",
                ),
            ),
            DeclareLaunchArgument(
                "world_name",
                default_value="sumo_maze_world",
            ),
            DeclareLaunchArgument(
                "robot_model",
                default_value=os.path.join(
                    package_share, "urdf", "robot.urdf"
                ),
                description="Absolute path to the standalone combined URDF.",
            ),
            DeclareLaunchArgument(
                "slam_params_file",
                default_value=os.path.join(
                    package_share, "config", "mapper_params_online_async.yaml"
                ),
                description="SLAM Toolbox YAML parameter file.",
            ),
            DeclareLaunchArgument(
                "rviz_config_file",
                default_value=os.path.join(
                    slam_toolbox_share, "config", "slam_toolbox_default.rviz"
                ),
                description="RViz configuration file.",
            ),
            DeclareLaunchArgument(
                "launch_rviz",
                default_value="true",
                description="Start RViz when true.",
            ),
            DeclareLaunchArgument(
                "entity_name",
                default_value="Mapping_Robot",
                description="Entity name used in Gazebo.",
            ),
            DeclareLaunchArgument("x", default_value="0.0"),
            DeclareLaunchArgument("y", default_value="0.0"),
            DeclareLaunchArgument("z", default_value="0.5"),
            DeclareLaunchArgument("yaw", default_value="0.0"),
            OpaqueFunction(function=_launch_setup),
        ]
    )
