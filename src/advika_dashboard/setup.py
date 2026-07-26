from setuptools import setup

package_name = 'advika_dashboard'
setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/static', ['static/index.html']),
        ('share/' + package_name + '/static', ['static/style.css']),
        ('share/' + package_name + '/static', ['static/app.js']),
    ],
    install_requires=['setuptools', 'flask>=3.0', 'flask-socketio>=5.0', 'eventlet>=0.30'],
    zip_safe=True,
    maintainer='Abhishek',
    description='Advika 3.0 Web Teleop Dashboard',
    entry_points={
        'console_scripts': [
            'dashboard = advika_dashboard.dashboard:main',
        ],
    },
)