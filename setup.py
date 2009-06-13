from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pywatch",
    version = "0.1",
    url = 'http://bitbucket.org/cmheisel/pywatch/',
    license = 'MIT',
    description = "Runs arbitrary commands if files specified to be watched change.",
    long_description = read('README'),

    author = 'Chris Heisel',
    author_email = 'chris@heisel.org',

    packages = find_packages('src'),
    package_dir = {'': 'src'},

    install_requires = ['setuptools'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', 
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

