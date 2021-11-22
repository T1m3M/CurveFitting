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