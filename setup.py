import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stef",
    version="0.0.1",
    author="Gina Muuss",
    author_email="muuss@uni-bonn.de",
    description="Submission TEst Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GinaMuuss/stef",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
