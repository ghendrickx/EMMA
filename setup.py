"""
EMMA: Ecotope map maker based on abiotic characteristics

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
from setuptools import setup, find_packages

with open('README.md', mode='r') as f:
    long_description = f.read()

setup(
    name='EMMA',
    version='1.1',
    authors=[
        'Gijs G. Hendrickx',
        'Soesja Brunink',
    ],
    author_email='G.G.Hendrickx@tudelft.nl',
    description='Ecotope-Map Maker based on Abiotics',
    long_description=long_description,
    long_description_content_type='text/markdown',
    download_url='https://github.com/ghendrickx/EMMA',
    packages=find_packages(exclude='tests'),
    license='Apache-2.0',
    keywords=['ecology', 'ecotope', 'estuary', 'hydrodynamics'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'netCDF4',
        'numpy',
        'shapely',
        'typer',
        'xarray',
    ],
    entry_points={
        'console_scripts': [
            'emma = src.console:app_emma',
        ]
    },
    python_requires='>=3.9',
)
