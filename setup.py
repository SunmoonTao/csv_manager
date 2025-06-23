
import os
from setuptools import setup, find_packages

# Read the contents of the README file
# This allows the long_description to be read from the README.md
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='csv_manager',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    description='A simple Python package for managing CSV files like a database.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/csv_manager', # Replace with your project URL
    author='Your Name', # Replace with your name
    author_email='your.email@example.com', # Replace with your email
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', # Or another appropriate license
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    python_requires='>=3.6', # Specify minimum Python version
)
