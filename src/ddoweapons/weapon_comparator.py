class float(float):
    """
    Override the built-in float type to add an averageDamage method. Basically
    just adding some polymorphism for duck typing
    """
    def averageDamage(self):
        return self


class Weapon:
    """
    Represents a weapon
    """
    def __init__(self, name, enhancementBonus, weaponDiceMultiplier,
                 baseDamageDice, critProfile, onHit):

        self.name = name
        self.enhancementBonus = int(enhancementBonus)
        self.weaponDiceMultiplier = float(weaponDiceMultiplier)
        self.baseDamageDice = DamageExpression(baseDamageDice)
        self.critProfile = CritProfile(critProfile)
        self.onHit = DamageExpression(onHit)

    def averageDamage(self, deadly):
        """
        Returns the average damage for the weapon
        """
        return ((self.weaponDiceMultiplier *
            self.baseDamageDice.averageDamage() + self.enhancementBonus +
            deadly) * (self.critProfile.effectiveHits() / 19) +
            self.onHit.averageDamage())


class DamageExpression:
    """
    Represents a sum of DamageDice and float objects
    """
    def __init__(self, string):
        self.summands = []
        summands = string.split('+')
        for summand in summands:
            self.summands.append(DamageDice(summand)
                                 if 'd' in summand else float(summand))

    def __str__(self):
        return ' + '.join([str(summand) for summand in self.summands])

    def averageDamage(self):
        """
        Returns the average damage for the expression
        """
        return sum(summand.averageDamage() for summand in self.summands)


class DamageDice:
    """
    Represents a damage dice expression of the form XdY where damage is
    calculated by rolling X Y-sided dice
    """
    def __init__(self, string):
        arr = string.split('d')
        self.diceNum = int(arr[0]) if arr[0] else 1
        self.dieSize = int(arr[1]) if arr[1] else 0

    def __str__(self):
        return str(self.diceNum) + 'd' + str(self.dieSize)

    def averageDamage(self):
        """
        Returns the average damage for the expression
        """
        return self.diceNum * (self.dieSize + 1) / 2


class CritProfile:
    """
    Represents a critical profile of the form P-QxM, where any attack rolls
    greater than or equal to P represent critical threats, and M is the
    critical multiplier
    """
    def __init__(self, string):
        arr = string.split('x')
        critMinMax = arr[0].split('-')
        self.numOfCrits = 1 + int(critMinMax[1]) - int(critMinMax[0])
        self.numOfHits = 19 - self.numOfCrits
        self.multiplier = int(arr[1])

    def __str__(self):
        return (str(21 - self.numOfCrits) + '-' +
                '20' + 'x' + str(self.multiplier))

    def effectiveHits(self):
        """
        A crit is essentially the same as M non-crits, except that on-hit
        effects are only applied once. Effective hits is the number of
        non-crits plus the number of crits times the critical multiplier to get
        the average number of effective hits you would get from a weapon after
        rolling every possible attack value from 1-20 exactly once
        """
        return self.numOfHits + self.numOfCrits * self.multiplier
