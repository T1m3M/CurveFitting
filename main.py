import matplotlib.pyplot as plt
from random import uniform, choices


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


def fitness(genome, actualPoints, polynomialDegree):
    sumOfSquaredErrors = 0

    for actualPoint in actualPoints:
        y_calculated = 0

        # calculate Y = a*X^0 + b*X^1 + c * X^2 + ... + n X^i
        for i in range(polynomialDegree + 1):
            y_calculated += genome[i] * pow(actualPoint.x, i)

        squaredError = pow((actualPoint.y - y_calculated), 2)
        sumOfSquaredErrors += squaredError

    meanSquaredError = sumOfSquaredErrors / len(actualPoints)

    return meanSquaredError


def tournament_selection(population, actualPoints, polynomialDegree):
    best_pairs = []

    for _ in range(2):
        # selecting 2 random pairs from population
        random_pairs = choices(population=population, k=2)

        # sort to get the least of them
        random_pairs = sorted(
            random_pairs,
            key=lambda genome: fitness(genome, actualPoints, polynomialDegree)
        )

        best_pairs.append(random_pairs[0])

    return best_pairs


def run_evolution(case, population_size=100, generation_limit=1000):
    population = population_generation(population_size, case.polynomialDegree)

    # sorting the population in ascending order
    population = sorted(
        population,
        key=lambda genome: fitness(genome, case.points, case.polynomialDegree)
    )

    # Elitism  (best 2 solutions remains in next generation)
    next_generation = population[:2]

    # tournament selection
    parents = tournament_selection(population, case.points, case.polynomialDegree)


def main():
    cases = loading_test_cases()

    run_evolution(cases[0])


if __name__ == '__main__':
    main()
