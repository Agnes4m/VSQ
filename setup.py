import setuptools
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="VSQ",
    version="0.0.5", 
    author="Umamusume-Agnes-Digital", 
    author_email="Z735803792@163.com", 
    description="VALVE-Server Queries(now for L4D2)",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    url="https://github.com/Umamusume-Agnes-Digital/VSQ",
    packages=["VSQ"],
    project_urls={
        "Bug Tracker": "https://github.com/Umamusume-Agnes-Digital/VSQ/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0,<4.0',

)