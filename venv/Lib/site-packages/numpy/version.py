
"""
Module to expose more detailed version info for the installed `numpy`
"""
version = "2.0.1"
__version__ = version
full_version = version

git_revision = "4c9f4316aaf8e80d9d18f089d1267d9cd74d0192"
release = 'dev' not in version and '+' not in version
short_version = version.split("+")[0]
