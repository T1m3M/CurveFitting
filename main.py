import matplotlib.pyplot as plt
from random import uniform, choices, sample, random
import numpy as np


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


def cost_function(coefficients, x, degree):
    y = 0
    # calculate Y = a*X^0 + b*X^1 + c * X^2 + ... + n X^i
    for i in range(degree + 1):
        y += coefficients[i] * pow(x, i)
    return y


def fitness(genome, actualPoints, polynomialDegree):
    sumOfSquaredErrors = 0

    for actualPoint in actualPoints:
        y_calculated = cost_function(genome, actualPoint.x, polynomialDegree)
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


def crossover(genome_a, genome_b):
    # 2-point crossover
    crossover_points = sample(range(1, len(genome_a) - 1), 2)
    crossover_points = sorted(crossover_points)
    # making sure point_1 < point_2
    point_1 = crossover_points[0]
    point_2 = crossover_points[1]

    return genome_a[:point_1] + genome_b[point_1:point_2] + genome_a[point_2:], \
        genome_b[:point_1] + genome_a[point_1:point_2] + genome_b[point_2:]


def mutation(genome, t, T, b=2.5):
    # Non-uniform floating point mutation
    lowerBound = -10
    upperBound = 10

    for i in range(len(genome)):
        delta_L = genome[i] - lowerBound
        delta_U = upperBound - genome[i]

        # flipping a coin to see whether it will increase or decrease
        if random() <= 0.5:
            y = delta_L
        else:
            y = delta_U

        r = random()
        delta = y * (1 - pow(r, pow(1 - t / T, b)))

        if y == delta_U:
            genome[i] = genome[i] + delta
        else:
            genome[i] = genome[i] - delta

    return genome


def plot_curve(case_number, coefficients, case):
    plt.ylim(-2, 2)

    X = np.linspace(0, 7, 100)
    Y = cost_function(coefficients, X, case.polynomialDegree)

    # scatter actual points
    plt.scatter(case.getXPoints(), case.getYPoints(), color='blue')

    # plot solution curve
    plt.plot(X, Y, color='red', linewidth=2, label="prediction")
    plt.title("Case " + str(case_number))

    # plt.savefig('plots\\case_' + str(case_number) + '.png')
    plt.show()


def run_evolution(case, population_size=100, generation_limit=2000):
    population = population_generation(population_size, case.polynomialDegree)

    for generation_number in range(generation_limit):
        # sorting the population in ascending order
        population = sorted(
            population,
            key=lambda genome: fitness(genome, case.points, case.polynomialDegree)
        )

        # Elitism  (best 2 solutions remains in next generation)
        next_generation = population[:2]

        # mating pool and mutation
        for _ in range(int(len(population) / 2) - 1):
            parents = tournament_selection(population, case.points, case.polynomialDegree)
            offspring_a, offspring_b = crossover(parents[0], parents[1])

            offspring_a = mutation(offspring_a, generation_number, generation_limit)
            offspring_b = mutation(offspring_b, generation_number, generation_limit)

            next_generation += [offspring_a, offspring_b]

        population = next_generation

    # sorting final generation's populating in ascending order
    population = sorted(
        population,
        key=lambda genome: fitness(genome, case.points, case.polynomialDegree)
    )

    best_solution = population[0]
    error = fitness(best_solution, case.points, case.polynomialDegree)

    # returning best solution
    return best_solution, error


def saving_solution_to_file(case_number, solution, error):
    with open("output.txt", "a") as f:
        f.write("CASE #" + str(case_number) + "\n")
        for coefficient in solution:
            f.write(str(coefficient) + " ")
        f.write("Error=" + str(error) + "\n\n")


def main():
    cases = loading_test_cases()

    for case_number in range(len(cases)):
        solution, error = run_evolution(cases[case_number])
        plot_curve(case_number + 1, solution, cases[case_number])

        print("Coefficients = " + str(solution))
        print("Error = " + str(error))

        # saving_solution_to_file(case_number + 1, solution, error)


if __name__ == '__main__':
    main()
