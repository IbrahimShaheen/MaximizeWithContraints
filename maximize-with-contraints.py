# run in conda python 3.12 with these packages
# $ python 
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


FACTORS = ["damage", "crit_chan", "crit_bon", "atk_spd", "multi", "force"]

step_size = 100
shards = 3500
    
equipment_factor_values = [
    5.97,  # duelist spark
    0,
    0,
    0.0, # gloves
    0.0, # ring
    0.0,
]

    

def main():
    data = []
    
    for i in range(0, int(shards / step_size) + 1):
        data.append(get_optimal_allocation(function_to_maximize, i * step_size))
        
        
    data = np.array(data)

    x = np.arange(data.shape[0])
    labels = [f"{i * step_size}" for i in range(0, len(data))]

    bottom = np.zeros(data.shape[0])
    for i in range(data.shape[1]):
        bar = plt.bar(x, data[:, i], bottom=bottom, label=f'points given to {FACTORS[i]}')
        bottom += data[:, i]


    plt.xticks(x, labels)
    plt.ylabel(f'''Maximized Value for loadout
                equipment_factor_values = {np.array(equipment_factor_values)}
               ''')
    plt.xlabel(f'Resource allocation ({step_size})')
    plt.title('''Resources points are allocated to each factor in order to maximize
                Y = K * [product of (m_i*x_i+c_i) for i..n] + B

                ''')
    plt.legend()
    plt.show()   
    



def function_to_maximize(vars):
    damage, crit_chan, crit_bonus, atk_spd, multi_strike, force = vars
    
    base_factor_values = [2, 1.3, 1.3, 1.3, 1.3, 1.5]
    base_artificial_weights = [1, 1, 1, 1, 1, 0.2]

    initial_factor_values = [0] * len(base_factor_values)
    for i in range(len(base_factor_values)):
        initial_factor_values[i] = base_factor_values[i] + equipment_factor_values[i]
    
    return (
        - (initial_factor_values[0] + base_artificial_weights[0] * 0.01 * damage)
        * (initial_factor_values[1] + base_artificial_weights[1] * 0.005 * crit_chan)
        * (initial_factor_values[2] + base_artificial_weights[2] * 0.005 * crit_bonus)
        * (initial_factor_values[3] + base_artificial_weights[3] * 0.002 * atk_spd)
        * (initial_factor_values[4] + base_artificial_weights[4] * 0.002 * multi_strike)
        * (initial_factor_values[5] + base_artificial_weights[5] * 0.01 * force)
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

    return int_values

main()
