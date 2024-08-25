from setuptools import setup, find_packages

setup(
    name="flask-streamy",
    version="0.1.0",
    description="A Flask package for managing SSE streams.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="nicholas@mendez.codes",
    url="https://github.com/snickdx/flask-streamy",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
