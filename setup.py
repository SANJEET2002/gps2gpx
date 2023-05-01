from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'gps2gpx gps2gpx is a Python library for capturing serial GPS data and converting it into a .gpx file format'
LONG_DESCRIPTION = """
gps2gpx is a Python library that allows you to read serial GPS data and convert it into a .gpx file format. It is designed to be lightweight, efficient, and non-blocking, using multi-threading to capture real-time GPS data without interrupting your program's main flow.

The library is mainly intended for use on Raspberry Pi, but it is also compatible with other platforms such as Linux and Windows. It supports a range of GPS devices and offers customizable data fields.

gps2gpx is open-source, allowing for community contributions and modifications. It is an ideal tool for tracking, mapping, and navigation applications where real-time GPS data is needed.
"""

# Setting up
setup(
    name="gps2gpx",
    version=VERSION,
    author="SANJEET2002 (sanjeet kumar)",
    author_email="<mail@sanjeetistc138@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pyserial'],
    keywords=['python', 'gps', 'gps', 'gps stream', 'gpx format'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
