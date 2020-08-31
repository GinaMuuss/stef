import setuptools
from os.path import dirname, join, abspath

with open("README.md", "r") as fh:
    long_description = fh.read()

rq_path = join(abspath(dirname(__file__)), 'requirements.txt')
requirements = []
with open(rq_path, 'r') as requirements_file:
    for line in requirements_file:
        line = line.strip()
        if not line:
            continue
        requirements.append(line)

setuptools.setup(
    name="stef",
    version="1.0.1",
    author="Gina Muuss",
    author_email="muuss@uni-bonn.de",
    description="Submission TEst Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GinaMuuss/stef",
    packages=["stef"],#setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={'console_scripts': ['stef_runtests = stef.scripts.runtests:main']},
    python_requires='>=3.6',
    install_requires=requirements,
    include_package_data=True
)
