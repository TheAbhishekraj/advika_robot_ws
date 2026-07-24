from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'advika_cad'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Install the CAD script itself
        (os.path.join('share', package_name, 'cad'), ['advika30_cad.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Abhishek',
    maintainer_email='abhishek@advika.local',
    description='Advika 3.0 CadQuery parametric CAD source of truth — exports 17 STLs',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'export_stl = advika_cad.export_stl:main',
        ],
    },
)
