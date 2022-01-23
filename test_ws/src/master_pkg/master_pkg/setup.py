from setuptools import setup

package_name = 'master_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ros',
    maintainer_email='ros@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'gps_talker = master_pkg.gps_publisher:main',
        	'imu_talker = master_pkg.imu_publisher:main',
        	'cv_talker = master_pkg.cv_publisher:main',
        	'slam_talker = master_pkg.slam_publisher:main',
        	'slam_listener = master_pkg.slam_subscriber:main',
        	'motor_driver_listener = master_pkg.motor_driver_subscriber:main',
        	'radio_listener = master_pkg.radio_subscriber:main',
        ],
    },
)
