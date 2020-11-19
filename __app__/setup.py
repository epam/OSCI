from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='osci-datalake',
    version='0.1',
    description='OSCI Datalake package to be reused across OSCI',
    author='Vladislav Isaiko, Aleksei Gavrilov',
    author_email='Vladislav_Isaiko@epam.com, Aleksei_Gavrilov1@epam.com',
    packages=['datalake'],
    install_requires=required,
    python_requires='>=3',
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Environment :: Console',
    ],
)
