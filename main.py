import matplotlib.pyplot as plt
from random import uniform


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Case:
    def __init__(self, numOfPoints, polynomialDegree):
        self.numOfPoints = numOfPoints
        self.polynomialDegree = polynomialDegree
        self.points = []

    def addPoint(self, point):
        self.points.append(point)

    def getXPoints(self):
        return [point.x for point in self.points]

    def getYPoints(self):
        return [point.y for point in self.points]


def cases_parsing(file_data, total_cases):
    counter = 0
    cases = []

    for _ in range(total_cases):
        first_line = file_data[counter].split()

        num_of_points = int(first_line[0])
        polynomial_degree = int(first_line[1])

        case = Case(num_of_points, polynomial_degree)

        counter += 1

        # reading points for each case
        for i in range(num_of_points):
            point_line = file_data[counter + i].split()
            point = Point(float(point_line[0]), float(point_line[1]))
            case.addPoint(point)

        counter += num_of_points
        cases.append(case)

    return cases


def loading_test_cases():
    with open("input-2.txt") as f:
        file_lines = f.read().splitlines()

    total_cases = int(file_lines[0])
    return cases_parsing(file_lines[1:], total_cases)


def genome_generation(polynomialDegree):
    return [round(uniform(-10, 10), 2) for _ in range(polynomialDegree + 1)]


def population_generation(population_size, polynomialDegree):
    return [genome_generation(polynomialDegree) for _ in range(population_size)]


def run_evolution(case, population_size=100, generation_limit=1000):
    population = population_generation(population_size, case.polynomialDegree)

    print(population)


def main():
    cases = loading_test_cases()

    run_evolution(cases[0])


if __name__ == '__main__':
    main()
