# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpinBox, QSplitter, QStatusBar, QTabWidget,
    QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(952, 819)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Vertical)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.gridLayout_5 = QGridLayout(self.widget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.pushButtonSelectModel = QPushButton(self.widget_2)
        self.pushButtonSelectModel.setObjectName(u"pushButtonSelectModel")

        self.gridLayout_3.addWidget(self.pushButtonSelectModel, 0, 0, 1, 1)

        self.lineEditSelectModel = QLineEdit(self.widget_2)
        self.lineEditSelectModel.setObjectName(u"lineEditSelectModel")
        self.lineEditSelectModel.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEditSelectModel, 0, 1, 1, 1)

        self.pushButtonSelectDataset = QPushButton(self.widget_2)
        self.pushButtonSelectDataset.setObjectName(u"pushButtonSelectDataset")

        self.gridLayout_3.addWidget(self.pushButtonSelectDataset, 1, 0, 1, 1)

        self.lineEditSelectDataset = QLineEdit(self.widget_2)
        self.lineEditSelectDataset.setObjectName(u"lineEditSelectDataset")
        self.lineEditSelectDataset.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEditSelectDataset, 1, 1, 1, 1)

        self.tabWidget = QTabWidget(self.widget_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.trainTab = QWidget()
        self.trainTab.setObjectName(u"trainTab")
        self.gridLayout = QGridLayout(self.trainTab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButtonTrain = QPushButton(self.trainTab)
        self.pushButtonTrain.setObjectName(u"pushButtonTrain")

        self.gridLayout.addWidget(self.pushButtonTrain, 3, 2, 1, 1)

        self.groupBoxArguments = QGroupBox(self.trainTab)
        self.groupBoxArguments.setObjectName(u"groupBoxArguments")
        self.gridLayout_2 = QGridLayout(self.groupBoxArguments)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.labelBatch = QLabel(self.groupBoxArguments)
        self.labelBatch.setObjectName(u"labelBatch")

        self.gridLayout_2.addWidget(self.labelBatch, 2, 0, 1, 1)

        self.comboBoxSizeImage = QComboBox(self.groupBoxArguments)
        self.comboBoxSizeImage.addItem("")
        self.comboBoxSizeImage.addItem("")
        self.comboBoxSizeImage.setObjectName(u"comboBoxSizeImage")

        self.gridLayout_2.addWidget(self.comboBoxSizeImage, 3, 1, 1, 1)

        self.labelSizeImage = QLabel(self.groupBoxArguments)
        self.labelSizeImage.setObjectName(u"labelSizeImage")

        self.gridLayout_2.addWidget(self.labelSizeImage, 3, 0, 1, 1)

        self.spinBoxPatience = QSpinBox(self.groupBoxArguments)
        self.spinBoxPatience.setObjectName(u"spinBoxPatience")
        self.spinBoxPatience.setMinimum(10)
        self.spinBoxPatience.setMaximum(100)
        self.spinBoxPatience.setSingleStep(10)

        self.gridLayout_2.addWidget(self.spinBoxPatience, 1, 1, 1, 1)

        self.labelDevice = QLabel(self.groupBoxArguments)
        self.labelDevice.setObjectName(u"labelDevice")

        self.gridLayout_2.addWidget(self.labelDevice, 6, 0, 1, 1)

        self.labelOptimizer = QLabel(self.groupBoxArguments)
        self.labelOptimizer.setObjectName(u"labelOptimizer")

        self.gridLayout_2.addWidget(self.labelOptimizer, 8, 0, 1, 1)

        self.spinBoxEpochs = QSpinBox(self.groupBoxArguments)
        self.spinBoxEpochs.setObjectName(u"spinBoxEpochs")
        self.spinBoxEpochs.setMinimum(1)
        self.spinBoxEpochs.setMaximum(9999)
        self.spinBoxEpochs.setSingleStep(10)

        self.gridLayout_2.addWidget(self.spinBoxEpochs, 0, 1, 1, 1)

        self.labelSavePeriod = QLabel(self.groupBoxArguments)
        self.labelSavePeriod.setObjectName(u"labelSavePeriod")

        self.gridLayout_2.addWidget(self.labelSavePeriod, 4, 0, 1, 1)

        self.labelEpochs = QLabel(self.groupBoxArguments)
        self.labelEpochs.setObjectName(u"labelEpochs")

        self.gridLayout_2.addWidget(self.labelEpochs, 0, 0, 1, 1)

        self.spinBoxBatch = QSpinBox(self.groupBoxArguments)
        self.spinBoxBatch.setObjectName(u"spinBoxBatch")
        self.spinBoxBatch.setMinimum(8)
        self.spinBoxBatch.setMaximum(128)
        self.spinBoxBatch.setSingleStep(8)

        self.gridLayout_2.addWidget(self.spinBoxBatch, 2, 1, 1, 1)

        self.labelPatience = QLabel(self.groupBoxArguments)
        self.labelPatience.setObjectName(u"labelPatience")

        self.gridLayout_2.addWidget(self.labelPatience, 1, 0, 1, 1)

        self.labelWorkers = QLabel(self.groupBoxArguments)
        self.labelWorkers.setObjectName(u"labelWorkers")

        self.gridLayout_2.addWidget(self.labelWorkers, 7, 0, 1, 1)

        self.spinBoxSavePeriod = QSpinBox(self.groupBoxArguments)
        self.spinBoxSavePeriod.setObjectName(u"spinBoxSavePeriod")
        self.spinBoxSavePeriod.setMinimum(-1)
        self.spinBoxSavePeriod.setMaximum(100)
        self.spinBoxSavePeriod.setSingleStep(10)
        self.spinBoxSavePeriod.setValue(-1)

        self.gridLayout_2.addWidget(self.spinBoxSavePeriod, 4, 1, 1, 1)

        self.comboBoxDevice = QComboBox(self.groupBoxArguments)
        self.comboBoxDevice.addItem("")
        self.comboBoxDevice.addItem("")
        self.comboBoxDevice.setObjectName(u"comboBoxDevice")

        self.gridLayout_2.addWidget(self.comboBoxDevice, 6, 1, 1, 1)

        self.spinBoxWorkers = QSpinBox(self.groupBoxArguments)
        self.spinBoxWorkers.setObjectName(u"spinBoxWorkers")
        self.spinBoxWorkers.setMinimum(1)
        self.spinBoxWorkers.setMaximum(8)

        self.gridLayout_2.addWidget(self.spinBoxWorkers, 7, 1, 1, 1)

        self.comboBoxOptimizer = QComboBox(self.groupBoxArguments)
        self.comboBoxOptimizer.addItem("")
        self.comboBoxOptimizer.addItem("")
        self.comboBoxOptimizer.addItem("")
        self.comboBoxOptimizer.addItem("")
        self.comboBoxOptimizer.addItem("")
        self.comboBoxOptimizer.addItem("")
        self.comboBoxOptimizer.addItem("")
        self.comboBoxOptimizer.setObjectName(u"comboBoxOptimizer")

        self.gridLayout_2.addWidget(self.comboBoxOptimizer, 8, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBoxArguments, 2, 0, 1, 3)

        self.tabWidget.addTab(self.trainTab, "")
        self.inferenceTab = QWidget()
        self.inferenceTab.setObjectName(u"inferenceTab")
        self.tabWidget.addTab(self.inferenceTab, "")

        self.gridLayout_3.addWidget(self.tabWidget, 2, 0, 1, 2)


        self.gridLayout_5.addWidget(self.widget_2, 0, 0, 1, 1)

        self.widgetVisualize = QWidget(self.widget)
        self.widgetVisualize.setObjectName(u"widgetVisualize")
        sizePolicy.setHeightForWidth(self.widgetVisualize.sizePolicy().hasHeightForWidth())
        self.widgetVisualize.setSizePolicy(sizePolicy)
        self.gridLayout_4 = QGridLayout(self.widgetVisualize)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.graphicsView = QGraphicsView(self.widgetVisualize)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout_4.addWidget(self.graphicsView, 1, 1, 1, 3)

        self.lineEditCurrentImg = QLineEdit(self.widgetVisualize)
        self.lineEditCurrentImg.setObjectName(u"lineEditCurrentImg")

        self.gridLayout_4.addWidget(self.lineEditCurrentImg, 2, 1, 1, 1)

        self.toolButtonPrev = QToolButton(self.widgetVisualize)
        self.toolButtonPrev.setObjectName(u"toolButtonPrev")
        self.toolButtonPrev.setArrowType(Qt.LeftArrow)

        self.gridLayout_4.addWidget(self.toolButtonPrev, 1, 0, 1, 1)

        self.pushButtonLoadResults = QPushButton(self.widgetVisualize)
        self.pushButtonLoadResults.setObjectName(u"pushButtonLoadResults")

        self.gridLayout_4.addWidget(self.pushButtonLoadResults, 2, 3, 1, 1)

        self.labelCurrentImg = QLabel(self.widgetVisualize)
        self.labelCurrentImg.setObjectName(u"labelCurrentImg")

        self.gridLayout_4.addWidget(self.labelCurrentImg, 2, 0, 1, 1)

        self.toolButtonNext = QToolButton(self.widgetVisualize)
        self.toolButtonNext.setObjectName(u"toolButtonNext")
        self.toolButtonNext.setArrowType(Qt.RightArrow)

        self.gridLayout_4.addWidget(self.toolButtonNext, 1, 4, 1, 1)


        self.gridLayout_5.addWidget(self.widgetVisualize, 0, 1, 1, 1)

        self.splitter.addWidget(self.widget)
        self.plainTextEditLog = QPlainTextEdit(self.splitter)
        self.plainTextEditLog.setObjectName(u"plainTextEditLog")
        sizePolicy.setHeightForWidth(self.plainTextEditLog.sizePolicy().hasHeightForWidth())
        self.plainTextEditLog.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        self.plainTextEditLog.setFont(font)
        self.splitter.addWidget(self.plainTextEditLog)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 952, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"YoloQT", None))
#if QT_CONFIG(tooltip)
        self.pushButtonSelectModel.setToolTip(QCoreApplication.translate("MainWindow", u"Opens dialog and lets you select model for training", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonSelectModel.setText(QCoreApplication.translate("MainWindow", u"Select model", None))
        self.lineEditSelectModel.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selected model path", None))
        self.pushButtonSelectDataset.setText(QCoreApplication.translate("MainWindow", u"Select dataset", None))
        self.lineEditSelectDataset.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selected dataset path", None))
        self.pushButtonTrain.setText(QCoreApplication.translate("MainWindow", u"Train", None))
        self.groupBoxArguments.setTitle(QCoreApplication.translate("MainWindow", u"Arguments", None))
        self.labelBatch.setText(QCoreApplication.translate("MainWindow", u"Batch", None))
        self.comboBoxSizeImage.setItemText(0, QCoreApplication.translate("MainWindow", u"416", None))
        self.comboBoxSizeImage.setItemText(1, QCoreApplication.translate("MainWindow", u"640", None))

#if QT_CONFIG(tooltip)
        self.comboBoxSizeImage.setToolTip(QCoreApplication.translate("MainWindow", u"imgsz", None))
#endif // QT_CONFIG(tooltip)
        self.labelSizeImage.setText(QCoreApplication.translate("MainWindow", u"Image size", None))
#if QT_CONFIG(tooltip)
        self.spinBoxPatience.setToolTip(QCoreApplication.translate("MainWindow", u"patience", None))
#endif // QT_CONFIG(tooltip)
        self.labelDevice.setText(QCoreApplication.translate("MainWindow", u"Device", None))
        self.labelOptimizer.setText(QCoreApplication.translate("MainWindow", u"Optimizer", None))
#if QT_CONFIG(tooltip)
        self.spinBoxEpochs.setToolTip(QCoreApplication.translate("MainWindow", u"epochs", None))
#endif // QT_CONFIG(tooltip)
        self.labelSavePeriod.setText(QCoreApplication.translate("MainWindow", u"Save period", None))
        self.labelEpochs.setText(QCoreApplication.translate("MainWindow", u"Epochs", None))
#if QT_CONFIG(tooltip)
        self.spinBoxBatch.setToolTip(QCoreApplication.translate("MainWindow", u"batch", None))
#endif // QT_CONFIG(tooltip)
        self.labelPatience.setText(QCoreApplication.translate("MainWindow", u"Patience", None))
        self.labelWorkers.setText(QCoreApplication.translate("MainWindow", u"Workers", None))
#if QT_CONFIG(tooltip)
        self.spinBoxSavePeriod.setToolTip(QCoreApplication.translate("MainWindow", u"save_period", None))
#endif // QT_CONFIG(tooltip)
        self.comboBoxDevice.setItemText(0, QCoreApplication.translate("MainWindow", u"0", None))
        self.comboBoxDevice.setItemText(1, QCoreApplication.translate("MainWindow", u"cpu", None))

#if QT_CONFIG(tooltip)
        self.comboBoxDevice.setToolTip(QCoreApplication.translate("MainWindow", u"0 = GPU", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBoxWorkers.setToolTip(QCoreApplication.translate("MainWindow", u"workers", None))
#endif // QT_CONFIG(tooltip)
        self.comboBoxOptimizer.setItemText(0, QCoreApplication.translate("MainWindow", u"auto", None))
        self.comboBoxOptimizer.setItemText(1, QCoreApplication.translate("MainWindow", u"SGD", None))
        self.comboBoxOptimizer.setItemText(2, QCoreApplication.translate("MainWindow", u"Adam", None))
        self.comboBoxOptimizer.setItemText(3, QCoreApplication.translate("MainWindow", u"AdamW", None))
        self.comboBoxOptimizer.setItemText(4, QCoreApplication.translate("MainWindow", u"NAdam", None))
        self.comboBoxOptimizer.setItemText(5, QCoreApplication.translate("MainWindow", u"RAdam", None))
        self.comboBoxOptimizer.setItemText(6, QCoreApplication.translate("MainWindow", u"RMSProp", None))

#if QT_CONFIG(tooltip)
        self.comboBoxOptimizer.setToolTip(QCoreApplication.translate("MainWindow", u"optimizer", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.trainTab), QCoreApplication.translate("MainWindow", u"Train", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.inferenceTab), QCoreApplication.translate("MainWindow", u"Inference", None))
        self.lineEditCurrentImg.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Results not loaded ->", None))
        self.toolButtonPrev.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.pushButtonLoadResults.setText(QCoreApplication.translate("MainWindow", u"Load results", None))
        self.labelCurrentImg.setText(QCoreApplication.translate("MainWindow", u"Current:", None))
        self.toolButtonNext.setText(QCoreApplication.translate("MainWindow", u"...", None))
    # retranslateUi

