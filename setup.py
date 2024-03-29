from setuptools import setup, find_packages
from Cython.Build import cythonize

import numpy as np

import os
import subprocess


################################################################################ version information

VERSION = '0.1.0'
__version__ = VERSION
ISRELEASED = False



######################################################################
# Writing version control information to the module
# adapted from MDTraj setup.py

def git_version():
    # Return the git revision as a string
    # copied from numpy setup.py
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
        GIT_REVISION = 'Unknown'

    return GIT_REVISION


def write_version_py(filename):
    from textwrap import dedent
    cnt = dedent("""\
            # THIS FILE IS GENERATED FROM SETUP.PY
            short_version = '%(version)s'
            version = '%(version)s'
            full_version = '%(full_version)s'
            git_revision = '%(git_revision)s'
            release = %(isrelease)s

            if not release:
            version = full_version
            """)
    # Adding the git rev number needs to be done inside write_version_py(),
    # otherwise the import of numpy.version messes up the build under Python 3.
    FULLVERSION = VERSION
    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    else:
        GIT_REVISION = 'Unknown'

    if not ISRELEASED:
        FULLVERSION += '.dev-' + GIT_REVISION[:7]

    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION,
                       'full_version': FULLVERSION,
                       'git_revision': GIT_REVISION,
                       'isrelease': str(ISRELEASED)})
    finally:
        a.close()



write_version_py('wasq/version.py')
setup(
    name = 'wasq',
    version = VERSION,
    packages = find_packages(),
    ext_modules = cythonize('wasq/metrics/dihedral_rmsd.pyx'),
    include_dirs = [np.get_include()],

    author = "Badi' Abdul-Wahid",
    author_email = 'abdulwahidc@gmail.com',
    description = 'Adaptive Sampling using WorkQueue',
    license = 'GPLv2',
    )
