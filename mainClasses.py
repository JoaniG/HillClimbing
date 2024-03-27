from dataclasses import dataclass, field
import random
import sys


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def find_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def find_closest(self, hospitals):
        closest = hospitals[0]
        distance = self.find_distance(closest.position)
        for hospital in hospitals:
            if self.find_distance(hospital.position) < self.find_distance(closest.position):
                closest = hospital
                distance = self.find_distance(closest.position)
        return closest, distance


@dataclass
class Grid:
    width: int
    height: int
    #points: set = field(default_factory=set)
    hospitals: set = field(default_factory=set)
    houses: set = field(default_factory=set)

    # def add_point(self, point):
    #     if point not in self.points:
    #         self.points.add(point)
    #         return True
    #     return False

    def check_point(self, point):
        if any(hospital.position == point for hospital in self.hospitals) or any(house.position == point for house in self.houses):
            return False
        return True

    def get_available_points(self):
        available_points = []
        for i in range(self.width):
            for j in range(self.height):
                point = Point(i, j)
                if self.check_point(point):
                    available_points.append(point)
        return available_points

    def place_hospital(self, point):
        if self.check_point(point):
            hospital = Hospital(point)
            self.hospitals.add(hospital)
            print(f"Hospital placed at {point}")
        else:
            print("Point already occupied. Unable to place hospital.")
    
    def move_hospital(self, hospital, direction):
        if direction == "left":
            if self.check_point(Point(hospital.position.x - 1, hospital.position.y)):
                hospital.position.x -= 1
                return True
            return False
            
        elif direction == "right":
            if self.check_point(Point(hospital.position.x + 1, hospital.position.y)):
                hospital.position.x += 1
                return True
            return False
            
        elif direction == "up":
            if self.check_point(Point(hospital.position.x, hospital.position.y - 1)):
                hospital.position.y -= 1
                return True
            return False
            
        elif direction == "down":
            if self.check_point(Point(hospital.position.x, hospital.position.y + 1)):
                hospital.position.y += 1
                return True
            return False
            

    def place_house(self, point):
        if self.check_point(point):
            house = House(point)
            self.houses.add(house)
            print(f"House placed at {point}")
        else:
            print("Point already occupied. Unable to place house.")

    def print_grid(self):
        for i in range(self.width):
            row = []
            for j in range(self.height):
                point = Point(i, j)
                if any(hospital.position == point for hospital in self.hospitals):
                    row.append('X ')
                elif any(house.position == point for house in self.houses):
                    row.append('O ')
                else:
                    row.append('| ')
            print(''.join(row))

    def place_hospitals(self, num_hospitals):
        available_points = self.get_available_points()
        points = random.sample(available_points, num_hospitals)
        for point in points:
            self.place_hospital(point)


    def place_houses(self, num_houses):
        available_points = self.get_available_points()
        points = random.sample(available_points, num_houses)
        for point in points:
            self.place_house(point)

    def find_cost(self):
        cost = 0
        for house in self.houses:
            closest_hospital, distance = house.position.find_closest(list(self.hospitals))
            cost += distance
        return cost

    def hill_climbing(self, num_hospitals):
        self.place_hospitals(num_hospitals)
        for hospital in self.hospitals:
            while True:
                cost = self.find_cost()
                if self.move_hospital(hospital, "left"):
                    if self.find_cost() < cost:
                        continue
                    else:
                        self.move_hospital(hospital, "right")
                    
                if self.move_hospital(hospital, "right"):
                    if self.find_cost() < cost:
                        continue
                    else:
                        self.move_hospital(hospital, "left")
                
                if self.move_hospital(hospital, "up"):
                    if self.find_cost() < cost:
                        continue
                    else:
                        self.move_hospital(hospital, "down")

                if self.move_hospital(hospital, "down"):
                    if self.find_cost() < cost:
                        continue
                    else:
                        self.move_hospital(hospital, "up")
                break
        
        return self.find_cost()

    def random_reset(self, num_hospitals, iterations):
        cost = 9999999
        for i in range(iterations):
            self.hospitals = set()
            new_cost = self.hill_climbing(num_hospitals)
            if new_cost < cost:
                cost = new_cost
                print(f'Found better way at iteration {i}: Cost of {cost}')
            else:
                print(f'{i}: Cost of {new_cost}')

            output_file = f'c:/Users/user/Desktop/Joani/Project/Optimization/{i}_grid_output.txt'
            with open(output_file, 'w') as file:
                original_stdout = sys.stdout
                sys.stdout = file
                self.print_grid()
                print(f'Cost of {new_cost}')
                sys.stdout = original_stdout
                

@dataclass
class Hospital():
    position: Point

    def __hash__(self):
        return hash(self.position)

    def find_neighbors(self):
        neighbors = []
        neighbors.append()
        return neighbors


@dataclass
class House:
    position: Point

    def __hash__(self):
        return hash(self.position)