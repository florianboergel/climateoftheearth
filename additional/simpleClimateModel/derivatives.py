import numpy as np

def first_derivative_lon(x, dx):
    """First in lon direction. Periodic boundary conditions.

    Args:
        x (numpy-2d-array): Field (lat, lon)
        dx (numpy-2d-array): Grid spacing

    Returns:
        numpy-2d-array: First derivative with respect to d/dlon
    """

    x_shifted_minus_one = np.roll(x, shift=1, axis=1) 
    x_shifted_plus_one = np.roll(x, shift=-1, axis=1) 
    
    return (x_shifted_plus_one - x_shifted_minus_one) / (2 * dx)


def second_derivative_lon(x, dx):

    x_shifted_minus_one = np.roll(x, shift=1, axis=1) 
    x_shifted_plus_one = np.roll(x, shift=-1, axis=1)

    return (x_shifted_plus_one - 2*x + x_shifted_minus_one) / (dx**2)


def first_derivative_lat(x, dy):

    x_shifted_minus_one = np.roll(x, shift=1, axis=0) 
    x_shifted_plus_one = np.roll(x, shift=-1, axis=0) 
    
    derivative = (x_shifted_plus_one - x_shifted_minus_one) / (2 * dy)
    
    derivative[0, :] = 0
    derivative[-1, :] = 0

    return derivative


def second_derivative_lat(x, dy):

    x_shifted_minus_one = np.roll(x, shift=1, axis=0) 
    x_shifted_plus_one = np.roll(x, shift=-1, axis=0) 

    derivative = (x_shifted_plus_one - 2*x + x_shifted_minus_one) / (dy**2)

    derivative[0, :] = 0
    derivative[-1, :] = 0 

    return derivative

def laplacian(x, dx, dy):
    return second_derivative_lon(x, dx) + second_derivative_lat(x, dy)