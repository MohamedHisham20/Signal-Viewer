# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSplitter, QVBoxLayout,
    QWidget)

class Ui_root_widget(object):
    def setupUi(self, root_widget):
        if not root_widget.objectName():
            root_widget.setObjectName(u"root_widget")
        root_widget.resize(1512, 774)
        self.splitter_2 = QSplitter(root_widget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setGeometry(QRect(0, 10, 1511, 771))
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setMinimumSize(QSize(200, 0))
        self.splitter.setMaximumSize(QSize(16777215, 16777215))
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.controls_widget = QWidget(self.splitter)
        self.controls_widget.setObjectName(u"controls_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(4)
        sizePolicy1.setVerticalStretch(8)
        sizePolicy1.setHeightForWidth(self.controls_widget.sizePolicy().hasHeightForWidth())
        self.controls_widget.setSizePolicy(sizePolicy1)
        self.controls_widget.setMinimumSize(QSize(300, 430))
        self.controls_widget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayoutWidget = QWidget(self.controls_widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 351, 511))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter.addWidget(self.controls_widget)
        self.non_rectangle_graph_widget = QWidget(self.splitter)
        self.non_rectangle_graph_widget.setObjectName(u"non_rectangle_graph_widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(4)
        sizePolicy2.setVerticalStretch(4)
        sizePolicy2.setHeightForWidth(self.non_rectangle_graph_widget.sizePolicy().hasHeightForWidth())
        self.non_rectangle_graph_widget.setSizePolicy(sizePolicy2)
        self.splitter.addWidget(self.non_rectangle_graph_widget)
        self.splitter_2.addWidget(self.splitter)
        self.widget = QWidget(self.splitter_2)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.new_graph_btn = QPushButton(self.widget)
        self.new_graph_btn.setObjectName(u"new_graph_btn")
        icon = QIcon()
        icon.addFile(u"./Icons/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.new_graph_btn.setIcon(icon)

        self.horizontalLayout.addWidget(self.new_graph_btn)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.graph_scroll_area = QScrollArea(self.widget)
        self.graph_scroll_area.setObjectName(u"graph_scroll_area")
        self.graph_scroll_area.setMinimumSize(QSize(1180, 0))
        self.graph_scroll_area.setAcceptDrops(True)
        self.graph_scroll_area.setWidgetResizable(True)
        self.graph_placeholder_widget = QWidget()
        self.graph_placeholder_widget.setObjectName(u"graph_placeholder_widget")
        self.graph_placeholder_widget.setGeometry(QRect(0, 0, 1178, 725))
        self.graph_scroll_area.setWidget(self.graph_placeholder_widget)

        self.verticalLayout_2.addWidget(self.graph_scroll_area)

        self.splitter_2.addWidget(self.widget)

        self.retranslateUi(root_widget)

        QMetaObject.connectSlotsByName(root_widget)
    # setupUi

    def retranslateUi(self, root_widget):
        root_widget.setWindowTitle(QCoreApplication.translate("root_widget", u"root_widget", None))
        self.new_graph_btn.setText(QCoreApplication.translate("root_widget", u"New Graph", None))
    # retranslateUi

