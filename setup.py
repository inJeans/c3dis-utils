import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="utils",
    version="0.0.1",
    author="Christoper Watkins",
    author_email="chris.watkins@csiro.au",
    description="Utility functions for the C3DIS ML Workshop",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/inJeans/c3dis-utils",
    packages=["utils",
              "utils.datasets"]
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    install_requires=[
          "PyDrive",
          "imbalanced-learn"
      ],
)