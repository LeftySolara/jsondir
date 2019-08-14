import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsondir",
    version="0.1.0",
    author="Jalen Adams",
    author_email="jalen@jalenkadams.me",
    description="Display a directory tree in JSON format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeftySolara/jsondir",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "jsondir=jsondir.jsondir:main"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Natural Language :: English"
    ],
)