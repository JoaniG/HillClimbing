""""
Optimization project using hill climbing algorithm.
We use this algorithm to find the optimal solution on where to place hospitals in a grid, minimizing the total distance to each house.
We use random reset to combat local minima, and we save each iteration on a file.
"""

import mainClasses as mc

def main():
    # Create a grid
    grid = mc.Grid(10, 10)
    num_hospitals = 2
    num_houses = 6
    grid.place_houses(num_houses)
    grid.print_grid()
    grid.random_reset(num_hospitals, 10)



if __name__ == '__main__':
    main()
