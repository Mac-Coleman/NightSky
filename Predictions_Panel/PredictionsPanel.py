from datetime import timedelta

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QSizePolicy, QVBoxLayout
from PySide6.QtCore import Qt

from skyfield.api import EarthSatellite

from Predictions_Panel.CulminationEntry import CulminationEntry
from Predictions_Panel.UI.PredictionsPanel import Ui_w_predictionsPanel

from object_widgets import ObjectSeparator


class PredictionsPanel(QWidget, Ui_w_predictionsPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.sa_results.setWidgetResizable(True)

        contentWidget = QWidget()
        contentWidget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Maximum)

        self.contentLayout = QVBoxLayout()
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        contentWidget.setLayout(self.contentLayout)

        self.sa_results.setWidget(contentWidget)

        self.pb_recalculate.clicked.connect(self.handleRecalculate)

    def handleRecalculate(self):

        for i in reversed(range(self.contentLayout.count())):
            self.contentLayout.itemAt(i).widget().setParent(None)

        timescale = QApplication.instance().timescale
        currentTime = QApplication.instance().skyTime
        oneWeek = timescale.utc(currentTime.utc_datetime() + timedelta(days=7))
        topocentric = QApplication.instance().wgs84

        satellites = QApplication.instance().databaseManager.getFavoriteSatellites()

        event_widgets = []

        for sat in satellites:
            line0, line1, line2, *_ = sat[5].split("\n")
            es = EarthSatellite(line1, line2)

            times, events = es.find_events(topocentric, currentTime, oneWeek, altitude_degrees=20.0)
            event_names = 'rises', 'culminates', 'sets'
            for ti, event in zip(times, events):
                name = event_names[event]
                title = f"{sat[3]} {name}"
                alt, az, dist = (es - topocentric).at(ti).altaz()
                desc = f"{ti.utc_strftime('%B %d, %H:%M:%S')}<br>Azimuth: <i>{az}</i>, Altitude: <i>{alt}</i><br> at a "\
                    f"distance of {dist.km:0.0f} kilometers."

                event_widgets.append(CulminationEntry(title, ti, alt, az, dist))

        event_widgets.sort(key=lambda x: x.time)

        for widget in event_widgets:
            self.contentLayout.addWidget(widget)
            self.contentLayout.addWidget(ObjectSeparator())

        if len(event_widgets) == 0:
            l = QLabel("<i>No results found...\nTry another search!</i>")
            l.setWordWrap(True)
            l.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            l.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.contentLayout.addWidget(l)