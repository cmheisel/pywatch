from setuptools import setup, find_packages

setup(
    name = "pywatch",
    version = "0.1",
    url = 'http://bitbucket.org/cmheisel/pywatch/',
    license = 'MIT',
    description = "Runs arbitrary commands if files specified to be watched change.",
    author = 'Chris Heisel',
    author_email = 'chris@heisel.org',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)

