import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="main_twyla",
    version="0.0.1",
    author="Rahul D",
    author_email="author@example.com",
    description="RESTful spell corrector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rmdotka92/TwylaNLP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
