import os
from setuptools import setup
from version import VERSION


# inside_tox = 'TOX_ENV_NAME' in os.environ
# core_dependency = f'hypermea-core=={VERSION}' if not inside_tox else 'hypermea-core'


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
    author='Michael Ottoson',
    author_email='michael@pointw.com',
    packages=['hypermea'],
    include_package_data=True,
    install_requires=[
        'libcst',
        'inflect==4.1.0',
        'click',
        'requests',
#        core_dependency
        f'hypermea-core=={VERSION}'
    ],
    entry_points='''
        [console_scripts]
        hy=hypermea.tool.commands:initialize
        hypermea=hypermea.tool.commands:initialize
    ''',
    zip_safe=False
)
