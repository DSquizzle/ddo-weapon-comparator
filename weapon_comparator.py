import matplotlib
from matplotlib import pyplot
import os.path

matplotlib.use('Qt5Agg')

TEXT_GREEN = '\033[32m'
ENDC = '\033[m'

class float(float):
    def averageDamage(self):
        return self

class Weapon:
    def __init__(self, name, weaponDiceMultiplier,
                 damageDice, critProfile, onHit):

        self.name = name
        self.weaponDiceMultiplier = float(weaponDiceMultiplier)
        self.damageDice = DamageDice(damageDice)
        self.critProfile = CritProfile(critProfile)
        self.onHit = DamageDice(onHit)

    def averageDamage(self, deadly):
        return ((self.weaponDiceMultiplier * self.damageDice.averageDamage() + deadly) * (self.critProfile.effectiveHits() / 19) + getattr(self.onHit, 'averageDamage', lambda: self.onHit)())


class DamageExpression:
    def __init__(self, string):
        self.summands = []
        summands = string.split('+')
        for summand in summands:
            self.summands.append(DamageDice(summand) if 'd' in summand else float(summand))

    def __str__(self):
        return ' + '.join([str(summand) for summand in self.summands])

    def averageDamage(self):
        return sum(summand.averageDamage() for summand in self.summands)


class DamageDice:
    def __init__(self, string):
        arr = string.split('d')
        self.diceNum = int(arr[0]) if arr[0] else 1
        self.dieSize = int(arr[1]) if arr[1] else 0

    def __str__(self):
        return str(self.diceNum) + 'd' + str(self.dieSize)

    def averageDamage(self):
        return self.diceNum * (self.dieSize + 1) / 2


class CritProfile:
    def __init__(self, string):
        arr = string.split('x')
        critMinMax = arr[0].split('-')
        self.numOfCrits = 1 + int(critMinMax[1]) - int(critMinMax[0])
        self.numOfHits = 19 - self.numOfCrits
        self.multiplier = int(arr[1])

    def __str__(self):
        return str(21 - self.numOfCrits) + '-' + '20' + 'x' + str(self.multiplier)

    def effectiveHits(self):
        return self.numOfHits + self.numOfCrits * self.multiplier


def safeInput(string, returnfunc):
    while True:
        try:
            return returnfunc(input(string))
        except KeyboardInterrupt as e:
            print()
            raise(e)
        except:
            print("Uh oh. Your answer appears to be formatted incorrectly. " +
                  "Please try again")


def ret(anything):
    return anything


def buildWeapons():
    weaponName = safeInput("Enter the name of your weapon: ", ret)
    multiplier = safeInput("How many W's does your weapon have? " +
                           "(Numeric values only): ", float)
    damageDice = safeInput("What is your weapon's damage dice? " +
                           "Please format this value as " +
                           TEXT_GREEN + "n" + ENDC + "d" +
                           TEXT_GREEN + "m" + ENDC +
                           " (e.g. a normal greatsword is 2d6): ", DamageDice)
    critProfile = safeInput("What is your weapon's crit profile? " +
                            "Please format this value as " +
                            TEXT_GREEN + "n" + ENDC + "-" +
                            TEXT_GREEN + "m" + ENDC +
                            "x" + TEXT_GREEN + "p" + ENDC +
                            " (e.g. a normal greatsword is 19-20x2): ",
                            CritProfile)
    onHit = safeInput("What is your weapon's on-hit damage? " +
                      "Please format this value as " +
                      TEXT_GREEN + "n" + ENDC + "d" +
                      TEXT_GREEN + "m" + ENDC +
                      " (e.g. 4d6), or leave blank if your weapon deals no " +
                      "on-hit damage. ", lambda x: DamageDice(x) if x else 0)
    return Weapon(weaponName, multiplier, damageDice, critProfile, onHit)


if __name__ == '__main__':
    buildAnother = 'y'
    weapons = []
    print("Let's make a graph! " +
          "This is a toy program to compare weapons in DDO")
    while buildAnother == 'y':
        try:
            weapons.append(buildWeapons())
            buildAnother = safeInput("Would you like to add another weapon " +
                                     "to the graph? (y/n) ", ret)
        except KeyboardInterrupt:
            buildAnother = safeInput("Would you like to add another weapon " +
                                     "to the graph? (y/n) ", ret)

    minDeadly = safeInput("What is the least amount of deadly you care to " +
                          "see in the graph (Numeric values only) ", int)
    maxDeadly = safeInput("What is the most amount of deadly you care to " +
                          "see in the graph (Numeric values only) ", int)
    deadlyRange = range(minDeadly, maxDeadly + 1)

    for weapon in weapons:
        pyplot.plot(deadlyRange, [weapon.averageDamage(deadly) for
                    deadly in deadlyRange],
                    label=weapon.name)

    pyplot.legend()
    saveName = safeInput("What would you like to name this graph? ", ret)
    pyplot.savefig(saveName)
    print(f"Saved graph to {os.path.dirname(os.path.abspath(__file__))}" +
          f"/{saveName}.png")
else:
    sos = Weapon('Sword of Shadow', 1, '2d6',
                 '15-20x5', '0d0')
    br = Weapon('Echo of Blackrazor', 1, '2d6',
                '17-20x4', '3d6')
