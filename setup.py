import os
from setuptools import setup, find_packages

setup_py_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(setup_py_dir)

setup(
    name='pyliquibase',
    version='2.0.0',
    packages=find_packages(),
    author='Memiiso',
    description='Python liquibase Wrapper',
    url='https://github.com/memiiso/pyliquibase',
    download_url='https://github.com/memiiso/pyliquibase/archive/master.zip',
    include_package_data=True,
    test_suite='tests',
    install_requires=["pyjnius==1.4.0"],
    python_requires='>=3',
)
