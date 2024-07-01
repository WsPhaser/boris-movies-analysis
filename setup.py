from setuptools import setup, find_packages

setup(
    name='boris-movies-analysis',
    version='0.1.0',
    author='Boris Krastev',
    author_email='bkrastev@outlook.com',
    description='Analysis of a movies dataset',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/WsPhaser/boris-movies-analysis',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=8.12.3',
)
