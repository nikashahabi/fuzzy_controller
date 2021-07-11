import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Create the three fuzzy variables - two inputs, one output
temperature = ctrl.Antecedent(np.arange(0, 51, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 26, 1), 'humidity')
fan_speed = ctrl.Consequent(np.arange(0, 1601, 1), 'fan_speed')

# Use triangular membership function to make 9 fuzzy sets
temperature['cold'] = fuzz.trimf(temperature.universe, [0, 0, 10])
temperature['medium'] = fuzz.trimf(temperature.universe, [5, 10, 20])
temperature['hot'] = fuzz.trimf(temperature.universe, [15, 20, 25])
humidity['dry'] = fuzz.trimf(humidity.universe, [0, 0, 10])
humidity['normal'] = fuzz.trimf(humidity.universe, [5, 10, 15])
humidity['wet'] = fuzz.trimf(humidity.universe, [10, 15, 20])
fan_speed['slow'] = fuzz.trimf(fan_speed.universe, [0, 0, 800])
fan_speed['moderate'] = fuzz.trimf(fan_speed.universe, [400, 800, 1200])
fan_speed['fast'] = fuzz.trimf(fan_speed.universe, [800, 1200, 1600])
temperature.view()

# Get temperature
while True:
    T = input("Input temperature\n")
    if int(T) < 25:
        break
humidity.view()
# Get humidity
while True:
    H = input("Input humidity\n")
    if int(H) < 20:
        break
fan_speed.view()
# T = input()
# H = input()

# Set rules
rule1 = ctrl.Rule(temperature['cold'] & humidity['dry'], fan_speed['moderate'])
rule2 = ctrl.Rule(temperature['cold'] & humidity['normal'], fan_speed['slow'])
rule3 = ctrl.Rule(temperature['cold'] & humidity['wet'], fan_speed['slow'])
rule4 = ctrl.Rule(temperature['medium'] & humidity['dry'], fan_speed['fast'])
rule5 = ctrl.Rule(temperature['medium'] & humidity['normal'], fan_speed['moderate'])
rule6 = ctrl.Rule(temperature['medium'] & humidity['wet'], fan_speed['slow'])
rule7 = ctrl.Rule(temperature['hot'] & humidity['dry'], fan_speed['fast'])
rule8 = ctrl.Rule(temperature['hot'] & humidity['normal'], fan_speed['fast'])
rule9 = ctrl.Rule(temperature['hot'] & humidity['wet'], fan_speed['moderate'])

# Build the fuzzy control system
fan_speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
speed = ctrl.ControlSystemSimulation(fan_speed_ctrl)

# Give inputs to the controller
speed.input['temperature'] = int(T)
speed.input['humidity'] = int(H)

# Compute and Print the output
speed.compute()
print(speed.output['fan_speed'], "RMP")
fan_speed.view(sim=speed)
