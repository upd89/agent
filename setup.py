#!/usr/bin/env python

import os
from setuptools import setup

setup(
    name = "upd89",
    version = "0.5.23",
    author = "Ueli Bosshard",
    author_email = "ubosshard@gmail.com",
    description = ("upd89 is a system update management "
                   "for debian based systems."),
    license = "MIT",
    keywords = "upd89 system update orchestration",
    url = "http://upd89.org",
    packages = ['upd89', 'upd89.classes', 'upd89.lib'],
    scripts=['bin/upd89'],
    data_files=[
        ('/etc/upd89', ['etc/config.ini']),
        ('/etc/init.d', ['init-script/upd89']),
    ],
    long_description='upd89 is a system update management ' +
        'for debian based systems.',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'daemonize',
        'schedule',
        'configparser',
        'bottle',
    ],
)

