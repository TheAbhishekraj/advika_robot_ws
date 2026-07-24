from setuptools import find_packages, setup

package_name = 'advika_hardware'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='Abhishek',
    maintainer_email='abhishek@advika.local',
    description='Advika 3.0 ESP32 bridge node, motor drivers and sensor publishers',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'esp32_bridge = advika_hardware.esp32_bridge_node:main',
            'battery_monitor = advika_hardware.battery_monitor_node:main',
        ],
    },
)
