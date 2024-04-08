import io
import matplotlib.figure
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class View:
    def __init__(self):
        self.layout = qtw.QVBoxLayout()
        self.lbl_PHigh = qtw.QLabel()
        self.lbl_PLow = qtw.QLabel()
        self.rb_SI = qtw.QRadioButton()  # Add rb_SI attribute
        self.le_PHigh = qtw.QLineEdit()  # Add le_PHigh attribute

    def setWidgets(self, *widgets):
        for widget in widgets:
            if isinstance(widget, qtw.QWidget):
                self.layout.addWidget(widget)
            elif isinstance(widget, matplotlib.figure.Figure):
                graphics_view = qtw.QGraphicsView()
                graphics_scene = qtw.QGraphicsScene()
                graphics_view.setScene(graphics_scene)

                pixmap = self.figure_to_pixmap(widget)
                graphics_scene.addPixmap(pixmap)

                self.layout.addWidget(graphics_view)
        self.layout.addWidget(self.lbl_PHigh)
        self.layout.addWidget(self.lbl_PLow)
        # Add rb_SI and le_PHigh to the layout
        self.layout.addWidget(self.rb_SI)
        self.layout.addWidget(self.le_PHigh)

    def figure_to_pixmap(self, figure):
        buffer = io.BytesIO()
        figure.savefig(buffer, format='png')
        buffer.seek(0)
        pixmap = qtg.QPixmap()
        pixmap.loadFromData(buffer.getvalue())
        return pixmap

    def updateLabel(self, label, text):
        label.setText(text)

    def setNewPHigh(self, model):
        self.updateLabel(self.lbl_PHigh, f"High Pressure: {model.p_high} kPa")

    def setNewPLow(self, model):
        self.updateLabel(self.lbl_PLow, f"Low Pressure: {model.p_low} kPa")
