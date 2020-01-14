import sys

import matplotlib
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure

from newuiv4_4 import Ui_MainWindow
import sip
import calculate as cal
import manage
import re
import datetime

init_point = [20, 20]


# —— —— —— 绘图画布初始 —— —— ——
# 绘图画布
class MyFigure(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)


# 绘图主函数
class Application(QMainWindow, Ui_MainWindow):
    step = 0
    #	引入一个路径变量，这样可以将文件引入以及，结果用连个按钮分步进行。
    filename = None

    def __init__(self, parent=None):
        super(Application, self).__init__(parent)
        self.setupUi(self)

    #  —— —— —— 自定义地块（矩形） —— —— ——
    # 自定义矩形地块显示函数
    def Custom_field(self):
        self.F = MyFigure(width=3, height=2, dpi=100)
        rec_width = float(self.lineEdit.text())
        rec_height = float(self.lineEdit_2.text())
        rec_list = [*init_point, rec_width, rec_height, 0]
        rectangle = cal.Rectangle(*rec_list)
        self.F.axes.plot(rectangle[0], rectangle[1], linewidth=1, color="blue")
        self.F.axes.axis('equal')
        self.horizontalLayout.addWidget(self.F)

    # 自定义矩形地块显示更新函数
    def Call_Custom_field(self):
        self.step += 1
        if self.step == 1:
            self.Custom_field()
        else:
            sip.delete(self.F)
            self.Custom_field()
        # 按钮6，调用地块显示更新

    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        self.Call_Custom_field()

    # —— —— —— 实际地块(可处理倾斜矩形) —— —— ——
    # Kml解析函数，返回GPS坐标值
    def Import_Kml(self):
        fname = QFileDialog.getOpenFileName(self, '打开文件', './', "Kml Files(*.kml);;\
			All Files(*)")
        self.filename = fname[0]
        if fname[0]:
            #			f = QtCore.QFile(fname[0])
            f = open(fname[0], 'r', encoding='utf-8')
            with f:
                data = f.read()
            f.close()
            c = re.sub(r"\s|<|>", "", data)
            d = re.findall(r"([0-9]+\.[0-9]{13})", c)
            f = list(map(float, d[0::]))
            return f
        else:
            pass

    # GPS转UTM，并绘制实际地块。
    def UTM_field(self):
        self.F = MyFigure(width=3, height=2, dpi=100)
        d = self.Import_Kml()
        if d:
            x = []
            y = []
            for a in range(0, len(d) - 1, 2):
                m, n = cal.wgs84toutm(d[a], d[a + 1])
                x.append(m)
                y.append(n)
            x_move = x[0] - 20
            y_move = y[0] - 20
            for b in range(0, len(x)):
                x[b] = x[b] - x_move
                y[b] = y[b] - y_move
            self.F.axes.plot(x, y)
            self.F.axes.axis('equal')
            self.horizontalLayout.addWidget(self.F)
        else:
            pass

    # 设置步数，更新画布，调用UTM_field函数绘图
    def IMP_field(self):
        self.step += 1
        if self.step == 1:
            self.UTM_field()
        else:
            sip.delete(self.F)
            self.UTM_field()

    # 按钮3,调用实际地块显示更新
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        self.IMP_field()

    # —— —— —— 地块以及路径等详细信息显示功能块 —— —— ——
    # 计算地块路径线等坐标信息
    def Field_Route_info(self, rec_width, rec_height, path_width, turn_r, curve, straight, \
                         not_reverse, EX, GREE, offset_para):
        # 原始地块
        rectangle = cal.Rectangle(*init_point, rec_width, rec_height, 0)
        # 地头预留的偏置宽度
        offset_width = cal.Offset_width(turn_r, path_width, not_reverse, offset_para)
        # 内部矩形块、幅宽线，环形作业组、矩形作业转弯点
        rec_offset = cal.Rec_Offset(*init_point, rec_width, rec_height, offset_width)
        offset_parallel = cal.Offset_Parallel(*init_point, rec_width, rec_height, \
                                              offset_width, path_width)
        rec_mutil_offsets = cal.Rec_Mutil_offsets(*init_point, rec_width, rec_height, offset_width, \
                                                  path_width)
        top_point, low_point = cal.Rec_turn_point(*init_point, rec_width, rec_height, \
                                                  offset_width, path_width)

        # 调用调度算法
        if GREE:  # goole or-tools
            all_turn_length, row_list, all_turn_name = manage.main(*init_point, rec_width, \
                                                                   rec_height, offset_width, path_width, turn_r, curve,
                                                                   straight, not_reverse)
        if EX:  # 经验算法
            all_turn_length, row_list, all_turn_name = manage.Experience(*init_point, rec_width, \
                                                                         rec_height, offset_width, path_width, turn_r,
                                                                         curve, straight, not_reverse)

        # 矩形转弯线、路径线，环形路径线、转弯线，环形跨度线（作业路径）
        # 矩形路径（*row_list为了对最后一个作业行进行补长、截短）
        rectangle_routes = cal.Rectangle_routes(*init_point, rec_width, rec_height, offset_width, \
                                                turn_r, path_width, row_list, offset_para)
        circle_routes = cal.Circle_routes(*init_point, rec_width, rec_height, top_point, low_point, \
                                          row_list, offset_width, path_width, turn_r)
        circle_turn = cal.Circle_turn(*init_point, rec_width, rec_height, offset_width, path_width, \
                                      turn_r)
        # 环形行间跨行（*其中有部分是不作业的）
        c2c_turn = cal.C2C_turn(top_point, low_point, row_list, turn_r, offset_width, path_width)
        x_, y_ = cal.Row_mark(row_list, top_point, low_point, path_width)

        # 进入线、矩形转弯线（非作业路径）
        route_in = cal.Rec_Route_In(*init_point, rec_width, rec_height, offset_width, path_width)
        all_turn = cal.All_Turn(*init_point, rec_width, rec_height, row_list, offset_width, \
                                path_width, turn_r, all_turn_name)

        # 矩形路径方向标识、环形路径方向标识（辅助功能）
        up_direction, down_direction = cal.Line_direction(row_list, top_point, low_point, \
                                                          path_width)
        circle_direction = cal.Circle_direction(*init_point, rec_width, rec_height, offset_width, \
                                                path_width, top_point, low_point, row_list)
        # 长度计算
        circle_turn_length = cal.Circle_turn_length(offset_width, path_width, turn_r)
        circle_route_length = cal.Circle_route_length(*init_point, rec_width, rec_height, top_point, \
                                                      low_point, row_list, offset_width, path_width, turn_r)
        c2c_turn_length = cal.C2C_turn_length(offset_width, turn_r, path_width)
        rec_route_length = cal.Rec_Route_length(*init_point, rec_width, rec_height, turn_r, path_width, \
                                                row_list, offset_para)
        rec_route_in_length = cal.Rec_Route_In_length(offset_width)

        work_length = circle_turn_length + circle_route_length + c2c_turn_length + rec_route_length
        none_work_length = rec_route_in_length + all_turn_length
        work_length = round(work_length, 2)
        none_work_length = round(none_work_length, 2)
        return rectangle, rec_offset, route_in, rec_mutil_offsets, circle_routes, circle_turn, \
               offset_parallel, rectangle_routes, all_turn, c2c_turn, up_direction, down_direction, \
               circle_direction, x_, y_, row_list, work_length, none_work_length

    # 计算实际地块路径等各种信息
    def Field_Route_info2(self, rec_width, rec_height, path_width, turn_r, curve, straight, \
                          not_reverse, EX, GREE, radian1, offset_para):

        rectangle, rec_offset, route_in, rec_mutil_offsets, circle_routes, circle_turn, \
        offset_parallel, rectangle_routes, all_turn, c2c_turn, up_direction, \
        down_direction, circle_direction, x_, y_, row_list, work_length, none_work_length = \
            self.Field_Route_info(rec_width, rec_height, path_width, turn_r, curve, straight, \
                                  not_reverse, EX, GREE, offset_para)

        rectangle = cal.revert_1_field(rectangle, radian1)
        rec_offset = cal.revert_1_field(rec_offset, radian1)
        route_in = cal.revert_1_field(route_in, radian1)
        x_, y_ = cal.revert_1_field([x_, y_], radian1)
        rec_mutil_offsets = cal.revert_2_field(rec_mutil_offsets, radian1)
        circle_routes = cal.revert_2_field(circle_routes, radian1)
        circle_turn = cal.revert_2_field(circle_turn, radian1)
        offset_parallel = cal.revert_2_field(offset_parallel, radian1)
        rectangle_routes = cal.revert_2_field(rectangle_routes, radian1)
        all_turn = cal.revert_2_field(all_turn, radian1)

        c2c_turn = cal.revert_2_field(c2c_turn, radian1)
        up_direction = cal.revert_2_field(up_direction, radian1)
        down_direction = cal.revert_2_field(down_direction, radian1)
        circle_direction = cal.revert_2_field(circle_direction, radian1)
        row_list = row_list
        work_length = round(work_length, 2)
        none_work_length = round(none_work_length, 2)

        return rectangle, rec_offset, route_in, rec_mutil_offsets, circle_routes, circle_turn, \
               offset_parallel, rectangle_routes, all_turn, c2c_turn, up_direction, \
               down_direction, circle_direction, x_, y_, row_list, work_length, none_work_length

    # 地块路径等各种信息显示
    def Display(self, origin, rectangle, rec_offset, route_in, rec_mutil_offsets, circle_routes, \
                circle_turn, offset_parallel, rectangle_routes, all_turn, c2c_turn, \
                up_direction, down_direction, circle_direction, x_, y_, row_list, work_length, none_work_length):

        # 一级数据结构（具体形式参见calculate）
        self.F = MyFigure(width=3, height=2, dpi=100)
        self.F.axes.plot(rectangle[0], rectangle[1], linewidth=1, color='blue')
        self.F.axes.plot(rec_offset[0], rec_offset[1], linewidth=1, color="blue")

        if origin:
            self.F.axes.plot(origin[0], origin[1], linewidth=1, color="blue", linestyle="--")

        # 进入矩形工作区路径线
        self.F.axes.plot(route_in[0], route_in[1], linewidth=1, color="red", linestyle="--")

        # 二级数据结构（具体形式参见calculate）
        for x in rec_mutil_offsets:
            self.F.axes.plot(x[0], x[1], linewidth=1, color="blue")

        for x in circle_routes:
            self.F.axes.plot(x[0], x[1], linewidth=1, color="coral", linestyle="--")
        for x in circle_turn:
            self.F.axes.plot(x[0], x[1], linewidth=1, color="coral", linestyle="--")
        for x in offset_parallel:
            self.F.axes.plot(x[0], x[1], linewidth=1, color="blue")
        for x in rectangle_routes:
            self.F.axes.plot(x[0], x[1], color="red", linewidth=1, linestyle="--")
        for x in all_turn:
            self.F.axes.plot(x[0], x[1], color="red", linewidth=1, linestyle="--")

        # 绘制环形行间转弯
        for x in c2c_turn:
            self.F.axes.plot(x[0], x[1], color="coral", linewidth=1, linestyle="--")

        # 绘制转弯的方向指示箭头。
        for x in up_direction:
            self.F.axes.plot(x[0], x[1], linewidth=1, color="blue")
        for x in down_direction:
            self.F.axes.plot(x[0], x[1], linewidth=1, color="red")
        # 环形行方向指示箭头。
        for x in circle_direction:
            self.F.axes.plot(x[0], x[1], linewidth=1, color="red")
        # 行号标记
        self.F.axes.axis("equal")

    # 做逻辑判断，根据turn_r与(path_width)/2的关系分为：n、o、T型转弯。
    # 根据有无倒车特性，再进一步划分转弯方式。
    # 函数自调有问题，需改进。

    # —— —— —— tab1，自定义地块路径展示 —— —— ——
    def Info_get(self):
        rec_width = float(self.lineEdit.text())
        rec_height = float(self.lineEdit_2.text())
        path_width = float(self.lineEdit_3.text())
        turn_r = float(self.lineEdit_4.text())
        offset_para = int(self.lineEdit_9.text())
        curve = self.radioButton_2.isChecked()
        straight = self.radioButton.isChecked()
        not_reverse = self.radioButton_3.isChecked()
        EX = self.radioButton_7.isChecked()
        GREE = self.radioButton_8.isChecked()
        return rec_width, rec_height, path_width, turn_r, curve, straight, not_reverse, EX, GREE, \
               offset_para

    def Call_Display(self):
        # 此正则表达式仍不能阻止例如：, '等符号。
        my_regex = QtCore.QRegExp("[0-9].[0-9]")
        my_validator = QtGui.QRegExpValidator(my_regex, self.lineEdit_4)
        self.lineEdit_4.setValidator(my_validator)
        self.step += 1
        rec_width, rec_height, path_width, turn_r, curve, straight, not_reverse, EX, GREE, \
        offset_para = self.Info_get()
        rectangle, rec_offset, route_in, rec_mutil_offsets, circle_routes, circle_turn, \
        offset_parallel, rectangle_routes, all_turn, c2c_turn, up_direction, \
        down_direction, circle_direction, x_, y_, row_list, work_length, none_work_length = \
            self.Field_Route_info(rec_width, rec_height, path_width, turn_r, curve, straight, \
                                  not_reverse, EX, GREE, offset_para)

        if self.step == 1:
            time_start = datetime.datetime.now()
            self.Display(None, rectangle, rec_offset, route_in, rec_mutil_offsets, circle_routes, \
                         circle_turn, offset_parallel, rectangle_routes, all_turn, c2c_turn, \
                         up_direction, down_direction, circle_direction, x_, y_, row_list, \
                         work_length, none_work_length)

            for i, (_x, _y) in enumerate(zip(x_, y_)):
                self.F.axes.text(_x, _y, str(i), color="red", ha="center")
            self.horizontalLayout.addWidget(self.F)
            # browser中显示路径的计算结果信息。
            display_list = "Row_list:"
            for x in row_list:
                if x == row_list[-1]:
                    display_list = display_list + str(x)
                else:
                    display_list = display_list + str(x) + "—"
            all_length = round(work_length + none_work_length, 2)
            all_length = str(all_length)
            work_length = str(work_length)
            none_work_length = str(none_work_length)

            time_end = datetime.datetime.now()
            runtime = time_end - time_start
            runtime_display = "{}s {}ms".format(runtime.seconds, \
                                                round(runtime.microseconds / 1000))
            self.textBrowser.setText(display_list + "\nWork_Length:" + work_length + \
                                     "m\nNone_Work_Length:" + none_work_length + \
                                     "m\nAll_length:" + all_length + "m\nRunTime:" + runtime_display)
        else:
            sip.delete(self.F)
            time_start = datetime.datetime.now()
            self.Display(None, rectangle, rec_offset, route_in, rec_mutil_offsets, circle_routes, \
                         circle_turn, offset_parallel, rectangle_routes, all_turn, c2c_turn, \
                         up_direction, down_direction, circle_direction, x_, y_, row_list, \
                         work_length, none_work_length)

            for i, (_x, _y) in enumerate(zip(x_, y_)):
                self.F.axes.text(_x, _y, str(i), color="red", ha="center")
            self.horizontalLayout.addWidget(self.F)
            # browser中显示路径的计算结果信息。
            display_list = "Row_list:"
            for x in row_list:
                if x == row_list[-1]:
                    display_list = display_list + str(x)
                else:
                    display_list = display_list + str(x) + "—"
            all_length = round(work_length + none_work_length, 2)
            all_length = str(all_length)
            work_length = str(work_length)
            none_work_length = str(none_work_length)

            time_end = datetime.datetime.now()
            runtime = time_end - time_start
            runtime_display = "{}s {}ms".format(runtime.seconds, \
                                                round(runtime.microseconds / 1000))
            self.textBrowser.setText(display_list + "\nWork_Length:" + work_length + \
                                     "m\nNone_Work_Length:" + none_work_length + \
                                     "m\nAll_length:" + all_length + "m\nRunTime:" + runtime_display)

    @pyqtSlot()
    def on_pushButton_8_clicked(self):
        self.Call_Display()

    # —— —— —— tab2，实际地块路径展示 —— —— ——
    def GPS_get(self):
        self.F = MyFigure(width=3, height=2, dpi=100)
        filename = self.filename
        print("filename", filename)
        if filename:
            f = open(filename, 'r', encoding="utf-8")
            with f:
                data = f.read()
            f.close()
            c = re.sub(r"\s|<|>", "", data)
            d = re.findall(r"([0-9]+\.[0-9]{13})", c)
            f = list(map(float, d[0::]))
            return f
        else:
            pass

    def UTM_get(self):
        d = self.GPS_get()
        if d:
            x = []
            y = []
            for a in range(0, len(d) - 1, 2):
                m, n = cal.wgs84toutm(d[a], d[a + 1])
                x.append(m)
                y.append(n)
            x_move = x[0] - 20
            y_move = y[0] - 20
            for b in range(0, len(x)):
                x[b] = x[b] - x_move
                y[b] = y[b] - y_move
            return x, y
        else:
            pass

    def IMP_Field_display(self):
        x, y = self.UTM_get()
        self.F.axes.plot(x, y)
        self.F.axes.axis('equal')

    def IMP_Field_info(self):
        x, y = self.UTM_get()
        x, y, radian1 = cal.Standard_field(x, y)
        l1 = ((x[1] - x[0]) ** 2 + (y[1] - y[0]) ** 2) ** .5
        l2 = ((x[2] - x[1]) ** 2 + (y[2] - y[1]) ** 2) ** .5
        l3 = ((x[3] - x[2]) ** 2 + (y[3] - y[2]) ** 2) ** .5
        l4 = ((x[4] - x[3]) ** 2 + (y[4] - y[3]) ** 2) ** .5

        rec_width = (l1 + l3) / 2
        rec_height = (l2 + l4) / 2
        path_width = float(self.lineEdit_5.text())
        turn_r = float(self.lineEdit_8.text())
        offset_para = int(self.lineEdit_10.text())
        curve = self.radioButton_11.isChecked()
        straight = self.radioButton_10.isChecked()
        not_reverse = self.radioButton_9.isChecked()
        EX = self.radioButton_12.isChecked()
        GREE = self.radioButton_13.isChecked()
        return rec_width, rec_height, path_width, turn_r, curve, straight, not_reverse, EX, GREE, \
               radian1, offset_para

    def IMP_Field_Route_info_display(self):
        time_start = datetime.datetime.now()
        rec_width, rec_height, path_width, turn_r, curve, straight, not_reverse, EX, GREE, radian1, \
        offset_para = self.IMP_Field_info()
        rectangle, rec_offset, route_in, rec_mutil_offsets, circle_routes, circle_turn, \
        offset_parallel, rectangle_routes, all_turn, c2c_turn, up_direction, \
        down_direction, circle_direction, x_, y_, row_list, work_length, none_work_length = \
            self.Field_Route_info2(rec_width, rec_height, path_width, turn_r, curve, straight, \
                                   not_reverse, EX, GREE, radian1, offset_para)
        origin = self.UTM_get()
        self.Display(origin, rectangle, rec_offset, route_in, rec_mutil_offsets, circle_routes, \
                     circle_turn, offset_parallel, rectangle_routes, all_turn, c2c_turn, \
                     up_direction, down_direction, circle_direction, x_, y_, row_list, \
                     work_length, none_work_length)
        for i, (_x, _y) in enumerate(zip(x_, y_)):
            self.F.axes.text(_x, _y, str(i), color="red", ha="center")
        self.horizontalLayout.addWidget(self.F)
        display_list = "Row_list:"
        for x in row_list:
            if x == row_list[-1]:
                display_list = display_list + str(x)
            else:
                display_list = display_list + str(x) + "—"
        all_length = round(work_length + none_work_length, 2)
        all_length = str(all_length)
        work_length = str(work_length)
        none_work_length = str(none_work_length)

        time_end = datetime.datetime.now()
        runtime = time_end - time_start
        runtime_display = "{}s {}ms".format(runtime.seconds, round(runtime.microseconds / 1000))
        self.textBrowser_2.setText(display_list + "\nWork_Length:" + work_length + \
                                   "m\nNone_Work_Length:" + none_work_length + \
                                   "m\nAll_length:" + all_length + "m\nRunTime:" + runtime_display)

    # 按钮9，显示地块及路径结果
    def Call_update(self):
        self.step += 1
        if self.step == 1:
            self.IMP_Field_Route_info_display()
        else:
            sip.delete(self.F)
            self.IMP_Field_Route_info_display()

    @pyqtSlot()
    def on_pushButton_9_clicked(self):
        self.Call_update()


if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    aw = Application()
    aw.show()
    sys.exit(qApp.exec_())
