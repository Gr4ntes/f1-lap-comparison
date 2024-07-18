from PyQt6 import QtCore, QtWidgets, QtGui
import sys
import fastf1
import numpy as np


class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.season_text = QtWidgets.QLabel("Season", self)
        self.season = QtWidgets.QLineEdit(self)
        self.race_text = QtWidgets.QLabel("Race", self)
        self.race_options = QtWidgets.QComboBox(self)
        self.driver1_text = QtWidgets.QLabel("Driver 1", self)
        self.driver1 = QtWidgets.QComboBox(self)
        self.driver2_text = QtWidgets.QLabel("Driver 2", self)
        self.driver2 = QtWidgets.QComboBox(self)
        self.query_button = QtWidgets.QPushButton("See Results", self)
        self.init_ui()

    def init_ui(self):
        self.setGeometry(200, 160, 400, 300)
        font = QtGui.QFont("Halvetica", 12)

        self.season_text.setFont(font)
        self.season_text.move(50, 25)

        self.season.resize(100, 25)
        self.season.move(50, 50)
        self.season.editingFinished.connect(self.on_editing_finished)

        self.race_text.setFont(font)
        self.race_text.move(160, 25)

        self.race_options.resize(200, 25)
        self.race_options.move(160, 50)

        self.driver1_text.setFont(font)
        self.driver1_text.move(50, 100)
        self.driver2_text.setFont(font)
        self.driver2_text.move(160, 100)
        self.driver1.resize(100, 25)
        self.driver1.move(50, 125)
        self.driver2.resize(100, 25)
        self.driver2.move(160, 125)

        self.query_button.resize(100, 50)
        self.query_button.move(150, 200)

        self.show()

    @QtCore.pyqtSlot()
    def on_editing_finished(self):
        year = self.season.text()
        print(year)
        races = fastf1.get_event_schedule(int(year), include_testing=False)
        countries = races['Country'].to_numpy()
        locations = races['Location'].to_numpy()
        options = []
        for i in range(countries.size):
            options.append(countries[i] + ', ' + locations[i])
        self.race_options.addItems(options)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = App()

    sys.exit(app.exec())