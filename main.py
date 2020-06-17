from game import Player, bcolors
from magic import Spell
from  inventory import Item
import random

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY APPEARS!" + bcolors.ENDC)


###Spells###
#Dark Spells
meteor = Spell("Meteor Strike", 20, 50, "Dark")
typhoon = Spell("Typhoon Strike", 25, 55, "Dark")
lighting = Spell("Lightning Strike", 50, 70, "Dark")
ultra = Spell("PLUS ULTRA", 100, 100, "Dark")
#Light Spells
cure = Spell("Cure", 10, 15, "Light")
cure_p = Spell("Cure +", 15, 20, "Light")

player1_spells = [meteor, typhoon, lighting, ultra, cure, cure_p]
enemy_spells = [meteor, lighting, cure]


###Items###
#Health Potions
red_potion = Item("Red Potion", "Potion", "Heals 10 HP", 10)
orange_potion = Item("Orange Potion", "Potion", "Heals 25 HP", 25)
white_potion = Item("White Potion", "Potion", "Heals 50 HP", 50)
#Mana Potions
blue_potion = Item("Blue Potion", "Potion", "Heals 10 MP", 10)
big_blue_potion = Item("Big Blue Potion", "Potion", "Heals 50 MP", 50)
#Elixirs
purple_elixir = Item("Purple Elixir", "Elixir", "Fully restores HP/MP of one party member", 999)
big_purple_elixir = Item("Big Purple Elixir", "Elixir", "Fully restores parties HP/MP", 999)
#Throwing Stars
shuriken = Item("Shuriken", "Throwing Star", "Throw a shuriken dealing 80 damage", 80)

player1_items = [{"Item": red_potion, "Quantity": 10},{"Item": orange_potion, "Quantity": 5},
                 {"Item": white_potion, "Quantity": 5},{"Item": blue_potion, "Quantity": 5},
                 {"Item": big_blue_potion, "Quantity": 5},{"Item": purple_elixir, "Quantity": 1},
                 {"Item": big_purple_elixir, "Quantity": 1},{"Item": shuriken, "Quantity": 3}]


###Player & Enemy###
#Instantiate Players
player1 = Player("Deku", 1000, 200, 1000, 100, player1_spells, player1_items)
player2 = Player("Todoroki", 1000, 200, 125, 125, player1_spells, player1_items)
player3 = Player("All-Might", 1000, 200, 200, 200, player1_spells, player1_items)
#Instantiate Enemies
enemy1 = Player("Stain", 2500, 200, 100, 100, enemy_spells, [])
enemy2 = Player("Spinner", 1000, 200, 50, 50, enemy_spells, [])


players = [player1, player2, player3]
enemies = [enemy1, enemy2]

running = True

while running:
    print("=========================")

    print("\n")
    print("NAME                 HP                                     MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("Choose Action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            chosen_enemy = player.choose_target(enemies)


            enemies[chosen_enemy].take_damage(dmg)
            print("\n" + player.name.replace(" ", "") + " attacked " + enemies[chosen_enemy].name.replace(" ", "") + " for", dmg, "points of damage.")

            if enemies[chosen_enemy].get_hp() == 0:
                print(enemies[chosen_enemy].name.replace(" ", "") + " has fallen.")
                del enemies[chosen_enemy]
        elif index == 1:
            print("-------------------------")
            player.choose_spell()
            print("    " + bcolors.FAIL + "0. Go Back" + bcolors.ENDC)
            spell_choice = int(input("Choose Spell:")) - 1

            if spell_choice == -1:
                continue

            spell = player.magic[spell_choice]
            magic_dmg = spell.generate_damage()
            chosen_enemy = player.choose_target(enemies)
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nYou do not have sufficient mana.\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "Light" and player.hp is not 100:
                player.heal(spell.damage)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(spell.damage), "HP." + bcolors.ENDC)
            elif spell.type == "Light" and player.hp is 100:
                print("\n" + bcolors.FAIL + "You're full health" + bcolors.ENDC)
                continue
            elif spell.type == "Dark":
                enemies[chosen_enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg) + " points of damage to", enemies[chosen_enemy].name.replace(" ", ""),  bcolors.ENDC)

                if enemies[chosen_enemy].get_hp() == 0:
                    print(enemies[chosen_enemy].name.replace(" ", "") + " has fallen.")
                    del enemies[chosen_enemy]

        elif index == 2:
            print("-------------------------")
            player.choose_item()
            print("    " + bcolors.FAIL + "0. Go Back" + bcolors.ENDC)
            item_choice = int(input("Choose Item: ")) - 1

            item = player.items[item_choice]["Item"]
            if player.items[item_choice]["Quantity"] == 0:
                print(bcolors.FAIL + "\n"  + "You do not have anymore", item.name + "(s).", "\n" + bcolors.ENDC)
                continue

            #Reduces quantity of item used
            player.items[item_choice]["Quantity"] -= 1

            if item_choice == -1:
                continue

            if item.type == "Potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals ", player.name.replace(" ", ""),"for ", str(item.prop), "HP" + bcolors.ENDC)

            elif item.type == "Elixir":

                if item.name == "Big Purple Elixir":
                    for i in players:
                        i.hp = i.max_hp
                        i.mp = i.max_mp
                else:
                    player.hp = player.max_hp
                    player.mp = player.max_mp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores your HP/MP." + bcolors.ENDC)

            elif item.type == "Throwing Star":
                chosen_enemy = player.choose_target(enemies)
                enemies[chosen_enemy].take_damage(item.prop)
                print(bcolors.OKBLUE + "\n" + player.name.replace(" ", "") + " used "+ item.name + " it deals", str(item.prop), "points of damage to",
                      enemies[chosen_enemy].name, bcolors.ENDC)

                if enemies[chosen_enemy].get_hp() == 0:
                    print(enemies[chosen_enemy].name.replace(" ", "") + " has fallen.")
                    del enemies[chosen_enemy]

        elif index!=0 and index!=1 and index!=2:
            print("\n" + bcolors.FAIL + "You seemed to have entered a bad number :(. You entered:", choice + ".",
                  "Your choices are '1', '2', or '3'."+ bcolors.ENDC)
            continue

    #Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    #Check if Player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "THE ENEMIES HAVE BEEN SLAIN!" + bcolors.ENDC)
        running = False
    #Check if Enemy won
    elif defeated_players == 3:
        print(bcolors.FAIL + "YOUR TEAM HAS BEEN SLAIN" + bcolors.ENDC)
        running = False
    #TIE?
    elif defeated_players == 3 and defeated_enemies == 2:
        print(bcolors.FAIL + "???")
        running = False

    '''
    if len(enemies) == 0:
        print(bcolors.OKGREEN + "THE ENEMIES HAVE BEEN SLAIN!" + bcolors.ENDC)
        running = False
    elif len(players) == 0:
        print(bcolors.FAIL + "YOUR TEAM HAS BEEN SLAIN" + bcolors.ENDC)
        running = False
    print("\n")
    '''

    #Enemy Attack Phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + enemy.name.replace(" ", "") + " attacked " +
                  players[target].name.replace(" ", "") + " for", enemy_dmg, "points of damage." + bcolors.ENDC)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "Light" and enemy.hp is not 100:
                enemy.heal(spell.damage)
                print(bcolors.OKBLUE + spell.name + " heals ", enemy.name.replace(" ",""), " for ", str(spell.damage), "HP." + bcolors.ENDC)
            elif spell.type == "Dark":

                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + enemy.name.replace(" ", "") + "'s " + spell.name + " deals " + str(magic_dmg)
                      + " points of damage to", players[target].name.replace(" ", ""),  bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has fallen.")
                    del players[target]