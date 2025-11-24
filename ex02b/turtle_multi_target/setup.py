from setuptools import find_packages, setup

import os
from glob import glob

package_name = 'turtle_multi_target'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        # (os.path.join('share', package_name, 'msg'), glob('msg/*.msg')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vlada',
    maintainer_email='vizdeneva@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turtle_tf2_broadcaster = turtle_multi_target.turtle_tf2_broadcaster:main',
            'dynamic_frame_tf2_broadcaster = turtle_multi_target.dynamic_frame_tf2_broadcaster:main',
            'static_turtle_controller = turtle_multi_target.static_turtle_controller:main',
            'switch_target = turtle_multi_target.switch_target:main',
            'static_frame_broadcaster = turtle_multi_target.static_frame_broadcaster:main'
        ],
    },
)
