from PyQt6 import QtCore, QtWidgets, QtGui
import sys
import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
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
        fastf1.plotting.setup_mpl(misc_mpl_mods=False)
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
        self.race_options.activated.connect(self.on_race_chosen)  # Connect the activated signal to a slot

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
        self.query_button.clicked.connect(self.plot)

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
        self.race_options.clear()
        self.race_options.addItems(options)

    @QtCore.pyqtSlot()
    def on_race_chosen(self):
        self.session = fastf1.get_session(int(self.season.text()), self.race_options.currentText(), 'Q')
        self.session.load()
        drivers = self.session.drivers
        driver_abbreviations = []
        for driver in drivers:
            driver_abbreviations.append(self.session.get_driver(driver)['Abbreviation'])
        self.driver1.clear()
        self.driver2.clear()
        self.driver1.addItems(driver_abbreviations)
        self.driver2.addItems(driver_abbreviations)

    @QtCore.pyqtSlot()
    def plot(self):
        driver1_lap = self.session.laps.pick_driver(self.driver1.currentText()).pick_fastest()
        driver2_lap = self.session.laps.pick_driver(self.driver2.currentText()).pick_fastest()
        driver1_tel = driver1_lap.get_car_data().add_distance()
        driver2_tel = driver2_lap.get_car_data().add_distance()

        fig, ax = plt.subplots()
        ax.plot(driver1_tel['Distance'], driver1_tel['Speed'], color="green",
                label=self.session.get_driver(self.driver1.currentText())['Abbreviation'])
        ax.plot(driver2_tel['Distance'], driver2_tel['Speed'], color="red",
                label=self.session.get_driver(self.driver2.currentText())['Abbreviation'])

        ax.set_xlabel('Distance in m')
        ax.set_ylabel('Speed in km/h')

        ax.legend()
        plt.suptitle(f"Fastest Lap Comparison \n "
                     f"{self.session.event['EventName']} {self.session.event.year} Qualifying")

        plt.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = App()

    sys.exit(app.exec())