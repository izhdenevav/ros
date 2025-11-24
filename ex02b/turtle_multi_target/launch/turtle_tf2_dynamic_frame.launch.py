from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    radius_arg = DeclareLaunchArgument(
        'radius', default_value='2.0',
        description='Радиус орбиты морковки вокруг turtle1'
    )

    direction_arg = DeclareLaunchArgument(
        'direction_of_rotation', default_value='1',
        description='1 - по часовой, -1 - против часовой'
    )

    return LaunchDescription([
        radius_arg,
        direction_arg,

        IncludeLaunchDescription(
            PathJoinSubstitution([
                FindPackageShare('turtle_multi_target'), 'launch', 'turtle_tf2.launch.py'])
        ),
        Node(
            package='turtle_multi_target',
            executable='dynamic_frame_tf2_broadcaster',
            name='dynamic_broadcaster1',
            parameters=[
                {'turtlename': 'turtle1'},
                {'carrot': 'carrot1'},
                {'radius': LaunchConfiguration('radius')},
                {'direction': LaunchConfiguration('direction_of_rotation')}
            ]
        ),
        Node(
            package='turtle_multi_target',
            executable='dynamic_frame_tf2_broadcaster',
            name='dynamic_broadcaster2',
            parameters=[
                {'turtlename': 'turtle3'},
                {'carrot': 'carrot2'},
                {'radius': LaunchConfiguration('radius')},
                {'direction': LaunchConfiguration('direction_of_rotation')}
            ]
        ),
    ])