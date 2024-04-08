import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import PyQt5.QtWidgets as qtw

# importing from previous work on least squares fit
from LeastSquares import LeastSquaresFit_Class

class Pump_Model():
    """
    This is the pump model.  It just stores data.
    """
    def __init__(self):
        self.PumpName = ""
        self.FlowUnits = ""
        self.HeadUnits = ""

        self.FlowData = np.array([])
        self.HeadData = np.array([])
        self.EffData = np.array([])

        self.HeadCoefficients = np.array([])
        self.EfficiencyCoefficients = np.array([])

        self.LSFitHead = LeastSquaresFit_Class()
        self.LSFitEff = LeastSquaresFit_Class()

class Pump_Controller():
    def __init__(self):
        self.Model = Pump_Model()
        self.View = Pump_View()

    def ImportFromFile(self, data):
        self.Model.PumpName = data[0].strip()  # Extract pump name from the data
        self.Model.FlowUnits = data[1].split()[0]  # Extract flow units from the data
        self.Model.HeadUnits = data[1].split()[1]  # Extract head units from the data

        self.SetData(data[3:])
        self.updateView()

    def SetData(self, data):
        self.Model.FlowData = np.array([])
        self.Model.HeadData = np.array([])
        self.Model.EffData = np.array([])

        for line in data:
            cells = line.split()
            self.Model.FlowData = np.append(self.Model.FlowData, float(cells[0]))  # Convert string to float
            self.Model.HeadData = np.append(self.Model.HeadData, float(cells[1]))  # Convert string to float
            self.Model.EffData = np.append(self.Model.EffData, float(cells[2]))  # Convert string to float

        self.LSFit()

    def LSFit(self):
        self.Model.LSFitHead.x = self.Model.FlowData
        self.Model.LSFitHead.y = self.Model.HeadData
        self.Model.LSFitHead.LeastSquares(2)  # Quadratic fit for Head data

        self.Model.LSFitEff.x = self.Model.FlowData
        self.Model.LSFitEff.y = self.Model.EffData
        self.Model.LSFitEff.LeastSquares(3)  # Cubic fit for Efficiency data

    def setViewWidgets(self, w):
        self.View.setViewWidgets(w)

    def updateView(self):
        self.View.updateView(self.Model)

class Pump_View():
    def __init__(self):
        self.LE_PumpName = qtw.QLineEdit()
        self.LE_FlowUnits = qtw.QLineEdit()
        self.LE_HeadUnits = qtw.QLineEdit()
        self.LE_HeadCoefs = qtw.QLineEdit()
        self.LE_EffCoefs = qtw.QLineEdit()
        self.ax = None
        self.canvas = None

    def updateView(self, Model):
        self.LE_PumpName.setText(Model.PumpName)
        self.LE_FlowUnits.setText(Model.FlowUnits)
        self.LE_HeadUnits.setText(Model.HeadUnits)
        self.LE_HeadCoefs.setText(Model.LSFitHead.GetCoeffsString())
        self.LE_EffCoefs.setText(Model.LSFitEff.GetCoeffsString())
        self.DoPlot(Model)

    def DoPlot(self, Model):
        headx, heady, headRSq = Model.LSFitHead.GetPlotInfo(2, npoints=500)  # Quadratic fit
        effx, effy, effRSq = Model.LSFitEff.GetPlotInfo(3, npoints=500)  # Cubic fit

        axes = self.ax
        axes.plot(headx, heady, label='Head Data')
        axes.plot(effx, effy, label='Efficiency Data')
        axes.legend()
        axes.set_xlabel('Flow Rate (' + Model.FlowUnits + ')')
        axes.set_ylabel('Head (' + Model.HeadUnits + ')')
        axes.set_title('Pump Performance')

        self.canvas.draw()

    def setViewWidgets(self, w):
        self.LE_PumpName, self.LE_FlowUnits, self.LE_HeadUnits, self.LE_HeadCoefs, self.LE_EffCoefs, self.ax, self.canvas = w
