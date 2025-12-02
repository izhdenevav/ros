import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    
    # --- НАСТРОЙКИ ---
    pkg_name = 'my_robot_description'
    urdf_file_name = '01-myfirst.urdf'

    # 1. Формируем пути
    pkg_share = FindPackageShare(pkg_name)
    urdf_path = PathJoinSubstitution([pkg_share, 'urdf', urdf_file_name])
    
    # !!! ВАЖНОЕ ИСПРАВЛЕНИЕ ДЛЯ МЕШЕЙ !!!
    # Gazebo ищет модели по пути model://urdf_tutorial/...
    # Ему нужно знать, где лежит папка share, в которой находится urdf_tutorial
    # Обычно это /opt/ros/jazzy/share или install/share
    
    # Получаем путь установки текущего пакета
    install_dir = get_package_share_directory(pkg_name)
    
    # Также нам нужен путь к urdf_tutorial, так как меши берутся оттуда
    # Если пакет urdf_tutorial не установлен, сделайте: sudo apt install ros-jazzy-urdf-tutorial
    try:
        urdf_tutorial_path = get_package_share_directory('urdf_tutorial')
        # Берем родительскую директорию (share), чтобы Gazebo нашел 'urdf_tutorial' внутри
        gz_resource_path = os.path.dirname(urdf_tutorial_path)
    except:
        # Если вдруг пакета нет, ставим хотя бы путь к нашему пакету
        gz_resource_path = os.path.dirname(install_dir)

    # Если у вас меши лежат прямо в вашем пакете my_robot_description, 
    # то нужно добавить путь и к нему:
    gz_resource_path += ":" + os.path.dirname(install_dir)

    # 2. Устанавливаем переменную окружения для Gazebo
    resource_env = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=gz_resource_path
    )

    # 3. Обработка URDF
    robot_description_content = Command(['xacro ', urdf_path])
    robot_description = {'robot_description': robot_description_content}

    # 4. Запуск Gazebo
    ros_gz_sim_pkg = get_package_share_directory('ros_gz_sim')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_pkg, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )

    # 5. Спавн робота
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'my_robot',
            '-z', '0.2'
        ],
        output='screen'
    )

    # 6. Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description] 
    )

    # 7. Мост
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V'
        ],
        output='screen'
    )

    # 8. RViz
    rviz_config_path = PathJoinSubstitution([pkg_share, 'rviz', 'urdf.rviz'])
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_path],
        output='screen'
    )

    return LaunchDescription([
        resource_env, # <-- Добавляем переменную среды ПЕРВЫМ пунктом
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
        bridge,
        rviz
    ])