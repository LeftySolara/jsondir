import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsondir",
    version="0.0.1",
    author="Jalen Adams",
    author_email="jalen@jalenkadams.me",
    description="Display a directory tree in JSON format or create one from a JSON file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeftySolara/jsondir",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
)