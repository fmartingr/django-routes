#!/usr/bin/env python
from setuptools import setup

package = 'routes'

setup(
    name=package,
    version=__import__(package).__VERSION__,
    description='Basic dynamic routing support for django',
    author='Felipe Martin',
    author_email='fmartingr@me.com',
    url='http://fmartingr.com',
    packages=[package],
    zip_safe=False,
    include_package_data=True,
    install_requires=open('requirements.txt').read().split('\n'),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'License :: GPLv2',  # Same as django-suit
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Environment :: Web Environment',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ]
)
