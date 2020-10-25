#!/usr/bin/env python
import os
import shutil
import sys

import sleemo

from setuptools import Command, find_packages, setup

if sys.argv[-1] == "publish":
    os.system("python setup.py upload")
    sys.exit()


class UploadCommand(Command):

    user_options = []

    def initialize_options(self): pass
    def finalize_options(self):   pass

    def run(self):
        try:
            cwd = os.path.join(os.path.abspath(os.path.dirname(__file__)))
            shutil.rmtree(os.path.join(cwd, 'dist'))
        except FileNotFoundError:
            pass

        os.system("python setup.py sdist")
        os.system('twine upload dist/*')
        os.system('git tag v{0}'.format(sleemo.__version__))
        os.system('git push github --tags')
        sys.exit()


setup_options = dict(
    name='sleemo',
    version=sleemo.__version__,
    description='AWS AppSync Lambda Application Framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Taewoo Kim',
    author_email='twkiiim@gmail.com',
    url='https://github.com/twkiiim/sleemo',
    packages=find_packages(exclude=['test*', 'image*', 'guide*', 'example*', 'docs*']),
    install_requires=['pytz'],
    license="MIT License",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    keywords='aws appsync lambda serverless framework',
    cmdclass={
        'upload': UploadCommand,
    },
)

setup(**setup_options)
