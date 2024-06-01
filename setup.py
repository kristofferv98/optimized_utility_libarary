
from setuptools import setup, find_packages

setup(
    name='optimized-utility-library',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'ujson',
        'matplotlib',
        'opencv-python'
    ],
    extras_require={
        'dev': [
            'pytest',
            'flake8'
        ]
    },
    author='Kristoffer Vatanehol',
    author_email='your.kristoffer.vatnehol@gmail.com',
    description='An optimized utility library for directory, file, image, and JSON operations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/optimized-utility-library',  # Update with your GitHub repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
