import setuptools
from importlib.machinery import SourceFileLoader

version = SourceFileLoader('version', 'aioviberbot/version.py').load_module()

setuptools.setup(
    name='aioviberbot',
    version=version.__version__,
    packages=['aioviberbot', 'aioviberbot.api', 'aioviberbot.api.viber_requests',
              'aioviberbot.api.messages', 'aioviberbot.api.messages.data_types'],
    install_requires=['aiohttp'],
    tests_require=['pytest'],
    url='https://github.com/antonmyronyuk/aioviberbot',
    author='Anton Myronyuk',
    author_email='antonmyronyuk@gmail.com',
    description='Viber Python Bot Async API',
    license='Apache',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
