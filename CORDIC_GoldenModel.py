from __future__ import division

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

import math
import string
import struct

circular = 1
linear = 0
hyperbolic = -1


def plot(x_values, y_values, x_label, y_label, plot_label):
    # Plot of Value of gain with number of iterations
    fig = plt.figure()
    ax = fig.add_subplot(111)

    line, = ax.plot(x_values, y_values, lw=2)

    ax.set_title(plot_label)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()
    plt.close()
    return


gain_val_list = [math.sqrt(2)]  # Stores value of gain after each iteration
max_iter_gain = 10  # Max number of iterations for calculating value of gain
iterations_list = [0]  # List that Stores the number of iterations performed

for i in range(1, max_iter_gain):
    gain_val_list.append(gain_val_list[i - 1] * math.sqrt(1 + 2 ** (-2 * i)))
    iterations_list.append(i)

# Plot for value of gain with each iteration
plot(iterations_list, gain_val_list, 'Iterations (i) $\\rightarrow$', 'Gain $A_{n}$ $\\rightarrow$',
     'Variation of A$_{n}$ with number of iterations')
print("Gain of the system is " + str(gain_val_list[len(gain_val_list) - 1]))


def ROM_lookup(iteration, coordinate):
    if (coordinate == circular):
        return math.degrees(math.atan(2 ** (-1 * iteration)))
    elif (coordinate == linear):
        return 2 ** (-1 * iteration)
    elif (coordinate == hyperbolic):
        return (math.atanh(2 ** (-1 * iteration)))


def rotation_mode(x, y, z, coordinate, iterations):
    a = 0.607252935  # = 1/K

    x_val_list = []
    y_val_list = []
    z_val_list = []
    iterations_list = []

    i = 0  # Keeps count on number of iterations

    current_x = x  # Value of X on ith iteration
    current_y = y  # Value of Y on ith iteration
    current_z = z  # Value of Z on ith iteration

    di = 0

    if (coordinate == hyperbolic):
        i = 1
    else:
        i = 0

    flag = 0

    if (iterations > 0):
        while (i < iterations):
            if (current_z < 0):
                di = -1
            else:
                di = +1
            next_z = current_z - di * ROM_lookup(i, coordinate)
            next_x = current_x - coordinate * di * current_y * (2 ** (-1 * i))
            next_y = current_y + di * current_x * 2 ** (-1 * i)

            current_x = next_x
            current_y = next_y
            current_z = next_z

            x_val_list.append(current_x)
            y_val_list.append(current_y)
            z_val_list.append(current_z)

            iterations_list.append(i)

            if (coordinate == hyperbolic):
                if ((i != 4) & (i != 13) & (i != 40)):
                    i = i + 1
                elif (flag == 0):
                    flag = 1
                elif (flag == 1):
                    flag = 0
                    i = i + 1
            else:
                i = i + 1
    return {'x': x_val_list, 'y': y_val_list, 'z': z_val_list, 'iteration': iterations_list, }

# #Circular_Test:
rot_x = 0.6073
rot_y = 0
rot_z = 37
crd_sys = circular
max_iter = 30

result_dict = rotation_mode(rot_x, rot_y, rot_z, crd_sys, max_iter)

plot(result_dict['iteration'], result_dict['x'], 'Iterations $\\rightarrow$', 'cos z$_{0}$ $\\rightarrow$', '')
print ("Xn = " + str(result_dict['x'][max_iter-1]))

plot(result_dict['iteration'], result_dict['y'], 'Iterations $\\rightarrow$', 'sin z$_{0}$ $\\rightarrow$', '')
print ("Yn = " + str(result_dict['y'][max_iter-1]))

plot(result_dict['iteration'], result_dict['z'], 'i $\\rightarrow$', 'z$_{i}$ $\\rightarrow$', '')
print ("Zn = " + str(result_dict['z'][max_iter-1]))

#Linear_Test:
rot_x = 0.2
rot_y = 0
rot_z = 1
crd_sys = linear
max_iter = 30

result_dict = rotation_mode(rot_x, rot_y, rot_z, crd_sys, max_iter)

plot(result_dict['iteration'], result_dict['x'], 'Iterations $\\rightarrow$', 'cos z$_{0}$ $\\rightarrow$', '')
print ("Xn = " + str(result_dict['x'][max_iter-1]))

plot(result_dict['iteration'], result_dict['y'], 'Iterations $\\rightarrow$', 'sin z$_{0}$ $\\rightarrow$', '')
print ("Yn = " + str(result_dict['y'][max_iter-1]))

plot(result_dict['iteration'], result_dict['z'], 'i $\\rightarrow$', 'z$_{i}$ $\\rightarrow$', '')
print ("Zn = " + str(result_dict['z'][max_iter-1]))

#Hyperbolic_Test:
rot_x = 1.2075
rot_y = 0
rot_z = 1
crd_sys = hyperbolic
max_iter = 30

result_dict = rotation_mode(rot_x, rot_y, rot_z, crd_sys, max_iter)

plot(result_dict['iteration'], result_dict['x'], 'Iterations $\\rightarrow$', 'cos z$_{0}$ $\\rightarrow$', '')
print ("Xn = " + str(result_dict['x'][max_iter-1]))

plot(result_dict['iteration'], result_dict['y'], 'Iterations $\\rightarrow$', 'sin z$_{0}$ $\\rightarrow$', '')
print ("Yn = " + str(result_dict['y'][max_iter-1]))

plot(result_dict['iteration'], result_dict['z'], 'i $\\rightarrow$', 'z$_{i}$ $\\rightarrow$', '')
print ("Zn = " + str(result_dict['z'][max_iter-1]))