"""
Django dedupe backend - store files only once

This thing stores your files in hash folder structure like git.
Files with the same hash will never be duplicated
"""
from setuptools import setup, find_packages


__version__ = "0.0.2"

def readme():
    try:
        return open('README.rst').read()
    except:
        return __doc__

setup(
    # package name in pypi
    name='django-dedupe-backend',
    # extract version from module.
    version=__version__,
    description="The super storage backend",
    long_description=readme(),
    classifiers=[],
    keywords='django storage backend that stores files in git',
    author='Lars van de Kerkhof',
    author_email='lars@permanentmarkers.nl',
    url='https://github.com/specialunderwear/django-dedupe-backend',
    license='GPL v3',
    # include all packages in the egg, except the test package.
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    # for avoiding conflict have one namespace for all apc related eggs.
    namespace_packages=[],
    # include non python files
    include_package_data=True,
    zip_safe=False,
    # specify dependencies
    install_requires=[
        'setuptools',
    ],
    # mark test target to require extras.
    extras_require = {
        'test':  ["mock"]
    },
)
