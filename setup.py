from setuptools import setup, find_packages

setup(
    name='pptx2img',
    version='0.1.0',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here, e.g., 'requests', 'numpy'
    ],
    author='Neeraj Narwal',
    author_email='neerajnarwal2000@gmail.com',
    description='This library helps in converting pptx slides to images using LibreOffice',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/captainnarwal/pptx2img',  # Use the repository URL without .git
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
