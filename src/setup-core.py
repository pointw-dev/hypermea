from setuptools import setup, find_packages
from version import VERSION


setup(
    name='hypermea-core',
    version=VERSION,
    description='The core library used by hypermea APIs.',
    long_description=open('./README-core.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Utilities'
    ],
    url='https://github.com/pointw-dev/hypermea',
    author='Michael Ottoson',
    author_email='michael@pointw.com',
    package_dir={'hypermea.core':'hypermea/core'},
    packages=find_packages(
        where='./hypermea/core',
        include=['hypermea.core.*']
    ),
    include_package_data=True,
    zip_safe=False
)
