from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
# Only needed for access to command line arguments
import sys


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        button = QPushButton("Press Me!")

        self.setFixedSize(QSize(1200, 600))
        self.setMaximumSize(QSize(1200, 600))
        self.setMinimumSize(QSize(800, 400))

        # Set the central widget of the Window.
        self.setCentralWidget(button)



# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
# window = QWidget()
# window = QPushButton("Push Me")
# window = QMainWindow()
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.