from setuptools import setup

setup(
    name='pygipo',
    version='0.1',
    packages=['pygipo'],
    include_package_data=True,
    install_requires=[
        'psycopg2>=2.7',
        'Django>=2.1',
        'python-gitlab>=1.3',
        'click>=7.0',
    ],
)

