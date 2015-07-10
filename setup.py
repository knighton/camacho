from setuptools import setup
from setuptools import find_packages

setup(name = 'Camacho',
      version = '0.0.1',
      description = 'Hyperoptimizer',
      author = 'James Knighton',
      author_email = 'jknighton@livefyre.com',
      url = 'https://github.com/knighton/camacho',
      license = 'MIT',
      install_requires = ['nltk', 'keras'],
      packages = find_packages(),
)
