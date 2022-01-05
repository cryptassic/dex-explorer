from setuptools import setup,find_packages

setup(
   name='explorer',
   version='1.0',
   description='Blockchain DEX explorer',
   author='Lukas Petravicius',
   packages=find_packages(),  #same as name
   install_requires=['wheel', 'coloredlogs==15.0.1','aiohttp==3.8.1','asyncio==3.4.3','web3==5.25.0','ciso8601==2.2.0'], #external packages as dependencies
   python_requires='>=3.6'
)