import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Player:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atk_low = atk - 10
        self.atk_high = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Use Magic", "Use Item(s)"]

    def generate_damage(self):
        return random.randrange(self.atk_low, self.atk_high)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1

        print("\n" + bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "ACTIONS:" + bcolors.ENDC)
        for item in self.actions:
            print("    " + str(i) + ".", item)
            i += 1

    def choose_spell(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "SPELLS:" + bcolors.ENDC)
        for spell in self.magic:
            print("    " + str(i) + ".", spell.name, "(Cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("    " + str(i) + ".", item["Item"].name + ":", item["Item"].description, "(x" + str(item["Quantity"]) + ")")
            i += 1

    def get_stats(self):
        hp_bar = ""
        hp_ticks = (self.hp / self.max_hp) * 100 / 4

        mp_bar = ""
        mp_ticks = (self.mp / self.max_mp) * 100 / 10

        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.max_hp)
        current_hp = ""

        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)

            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.max_mp)
        current_mp = ""

        if len(mp_string) < 7:
            decreased = 7 - len(mp_string)

            while decreased > 0:
                current_mp += " "
                decreased -= 1

            current_mp += mp_string
        else:
            current_mp = mp_string

        '''I noticed that depending on the length of the player's name, it would have an effect on the HP bars and how 
        they lined up. So I added this to adjusted for the longest name "All Might" which is 9 characters long. 
        However, this does mean that this would need to be changed when the longer of the names is changed.'''
        if len(self.name) < 9:
            while len(self.name) < 9:
                self.name += " "


        print(bcolors.BOLD + self.name + "    "+
              current_hp + bcolors.OKGREEN + " " + hp_bar + bcolors.ENDC + " " + bcolors.BOLD
              + current_mp + " " + bcolors.OKBLUE + mp_bar  + bcolors.ENDC)

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("    " + str(i) + ".", enemy.name)
                i += 1
        choice = int(input("Choose Target: ")) - 1
        return choice

    def get_enemy_stats(self):
        hp_bar = ""
        hp_ticks = (self.hp / self.max_hp) * 100 / 2

        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.max_hp)
        current_hp = ""

        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)

            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        '''I noticed that depending on the length of the player's name, it would have an effect on the HP bars and how 
        they lined up. So I added this to adjusted for the longest name "Spinner" which is 7 characters. However, this 
        does mean that this would need to be changed when the longer of the names is changed.'''
        if len(self.name) < 7:
            while len(self.name) < 7:
                self.name += " "

        print(bcolors.BOLD + self.name + "      " +
          current_hp + " " + bcolors.FAIL + hp_bar + bcolors.ENDC)

    def choose_enemy_spell(self):
        # Choses a random spell between 0 and x, the length of the magic list
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        pct = self.hp / self.max_hp * 100

        if self.mp < spell.cost or spell.type == "Light" and pct > 50:
            self.choose_enemy_spell()
        else:
            return spell, magic_dmg