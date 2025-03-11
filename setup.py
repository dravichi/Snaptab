from setuptools import setup, find_namespace_packages

setup(
    name='snaptab',
    version='0.1.1',
    description='Build your own table dataset from PDFs in a single snap!',
    author='Anathapindika Dravichi',
    author_email='anathapindika_12201220@csepup.ac.in',
    license='MIT',
    packages=find_namespace_packages(include=['snaptab', 'snaptab.*']),
    include_package_data=True,
    install_requires=[
        'pdf2image',
        'PyPDF2',
        'ultralytics',
    ],
    entry_points={
        'console_scripts': [
            'snaptab=snaptab.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Keep this in the classifiers
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
