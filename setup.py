
from setuptools import setup, find_packages
import hownix

setup(
    name='hownix',
    version=hownix.__version__,
    description='find and understand *nix commands',
    author='Codanda B. Appachu',
    url='https://github.com/cappachu/hownix',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hownix = hownix.hownix:main',
        ]
    },
    package_data={
        'hownix': ['nix_commands.txt'],
    },
    install_requires=[
        'argparse',
        'clint',
        'requests',
        'pyquery',
    ],
)
