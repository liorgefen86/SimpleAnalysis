from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QFileDialog, QWidget, QStatusBar
from PyQt5.QtGui import QIcon
import sys
import platform
import os


class UserInterface(QMainWindow):
    """
    Class responsible for creating the user interface and the interaction with
    the user

    Args:
        title [str]:
            main window title
        size [tuple, size=2]:
            size of the window in pixels (npixels_x, npixels_y)
    """
    def __init__(self, title='Simple Analysis', size=(320, 240)):
        self.app = QApplication([])  # initialisation of the Qt application
        super().__init__()  # calling the super class constructor

        # set main window geometry:
        # first two ints are the initial location in x and y
        # last two are the initial size in x and y
        self.setGeometry(100, 100, size[0], size[1])
        self.setWindowTitle(title)

        # getting information on the current os and its version
        current_os = platform.system()
        if current_os == 'Darwin':
            current_os = 'macOS'
            os_version = platform.mac_ver()[0]
        else:
            os_version = platform.release()

        # creation a status bar and display os information on it
        statusbar = QStatusBar()
        statusbar.setGeometry(0, size[1]-50, size[0], 50)
        statusbar.showMessage(f'OS:{current_os:s}\tVersion:{os_version:s}')
        self.setStatusBar(statusbar)

        frame = QWidget(self)
        frame.setGeometry(0, 0, size[0], size[1]-50)

        self.btn_charge = QPushButton('Load file', frame)
        self.btn_charge.setIcon(QIcon('icons/load.png'))
        self.btn_charge.move(5, 5)
        self.btn_charge.pressed.connect(self.__select_file)

        self.__show_application()

    def __select_file(self):
        file_dialog = QFileDialog.Options()
        file_dialog |= QFileDialog.DontUseNativeDialog
        self._fileName, _ = QFileDialog.getOpenFileName(
            self,
            caption='Select Excel file',
            directory=os.curdir,
            filter='Excel files (*.xlsx)',
            options=file_dialog
        )
        if self._fileName:
            print(self._fileName)

    def __show_application(self):
        self.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    gui = UserInterface()
