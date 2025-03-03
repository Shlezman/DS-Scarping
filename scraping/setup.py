from setuptools import setup, find_packages

setup(
    name="scraping",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4~=4.12.3',
        'pandas~=2.2.3',
        'playwright~=1.49.1'
    ],
)
