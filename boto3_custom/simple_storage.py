import boto3     # AWS SDK & API for Python
import pandas as pd
import os

def upload(obj, sub_dir='', buc):
    """
    Upload a directory or a file to S3 bucket

    :param obj: str -- name of target object (subdirectory or file) to upload
    :param sub_dir: str -- name of subdirectory under main directory
                into which a FILE is uploaded. REQUIRED when uploading file
    :param buc: str -- unique S3 bucket name
    :param main_dir: str -- name of main directory for upload
    """
    # initiate S3 client session
    session = boto3.session.Session(profile_name='dl_user')
    s3 = session.client('s3')

    # get names of directories and files in local working directory
    directories = [item.name for item in os.scandir() if item.is_dir()]
    files = [item.name for item in os.scandir() if item.is_file()]
    # fix formats: directories end in exactly 1 slash ('/')
    sub_dir = _fix_dir(sub_dir)

    # correct input if user enters directory prepended in input string
    # (e.g., obj='dir/file.csv')
    if sub_dir == '/' and '/' in obj:
        sub_dir, obj = obj.split('/')
        sub_dir = _fix_dir(sub_dir)
        if sub_dir[:-1] in directories:
            files = [item.name for item in os.scandir(sub_dir) if item.is_file()]
        else:
            raise IOError('subdirectory ' + sub_dir[:-1] + ' not found locally.')

    # directory upload
    if obj in directories:
        obj_type = 'directory'
        # recursively walk through subdirectories and files
        for local_root, dirs, files in os.walk(obj):
            for file in files:
                s3.upload_file(os.path.join(local_root, file), buc,
                               os.path.join(main_dir, local_root, file))
    # file upload
    elif obj in files:
        obj_type = 'file'
        if sub_dir == '/':
            # if subdirectory is blank
            raise IOError('Destination subdirectory is required for upload.')
        s3.upload_file(Filename=obj, Bucket=buc,
                       Key=os.path.join(main_dir, sub_dir, obj))
    else:
        raise FileNotFoundError(obj + ' not found.')

    print(f"Upload of {obj_type} '{obj}' is complete.")


def read_file(sub_dir, file, buc):
    """
    Read an S3 file, as a pandas.DataFrame, in a subdirectory

    :param sub_dir: str -- REQUIRED name of subdirectory within main directory
    :param file: str -- name of target file to download and read
    :param buc: str -- unique S3 bucket name
    :param main_dir: str -- name of main directory

    :return: pandas.DataFrame
    """
    # get names of directories in local working directory
    directories = [item.name for item in os.scandir() if item.is_dir()]

    # fix formats: directories end in exactly 1 slash ('/')
    sub_dir = _fix_dir(sub_dir)

    # error: subdirectory not found
        # note: sub_dir[:-1] trims the trailing slash '/'
    if sub_dir[:-1] not in directories:
        raise IOError('subdirectory ' + sub_dir[:-1] + ' not found locally.')

    session = boto3.session.Session(profile_name='dl_user')
    s3 = session.client('s3')

    # HTTP response, with target data in 'Body' key
    try:
        response: dict = s3.get_object(Bucket=buc,
                                       Key=os.path.join(
                                           main_dir, sub_dir, file))
    except s3.exceptions.NoSuchKey:
        # if target file is not here
        raise FileNotFoundError(file + ' is not found here.')

    try:
        # if 'Unnamed: 0' appears in df
        df = pd.read_csv(response['Body'], index_col='Unnamed: 0')
    except KeyError:
        df = pd.read_csv(response['Body'])
    return df


def _fix_dir(s: str):
    """
    ensure that string ends in exactly one forward slash (/)
    'folder1'   --> 'folder1/'
    'folder1//' --> 'folder1/'
    'folder1/'  --> 'folder1/'

    :param s: str

    :return: string ending in exactly one forward slash (/)
    """
    while s.endswith('/'):
        s = s[:-1]
    s += '/'
    return s
