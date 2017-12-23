import sys

from os import path as p

from setuptools import setup, find_packages

exec(open('hydt/version.py').read())


def read(filename, parent=None):
    parent = (parent or __file__)

    try:
        with open(p.join(p.dirname(parent), filename)) as f:
            return f.read()
    except IOError:
        return ''


def parse_requirements(filename, parent=None):
    parent = (parent or __file__)
    filepath = p.join(p.dirname(parent), filename)
    content = read(filename, parent)

    for line_number, line in enumerate(content.splitlines(), 1):
        candidate = line.strip()

        if candidate.startswith('-r'):
            for item in parse_requirements(candidate[2:].strip(), filepath):
                yield item
        else:
            yield candidate


setup(
    name='hydt',
    author='Mark Henderson',
    email='emehrkay@gmail.com',
    version=__version__,
    packages=find_packages(),
    install_requires=list(parse_requirements('requirements.txt')),
    entry_points={
        'console_scripts': [
            'hydt=hydt.main:main',
        ],
    }
)
