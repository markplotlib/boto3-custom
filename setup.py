import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="boto3_custom",
    version="0.1",
    author="Mark Chesney",
    author_email="markplotlib@gmail.com",
    description="helper code to access an AWS S3 bucket",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy',
                      'pandas',
                      'boto3'],
    python_requires='>=3.6',
)
