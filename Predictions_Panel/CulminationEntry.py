from PySide6.QtWidgets import QWidget

from Predictions_Panel.UI.CulminationEntry import Ui_w_culminationEntry


class CulminationEntry(QWidget, Ui_w_culminationEntry):
    def __init__(self, title, time, alt, az, dist, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.lb_title.setText(f"<h1>{title}</h1>")
        self.lb_date.setText(f"<i>{time.utc_strftime('%B %d')}</i>")
        self.lb_time.setText(f"<i>{time.utc_strftime('%H:%M:%S')}</i>")
        self.lb_dist.setText(f"<i>{dist.km:.0f} km</i>")
        self.lb_alt.setText(f"<i>{alt.degrees:.2f}°</i>")
        self.lb_az.setText(f"<i>{az.degrees:.2f}°</i>")
        self.time = time.utc_datetime()