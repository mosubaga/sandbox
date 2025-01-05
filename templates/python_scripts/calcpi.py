import random
import math

def calculate_pi(num_points):
    
    """
    Calculate the value of pi using Monte Carlo simulation.
    
    Parameters:
        num_points (int): The number of random points to generate.
    
    Returns:
        float: The estimated value of pi.
    """
    inside_circle = 0

    for _ in range(num_points):
        # Generate random (x, y) coordinates between 0 and 1
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)

        # Check if the point is inside the quarter-circle
        if math.sqrt(x**2 + y**2) <= 1:
            inside_circle += 1

    # Estimate pi (area of the quarter-circle is pi/4)
    pi_estimate = 4 * (inside_circle / num_points)
    return pi_estimate

# Number of points to simulate
num_points = 10_000_000

# Calculate pi
estimated_pi = calculate_pi(num_points)
print(f"Estimated value of pi (using {num_points} points): {estimated_pi}")
