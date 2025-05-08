# run in conda python 3.12 with these packages
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


# def proportional_to_dps(vars):
#     damage, crit_chan, crit_bonus, atk_spd, multi_strike = vars
#     return (
#         -(7.37 + 0.005 * damage)
#         * (1.3 + 0.005 * crit_chan)
#         * (1.3 + 0.005 * crit_bonus)
#         * (1.3 + 0.002 * atk_spd)
#         * (1.3 + 0.002 * multi_strike)
#     )



# def proportional_to_dps(vars):
#     damage, crit_chan, crit_bonus, atk_spd, multi_strike = vars
#     return (
#         -(10 + .01 * damage)
#         * (8 + .02 * crit_chan)
#         * (6 + .03 * crit_bonus)
#         * (4 + .04 * atk_spd)
#         * (2 + .05 * multi_strike)
#     )



# def function_to_maximize(vars):
#     x1, x2, x3, x4, x5 = vars
#     return (
#         -(10 + .01 * x1)
#         * (8 + .02 * x2)
#         * (6 + .03 * x3)
#         * (4 + .04 * x4)
#         * (2 + .05 * x5)
#     )


# def function_to_maximize(initial_factor_values, vars):
#     damage, crit_chan, crit_bonus, atk_spd, multi_strike = vars
    
#     (7.97, 1.3, 1.3, 1.3, 1.3) = initial_factor_values
#     init_damage, init_crit_chance, init_crit_bon, init_ats, init_multi = initial_factor_values
#     return (
#         -(init_damage + 0.005 * damage)
#         * (init_crit_chance + 0.005 * crit_chan)
#         * (init_crit_bon + 0.005 * crit_bonus)
#         * (init_ats + 0.002 * atk_spd)
#         * (init_multi + 0.002 * multi_strike)
#     )



    
def main():
    data = []
    
    for i in range(0, 50):
        data.append(get_optimal_allocation(function_to_maximize, i * 200))
        
        
    data = np.array(data)

    x = np.arange(data.shape[0])
    labels = [f"{i * 2}" for i in range(0, len(data))]

    bottom = np.zeros(data.shape[0])
    for i in range(data.shape[1]):
        bar = plt.bar(x, data[:, i], bottom=bottom, label=f'points given to factor x{i + 1}')
        bottom += data[:, i]
        
     
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(height),
            ha='center',
            va='bottom'
        )


    plt.xticks(x, labels)
    plt.ylabel('Maximized Value')
    plt.xlabel('Resource allocation (100pts)')
    plt.title('''Resources points are allocated to each factor in order to maximize \n
                Y = K * [product of (m_i*x_i+c_i) for i..n] + B''')
    plt.legend()
    plt.show()   
    



def function_to_maximize(initial_factor_values, vars):
    damage, crit_chan, crit_bonus, atk_spd, multi_strike = vars
    
    base_factor_values = [2, 1.3, 1.3, 1.3, 1.3]
    equipment_factor_values = [
        5.97,  # duelist spark
        0,
        0,
        0.6,
        ]
    for i in range(len(base_factor_values)):
        initial_factor_values[i] = base_factor_values[i] + equipment_factor_values[i]
    
    return (
        - (initial_factor_values[0] + 0.01 * damage)
        * (initial_factor_values[1] + 0.005 * crit_chan)
        * (initial_factor_values[2] + 0.005 * crit_bonus)
        * (initial_factor_values[3] + 0.002 * atk_spd)
        * (initial_factor_values[5] + 0.002 * multi_strike)
    )
    
    



def get_optimal_allocation(function_to_minimize, contraint):
    constraint = {"type": "eq", "fun": lambda vars: sum(vars) - contraint}

    initial_guess = [0, 0, 0, 0, 0]

    bounds = [(0, None)] * 5

    result = minimize(function_to_minimize, initial_guess, constraints=[constraint], bounds=bounds)


    optimal_values = result.x
    max_value = -result.fun

    print(f"Optimal values: {optimal_values}")
    print(f"Sum of values = {sum(optimal_values)}")

    print(f"Maximum value of the function: {max_value}")

    value_divisors = [1, 2, 2, 5, 5]
    percents_values = []
    for i in range(len(optimal_values)):
        percents_values.append(int(optimal_values[i] / value_divisors[i]))


    print(f"Optimal percent_values: {percents_values}")
    

    return percents_values

main()
