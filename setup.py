from distutils.core import setup
import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='UTF-8')

setup(
    name='dobbi',
    packages=['dobbi', 'dobbi.collections'],
    version='0.13',
    license='Apache License 2.0',
    description='An open-source NLP library: fast text cleaning and preprocessing.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Iaroslav Amerkhanov',
    author_email='amerkhanov.y@gmail.com',
    url='https://github.com/iaramer/dobbi',
    download_url='https://github.com/iaramer/dobbi/archive/refs/tags/v0_13.tar.gz',
    keywords=['nlp', 'text', 'string', 'regexp', 'preprocess', 'clean'],
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
