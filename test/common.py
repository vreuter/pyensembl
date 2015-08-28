from __future__ import absolute_import

import functools

from pyensembl import (
    ensembl_grch37,
    ensembl_grch38,
    cached_release
)
from nose.tools import nottest

major_releases = [
    ensembl_grch37,
    ensembl_grch38
]

contigs = list(range(1, 23)) + ["X", "Y", "M"]

@nottest
def test_ensembl_releases(*versions):
    """
    Run a unit test which takes an EnsemblRelease as an argument
    for multiple releases (most recent for each reference genome)
    """
    if len(versions) == 0:
        ensembl_releases = major_releases
    else:
        ensembl_releases = [cached_release(version) for version in versions]

    def decorator(test_fn):
        @functools.wraps(test_fn)
        def new_test_fn():
            for ensembl in ensembl_releases:
                test_fn(ensembl)
        return new_test_fn
    return decorator


# TemporaryDirectory only got added to Python in version 3.2
try:
    # pylint: disable=no-name-in-module
    from tempfile import TemporaryDirectory
except ImportError:
    # only added in Python 3.2
    from tempfile import mkdtemp
    from shutil import rmtree

    class TemporaryDirectory(object):
        def __init__(self):
            self.name = mkdtemp()

        def __enter__(self, *args, **kwargs):
            return self.name

        def __exit__(self, type, value, traceback):
            rmtree(self.name)
            # don't suppress exceptions
            return False