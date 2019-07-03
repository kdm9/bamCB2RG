from setuptools import setup

desc = """
bamCB2RG: Re-label reads in a BAM such that cells are considered samples for variant calling
indiviudal cells in 10X Genomics Chromium data.
"""

setup(
    name="bamCB2RG",
    py_modules=['bamCB2RG', ],
    version="0.1.0",
    install_requires=["pysam"],
    description=desc,
    author="Kevin Murray",
    author_email="foss@kdmurray.id.au",
    url="https://github.com/kdmurray91/bamCB2RG",
    keywords=["single-cell", "genomics", "10X Chromium", "BAM"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
