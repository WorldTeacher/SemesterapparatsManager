import matplotlib

matplotlib.use("QtAgg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt6 import QtCore, QtWidgets


class graph(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.canvas = FigureCanvas(fig)
        super().__init__(fig)


# display graph with multiple lines
class GraphWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, data=None, legend_labels=None):
        super().__init__()
        self.graph = graph(self, width=7, height=4.5, dpi=100)
        self.graph.axes.plot(data["x"], data["y"], "r", data["x"], data["y2"], "b")
        self.toolbar = NavigationToolbar(self.graph, self)
        # set legend
        self.graph.axes.legend(legend_labels, loc="upper left")
        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.graph)
        self.setLayout(layout)

    # def set_area(self, top=1, bottom= 0.07, left=0.1, right=0.994,hspace=0.2,wspace=0.2):
    # self.graph.


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    data = {
        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "y": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "y2": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    }
    widget = GraphWidget(data=data, legend_labels=["+", "-"])
    widget.show()
    sys.exit(app.exec())
