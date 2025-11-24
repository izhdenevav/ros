from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess, TimerAction

from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),
        Node(
            package='turtle_multi_target',
            executable='turtle_tf2_broadcaster',
            name='broadcaster1',
            parameters=[
                {'turtlename': 'turtle1'}
            ]
        ),
        Node(
            package='turtle_multi_target',
            executable='turtle_tf2_broadcaster',
            name='broadcaster2',
            parameters=[
                {'turtlename': 'turtle2'}
            ]
        ),
        Node(
            package='turtle_multi_target',
            executable='turtle_tf2_broadcaster',
            name='broadcaster3',
            parameters=[
                {'turtlename': 'turtle3'}
            ]
        ),
        Node(
            package='turtle_multi_target', 
            executable='static_frame_broadcaster',
            name='static_target_broadcaster'
        ),
        TimerAction(
            period=2.0,
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn',
                        '{x: 1.0, y: 1.0, theta: 0.0, name: "turtle2"}'],
                    output='screen'
                )
            ]
        ),
        TimerAction(
            period=5.0,
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn',
                        '{x: 8.0, y: 8.0, theta: 0.0, name: "turtle3"}'],
                    output='screen'
                )
            ]
        ),
        Node(
            package='turtle_multi_target',
            executable='static_turtle_controller',
            name='stop_turtle3',
            parameters=[{'turtle_name': 'turtle3'}],
        ),
        Node(
            package='turtle_multi_target', 
            executable='switch_target',
            name='switch_target'
        ),
    ])