from setuptools import setup

setup(
    name="chip8",
    version="1.0.0",
    author="shivrm",
    author_email="shivrams.2006@gmail.com",
    description = "A CHIP-8 Interpreter made in Python",
    license="MIT",
    
    packages=['chip8'],
    install_requires=["setuptools", "pygame"],    
)