from distutils.core import setup

setup(
    name='dobbi',
    py_modules=['dobbi'],
    version='0.02',
    license='Apache License 2.0',
    description='An open-source NLP library: fast text cleaning and preprocessing',
    author='Iaroslav Amerkhanov',
    author_email='amerkhanov.y@gmail.com',
    url='https://github.com/iaramer/dobbi',
    download_url='https://github.com/iaramer/dobbi/archive/refs/tags/v0_02.tar.gz',
    keywords=['nlp', 'text', 'string', 'regexp', 'preprocess', 'clean'],
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)
