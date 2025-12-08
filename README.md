# ros

1 задание

ros2 launch my_robot_description display.launch.py

ros2 run ros_gz_bridge parameter_bridge /scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan

ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(cat /home/vlada/ros2_ws/src/my_robot_description/urdf/01-myfirst.urdf)"

ros2 run rqt_robot_steering rqt_robot_steering

2 задание

ros2 run ros_gz_bridge parameter_bridge /scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan depth_camera@sensor_msgs/msg/Image@gz.msgs.Image depth_camera/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked
