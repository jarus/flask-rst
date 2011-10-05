from setuptools import setup, find_packages

setup(
    name='flask-rst',
    version='0.1',
    url='http://bitbucket.org/Jarus/flask-rstblog',
    license='BSD',
    author='Christoph Heer',
    author_email='Christoph.Heer@googlemail.com',
    description='Create a static website from simple reStructuredText files',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points = {
        'console_scripts': ['flask-rst = flaskrst.cli:main'],
    },
    install_requires=[
        'Flask>=0.7',
        'Flask-Script',
        'PyYAML',
        'docutils',
        'pygments'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
