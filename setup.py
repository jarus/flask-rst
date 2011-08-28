from setuptools import setup

setup(
    name='flask-rst',
    version='0.1',
    url='http://bitbucket.org/Jarus/flask-rstblog',
    license='BSD',
    author='Christoph Heer',
    author_email='Christoph.Heer@googlemail.com',
    description='',
    packages=['flaskrst'],
    platforms='any',
    entry_points = {
            'console_scripts': ['flask-rst = flaskrst.cli:main'],
    },
    install_requires=[
        'Flask',
        'Flask-Script',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)