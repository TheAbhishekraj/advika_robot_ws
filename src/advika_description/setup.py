import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'advika_description'

setup(
    name=package_name,
    version='3.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # URDF files
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.xacro')),
        (os.path.join('share', package_name, 'urdf/alternative'), glob('urdf/alternative/*.urdf')),
        # Fusion 360 STL meshes (PRIMARY design files — frozen 2026-07-26)
        (os.path.join('share', package_name, 'stl'), glob('stl/*.stl')),
        # RViz configs
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*')),
        # Alternative CAD STL meshes (CadQuery auto-generated — reference only)
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*.stl')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Abhishek / Bihar Bazaar Dev',
    maintainer_email='abhishek@advika.local',
    description='Advika 3.0 URDF/xacro description and Fusion 360 STL meshes',
    license='MIT',
    tests_require=['pytest'],
    entry_points={'console_scripts': []},
)