import random
import math
import matplotlib.pyplot as plt

class AttackCalculator:

    @staticmethod
    def calculate_effective_attack_level(attack_level, attack_level_boost, accurate_style=True):

        effective_attack_level = math.floor((attack_level + attack_level_boost) * 1.20)

        if accurate_style:

            effective_attack_level += 11

        else:

            effective_attack_level += 8
    
        effective_attack_level = math.floor(effective_attack_level)

        print("Effective attack level:", effective_attack_level)

        return effective_attack_level
    
    @staticmethod
    def calculate_attack_roll(effective_attack_level, equipment_attack_bonus):

        attack_roll = math.floor(effective_attack_level * (equipment_attack_bonus + 64))

        return attack_roll
    
    @staticmethod
    def calc_successful_hit(attack_roll, defence_roll, maximum_hit):

        random_attack_roll = random.randint(0, attack_roll)

        random_defence_roll = random.randint(0, defence_roll)

        if random_attack_roll > random_defence_roll:

            random_hit_roll = random.randint(0, maximum_hit)

            return random_hit_roll
        
        else:

            return 0
        

class DefenceCalculator:

    @staticmethod
    def calculate_defence_roll(target_defence_level, target_style_defence_bonus):

        defence_roll = (target_defence_level + 9) * (target_style_defence_bonus + 64)

        return defence_roll
    

class Scythe:
    def __init__(self, attack_roll=None, defence_roll=None, maximum_hit=None):
        self.attack_roll = attack_roll
        self.defence_roll = defence_roll
        self.maximum_hit = maximum_hit

    def swing(self, attack_roll, defence_roll, maximum_hit, boss_hp):
        # scythe hits with 3 attacks

        # full max hit
        attack = AttackCalculator.calc_successful_hit(attack_roll, defence_roll, maximum_hit)
        boss_hp -= min(attack, boss_hp)

        # 50% of max hit
        attack = AttackCalculator.calc_successful_hit(attack_roll, defence_roll, maximum_hit / 2)
        boss_hp -= min(attack, boss_hp)

        # 25% of max hit
        attack = AttackCalculator.calc_successful_hit(attack_roll, defence_roll, maximum_hit / 4)
        boss_hp -= min(attack, boss_hp)

        return boss_hp

class DragonWarhammer:
    def __init__(self, attack_roll=None, defence_roll=None, maximum_hit=None):
        self.attack_roll = attack_roll
        self.defence_roll = defence_roll
        self.maximum_hit = maximum_hit

    def spec(self, maximum_hit, boss_hp, defence_level):
        # guarenteed dwh spec landing, would need to just calc whether hit successful if to be used in other ways 

        attack = random.randint(0, maximum_hit)

        boss_hp -= attack

        defence_reduction = defence_level * 0.3

        defence_level -= math.floor(defence_reduction)

        return boss_hp, defence_level
    
    # use this for not guarenteed spec landing
    def spec2(self, maximum_hit, boss_hp, defence_level, attack_roll, tekton_crush_defence_roll):

        attack = AttackCalculator.calc_successful_hit(attack_roll, tekton_crush_defence_roll, maximum_hit)

        if attack > 0:
            boss_hp -= attack

            defence_reduction = defence_level * 0.3

            defence_level -= math.floor(defence_reduction)
            
        return boss_hp, defence_level


class Vengeance:
    def __init__(self, enemy_maximum_hit=None, player_hp=None):
        self.enemy_maximum_hit = enemy_maximum_hit
        self.player_hp = player_hp
     
    def taste_vengeance(self, enemy_maximum_hit, player_hp, boss_hp):
        # Venge reflects 75% of damage taken
        random_hit_roll = random.randint(1, enemy_maximum_hit)

        vengeance_damage = math.floor(random_hit_roll * 0.75)

        boss_hp -= vengeance_damage

        # player hp doesnt update correctly, not relevant when only tracking player damage vs boss
        self.player_hp = player_hp - random_hit_roll

        return boss_hp

        
class BossMechanics:
    def __init__(self):
        self.boss_kills = 0

    def check_boss_death(self, current_boss_hp):

        if current_boss_hp == 0:

            self.boss_kills += 1

            print("Boss killed!")
            
            return True
        
        return False

    def anvil_healing(self, boss_hp):

        random_cycle_roll = random.randint(3, 6)

        # heals for 5hp per cycle 
        boss_hp += (random_cycle_roll * 5)

        return boss_hp


class TektonSimulations:
    def __init__(self, dwh_attack_roll, scythe_attack_roll, enemy_maximum_hit, player_hp, original_boss_hp):
        self.dwh_attack_roll = dwh_attack_roll
        self.scythe_attack_roll = scythe_attack_roll
        self.enemy_maximum_hit = enemy_maximum_hit
        self.scythe_maximum_hit = 48
        self.dragon_warhammer_aggressive_max_hit = 79
        self.dragon_warhammer_accurate_max_hit = 78
        self.player_hp = player_hp
        self.original_boss_hp = original_boss_hp
        self.attack_calculator = AttackCalculator()
        self.defence_calculator = DefenceCalculator()
        self.boss_mechanics = BossMechanics()
        self.scythe = Scythe()
        self.vengeance = Vengeance()
        self.dragon_warhammer = DragonWarhammer()

    def simulate_tekton_after_anvil(self, initial_boss_hp):
        self.boss_hp = initial_boss_hp

        # set defence to 2dwh hitting
        self.defence_level = 120
        self.boss_kills = 0

        # 2nd phase
        self.boss_hp = self.boss_mechanics.anvil_healing(self.boss_hp)
    
        tekton_slash_defence_roll = self.defence_calculator.calculate_defence_roll(self.defence_level, 290)

        self.boss_hp = self.scythe.swing(self.scythe_attack_roll, tekton_slash_defence_roll, self.scythe_maximum_hit, self.boss_hp)
        
        self.boss_hp = self.vengeance.taste_vengeance(self.enemy_maximum_hit, self.player_hp, self.boss_hp)
        
        for _ in range(3):
            self.boss_hp = self.scythe.swing(self.scythe_attack_roll, tekton_slash_defence_roll, self.scythe_maximum_hit, self.boss_hp)

            if self.boss_mechanics.check_boss_death(self.boss_hp):
                self.boss_kills += 1
                return 

        # Returns to non-enraged form
        tekton_slash_defence_roll = self.defence_calculator.calculate_defence_roll(self.defence_level, 165)

        for _ in range(7):
            self.boss_hp = self.scythe.swing(self.scythe_attack_roll, tekton_slash_defence_roll, self.scythe_maximum_hit, self.boss_hp)

            if self.boss_mechanics.check_boss_death(self.boss_hp):
                self.boss_kills += 1
                return 
            
        print("Boss was not killed!")


    # this is for guarenteed 2 dwh
    def full_tekton_fight(self, original_boss_hp, original_defence_level):
        self.boss_hp = original_boss_hp
        self.defence_level = original_defence_level
        self.boss_kills = 0

        # 1st phase of tekton
        tekton_crush_defence_roll = DefenceCalculator.calculate_defence_roll(self.defence_level, 105)
        tekton_slash_defence_roll = DefenceCalculator.calculate_defence_roll(self.defence_level, 165)
        
        self.boss_hp, self.defence_level = self.dragon_warhammer.spec(self.dragon_warhammer_aggressive_max_hit, self.boss_hp, self.defence_level)
        self.boss_hp, self.defence_level = self.dragon_warhammer.spec(self.dragon_warhammer_accurate_max_hit, self.boss_hp, self.defence_level)
        
        for _ in range(5):
            self.boss_hp = self.scythe.swing(self.scythe_attack_roll, tekton_slash_defence_roll, self.scythe_maximum_hit, self.boss_hp)

            if self.boss_mechanics.check_boss_death(self.boss_hp):
                self.boss_kills += 1
                return

        # do something with this here so you can compare the likelihood to kill the boss at different values
        print("Hp left when returning to anvil:", self.boss_hp)
        print(f"Hp % left after first anvil: {self.boss_hp / original_boss_hp * 100:.2f} %")

        # 2nd phase
        self.boss_hp = self.boss_mechanics.anvil_healing(self.boss_hp)
    
        tekton_slash_defence_roll = self.defence_calculator.calculate_defence_roll(self.defence_level, 290)

        self.boss_hp = self.scythe.swing(self.scythe_attack_roll, tekton_slash_defence_roll, self.scythe_maximum_hit, self.boss_hp)
        
        self.boss_hp = self.vengeance.taste_vengeance(self.enemy_maximum_hit, self.player_hp, self.boss_hp)
        
        for _ in range(3):
            self.boss_hp = self.scythe.swing(self.scythe_attack_roll, tekton_slash_defence_roll, self.scythe_maximum_hit, self.boss_hp)

            if self.boss_mechanics.check_boss_death(self.boss_hp):
                self.boss_kills += 1
                return 

        # Returns to non-enraged form
        tekton_slash_defence_roll = self.defence_calculator.calculate_defence_roll(self.defence_level, 165)

        for _ in range(7):
            self.boss_hp = self.scythe.swing(self.scythe_attack_roll, tekton_slash_defence_roll, self.scythe_maximum_hit, self.boss_hp)

            if self.boss_mechanics.check_boss_death(self.boss_hp):
                self.boss_kills += 1
                return

        print("Boss was not killed!")

    # this version includes having to roll 2 dwh specs
    def full_tekton_fight_2_dwh(self, original_boss_hp, original_defence_level):
        self.boss_hp = original_boss_hp
        self.defence_level = original_defence_level
        self.boss_kills = 0

        # 1st phase of tekton
        tekton_crush_defence_roll = DefenceCalculator.calculate_defence_roll(self.defence_level, 105)
        tekton_slash_defence_roll = DefenceCalculator.calculate_defence_roll(self.defence_level, 165)
        dwh_attack_roll = AttackCalculator.calculate_attack_roll(self.dwh_attack_roll, 180)
        
        # first spec guarenteed
        self.boss_hp, self.defence_level = self.dragon_warhammer.spec(self.dragon_warhammer_aggressive_max_hit, self.boss_hp, self.defence_level)
        
        # 2nd spec not guarenteed, so use other dwh method
        self.boss_hp, self.defence_level = self.dragon_warhammer.spec2(self.dragon_warhammer_accurate_max_hit, self.boss_hp, self.defence_level, dwh_attack_roll, tekton_crush_defence_roll)

        if self.defence_level >= 170:
            print("2nd dwh didn't hit, leave raid")
            return

        for _ in range(5):
            self.boss_hp = self.scythe.swing(self.scythe_attack_roll, tekton_slash_defence_roll, self.scythe_maximum_hit, self.boss_hp)

            if self.boss_mechanics.check_boss_death(self.boss_hp):
                self.boss_kills += 1
                return

        # do something with this here so you can compare the likelihood to kill the boss at different values
        print("Hp left when returning to anvil:", self.boss_hp)
        print(f"Hp % left after first anvil: {self.boss_hp / original_boss_hp * 100:.2f} %")

        # 2nd phase
        self.boss_hp = self.boss_mechanics.anvil_healing(self.boss_hp)
    
        tekton_slash_defence_roll = self.defence_calculator.calculate_defence_roll(self.defence_level, 290)

        self.boss_hp = self.scythe.swing(self.scythe_attack_roll, tekton_slash_defence_roll, self.scythe_maximum_hit, self.boss_hp)
        
        self.boss_hp = self.vengeance.taste_vengeance(self.enemy_maximum_hit, self.player_hp, self.boss_hp)
        
        for _ in range(3):
            self.boss_hp = self.scythe.swing(self.scythe_attack_roll, tekton_slash_defence_roll, self.scythe_maximum_hit, self.boss_hp)

            if self.boss_mechanics.check_boss_death(self.boss_hp):
                self.boss_kills += 1
                return 

        # Returns to non-enraged form
        tekton_slash_defence_roll = self.defence_calculator.calculate_defence_roll(self.defence_level, 165)

        for _ in range(7):
            self.boss_hp = self.scythe.swing(self.scythe_attack_roll, tekton_slash_defence_roll, self.scythe_maximum_hit, self.boss_hp)

            if self.boss_mechanics.check_boss_death(self.boss_hp):
                self.boss_kills += 1
                return

        print("Boss was not killed!")


    # could this become a class so you can reuse it?
    def run_simulations(self, start_hp, end_hp, hp_step, num_simulations_per_hp, buffed=True):
        results = {}

        for current_hp in range(start_hp, end_hp + 1, hp_step):
            boss_kills = 0

            for _ in range(num_simulations_per_hp):
                print("Running sim at:", current_hp, "hp")

                self.simulate_tekton_after_anvil(current_hp)

                boss_kills += tekton_simulator.boss_kills

                print("-" * 30)

            chance_to_kill = boss_kills / num_simulations_per_hp
            results[current_hp] = chance_to_kill

        print(f"{num_simulations_per_hp} Simulations for {'post' if buffed else 'pre'} buff scythe {'post' if buffed else 'pre'} anvil tekton at different HP values:")
        print(results)

        return results
        

class Plotter:
    def __init__(self):
        pass

    def plot_results(self, results1, results2):
        hp_values1, chance_to_kill1 = zip(*results1.items())
        hp_values2, chance_to_kill2 = zip(*results2.items())

        plt.plot(hp_values1, chance_to_kill1, marker='o', label='Post buff', color='blue')
        plt.plot(hp_values2, chance_to_kill2, marker='o', label='Pre buff', color='red')

        plt.title('Chance to Kill Tekton post anvil, 1000 sims per hp')
        plt.xlabel('Hitpoints')
        plt.ylabel('Chance to Kill')
        plt.grid(True)
        plt.legend()

        plt.xticks(range(min(hp_values1), max(hp_values1) + 1, 10))

        plt.show()

# variables for the sim
original_boss_hp = 450
original_defence_level = 246

dwh_attack_roll = 155

enemy_maximum_hit = 87
player_hp = 121
scythe_maximum_hit = 48


# buffed scythe gives 182 slash bonus
buffed_scythe_attack_roll = AttackCalculator.calculate_attack_roll(152, 182)

# # pre buff scythe was 167 slash bonus
pre_buffed_scythe_attack_roll = AttackCalculator.calculate_attack_roll(152, 167)

start_hp = 10
end_hp = 450
hp_step = 10
num_simulations_per_hp = 1000

if __name__ == "__main__":
    tekton_simulator = TektonSimulations(dwh_attack_roll, buffed_scythe_attack_roll, enemy_maximum_hit, player_hp, original_boss_hp)
    tekton_simulator.full_tekton_fight_2_dwh(original_boss_hp, original_defence_level)


    # results_post_scythe_buff = tekton_simulator.run_simulations(start_hp, end_hp, hp_step, num_simulations_per_hp, buffed=True)

    # tekton_simulator = TektonSimulations(dwh_attack_roll, pre_buffed_scythe_attack_roll, enemy_maximum_hit, player_hp, original_boss_hp)
    # results_pre_scythe_buff = tekton_simulator.run_simulations(start_hp, end_hp, hp_step, num_simulations_per_hp, buffed=False)

    # plotter = Plotter()
    # plotter.plot_results(results_post_scythe_buff, results_pre_scythe_buff)


# Create an instance of TektonSimulator
# tekton_simulator = TektonSimulations(dwh_attack_roll, scythe_attack_roll, enemy_maximum_hit, player_hp, original_boss_hp)

# tekton_simulator.full_tekton_fight(original_boss_hp, original_defence_level)

