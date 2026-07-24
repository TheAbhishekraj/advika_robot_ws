from setuptools import find_packages, setup

package_name = 'advika_sensors'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'opencv-python'],
    zip_safe=True,
    maintainer='Abhishek',
    maintainer_email='abhishek@advika.local',
    description='Advika 3.0 LiDAR, ToF, IMU and camera ROS2 driver nodes',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'lidar_node = advika_sensors.ld06_driver:main',
            'tof_node = advika_sensors.tof_publisher:main',
            'imu_node = advika_sensors.bno055_publisher:main',
            'camera_node = advika_sensors.dual_camera_publisher:main',
        ],
    },
)
