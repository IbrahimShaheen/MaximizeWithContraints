# run in conda python 3.12 with these packages
# $ python 
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import os
import time


FACTORS = ["damage", "crit_chan", "crit_bon", "atk_spd", "multi", "force"]

step_size = 100
shards = 5517
c = [.01, .005, .005, .002, .002, .01]
base_factor_values = [2, 1.3, 1.3, 1.3, 1.3, 1.5]
base_artificial_weights = [1, 1, 1, 1, 0.5, 0.1]

equipment_factor_values = [
    #damage
    5.97,
    
    #crit chance
    0,
    
    #crit bonus
    0,
    
    #atk spd
    0.6,
    
    #multi
    0,
    
    #force
    0, # visor
]
    

def main():
    data = []
    
    for i in range(0, int(shards / step_size) + 1):
        data.append(get_optimal_allocation(function_to_maximize, i * step_size)[0])
        
        
    data = np.array(data)

    x = np.arange(data.shape[0])
    labels = [f"{i * step_size}" for i in range(0, len(data))]

    plt.rcParams['figure.figsize'] = (25.6, 14.4)
    plt.rcParams['figure.dpi'] = 100

    bottom = np.zeros(data.shape[0])
    for i in range(data.shape[1]):
        bar = plt.bar(x, data[:, i], bottom=bottom, label=f'points given to {FACTORS[i]}')
        bottom += data[:, i]

    shards_result = get_optimal_allocation(function_to_maximize, shards)[1]
    optimal_percent = [0] * len(FACTORS)
    for i in range(len(FACTORS)):
        optimal_percent[i] = c[i]*100 * shards_result.x[i].round(0)
    plt.xticks(x, labels)
    plt.ylabel(f'''Maximized Value for loadout
               ''')
    plt.xlabel(f'''Resource allocation ({step_size})
               Resources points are allocated to each factor in order to maximize Y = K * [product of (m_i*x_i+c_i) for i..n] + B''')
    plt.title(f'''
                factors = {np.array(FACTORS)}, base_factor_values = {np.array(base_factor_values)}, c = {np.array(c)}
                
                base_artificial_weights = {np.array(base_artificial_weights)}
                equipment_factor_values = {np.array(equipment_factor_values).round(2)}
                Max_val = {-shards_result.fun} optimal_values = {shards_result.x.round(0)}
                PRECENTS = {np.array(optimal_percent)}
                ''')
    plt.legend()
    
    # Create relative directory if it doesn't exist
    relative_dir = "example_runs"
    os.makedirs(relative_dir, exist_ok=True)
    filename = f"{int(time.time())}.png"
    relative_path = os.path.join(relative_dir, filename)
    plt.savefig(relative_path)
    plt.show()



def function_to_maximize(vars):
    damage, crit_chan, crit_bonus, atk_spd, multi_strike, force = vars
    


    initial_factor_values = [0] * len(base_factor_values)
    for i in range(len(base_factor_values)):
        initial_factor_values[i] = base_factor_values[i] + equipment_factor_values[i]
    
    return (
        - (initial_factor_values[0] + base_artificial_weights[0] * c[0] * damage)
        * (initial_factor_values[1] + base_artificial_weights[1] * c[1] * crit_chan)
        * (initial_factor_values[2] + base_artificial_weights[2] * c[2] * crit_bonus)
        * (initial_factor_values[3] + base_artificial_weights[3] * c[3] * atk_spd)
        * (initial_factor_values[4] + base_artificial_weights[4] * c[4] * multi_strike)
        * (initial_factor_values[5] + base_artificial_weights[5] * c[5] * force)
    )
    
    



def get_optimal_allocation(function_to_minimize, contraint):
    constraint = {"type": "eq", "fun": lambda vars: sum(vars) - contraint}

    initial_guess = [0] * len(FACTORS)

    bounds = [(0, None)] * len(FACTORS)

    result = minimize(function_to_minimize, initial_guess, constraints=[constraint], bounds=bounds)


    optimal_values = result.x
    max_value = -result.fun

    print(f"Optimal values: {optimal_values}")
    print(f"Sum of values = {sum(optimal_values)}")

    print(f"Maximum value of the function: {max_value}")

    int_values = []
    for i in range(len(optimal_values)):
        int_values.append(int(optimal_values[i]))

    return int_values, result

main()
