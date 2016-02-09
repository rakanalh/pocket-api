from setuptools import setup

setup(
    name='pocket-api',
    version='0.1.2',
    author='Rakan Alhneiti',
    author_email='rakan.alhneiti@gmail.com',

    py_modules=['pocket'],

    # Details
    url='https://github.com/rakanalh/pocket-api',

    license='LICENSE',
    description='A python wrapper around GetPocket API V3. ',
    long_description=open('README.md').read(),

    install_requires=[
        'requests',
    ],
    test_requires=[
        'pytest'
        'flake8==2.4.1'
        'responses==0.5.0'
    ]
)
