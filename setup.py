from setuptools import setup, find_packages

setup(
    name='circle_simulation',  # Your package name
    version='0.1.0',     # Version of your package
    author='Dovid Gestetner',
    author_email='daveg6366@gmail.com',
    description='Physical simulation of bouncing, colliding 2d circles implemented entirely in Python',
    long_description=open('README.md').read(),  # Read long description from README
    long_description_content_type='text/markdown',  # Specify markdown if your README is in markdown
    url='https://github.com/yourusername/your_project',  # URL of your project
    packages=find_packages(),  # Automatically find and include all packages
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
    install_requires=[
        # Add any dependencies your package needs here
    ],
)
