from setuptools import Extension, setup

setup(
    name="artfast",
    version="1.0",
    description="Small integer helpers in C",
    ext_modules=[Extension("artfast", ["artfast.c"])],
)
