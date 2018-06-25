from setuptools import setup

setup(
    name='pygipo',
    version='0.1',
    packages=['pygipo'],
    include_package_data=True,
    install_requires=[
        'psycopg2==2.7.3',
        'Django==2.0.4',
        'python-gitlab==1.3.0',
    ],
)

