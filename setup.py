#! /usr/bin/env python

from distutils.version import LooseVersion
import os

from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext as _build_ext


class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


DISTNAME = 'scikit-garden'
DESCRIPTION = "A garden of scikit-learn compatible trees"
URL = 'https://github.com/scikit-garden/scikit-garden'
MAINTAINER = 'Manoj Kumar'
MAINTAINER_EMAIL = 'mks542@nyu.edu'
LICENSE = 'new BSD'
VERSION = '0.1.3'

CYTHON_MIN_VERSION = '0.23'


message = ('Please install cython with a version >= {0} in order '
           'to build a scikit-garden development version.').format(
           CYTHON_MIN_VERSION)

libraries = []
if os.name == 'posix':
    libraries.append('m')


extensions = []
for name in ['_tree', '_splitter', '_criterion', '_utils']:
    extensions.append(Extension(
        'skgarden.mondrian.tree.{}'.format(name),
        sources=['skgarden/mondrian/tree/{}.pyx'.format(name)],
        include_dirs=[],
        libraries=libraries,
        extra_compile_args=['-O3'],
    ))

if __name__ == "__main__":
    setup(name=DISTNAME,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          packages=find_packages(),
          include_package_data=True,
          description=DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=VERSION,
          zip_safe=False,  # the package can run out of an .egg file
          classifiers=[
              'Intended Audience :: Science/Research',
              'Intended Audience :: Developers',
              'License :: OSI Approved',
              'Programming Language :: C',
              'Programming Language :: Python',
              'Topic :: Software Development',
              'Topic :: Scientific/Engineering',
              'Operating System :: Microsoft :: Windows',
              'Operating System :: POSIX',
              'Operating System :: Unix',
              'Operating System :: MacOS'
            ],
          install_requires=["numpy", "scipy", "scikit-learn>=0.18", "cython"],
          setup_requires=["cython", "numpy"],
          cmdclass={'build_ext': build_ext},
          ext_modules=extensions)
