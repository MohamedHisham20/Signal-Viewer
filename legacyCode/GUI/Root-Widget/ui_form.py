# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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
from PySide6.QtWidgets import (QApplication, QScrollArea, QSizePolicy, QSplitter,
    QVBoxLayout, QWidget)

class Ui_root_widget(object):
    def setupUi(self, root_widget):
        if not root_widget.objectName():
            root_widget.setObjectName(u"root_widget")
        root_widget.resize(1512, 774)
        self.splitter_2 = QSplitter(root_widget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setGeometry(QRect(0, 0, 1511, 771))
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setMinimumSize(QSize(200, 0))
        self.splitter.setMaximumSize(QSize(16777215, 16777215))
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.controls_widget = QWidget(self.splitter)
        self.controls_widget.setObjectName(u"controls_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(4)
        sizePolicy1.setVerticalStretch(8)
        sizePolicy1.setHeightForWidth(self.controls_widget.sizePolicy().hasHeightForWidth())
        self.controls_widget.setSizePolicy(sizePolicy1)
        self.controls_widget.setMinimumSize(QSize(20, 0))
        self.verticalLayoutWidget = QWidget(self.controls_widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 301, 511))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter.addWidget(self.controls_widget)
        self.non_rectangle_graph_widget = QWidget(self.splitter)
        self.non_rectangle_graph_widget.setObjectName(u"non_rectangle_graph_widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(4)
        sizePolicy2.setVerticalStretch(4)
        sizePolicy2.setHeightForWidth(self.non_rectangle_graph_widget.sizePolicy().hasHeightForWidth())
        self.non_rectangle_graph_widget.setSizePolicy(sizePolicy2)
        self.splitter.addWidget(self.non_rectangle_graph_widget)
        self.splitter_2.addWidget(self.splitter)
        self.graph_scroll_area = QScrollArea(self.splitter_2)
        self.graph_scroll_area.setObjectName(u"graph_scroll_area")
        self.graph_scroll_area.setMinimumSize(QSize(1200, 0))
        self.graph_scroll_area.setWidgetResizable(True)
        self.graph_placeholder_widget = QWidget()
        self.graph_placeholder_widget.setObjectName(u"graph_placeholder_widget")
        self.graph_placeholder_widget.setGeometry(QRect(0, 0, 1198, 769))
        self.graph_scroll_area.setWidget(self.graph_placeholder_widget)
        self.splitter_2.addWidget(self.graph_scroll_area)

        self.retranslateUi(root_widget)

        QMetaObject.connectSlotsByName(root_widget)
    # setupUi

    def retranslateUi(self, root_widget):
        root_widget.setWindowTitle(QCoreApplication.translate("root_widget", u"root_widget", None))
    # retranslateUi

