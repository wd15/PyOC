#!/usr/bin/env python

from numpy.distutils.core import setup, Extension, find_packages
import subprocess
# from setuptools import setup, find_packages
import os


def git_version():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = ""

    return GIT_REVISION


def getVersion(version, release=True):
    if os.path.exists('.git'):
        _git_version = git_version()[:7]
    else:
        _git_version = ''
    if release:
        return version
    else:
        return version + '-dev.' + _git_version

wrapper = Extension('my_wrapper', sources=['my_wrapper.f90'], libraries=['my_module'])

setup(
    libraries = [('my_module', dict(sources=['my_module.f90'],
                                    extra_f90_compile_args=["-ffixed-form"]))],
    ext_modules = [wrapper]
)

# extension = Extension('wrapper_interface',
#                       sources=['pyopencalphad/fortran/liboctqpy.f90'],
#                       libraries=['pyopencalphad/fortr/liboctq.o', '../oc/liboceq.a']

liboctq = ('liboctq',
           dict(sources=['pyopencalphad/fortran/liboctq.f90'],
                extra_args=["-fPIC"]))
                      p
setup(name='pyopencalphad',
      version=getVersion('0.1', release=False),
      description='Python interface for OpenCalphad',
      author='Shengyen Li, Daniel Wheeler',
      author_email='shengyen.li@nist.gov',
      url='https://github.com/usnistgov/pyopencalphad',
      packages=find_packages(),
      package_data={'': ['tests/*.py']},
      libraries=Extension('wrapper', {'sources' : ['pyopencalphad/wrapper.py'],
                                      'libraries' : ['wrapper']}),

      )
