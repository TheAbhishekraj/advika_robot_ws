from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'advika_sim'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'launch/selectors'), glob('launch/selectors/*.py')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf') + glob('worlds/*.world')),
        (os.path.join('share', package_name, 'worlds/3bhk_house'), glob('worlds/3bhk_house/*')),
        (os.path.join('share', package_name, 'worlds/warehouse'), glob('worlds/warehouse/*')),
        (os.path.join('share', package_name, 'worlds/office'), glob('worlds/office/*')),
        (os.path.join('share', package_name, 'worlds/advika_playground'), glob('worlds/advika_playground/*')),
        (os.path.join('share', package_name, 'models/LivingRoom'), glob('models/LivingRoom/*')),
        (os.path.join('share', package_name, 'models/NUS_SEDS_OGV'), glob('models/NUS_SEDS_OGV/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='abhishek',
    maintainer_email='abhishek@todo.todo',
    description='Advika 3.0 Simulation Package',
    license='MIT',
    tests_require=['pytest'],
    entry_points={},
)
