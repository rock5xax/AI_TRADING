from setuptools import setup, find_packages

setup(
    name="ai_trading",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask",
        "pytest",
        "pytest-mock",
        "breeze-connect",
    ],
)
