# DDO Weapon Comparator
Different weapons in DDO deal different amounts of damage, according to the formula `W[XdY + Z] + D`, adjusted by the critical profile `P-QxM`. These two weapon characteristics, in conjunction with a character's melee/ranged power and various source of on-hit damage, determine a weapon's **damage per _strike_** (dps). Damage per strike, in turn, can be used to calculate **damage per _second_** (DPS) according to the formula `DPS = dps * animations per second * attacks per animation`. Because this tool is currently intended to be used to compare two different weapons of the same type (combat style), variations in attack speed and doublestrike/doubleshot are expected to be low from weapon to weapon, so weapons are compared in terms of  dps rather than DPS.

For a given weapon, most of the variables in the calculations above can be expected to change slowly as a character levels, or remain constant when a character is at max level. The exception to this rule is the `D` variable in the first formula, which tends to change quite rapidly as characters level up, upgrade their gear, or otherwise increase their power. As such, when comparing weapons, it is often useful to examine graphs of their dps across a wide range values for `D`. The traditional way to view such graphs is to type a formula for each weapon of interest into a spreadsheet application, generate a number of rows within the range of interest, and employ a graphing utility built into the spreadsheet application to visually represent the generated data. To be honest, this is a perfectly fine way to compare weapons. After all, weapon damage calculation is a simple enough problem that the numerous disadvantages that come with using spreadsheets for serious problems mostly don't apply. That said, spreadsheets are tacky, and they do require a non-trivial amount of work to make even simple graphs. DDO Weapon Comparator aims to be an intuitive, easy-to-use tool that replaces spreadsheets in the generation of these graphs. Users can simply enter the properties of a weapon modified by character feats, enhancements, etc., click the "Add Plot" button, and immediately see a line representing that weapon in a graph. Multiple plots can be superimposed onto the same graph to quickly determine how different weapons compare at different values of `D`.

## Limitations
At this moment, DDO Weapon Comparator does not take into account a character's melee/ranged power, which may have a significant impact on weapon superiority. This will be fixed in a future patch. Furthermore, dps comparisons are made in terms of damage per strike, not damage per second, so differences in attack speed/doublestrike/doubleshot from weapon to weapon are ignored, and damage per second calculations between different combat styles (e.g. THF vs Inquisitive) are not possible.

## Getting Started
### As a User
If you aren't interested in developing the project, you can simply install it with pip. Do note that you'll need to have Python version 3.8.0 or higher, and you may need to upgrade your pip installation before installing the project. Since this project is an application and not a library, a global installation may actually be preferable to an isolated (virtual environment) installation, but if you find that you need elevated privileges to install the application, then a virtual environment is still recommended.
<details><summary>How to create and enter a virtual environment</summary>

<details><summary>On Linux</summary>

```
python3.8 -m venv ddoweapons
source ddoweapons/bin/activate
```
</details>

<details><summary>On Windows</summary>

```
python -m venv ddoweapons
ddoweapons\scripts\activate
```
</details>

</details>

To install the application, just run
```
pip install --upgrade pip
pip install https://github.com/DSquizzle/ddo-weapon-comparator/archive/users.zip
```
Once the project has been installed, you can run it from the command line. If the application was installed in a virtual environment, then the virtual environment must be active for the command to work.
```
ddoweapons
```
### As a Developer
Make sure you have the prerequisites installed. As for all Python projects, it is recommended that you work inside of a virtual environment. If you aren't familiar with virtual environments, [read up!](https://realpython.com/python-virtual-environments-a-primer/)
```
python3 -m venv ddoweapons
source ddoweapons/bin/activate
pip install --upgrade pip
pip install matplotlib
pip install pyqt5
```
You are now ready to clone the repository
```
git clone https://github.com/DSquizzle/ddo-weapon-comparator
cd ddo-weapon-comparator
```
Finally, you can install and run the application
```
pip install -e .
ddoweapons
```

## Known Bugs
* It is possible to add a plot for an existing weapon and change the name of the weapon rendering the original plot unremovable
* The GUI layout can be very ugly when the window is maximized on large screens

## Built With
* [Matplotlib](https://matplotlib.org/)
* [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)

## Authors
* Danish Roshan

## License
This project is licensed under the MIT License - see the LICENSE file for details
