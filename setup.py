import platform
from setuptools import setup, Extension

if platform.python_implementation() is "CPython":
    libc_module = Extension("nullx.libc",
                            define_macros=[("MAJOR_VERSION", "1"),
                                            ("MINOR_VERSION", "0")],
                            include_dirs=["nullx/libc"],
                            sources=["nullx/libc/rand.c", "nullx/libc/libc.c"],
                            )

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(name="nullx",
    version="0.1",
    description="A collection of tools useful for CTFs",
    long_description=long_description,
    author="Bill Kudo",
    author_email="bluesky42624@gmail.com",
    license="MIT",
    ext_modules=[] if platform.python_implementation() is not "CPython" else [libc_module],
    packages=["nullx", "nullx.crypto", "nullx.net", "nullx.pwn"],
    scripts=["bin/dl", "bin/filter"],
    install_requires=["click", "supersonic"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ])
