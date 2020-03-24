import datetime
import time
import sys
import os
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QFont, QBrush
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QApplication, QTableWidget, QHeaderView,
                             QGridLayout, QTableWidgetItem, QLineEdit,
                             QFileDialog, QCheckBox, QMessageBox, QMenu, QInputDialog)


class Qtmainwin(QWidget):
    """
        Qtwindows类
    """

    def __init__(self):
        super().__init__()
        self.Create_database = None
        self.Data_analysis = None
        self.FileSelectionStr = False
        self.ContrastFileSelectionStr = False
        self.initUI()
        self.setUI()

    def initUI(self):
        """
            initUI为窗口方法
        """
        self.setWindowTitle("数据分析")  # 设定窗口名字
        self.setWindowIcon(QIcon("Icon/Main.ico"))  # 指定图标
        self.setWindowOpacity(0.9)  # 透明度
        palette = QPalette()  # 设置背景颜色
        palette.setColor(QPalette.Background, Qt.black)  # 颜色设置
        self.setPalette(palette)  # 主窗口设置颜色为white
        desktop = QApplication.desktop()  # 获取显示器分辨率大小
        screenRect = desktop.screenGeometry()
        height = screenRect.height()
        width = screenRect.width()
        self.setMinimumSize(QSize(width / 2, height / 2))
        self.setMaximumSize(QSize(width / 2, height / 2))

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("Icon/timg.jpg")))
        # palette.setColor(QPalette.Background,Qt.red)
        self.setPalette(palette)
        self.show()  # 启动最大化

    def setUI(self):
        self.Create_database = QPushButton("字典选择")
        self.Create_database.setFixedSize(80, 80)  # 设置按钮大小
        icon = QIcon()
        #icon.addPixmap(QPixmap("./Icon/Create_database.png"), QIcon.Normal, QIcon.Off)  # 选择图标
        self.Create_database.setIcon(icon)  # 设置图标
        self.Create_database.setIconSize(QSize(80, 80))  # 设置图标大小
        self.Create_database.clicked.connect(self.FileSelection)

        self.Data_analysis = QPushButton("对比数据选择")
        self.Data_analysis.setFixedSize(80, 80)  # 设置按钮大小
        icon = QIcon()
        #icon.addPixmap(QPixmap("./Icon/Data_analysis.png"), QIcon.Normal, QIcon.Off)  # 选择图标
        self.Data_analysis.setIcon(icon)  # 设置图标
        self.Data_analysis.setIconSize(QSize(80, 80))  # 设置图标大小
        self.Data_analysis.clicked.connect(self.ContrastFileSelection)

        self.dispose = QPushButton("处理")
        self.dispose.setFixedSize(80, 80)  # 设置按钮大小
        icon = QIcon()
        #icon.addPixmap(QPixmap("./Icon/Data_analysis.png"), QIcon.Normal, QIcon.Off)  # 选择图标
        self.dispose.setIcon(icon)  # 设置图标
        self.dispose.setIconSize(QSize(80, 80))  # 设置图标大小
        self.dispose.clicked.connect(self.ProcessingData)

        self.data = QTableWidget(0, 1)
        self.data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 使所有表格充满行
        self.data.setHorizontalHeaderLabels(['详情'])  # 设置水平方向的表头标签
        self.data.setContextMenuPolicy(Qt.CustomContextMenu)  # 设置允许右键创建
        #        self.data.customContextMenuRequested.connect(self.generateMenu)  # 设置右键函数

        grid = QGridLayout()  # 创建了一个网格布局
        self.setLayout(grid)  # 设置窗口的布局界面
        # grid.setSpacing(2)  # 即各控件之间的上下间距为10（以像素为单位）。同理还有grid.setMargin（int）为设置控件之间的左右间距。
        grid.addWidget(self.Create_database, 0, 0, 1, 1)
        grid.addWidget(self.Data_analysis, 0, 2, 1, 1)
        grid.addWidget(self.dispose, 1, 1, 1, 1)
        grid.addWidget(self.data, 0, 3, 4, 1)

    # def ProcessingProgram(self):

    def FileSelection(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "选取文件", ' ',
                                                         "All Files(*);;Text Files(*.txt)")
        if len(fileName) < 1:
            self.FileSelectionStr = False
            return 0
        self.FileSelectionStr = fileName
        text = '字典选择：' + fileName
        i = self.data.rowCount()  # 获取当前行数
        self.data.insertRow(i)  # 在当前行数下插入一行
        newItem = QTableWidgetItem("%s" % text)  # 写入数据
        self.data.setItem(i, 0, newItem)
        self.data.verticalScrollBar().setValue(self.data.maximumHeight())

    def ContrastFileSelection(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "选取文件", '',
                                                         "All Files(*);;Text Files(*.txt)")

        if len(fileName) < 1:
            self.ContrastFileSelectionStr = False
            return 0
        self.ContrastFileSelectionStr = fileName
        text = '对比文件选择：' + fileName
        i = self.data.rowCount()  # 获取当前行数
        self.data.insertRow(i)  # 在当前行数下插入一行
        newItem = QTableWidgetItem("%s" % text)  # 写入数据
        self.data.setItem(i, 0, newItem)
        self.data.verticalScrollBar().setValue(self.data.maximumHeight())

    def ProcessingData(self):
        if not bool(self.ContrastFileSelectionStr) & bool(self.FileSelectionStr):
            print(1)
            return 0
        Data = dict()
        ErrorData = list()
        with open(self.FileSelectionStr, 'r') as fo:
            text = '字典文件正在读取'
            i = self.data.rowCount()  # 获取当前行数
            self.data.insertRow(i)  # 在当前行数下插入一行
            newItem = QTableWidgetItem("%s" % text)  # 写入数据
            self.data.setItem(i, 0, newItem)
            self.data.verticalScrollBar().setValue(self.data.maximumHeight())
            QApplication.processEvents()
            DictData = fo.readlines()

        with open(self.ContrastFileSelectionStr, 'r') as fo:
            text = '对比文件正在读取'
            i = self.data.rowCount()  # 获取当前行数
            self.data.insertRow(i)  # 在当前行数下插入一行
            newItem = QTableWidgetItem("%s" % text)  # 写入数据
            self.data.setItem(i, 0, newItem)
            self.data.verticalScrollBar().setValue(self.data.maximumHeight())
            QApplication.processEvents()
            CorrelationData = fo.readlines()

        text = '数据正在处理'
        i = self.data.rowCount()  # 获取当前行数
        self.data.insertRow(i)  # 在当前行数下插入一行
        newItem = QTableWidgetItem("%s" % text)  # 写入数据
        self.data.setItem(i, 0, newItem)
        self.data.verticalScrollBar().setValue(self.data.maximumHeight())
        QApplication.processEvents()

        StartTime = time.perf_counter()
        for i in DictData:
            Data[i] = 1
        count = 0
        for i in CorrelationData:
            if i not in Data:
                ErrorData.append(i)
                text = '错误：' + i[0:-1]
                i = self.data.rowCount()  # 获取当前行数
                self.data.insertRow(i)  # 在当前行数下插入一行
                newItem = QTableWidgetItem("%s" % text)  # 写入数据
                self.data.setItem(i, 0, newItem)
                self.data.verticalScrollBar().setValue(self.data.maximumHeight())
                count += 1
                if count > 40000:
                    count = 0
                    QApplication.processEvents()

        EndTime = time.perf_counter()
        text = '处理完成，耗时%sS' % (EndTime - StartTime)
        i = self.data.rowCount()  # 获取当前行数
        self.data.insertRow(i)  # 在当前行数下插入一行
        newItem = QTableWidgetItem("%s" % text)  # 写入数据
        self.data.setItem(i, 0, newItem)
        self.data.verticalScrollBar().setValue(self.data.maximumHeight())
        QApplication.processEvents()

        path = ".\错误数据"
        isExists = os.path.exists(path)  # 判断是否存在这个文件夹
        if not isExists:  # 如果不存在则创建
            os.makedirs(path)

        t = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        with open(path + '\%s错误数据详情.txt' % t, 'w') as fo:
            fo.writelines(ErrorData)

        text = '错误详情已生成'
        i = self.data.rowCount()  # 获取当前行数
        self.data.insertRow(i)  # 在当前行数下插入一行
        newItem = QTableWidgetItem("%s" % text)  # 写入数据
        self.data.setItem(i, 0, newItem)
        self.data.verticalScrollBar().setValue(self.data.maximumHeight())
        QApplication.processEvents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Windows = Qtmainwin()
    sys.exit(app.exec_())
