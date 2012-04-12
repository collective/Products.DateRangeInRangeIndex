from setuptools import setup, find_packages
import sys, os

version = '1.2'
shortdesc = \
'zope index to query a daterange on objects with a daterange'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()
tests_require = ['interlude']

setup(name='Products.DateRangeInRangeIndex',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content', 
            'License :: OSI Approved :: BSD License',                        
      ],
      keywords='date start end range query zope index catalog overlap',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      license='Simplified BSD',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          'Zope2',
          'zope.catalog',
      ],
      tests_require=tests_require,
      extras_require = dict(
          test=tests_require,
      ),
)
