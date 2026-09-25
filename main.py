from PySide6.QtWidgets import QApplication
from ui.dashboard import MainWindow
import sys
app=QApplication(sys.argv); w=MainWindow(); w.show(); sys.exit(app.exec())
