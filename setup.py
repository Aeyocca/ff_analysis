from setuptools import setup, find_packages

setup(
    name='ff_analysis',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='FF analysis suite for the Boyz fantasy league',
    long_description=open('README.md').read(),
    install_requires=  ['numpy',
			'json',
			'pandas',
			'sys',
			're'],
    url='https://github.com/Aeyocca/ff_analysis',
    author='Alan E. Yocca',
    author_email='aeyap42@gmail.com'
)
