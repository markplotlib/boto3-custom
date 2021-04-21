# S3 utility package

This package allows users to access data directly in an AWS Simple Storage Service (S3) bucket.
 With it, users can upload data to S3 and read directly from S3.

# Table of Contents
1. [Installation](#installation)
2. [Imports](#imports)
3. [S3](#s3)

## Data Lake, for Unstructured Data
The Data Lake rests in AWS's **Simple Storage Service** (S3), holding unstructured data in its raw form.

## Installation
To install this package:

1. Open a **Terminal** instance -- this command may not work in a Jupyter notebook.
3. Copy this line and paste it into the command prompt:
* `pip install git+https://https://github.com/markplotlib/boto3-custom.git`

### Prerequisite: AWS S3 Bucket Credentials

## Imports

Paste this Python code line into a Jupyter notebook.

```Python
from boto3_custom.simple_storage import upload, read_file
```

Helpful Jupyter Notebook tip: After typing in any function, press **Shift+Tab** to learn more about the function. [More tips are found here](https://towardsdatascience.com/jypyter-notebook-shortcuts-bf0101a98330).

## S3

Unstructured raw data files can be uploaded and accessed here in the data lake
hosted on Amazon's Simple Storage Service (S3).

### `upload`

Users can upload either a directory or a file to an S3 bucket.

* When uploading a file, a subdirectory **can** be specified.

#### examples

```Python
upload('new_folder')

upload(obj='data.csv', sub_dir='new_folder')
```

### `read_file`

Users can read an S3 file into a notebook, as a pandas.DataFrame, from S3.

* The file cannot reside in the root directory of a bucket.
* * It **must** reside in a subdirectory. As such, `read_file` requires a subdirectory in the function call.

#### examples

```Python
df2 = read_file('folder1', 'data2.csv')
df1 = read_file(sub_dir='folder1/', file='data1.csv')
df3 = read_file(file='data3.csv', sub_dir='folder1/')
```

### Package Management
#### Package Requirements
This utility package requires these APIs:
* **public**
* * `boto3`: a Software Development Kit to interface Amazon Web Services via Python
* * `pandas`: Python library for data analysis
* * `numpy`: Python library for numerical computations

#### Update Instructions
This is necessary to update to the latest version.

`python -m pip install --upgrade git+https://https://github.com/markplotlib/boto3-custom.git`
