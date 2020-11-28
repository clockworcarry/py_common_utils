import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_common_utils_gh",
    version="1.0.1",
    author="Gabriel Helie",
    author_email="ghfin123@gmail.com",
    description="All-purpose python utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clockworcarry/py_common_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
)