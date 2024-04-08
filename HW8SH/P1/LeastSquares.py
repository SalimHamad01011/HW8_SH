import numpy as np
import matplotlib.pyplot as plt
from math import *

class LeastSquaresFit_Class():
    def __init__(self, xdata=None, ydata=None):
        self.x = xdata if xdata is not None else np.array([])
        self.y = ydata if ydata is not None else np.array([])
        self.coeffs = np.array([])

    def RSquared(self, a):
        AvgY = np.mean(self.y)  # calculates the average value of y
        SSTot = 0
        SSRes = 0
        for i in range(len(self.y)):
            SSTot += (self.y[i] - AvgY)**2
            SSRes += (self.y[i] - self.Poly(self.x[i], a))**2
        RSq = 1 - SSRes/SSTot
        return RSq

    def Poly(self, xval, a):
        p = np.poly1d(a)
        return p(xval)

    def LeastSquares(self, power):
        self.coeffs = np.polyfit(self.x, self.y, power)
        return self.coeffs

    def GetCoeffsString(self):
        s = ''
        n = 0
        for c in self.coeffs:
            s += ('' if n == 0 else ', ') + "{:0.4f}".format(c)
            n += 1
        return s

    def GetPlotInfo(self, power, npoints=500):
        Xmin = min(self.x)
        Xmax = max(self.x)
        Ymin = min(self.y)
        Ymax = max(self.y)
        dX = 1.0 * (Xmax - Xmin) / npoints

        a = self.LeastSquares(power)

        xvals = []
        yvals = []
        for i in range(npoints):
            xvals.append(Xmin + i * dX)
            yvals.append(self.Poly(xvals[i], a))
        RSq = self.RSquared(a)
        return xvals, yvals, RSq

# Example xdata and ydata
xdata = np.array([1, 2, 3, 4, 5])
ydata = np.array([2.2, 2.8, 3.5, 4.1, 5.0])

# Initialize the LeastSquaresFit_Class with the data
ls_fit = LeastSquaresFit_Class(xdata, ydata)

# Fit the data with a polynomial of order 2 (quadratic)
coeffs = ls_fit.LeastSquares(power=2)

# Get the coefficients string
coeffs_string = ls_fit.GetCoeffsString()
print(f"Polynomial Coefficients: {coeffs_string}")

# Get the plot info for 500 points
xvals, yvals, RSq = ls_fit.GetPlotInfo(power=2, npoints=500)

# Plotting
plt.scatter(xdata, ydata, label='Original Data')
plt.plot(xvals, yvals, color='red', label=f'Least Squares Fit, $R^2$={RSq:.4f}')
plt.legend()
plt.xlabel('X Data')
plt.ylabel('Y Data')
plt.title('Least Squares Fit to Data')
plt.show()

# Print R squared value
print(f"R Squared Value: {RSq}")
