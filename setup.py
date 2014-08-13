from distutils.core import setup, Extension
import numpy

all_packages = [
        'gridcells',
        'gridcells.analysis',
        'gridcells.core',
        'gridcells.plotting',
]

default_swig_opts = ['-builtin',
                     '-O',
                     '-ignoremissing',
                     '-c++',
                     '-Iexternal/armanpy/include',
                     '-Isrc/include']
field_ext = Extension('gridcells.analysis._fields',
                            ['src/fields.cpp', 'src/fields.i'],
                             swig_opts=default_swig_opts)
common_ext = Extension('gridcells.core._common',
                            ['src/common.cpp', 'src/common.i'],
                            swig_opts=default_swig_opts)

setup(
        name='gridcells',
        version='0.1dev',
        description='Package for grid cell analysis and simulation.',
        author='Lukas Solanka',
        author_email='lsolanka@gmail.com',
        packages=all_packages,
        ext_modules=[field_ext, common_ext],
        include_dirs=['src/include', 'external/armanpy/include',
                      'external/armadillo/include',
                      numpy.get_include()],
        install_requires=['numpy>=1.8.0',
                          'scipy>=0.13.3']
)
