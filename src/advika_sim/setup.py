from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'advika_sim'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include launch files
        (os.path.join('share', package_name, 'launch'),
            glob('../../simulation/launch/*.py')),
        # Include config files
        (os.path.join('share', package_name, 'config'),
            glob('../../simulation/config/*')),
        # Include URDF
        (os.path.join('share', package_name, 'urdf'),
            glob('../../simulation/urdf/*')),
        # Include Gazebo worlds
        (os.path.join('share', package_name, 'worlds'),
            glob('../../simulation/gazebo_worlds/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Abhishek',
    maintainer_email='abhishek@advika.local',
    description='Advika 3.0 Gazebo simulation, HITL, MCP bridge, safety monitor',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sim_mcp_bridge = advika_sim.sim_mcp_bridge:main',
            'safety_monitor = advika_sim.safety_monitor:main',
            'hitl_server = advika_sim.hitl_bridge:main',
            'run_scenario = advika_sim.run_scenario:main',
        ],
    },
)
