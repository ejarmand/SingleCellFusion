import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'),
                      fd.read())


setup(
    name="singlecellfusion",
    version="0.1.0",
    url="https://github.com/mukamel-lab/SingleCellFusion",
    license='GNU General Public License Version 2',

    author="Mukamel Lab",
    author_email="lab@brainome.ucsd.edu",

    description="Analyzes single-cell transcriptomic and epigenomic data",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),

    install_requires=['loompy>=2.0.16',
                      'numpy>=1.15.4',
                      'scikit-learn>=0.19.1',
                      'scipy>=1.1.0',
                      'pandas>=0.23.4',
                      'numba>=0.41.0'
                      ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
