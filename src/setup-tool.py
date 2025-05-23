import os
from setuptools import setup, find_packages
from version import VERSION


setup(
    name='hypermea',
    version=VERSION,
    description='Simple Commands, Serious APIs.',
    long_description=open('../README.md').read(),
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
    project_urls = {
        'Documentation': 'https://pointw-dev.github.io/hypermea'
    },
    author='Michael Ottoson',
    author_email='michael@pointw.com',
    packages=['hypermea'],
    include_package_data=True,
    # package_data={
    #     "hypermea": ["skel/**/*.py"]  # or use **/* if nested
    # },    
    install_requires=[
        'libcst',
        'inflect==4.1.0',   # 4.1.0   7.5.0 runs verrrrry slowly ?!??!
        'click',
        'requests',
        f'hypermea-core=={VERSION}'
    ],
    entry_points='''
        [console_scripts]
        hy=hypermea.tool.commands:initialize
        hypermea=hypermea.tool.commands:initialize
    ''',
    zip_safe=False
)
