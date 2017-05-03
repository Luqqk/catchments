from setuptools import setup


with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()


setup(
    name='catchments',
    version='1.1.0',
    description='Python wrapper for multiple APIs, that provide catchments-areas',
    long_description=readme + '\n\n' + history,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
    include_package_data=True,
    scripts=['bin/catchments-skobbler.py', 'bin/catchments-here.py'],
    test_suite='nose.collector',
    tests_require=['nose', 'requests']
)
