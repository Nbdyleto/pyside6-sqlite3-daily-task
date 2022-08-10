# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(852, 514)
        self.calendarWidget = QCalendarWidget(Form)
        self.calendarWidget.setObjectName(u"calendarWidget")
        self.calendarWidget.setGeometry(QRect(40, 150, 411, 311))
        
        """
        self.calendarWidget.setStyleSheet(u""
        "QCalendarWidget QAbstractItemView {\n"
            "border : 4px solid rgb(68, 71, 90); \n"
            "background-color:#44475a; \n"
        "} \n"
        "QCalendarWidget QToolButton {\n"
            "background-color:#44475a; \n"
        "}\n"
        )
        """

        self.tasksListWidget = QListWidget(Form)
        self.tasksListWidget.setObjectName(u"tasksListWidget")
        self.tasksListWidget.setGeometry(QRect(480, 150, 341, 301))
        self.tasksListWidget.setStyleSheet(u"font:12pt;")
        self.saveButton = QPushButton(Form)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setGeometry(QRect(480, 460, 341, 28))
        self.saveButton.setStyleSheet(u"border-radius:10px;\n"
"background-color: #01BFFF;\n"
"color:white;\n"
"font:11pt;")
        self.addButton = QPushButton(Form)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setGeometry(QRect(730, 110, 93, 28))
        self.addButton.setStyleSheet(u"border-radius:10px;\n"
"background-color: #01BFFF;\n"
"color:white;\n"
"")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 851, 101))
        self.label.setStyleSheet(u"font-size : 24pt;\n"
"background : #01BFFF;\n"
"color:white;\n"
"border-radius:8px;")
        self.label.setAlignment(Qt.AlignCenter)
        self.taskLineEdit = QLineEdit(Form)
        self.taskLineEdit.setObjectName(u"taskLineEdit")
        self.taskLineEdit.setGeometry(QRect(480, 110, 241, 31))
        self.taskLineEdit.setStyleSheet(u"font:12pt;")

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.saveButton.setText(QCoreApplication.translate("Form", u"Save Changes", None))
        self.addButton.setText(QCoreApplication.translate("Form", u"Add new", None))
        self.label.setText(QCoreApplication.translate("Form", u"Daily Task Planner", None))
    # retranslateUi

