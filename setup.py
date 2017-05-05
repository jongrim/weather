from setuptools import setup

setup(
    name='whats_the_weather',
    version='0.1',
    description='Weather in your terminal',
    url='https://github.com/jongrim/whats-the-weather',
    author='Jonathan Grim',
    author_email='jonjongrim@gmail.com',
    license='MIT',
    packages=['whats_the_weather'],
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'wtw = whats_the_weather.__main__:main'
        ]
    }
)
