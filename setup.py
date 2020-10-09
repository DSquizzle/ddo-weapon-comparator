from setuptools import setup
  
setup(
    name = "DDO-Weapon-Comparator",
    version = "0.1.0",
    description = "A simple tool to compare weapons in DDO",
    license = "MIT",
    py_modules = ['gui', 'weapon_comparator'],
    install_requires = [
        'matplotlib',
        'pyqt5',
        ],
    entry_points = {
        'console_scripts': ['ddo=gui']
        }
    )
