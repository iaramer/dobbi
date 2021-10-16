from distutils.core import setup

setup(
    name='dobbi',
    packages=['dobbi'],
    version='0.01',
    license='Apache License 2.0',
    description='An open-source library for fast NLP text cleaning and preprocessing.',
    author='Iaroslav Amerkhanov',
    author_email='amerkhanov.y@gmail.com',
    url='https://github.com/iaramer/dobbi',
    download_url='https://github.com/iaramer/dobbi/archive/refs/tags/v0_01.tar.gz',
    keywords=['nlp', 'text', 'string', 'preprocessing', 'cleaning', 'regexp'],
    #   install_requires=[
    #           'validators',
    #           'beautifulsoup4',
    #       ],
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: Apache License 2.0',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)
