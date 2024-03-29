# -*- coding: utf-8 -*-
"""
@author: Jussi (jnu@iki.fi)
"""

from setuptools import setup, find_packages


setup(
    name='gaitbase',
    version='0.10',
    description='Database for gait measurements',
    author='Jussi Nurminen',
    author_email='jnu@iki.fi',
    license='GPLv3',
    url='https://github.com/NCH-Motion-Laboratory/gaitbase',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gaitbase=gaitbase._gaitbase:main',
            'gaitbase_make_shortcut=gaitbase.utils:make_my_shortcut',
            'gaitbase_recreate_db=gaitbase.recreate_db:main'
        ]
    },
    include_package_data=True
)
