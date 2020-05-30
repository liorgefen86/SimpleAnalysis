from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QFileDialog, QWidget, QStatusBar, QHBoxLayout, QGridLayout, QLabel
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt
import sys
import platform
import os
from data_analysis import DataAnalysis
import matplotlib
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


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
        self.plot_order = []

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

        self.__set_main_widget()

        # call method to display application
        self.__show_application()

    def __set_main_widget(self):
        # creation of a widget to hold the buttons
        main_widget = QWidget(self)

        # select button will open a filedialog to let the user select the file
        self.btn_select = UserInterface._create_button(
            text='Select file',
            icon_path='icons/select.png',
            connect_fn=self.__select_file
        )

        # load button will load the selected file and start its processing
        self.btn_load = UserInterface._create_button(
            text='Load file',
            icon_path='icons/load.png',
            connect_fn=self.__load_file
        )

        # creating the main layout
        self.main_layout = QGridLayout()

        # creating an horizonal box to display the buttons on
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.btn_select)
        self.hbox.addWidget(self.btn_load)
        self.hbox.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.hbox.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addLayout(self.hbox, 0, 0)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)

    def __select_file(self):
        """
        method used to open a filedialog to let user select a file
        Return:
            None
        """
        if hasattr(self, 'da'):
            for ind in range(self.main_layout.count()):
                layout_item = self.main_layout.itemAt(ind)
                if layout_item.objectName() == 'grid_stats':
                    self.main_layout.removeItem(layout_item)

        self.fileName, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select Excel file',
            directory=os.curdir,
            filter='Excel files (*.xlsx)',
            options=QFileDialog.DontUseNativeDialog
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
            self.da = DataAnalysis.create_object(file_path=self.fileName)
            self.da.get_statistics()

            stats = self.da.stats

            grid = QGridLayout()
            grid.setObjectName('grid_stats')
            self.fields = stats.columns
            self.qties = stats.index

            self.active_buttons = dict()

            for indf, field in enumerate(self.fields, 1):
                self.active_buttons[field] = False
                btn = LabelButton.create_label_button(
                    label=field,
                    window=self,
                    connect_fns=[]
                )

                grid.addWidget(btn, indf, 0)
            for indq, qty in enumerate(self.qties, 1):
                grid.addWidget(QLabel(qty), 0, indq)

            for indf, field in enumerate(self.fields):
                for indq, qty in enumerate(self.qties):
                    grid.addWidget(QLabel(str(stats.iloc[indq, indf])), 1+indf, 1+indq)

            self.main_layout.addLayout(grid, 1, 0, 1, 2)

            if not hasattr(self, 'btn_draw'):
                self.btn_draw = UserInterface._create_button(
                    text='Draw Chart',
                    icon_path='icons/load.png',
                    connect_fn=self.__draw_chart
                )
                self.hbox.addWidget(self.btn_draw)

        else:
            self.statusBar().showMessage(self.os_text + '\t\t\tNo file selected')

    def __draw_chart(self):
        if sum(self.active_buttons.values()) < 2:
            print('Not enough fields were selected.\nPlease select at least 2.')
        else:
            if sum(self.active_buttons.values()) > 2:
                print('More than 2 fields were selected.\nThe plot would use the two first selected ones.')

            if not hasattr(self, 'fig'):
                self.fig = Figure(figsize=(10, 7), dpi=150)
                self.axes = self.da.scatter_plot(
                    self.fig,
                    self.plot_order[0],
                    self.plot_order[1],
                    self.palette().color(QPalette.Background).getRgbF()
                )

                self.canvas = FigureCanvas(self.fig)
                self.canvas.setMinimumSize(self.size().width(), 480)

                self.main_layout.addWidget(self.canvas)
            else:
                self.__update_figure()

    def __update_figure(self):
        self.axes.cla()
        self.axes = self.da.scatter_plot(
            self.fig,
            self.plot_order[0],
            self.plot_order[1],
            self.palette().color(QPalette.Background).getRgbF()
        )
        self.canvas.draw()

    def __show_application(self):
        """
        method used for displaying the application<<<<<
        Return:
             None
        """
        self.show()
        sys.exit(self.app.exec_())

    @staticmethod
    def _create_button(text, icon_path=None, connect_fn=None):
        btn = QPushButton(text)

        if icon_path:
            btn.setIcon(QIcon(icon_path))
        if connect_fn:
            btn.pressed.connect(connect_fn)
        btn.setMinimumWidth(150)
        btn.setMaximumWidth(150)

        return btn


class LabelButton(QPushButton):
    """
    class used for field buttons (quantitative fields found in the selected data)
    Args:
        label [str]: button's label
    Return:
        None
    """
    def __init__(self, label):
        super(LabelButton, self).__init__()

        self.setText(label)
        self.setCheckable(True)
        self.setMaximumHeight(32)

    @staticmethod
    def create_label_button(label, window, connect_fns=None):
        """
        initialize a LabelButton button
        Args:
            label [str]: button's label
            connect_fns [array of functions]: function to connect to the button
        Return:
            LabelButton
        """
        btn = LabelButton(label=label)

        if not hasattr(window, 'active_buttons'):
            window.active_buttons = {label: False}

        # loop through the functions list and assign to the button
        btn.toggle()
        if connect_fns:
            for fn in connect_fns:
                btn.pressed.connect(fn)
        btn.pressed.connect(lambda: LabelButton.toggle_status(window, label))

        return btn

    @staticmethod
    def toggle_status(window, label):
        window.active_buttons[label] = not window.active_buttons[label]
        if window.active_buttons[label]:
            window.plot_order.append(label)
        else:
            window.plot_order.remove(label)


if __name__ == '__main__':
    gui = UserInterface()
