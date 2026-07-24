from setuptools import find_packages, setup

package_name = 'advika_navigation'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Abhishek',
    maintainer_email='abhishek@advika.local',
    description='Advika 3.0 Nav2 configuration, SLAM, and autonomous navigation',
    license='MIT',
    tests_require=['pytest'],
    entry_points={'console_scripts': []},
)
