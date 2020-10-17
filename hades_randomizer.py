'''
Running this Python file will present you with a randomized set of rules (mirror options, keepsakes, weapon type, pacts) for the game Hades

This program was mostly just a fun project to do on a lazy afternoon. The code was written by some friends and I, whom you can find at:
https://github.com/sqrtroot
https://github.com/ManDeJan
https://github.com/Druyv

To run the randomiser, either download the file and run it using Python, or visit https://repl.it/@nickgoris/Hades-Randomizer to run it in an online shell
'''

from dataclasses import dataclass
from random import choice,randint
import os

companions = ["Battie", "Mort", "Shady", "Rib", "Fidi", "Antos"]

infernal_arms = {
  "Stygius":["Zagreus","Nemesis","Poseidon","Arthur"], 
  "Varatha":["Zagreus","Achilles","Hades","Guan Yu"], 
  "Aegis":["Zagreus","Chaos","Zeus","Beowulf"], 
  "Coronacht":["Zagreus","Chiron","Hera","Rama"], 
  "Malphon":["Zagreus","Talos","Demeter","Gilgamesh"], 
  "Exagryph":["Zagreus","Eris","Hestia","Lucifer"] 
  }

keepsakes = ["Old Spiked Collar","Myrmidon Bracer","Black Shawl","Butterfly","Bone Hourglass","Chthonic Coin Purse","Skull Earring","Distant Memory","Harpy Feather Duster","Lucky Tooth","Thunder Signet","Conch Shell","Owl Pendant","Eternal Rose","Blood-Filled Vial","Adamant Arrowhead","Overflowing Cup","Lambent Plume","Frostbitten Horn","Cosmic Egg","Shattered Shackle","Evergreen Acorn","Broken Spearpoint","Pom Blossom","Sigil of the Dead"]

floor = ["Tartarus", "Asphodel", "Elysium", "Styx"]

mirror = [
    ["Shadow Presence","Fiery Presence"],
    ["Chthonic Vitality", "Dark Regeneration"],
    ["Death Defiance", "Stubborn Defiance"],
    ["Greater Reflex", "Ruthless Reflex"],
    ["Boiling Blood", "Abyssal Blood"],
    ["Infernal Soul", "Stygian Soul"],
    ["Deep Pockets", "Golden Touch"],
    ["Thick Skin", "High Confidence"],
    ["Privileged Status", "Family Favourite"],
    ["Olympian Favour", "Dark Foresight"],
    ["God's Pride", "God's Legacy"],
    ["Fated Authority", "Fated Persuasion"]
]

pop = {
    'Hard Labor'           : [1, 2, 3, 4, 5],
    'Lasting Consequences' : [1, 2, 3, 4],
    'Convenience Fee'      : [1, 2],
    'Jury Summons'         : [1, 2, 3],
    'Extreme Measures'     : [1, 3, 6, 10],
    'Calisthenics Program' : [1, 2],
    'Benefits Package'     : [2, 5],
    'Middle Management'    : [2],
    'Underworld Customs'   : [2],
    'Forced Overtime'      : [3, 6],
    'Heightened Security'  : [1],
    'Routine Inspection'   : [2, 4, 6, 8],
    'Damage Control'       : [1, 2],
    'Approval Process'     : [2, 5],
    'Tight Deadline'       : [1, 3, 6]
}

clear = (lambda: os.system('cls')) if os.name == 'nt' else (lambda: os.system('clear')) if os.name == 'posix' else exit()

@dataclass
class Pact:
    name: str
    level: int

    def __repr__(self):
      return str(f'{self.name:20}(level {pop[self.name].index(self.level)+1}, heat {self.level})')

def make_pacts(name, levels):
    return [Pact(name, level) for level in levels]

pops = [subitem for item in map(lambda p: make_pacts(p,pop[p]), pop) for subitem in item]

heath = lambda l: sum(map(lambda e: e.level, l))

def generate_pacts(pacts, target, max_tries=100):
    if target:
        not_used = pacts
        choices = []
        tries = 0
        while tries < max_tries:
            try:
                c = choice(not_used)
                nextHeat = heath(choices + [c])
                if nextHeat < target:
                    choices += [c]
                    not_used = list(filter(lambda e: e.name != c.name and e.level+nextHeat <= target, not_used))
                elif nextHeat == target:
                    choices += [c]
                    return choices
            except IndexError:
                return choices
        raise Exception("failed after max tries")
    return []

# def generate_pacts(pacts, target, max_tries=100):
#     if target:
#         choices = {}
#         tries = 0
#         current_heat = 0
#         while tries < max_tries:
#             c = choice(list(pacts))
#             if c not in choices:
#                 choices[c] = pacts[c][0]
#                 current_heat += pacts[c][0]
#             else:
#                 try:
#                     choices[c] = pacts[c][c.index(choices[c])+1]
#                     current_heat += pacts[c][c.index(choices[c])+1] - pacts[c][c.index(choices[c])]
#                 except:
#                     tries+=1
#             if current_heat == target:
#                 return choices, current_heat
#         return choices,current_heat



def pick_keepsakes(different=True,keepsakes=keepsakes,floors=floor):
    dct = {floor:None for floor in floors}
    used_keepsakes = []
    if different:
        for floor in dct:
            ks = choice(keepsakes)
            while ks in used_keepsakes and ks != used_keepsakes[-1]:
                ks = choice(keepsakes)
            dct[floor] = ks
            used_keepsakes.append(ks)
    else:
        dct = dict.fromkeys(dct,choice(keepsakes))
    return dct

    
settings = True
while(True):
    if settings:
        print("DISCLAIMER:\nForcing a very high heat may result in an actual lower heat. Feel free to simply up some categories to make up the difference.\n")
        max_heat = int(input("Max heat? "))
        max_heat = max_heat if max_heat <= 60 else 60

        print()
        
        rand_heat = bool(input("Force heat?\nPress enter to force max heat, type anything for random heat (lower than max heat) "))

        heat = randint(0,max_heat) if rand_heat else max_heat

        print()

        diff_k = bool(input("Different keepsakes?\nPress enter for same keepsake every floor, type anything for different keepsakes "))
        
        print()

        diff_c = bool(input("Different companions?\nPress enter for same companions every floor, type anything for different companions "))
        settings = False

    clear()

    print(f'Mirror upgrades:',*[choice(x) for x in mirror],'', sep='\n')

    weapon=choice(list(infernal_arms))
    print(f'Weapon:\n{weapon}({choice(infernal_arms[weapon])} aspect)\n')

    print(f'{"Different keepsakes:" if diff_k else "All same keepsakes: "}',*[f'{key:8}: {value}' for key,value in pick_keepsakes(diff_k).items()],sep='\n')
    
    print(f'\nChosen companion: {choice(companions)}')


    print()
    # pacts,c_heat = generate_pacts(pop,heat)
    # print(f'Pacts for heat {heat} (max heat was {max_heat}, actual heat is {c_heat}):')
    # print(*[f'{p:20}: {h}' for p,h in pacts.items()], sep='\n')
    pacts = generate_pacts(pops,heat)
    print(f'Pacts for heat {heat} (max heat was {max_heat}, actual heat is {sum(p.level for p in pacts)}):')
    print(*pacts, sep='\n')

    if(input("\n\nPress enter to run again with same settings, type anything for new settings ")):
        settings = True
    clear()