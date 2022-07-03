from setuptools import find_packages
from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(name='lotame',
      version='3.0.0',
      description='Simple python wrapper for LOTAME API',
      install_requires=[
          'httplib2==0.19.0',
          'urllib3>=1.23,<1.27',
          'requests==2.28.1'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.8'
      ],
      keywords=(
          'lotame python wrapper client audience behavior api sdk'),
      url='https://github.com/bkmurchison/lotame',
      author='Paulo Kuong',
      author_email='paulo.kuong@gmail.com',
      maintainer='BK Murchison',
      maintainer_email='bryant.k.murchison@devtelligent.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      long_description=long_description)
