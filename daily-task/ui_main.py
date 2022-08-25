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
    QSize, QTime, QUrl, Qt, QAbstractItemModel, )
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget, QAbstractItemView)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(950, 514)

        self.tblTopics = QTableWidget(Form)
        self.tblTopics.setGeometry(QRect(690, 200, 113, 100))
        self.tblTopics.setObjectName(u'tblTopics')
        self.tblTopics.setVisible(False)
        self.tblTopics.setColumnCount(1)
        self.tblTopics.setRowCount(1)
        item = QTableWidgetItem()
        self.tblTopics.setHorizontalHeaderItem(0, item)
        
        self.tableWidget = QTableWidget(Form)
        self.tableWidget.setGeometry(QRect(40, 150, 770, 320))
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        #self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setSortingEnabled(False)

        self.tableWidget.setColumnCount(5)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)

        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: #282a36; 
                border-radius: 0px;
            }

            QTableWidget::item {
                color: #f8f8f2;                    
                background-color: #44475a;
                margin-top: 5px;          
                border-radius: 0px;
                padding-left: 2px;
            }

            QTableWidget::item:selected {
                background-color: #6272a4;
                selection-color : #000000;
            }
            QHeaderView::section {
                background-color:#6272a4;
                selection-color: #000000;
            }
        """)

        self.calendarWidget = QCalendarWidget(Form)
        self.calendarWidget.setObjectName(u"calendarWidget")
        self.calendarWidget.setGeometry(QRect(230, 205, 340, 320))
        self.calendarWidget.setVisible(False)
        self.calendarWidget.setStyleSheet("""
        QCalendarWidget QToolButton {
            height: 30px;
            width: 75px;
            color: #f8f8f2;
            font-size: 15px;
            icon-size: 15px;
            background-color: #44475a;
            margin-top: 1px;
        }
        QCalendarWidget QMenu {
            width: 150px;
            left: 20px;
            color: white;
            font-size: 15px;
            background-color: #44475a;
        }
        QCalendarWidget QSpinBox { 
            width: 50px; 
            font-size: 15px; 
            color: #f8f8f2; 
            padding-left: 19px;
            background-color: #44475a; 
            selection-background-color: #44475a;
            selection-color: #f8f8f2;
        }

        QCalendarWidget QSpinBox::up-button { 
            subcontrol-origin: border;  
            subcontrol-position: top right;  
            width:15px; 
        }
        QCalendarWidget QSpinBox::down-button {
            subcontrol-origin: border; 
            subcontrol-position: bottom right;  
            width:15px;
        }
        QCalendarWidget QSpinBox::up-arrow { 
            width:10px; 
            height:10px; 
        }
        QCalendarWidget QSpinBox::down-arrow { 
            width:10px; 
            height:10px; 
        }
        
        /* header row */
        QCalendarWidget QWidget { 
            alternate-background-color: #6272a4; 
        }
        
        /* normal days */
        QCalendarWidget QAbstractItemView:enabled 
        {
            font-size:15px;  
            color: #f8f8f2;  
            background-color: #44475a;  
            selection-background-color: #6272a4; 
            selection-color: black; 
        }
        
        /* days in other months */
        /* navigation bar */
        QCalendarWidget QWidget#qt_calendar_navigationbar
        { 
            background-color: #44475a; 
        }

        QCalendarWidget QAbstractItemView:disabled 
        { 
            color: #6272a4; 
        }

        """)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 950, 101))
        self.label.setStyleSheet(u"font-size : 24pt;\n"
"background : #44475a;\n"
"color:white;\n"
"border-radius:8px;")
        self.label.setAlignment(Qt.AlignCenter)

        self.tblTopics = QTableWidget(Form)
        self.tblTopics.setGeometry(QRect(690, 171, 100, 190))
        self.tblTopics.setObjectName(u'tblTopics')
        self.tblTopics.setVisible(False)
        self.tblTopics.setColumnCount(1)
        self.tblTopics.setRowCount(1)
        item = QTableWidgetItem()
        self.tblTopics.setHorizontalHeaderItem(0, item)
        self.tblTopics.setFocusPolicy(Qt.NoFocus)
        self.tblTopics.setSelectionBehavior(QAbstractItemView.SelectRows)
        #self.tblTopics.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblTopics.verticalHeader().setVisible(False)
        self.tblTopics.horizontalHeader().setVisible(False)
        self.tblTopics.setShowGrid(False)
        self.tblTopics.setSortingEnabled(False)
        self.tableWidget.setWordWrap(True)
        self.tblTopics.setStyleSheet("""
            QTableWidget {
                background-color: #282a36; 
            }
            QTableWidget::item {
                color: #f8f8f2;                    
                background-color: #44475a;
                margin-top: 5px;         
                padding-left: 2px;
            }
            QHeaderView::section {
                background-color:#6272a4;
                selection-color: #000000;
            }
        """)
        

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", u"Form", None))
        self.label.setText(_translate("Form", u"Daily Task Planner", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", u"Task Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", u"Status"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", u"Start Date"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", u"End Date"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", u"Topic"))
        
        item = self.tblTopics.horizontalHeaderItem(0)
        item.setText(_translate("Form", u"topic_name"))
    # retranslateUi

