# OLD VERSION OF THE SIMULATOR, MAYBE GOOD TO KEEP FOR THE FUNCTIONS WRITTEN?

import random
import math

def calculate_effective_attack_level(attack_level, attack_level_boost, accurate_style=True):
    
    effective_attack_level = math.floor((attack_level + attack_level_boost) * 1.20)

    if accurate_style:
        effective_attack_level += 11
    else:
        effective_attack_level += 8
    
    effective_attack_level = math.floor(effective_attack_level)
    print("Effective attack level:", effective_attack_level)
    return effective_attack_level


def calculate_attack_roll(effective_attack_level, equipment_attack_bonus):
    attack_roll = math.floor(effective_attack_level * (equipment_attack_bonus + 64))
    return attack_roll

def calculate_defence_roll(target_defence_level, target_style_defence_bonus):
    defence_roll = (target_defence_level + 9) * (target_style_defence_bonus + 64)
    return defence_roll


def calc_successful_hit(attack_roll, defence_roll, maximum_hit):
    random_attack_roll = random.randint(0, attack_roll)
    random_defence_roll = random.randint(0, defence_roll)

    if random_attack_roll > random_defence_roll:
        random_hit_roll = random.randint(0, maximum_hit)
        return random_hit_roll
    else:
        return 0

def scythe_swing(attack_roll, defence_roll, maximum_hit):
    global boss_hp

    # roll first hit, full max hit
    attack = calc_successful_hit(attack_roll, defence_roll, maximum_hit)
    boss_hp -= min(attack, boss_hp)
    
    # roll second hit, 50% of max hit
    attack = calc_successful_hit(attack_roll, defence_roll, maximum_hit / 2)
    boss_hp -= min(attack, boss_hp)
    
    # roll third hit, 25% of max hit
    attack = calc_successful_hit(attack_roll, defence_roll, maximum_hit / 4)
    boss_hp -= min(attack, boss_hp)


def dragon_warhammer_spec(attack_roll, defence_roll, maximum_hit):
    global defence_level, boss_hp, first_spec, second_spec_missed

    if first_spec is None:
        random_hit_roll = random.randint(0, maximum_hit)
        boss_hp -= random_hit_roll

        defence_reduction = defence_level * 0.3
        defence_level = math.floor(defence_level - defence_reduction)

        first_spec = True

    else:
        second_dwh_spec = calc_successful_hit(attack_roll, defence_roll, maximum_hit)

        if second_dwh_spec > 0:
            print("Second spec hits")
            boss_hp -= second_dwh_spec

            defence_reduction = defence_level * 0.3
            defence_level = math.floor(defence_level - defence_reduction)
        else:
            print("Second spec misses, leaving raid \n")
            second_spec_missed = True
            
    return defence_level

def taste_vengeance(enemy_maximum_hit, player_hp):
    global boss_hp

    # venge reflects 75% of damage taken
    random_hit_roll = random.randint(1, enemy_maximum_hit)
    vengeance_damage = math.floor(random_hit_roll * 0.75)
    print("Taste vengeance! Boss was hit for", vengeance_damage)

    boss_hp -= vengeance_damage
    player_hp = player_hp - random_hit_roll

    return damage_hit

def check_boss_death():
    global boss_hp, boss_kills

    if boss_hp == 0:
        boss_kills += 1
        # add other stuff here to do more with the data for simmming
        (print("Boss killed! \n"))
        return True
    return False


def anvil_healing():
    global boss_hp

    random_cycle_roll = random.randint(3,6)
    boss_hp += (random_cycle_roll * 5)
    print("boss healed for:",(random_cycle_roll * 5))

def check_second_spec():
    global second_spec_missed

    if second_spec_missed:
        return True

# global variables
defence_level = 246
damage_hit = 0
boss_hp = 450

original_boss_hp = 450
original_defence_level = 246

enemy_maximum_hit = 87
player_hp = 121
dwh_maximum_hit = 79
scythe_maximum_hit = 48

# weapons
# 2nd dwh spec
dwh_attack_roll = calculate_attack_roll(155, 155)

# bf / bellator, scythe on aggressive
# scythe_attack_roll = calculate_attack_roll(152, 162)

# tort / bellator, scythe on accurate
scythe_attack_roll = calculate_attack_roll(152, 167)

def simulate_tekton():
    global boss_hp, first_spec, second_spec_missed

    first_spec = None
    second_spec_missed = False

    dwh_maximum_hit = 79
    scythe_maximum_hit = 48

    # 1st phase of tekton
    tekton_crush_defence_roll = calculate_defence_roll(defence_level, 105)
    tekton_slash_defence_roll = calculate_defence_roll(defence_level, 165)

    dragon_warhammer_spec(dwh_attack_roll, tekton_crush_defence_roll, dwh_maximum_hit)
    # set warhammer to accurate
    dwh_maximum_hit = 78

    # guarentee two hammers to land, for simulation purposes
    first_spec = None
    dragon_warhammer_spec(dwh_attack_roll, tekton_crush_defence_roll, dwh_maximum_hit)

    if second_spec_missed:
        return

    for _ in range(5):
        scythe_swing(scythe_attack_roll, tekton_slash_defence_roll, scythe_maximum_hit)

        if check_boss_death():
            return

    print("Hp left:", boss_hp)
    print(f"Hp % left after first anvil:{boss_hp/original_boss_hp * 100:.2f} %")

    # 2nd phase of tekton, heals slightly, becomes enraged (higher defence for a period of time)
    anvil_healing()
    tekton_slash_defence_roll = calculate_defence_roll(defence_level, 290)

    scythe_swing(scythe_attack_roll, tekton_slash_defence_roll, scythe_maximum_hit)
    taste_vengeance(enemy_maximum_hit, player_hp)

    for _ in range(3):
        scythe_swing(scythe_attack_roll, tekton_slash_defence_roll, scythe_maximum_hit)

        if check_boss_death():
            return

    # returns to non-enraged form
    tekton_slash_defence_roll = calculate_defence_roll(defence_level, 165)

    for _ in range(7):
        scythe_swing(scythe_attack_roll, tekton_slash_defence_roll, scythe_maximum_hit)

        if check_boss_death():
            return

    print("Hp left:", boss_hp)
    print(f"hp % left: {boss_hp/original_boss_hp * 100:.2f} % \n")
    # if hp left then FAIL



def simulate_tekton_after_anvil():
    global boss_hp, first_spec, second_spec_missed, boss_kills

    # sim that 2 hammers landed
    defence_level = 120

    # 2nd phase
    anvil_healing()

    tekton_slash_defence_roll = calculate_defence_roll(defence_level, 290)

    scythe_swing(scythe_attack_roll, tekton_slash_defence_roll, scythe_maximum_hit)
    taste_vengeance(enemy_maximum_hit, player_hp)

    for _ in range(3):
        scythe_swing(scythe_attack_roll, tekton_slash_defence_roll, scythe_maximum_hit)

        if check_boss_death():
            return

    # returns to non-enraged form
    tekton_slash_defence_roll = calculate_defence_roll(defence_level, 165)

    for _ in range(7):
        scythe_swing(scythe_attack_roll, tekton_slash_defence_roll, scythe_maximum_hit)

        if check_boss_death():
            return

    print("Hp left:", boss_hp)
    print(f"hp % left: {boss_hp/original_boss_hp * 100:.2f} % \n")


# simulation stuff
# boss_kills = 0
# num_simulations = 1000

# for i in range(num_simulations):
#     # reset variables 
#     boss_hp = original_boss_hp
#     defence_level = original_defence_level

#     simulate_tekton()

# print("Simulation for tekton at 60% (270hp)")
# print(f"Total boss kills in {num_simulations} simulations: {boss_kills}")



# Set the range of percentages you want to simulate (e.g., from 50% to 60%)
# start_percentage = 50
# end_percentage = 60
# percentage_step = 1

# # Dictionary to store results
# results = {}

# for current_percentage in range(start_percentage, end_percentage + 1, percentage_step):
#     # Reset variables
#     boss_hp = original_boss_hp
#     defence_level = original_defence_level

#     # Set boss HP based on current percentage
#     boss_hp = int(original_boss_hp * (current_percentage / 100))

#     # Run the simulation
#     simulate_tekton_after_anvil()

#     # Update results
#     results[current_percentage] = boss_kills

# # Print results
# print("Simulation for tekton at different percentages:")
# for percentage, kills in results.items():
#     print(f"{percentage}% HP: {kills} kills out of {num_simulations}")



# Set the range of HP values you want to simulate (e.g., from 225 to 270)
start_hp = 180
end_hp = 180
hp_step = 1
num_simulations_per_hp = 10

# Dictionary to store results
results = {}

for current_hp in range(start_hp, end_hp + 1, hp_step):
    # Initialize total kills for the current HP value
    total_kills = 0
    boss_kills = 0 

    for _ in range(num_simulations_per_hp):
        print(current_hp)
        # Reset variables
        boss_hp = current_hp
        defence_level = original_defence_level

        simulate_tekton_after_anvil()

        total_kills += boss_kills

    # Calculate average kills for the current HP value
    chance_to_kill = ( boss_kills / num_simulations_per_hp )

    # Update results
    results[current_hp] = chance_to_kill
 

print("Simulation for tekton at different HP values:")

for hp, chance_to_kill in results.items():


    print("Average kill per simulation:", chance_to_kill)

    percentage_chance_to_kill = results[hp] * 100

    print(f"{hp} HP: {chance_to_kill:.2f} average kills out of {num_simulations_per_hp} simulations "f"({percentage_chance_to_kill:.2f}% chance)\n")












# def calculate_hit_chance(attack_roll, defence_roll):
#     if attack_roll > defence_roll:
#         hit_chance = 1 - ((defence_roll + 2) / (2 * (attack_roll + 1)))
#     else:
#         hit_chance = attack_roll / (2 * (defence_roll + 1))

#     print(hit_chance)
#     return hit_chance

# def calculate_average_melee_damage(maximum_hit, hit_chance):
#     average_melee_damage = (maximum_hit * hit_chance) / 2
#     print(average_melee_damage)
#     return average_melee_damage
