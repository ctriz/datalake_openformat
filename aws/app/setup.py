from setuptools import setup

setup(
    name='hudi-app',
    version='1.0.0',
    py_modules=['hudi_trips_cow', 'hudi_trips_mor'],
    entry_points={
        'console_scripts': [
            'run-hudi_trips_cow=hudi_trips_cow:main',
            'run-hudi_trips_mor=hudi_trips_mor:main',
        ],
    },
)

