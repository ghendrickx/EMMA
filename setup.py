"""
EMMA: Ecotope map maker based on abiotic characteristics

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
from setuptools import setup

with open('README.md', mode='r') as f:
    long_description = f.read()

setup(
    name='EMMA',
    version='1.0',
    authors=[
        'Soesja Brunink',
        'Gijs G. Hendrickx',
    ],
    author_email='G.G.Hendrickx@tudelft.nl',
    description='Ecotope map maker based on abiotic characteristics',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        'config', 'examples', 'src'
    ],
    license='Apache-2.0',
    keywords=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'numpy',
        'netCDF4',
        'shapely',
    ],
    python_requires='>=3.7'
)
