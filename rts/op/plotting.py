import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QThread
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import time
from rts.core.pts import ParaTaskSet
from rts.gen.egen import Egen
from rts.sched.bcl_naive import BCLNaive
from rts.op.stat import Stat
from rts.popt.cho import Cho


class BackgroundTask(QObject):
    """
    BackgroundTask Class work for parallel assignment

    Author : Seong-Hyeon Park
    Data : 02 April 2019
    ..todo::Check graph interface
    Bug : None
    """
    # variable for transmitting signal
    sig_numbers = pyqtSignal(pd.DataFrame, int)

    def __init__(self, parent=None):
        """
        :param parent: for inheritance
        """
        super(self.__class__, self).__init__(parent)

    @pyqtSlot()
    def parallel_assignment(self):
        """
        Function : work for parallel assignment at background
        :return: No return
        """
        # create generator
        gen_param = {
            'num_task': 10,
            'min_exec_time': 30,
            'max_exec_time': 100,
            'min_period': 60,
            'max_period': 200,
            'tot_util': 4.0,
            'util_over': False,
        }
        u = Egen(**gen_param)
        print(u)
        print('--------')

        # logger
        stat_param = {
            'id': 0,
            'min': 0.0,
            'max': 4.0,
            'inc': 0.1,
        }
        stat_single = Stat(**stat_param)
        stat_max = Stat(**stat_param)
        stat_random = Stat(**stat_param)
        stat_cho = Stat(**stat_param)

        num_iter = 100000
        notify_every = 10000

        for i in range(num_iter):
            if i % notify_every == 0:
                print("{} % : {} / {}".format(i * 100 / num_iter, i, num_iter))

            # generate tasks
            ts = u.next_task_set()
            if ts == -1:
                print("error")

            # schedulability check param
            sched_param = {
                'num_core': 4.0,
            }

            # single thread
            pts_param_single = {
                'base_ts': ts,
                'max_option': 4,
                'overhead': 0.1,
                'variance': 0.8,
                'popt_strategy': 'single',
            }
            pts = ParaTaskSet(**pts_param_single)
            pts_util = pts.tot_util()

            # single thread schedulability
            bcl_naive = BCLNaive(**sched_param)
            sched_single = bcl_naive.is_schedulable(pts)
            stat_single.add(pts_util, sched_single)
            stat_single.normalize()
            single_list = stat_single.norm_data

            # max thread
            pts.popt_strategy = 'max'
            pts.serialize_pts()

            # max thread schedulability
            sched_max = bcl_naive.is_schedulable(pts)
            stat_max.add(pts_util, sched_max)
            stat_max.normalize()
            max_list = stat_max.norm_data

            # random thread
            pts.popt_strategy = 'random'
            pts.serialize_pts()
            rnd_selected_option = pts.popt_list

            # random thread schedulability
            sched_random = bcl_naive.is_schedulable(pts)
            stat_random.add(pts_util, sched_random)
            stat_random.normalize()
            random_list = stat_random.norm_data

            # cho
            pts.popt_strategy = 'custom'
            pts.serialize_pts()

            # cho schedulability
            popt_param = {
                'num_core': 4.0,
                'max_option': 4,
            }

            cho = Cho(**popt_param)
            sched_cho = cho.is_schedulable(pts)

            stat_cho.add(pts_util, sched_cho)
            stat_cho.normalize()
            cho_list = stat_cho.norm_data

            if not sched_cho:
                if sched_single or sched_max or sched_random:
                    print('!!something wrong')
                    # print(pts)
                if sched_single:
                    print('sched_single')
                if sched_max:
                    print('sched_max')
                if sched_random:
                    print('sched_random')
                    print('rnd dbg:')
                    print(rnd_selected_option)
                    rnd_dbg = cho.is_schedulable_dbg(pts, rnd_selected_option)
                    print(rnd_dbg)
                    print('cho verbose result:')
                    _, cho_selected_option = cho.is_schedulable_verbose(pts)
                    print('cho dbg:')
                    print(cho_selected_option)
                    cho_dbg = cho.is_schedulable_dbg(pts, cho_selected_option)
                    print(rnd_dbg)

            concat_data = {
                           'single': single_list,
                           'random': random_list,
                           'max': max_list,
                           'cho': cho_list}
            data_frame = pd.DataFrame(concat_data)
            self.sig_numbers.emit(data_frame, num_iter)
            time.sleep(0.1)


class Window(QWidget):
    """
    Window Class is making GUI

    Author : Seong-Hyeon Park
    Data : 02 April 2019
    ..todo::None
    Bug : None
    """
    def __init__(self):
        """
        Function : initialize UI components
        """
        super().__init__()
        self.setGeometry(600, 200, 1200, 600)
        self.setWindowTitle("Plotting Middle Result")
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.sub_plot = self.fig.add_subplot(111)
        self.tableWidget = QTableWidget()
        self.button_start = QPushButton('Start', self)
        self.set_up()

    def set_up(self):
        """
        Function: set up UI components
        :return: None
        """
        self.sub_plot.set_title('Parallel Assignment Graph')
        self.canvas.draw()

        # Table setting
        self.tableWidget.setRowCount(40)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Single", "Max","Random", "Cho"])

        # Left Layout
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.canvas)

        # Right Layout
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.tableWidget)
        right_layout.addWidget(self.button_start)

        # Compiling Layout
        whole_layout = QHBoxLayout()
        whole_layout.addLayout(left_layout)
        whole_layout.addLayout(right_layout)
        whole_layout.setStretchFactor(left_layout, 1)
        whole_layout.setStretchFactor(right_layout, 1)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.setLayout(whole_layout)

    @pyqtSlot(pd.DataFrame, int)
    def update_status(self, data_frame, num_iter):
        """
        Function : receiving signals for update table and graph
        :param data_frame: receive signal for list
        :param num_iter: receive signal for iteration
        :return: None
        """
        if num_iter % 100000 == 0:
            self.sub_plot.cla()
            self.sub_plot.plot('single', data=data_frame, marker='', color='blue', label="single")
            self.sub_plot.plot('random', data=data_frame, marker='', color='yellow', linewidth=2, label="random")
            self.sub_plot.plot('max', data=data_frame, marker='', color='red', linewidth=2, label="max")
            self.sub_plot.plot('cho', data=data_frame, marker='', color='green', linewidth=2, label="cho")
            self.sub_plot.legend()
            self.canvas.draw()

        for row in range(0, 40):
            for col in range(0, 4):
                result = str('{:.5f}'.format(data_frame.iloc[row, col]))
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(result)))


class MainLoop(QObject):
    """
    MainLoop Class controls GUI object and background tasks

    Author : Seong-Hyeon Park
    Data : 02 April 2019
    ..todo::None
    Bug : None
    """
    def __init__(self, parent=None):
        """
        Function : initialize GUI components and start background task
        :param parent: for inheritance
        """
        super(self.__class__, self).__init__(parent)

        self.gui = Window()
        self.background_task = BackgroundTask()
        self.background_thread = QThread()
        self.background_task.moveToThread(self.background_thread)
        self.background_thread.start()
        self.connect_signal()
        self.gui.show()

    def connect_signal(self):
        """
        Function : when button clicked, background task starts, and update GUI
        :return: None
        """
        self.gui.button_start.clicked.connect(self.background_task.parallel_assignment)
        self.background_task.sig_numbers.connect(self.gui.update_status)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    plot = Window()
    plot.show()
    main = MainLoop(app)
    sys.exit(app.exec())
