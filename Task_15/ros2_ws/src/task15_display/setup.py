from setuptools import find_packages, setup

package_name = 'task15_display'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    ('share/ament_index/resource_index/packages',
        ['resource/task15_display']),
    ('share/task15_display', ['package.xml']),
    ('share/task15_display/launch',
        ['launch/display.launch.py']),
    ('share/task15_display/urdf',
        ['urdf/robot.urdf']),
],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pablo',
    maintainer_email='ahmedsaeedelbadawy@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
