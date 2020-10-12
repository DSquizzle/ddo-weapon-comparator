from setuptools import setup
  
setup(
    name = 'DDO-Weapon-Comparator',
    version = '0.1.0',
    description = 'A simple tool to compare weapons in DDO',
    license = 'MIT',
    packages = ['ddoweapons'],
    package_dir = {'' : 'src'},
    python_requires = '>=3.8.0',
    install_requires = [
        'matplotlib',
        'pyqt5',
        ],
    entry_points = {
        'console_scripts': ['ddoweapons=ddoweapons.gui:main']
        }
    )
