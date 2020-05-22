from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QFileDialog, QWidget, QStatusBar, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
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
    Return:
        None
    """
    def __init__(self, title='Simple Analysis', size=(320, 240)):
        self.app = QApplication([])  # initialisation of the Qt application
        super().__init__()  # calling the super class constructor

        # set main window geometry:
        # first two ints are the initial location in x and y
        # last two are the initial size in x and y
        self.setGeometry(100, 100, size[0], size[1])
        self.setWindowTitle(title)

        self.fileName = ''

        # getting information on the current os and its version
        current_os = platform.system()
        if current_os == 'Darwin':
            current_os = 'macOS'
            os_version = platform.mac_ver()[0]
        else:
            os_version = platform.release()
        self.os_text = f'OS:{current_os:s}\tVersion:{os_version:s}'

        # creation a status bar and display os information on it
        statusbar = QStatusBar()
        statusbar.setGeometry(0, size[1]-50, size[0], 50)
        statusbar.showMessage(self.os_text)
        self.setStatusBar(statusbar)

        # creation of a widget to hold the buttons
        frame = QWidget(self)
        frame.setGeometry(0, 0, size[0], size[1]-50)

        # select button will open a filedialog to let the user select the file
        self.btn_select = QPushButton('Select file')
        self.btn_select.setIcon(QIcon('icons/load.png'))
        self.btn_select.pressed.connect(self.__select_file)

        # load button will load the selected file and start its processing
        self.btn_load = QPushButton('Load file')
        self.btn_load.setIcon(QIcon('icons/load.png'))
        self.btn_load.pressed.connect(self.__load_file)

        # creating an horizonal box to display the button on
        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_select)
        hbox.addWidget(self.btn_load)
        hbox.setAlignment(Qt.AlignTop)
        frame.setLayout(hbox)

        # call method to display application
        self.__show_application()

    def __select_file(self):
        """
        method used to open a filedialog to let user select a file
        Return:
            None
        """
        file_dialog = QFileDialog.Options()
        file_dialog |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(
            self,
            caption='Select Excel file',
            directory=os.curdir,
            filter='Excel files (*.xlsx)',
            options=file_dialog
        )
        if self.fileName:
            self.statusBar().showMessage(self.os_text+'\t\t\tFile charged.')
        else:
            self.statusBar().showMessage(self.os_text)

    def __load_file(self):
        """
        loading selected file and will launch the preliminary analysis
        Return:
            None
        """
        if self.fileName:
            pass
        else:
            self.statusBar().showMessage(self.os_text + '\t\t\tNo file selected')

    def __show_application(self):
        """
        method used for displaying the application
        Return:
             None
        """
        self.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    gui = UserInterface()
