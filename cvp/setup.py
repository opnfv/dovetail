import setuptools


__author__ = 'serena'

try:
    import multiprocessing  # noqa
except ImportError:
    pass

setuptools.setup(
    setup_requires=['pbr==2.0.0'],
    pbr=True)
