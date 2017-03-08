from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='catchments',
    version='0.9.0',
    description='A simple package for acquiring and manipulating catchments from Skobbler and Here API',
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    keywords='gis api catchments',
    url='http://github.com/Luqqk/catchments',
    author='Łukasz Mikołajczak (Luqqk)',
    author_email='mikolajczak.luq@gmail.com',
    license='MIT',
    packages=['catchments'],
    install_requires=[
        'requests',
    ],
    zip_safe=False,
    scripts=['bin/catchments-cls.py'],
    test_suite='nose.collector',
    tests_require=['nose']
)
