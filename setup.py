from setuptools import setup, find_namespace_packages

setup(
    name='snaptab',
    version='0.1.7',
    description='Build your own table dataset from PDFs in a single snap!',
    author='Anathapindika Dravichi',
    author_email='anathapindika_12201220@csepup.ac.in',
    license='MIT',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(include=['snaptab', 'snaptab.*']),
    include_package_data=True,
    install_requires=[
        "pdf2image>=1.16.0",
        "PyPDF2>=3.0.0",
        "ultralytics>=8.0.0",
    ],
    entry_points={
        'console_scripts': [
            'snaptab=snaptab.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
