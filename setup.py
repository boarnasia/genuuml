from os.path import join, dirname
from setuptools import setup, find_packages


PACKAGE_NAME = 'genuuml'

# Load __version__
with open(join(PACKAGE_NAME, 'version.py'), 'r') as f:
    exec(f.read())


setup(
    name='genuuml',
    version=__version__,
    url='',
    description='PlantUML generator from python script',
    long_description=open('README.rst').read(),
    author='boarnasia',
    license='MIT',
    packages=(PACKAGE_NAME, ),
    entry_points={
        'console_scripts': ['genuuml = genuuml.cli:main'],
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators ',
        'Topic :: Software Development :: Documentation',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'Click==7.0',
        'tree-format==0.1.2',
    ],
    extras_require={
        'dev': [
            'ipython',
            'pytest',
            'pytest-pep8',
            'pytest-cov',
            'tox',
            'mypy',
        ],
        'test': [
            'pytest',
        ],
    }
)
