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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_graph_widget(object):
    def setupUi(self, graph_widget):
        if not graph_widget.objectName():
            graph_widget.setObjectName(u"graph_widget")
        graph_widget.resize(1100, 342)
        graph_widget.setMinimumSize(QSize(0, 336))
        self.frame = QFrame(graph_widget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 0, 1081, 331))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.reorder_label = QLabel(self.frame)
        self.reorder_label.setObjectName(u"reorder_label")
        self.reorder_label.setGeometry(QRect(10, 160, 24, 24))
        self.reorder_label.setCursor(QCursor(Qt.OpenHandCursor))
        self.reorder_label.setAcceptDrops(True)
        self.reorder_label.setPixmap(QPixmap(u"./Icons/reorder.png"))
        self.reorder_label.setScaledContents(True)
        self.graph_placeholder = QWidget(self.frame)
        self.graph_placeholder.setObjectName(u"graph_placeholder")
        self.graph_placeholder.setGeometry(QRect(50, 10, 1051, 261))
        self.verticalLayoutWidget = QWidget(self.graph_placeholder)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(-1, -1, 1051, 261))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.layoutWidget = QWidget(self.frame)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(370, 290, 321, 32))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.beginning_btn = QPushButton(self.layoutWidget)
        self.beginning_btn.setObjectName(u"beginning_btn")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.beginning_btn.sizePolicy().hasHeightForWidth())
        self.beginning_btn.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u"./Icons/begin.png", QSize(), QIcon.Normal, QIcon.Off)
        self.beginning_btn.setIcon(icon)

        self.horizontalLayout.addWidget(self.beginning_btn)

        self.fast_backward_btn = QPushButton(self.layoutWidget)
        self.fast_backward_btn.setObjectName(u"fast_backward_btn")
        sizePolicy.setHeightForWidth(self.fast_backward_btn.sizePolicy().hasHeightForWidth())
        self.fast_backward_btn.setSizePolicy(sizePolicy)
        icon1 = QIcon()
        icon1.addFile(u"./Icons/fast-backward.png", QSize(), QIcon.Normal, QIcon.Off)
        self.fast_backward_btn.setIcon(icon1)

        self.horizontalLayout.addWidget(self.fast_backward_btn)

        self.pause_play_btn = QPushButton(self.layoutWidget)
        self.pause_play_btn.setObjectName(u"pause_play_btn")
        sizePolicy.setHeightForWidth(self.pause_play_btn.sizePolicy().hasHeightForWidth())
        self.pause_play_btn.setSizePolicy(sizePolicy)
        icon2 = QIcon()
        icon2.addFile(u"./Icons/pause.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pause_play_btn.setIcon(icon2)

        self.horizontalLayout.addWidget(self.pause_play_btn)

        self.fast_forward_btn = QPushButton(self.layoutWidget)
        self.fast_forward_btn.setObjectName(u"fast_forward_btn")
        sizePolicy.setHeightForWidth(self.fast_forward_btn.sizePolicy().hasHeightForWidth())
        self.fast_forward_btn.setSizePolicy(sizePolicy)
        icon3 = QIcon()
        icon3.addFile(u"./Icons/fast-forward.png", QSize(), QIcon.Normal, QIcon.Off)
        self.fast_forward_btn.setIcon(icon3)

        self.horizontalLayout.addWidget(self.fast_forward_btn)

        self.end_btn = QPushButton(self.layoutWidget)
        self.end_btn.setObjectName(u"end_btn")
        sizePolicy.setHeightForWidth(self.end_btn.sizePolicy().hasHeightForWidth())
        self.end_btn.setSizePolicy(sizePolicy)
        icon4 = QIcon()
        icon4.addFile(u"./Icons/end.png", QSize(), QIcon.Normal, QIcon.Off)
        self.end_btn.setIcon(icon4)

        self.horizontalLayout.addWidget(self.end_btn)

        self.graph_title_lbl = QLabel(self.frame)
        self.graph_title_lbl.setObjectName(u"graph_title_lbl")
        self.graph_title_lbl.setGeometry(QRect(50, 280, 201, 41))
        self.graph_title_lbl.setStyleSheet(u"font: 24pt \"Helvetica Neue\";")
        self.graph_title_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)

        self.retranslateUi(graph_widget)

        QMetaObject.connectSlotsByName(graph_widget)
    # setupUi

    def retranslateUi(self, graph_widget):
        graph_widget.setWindowTitle(QCoreApplication.translate("graph_widget", u"graph_widget", None))
        self.reorder_label.setText("")
        self.beginning_btn.setText("")
        self.fast_backward_btn.setText("")
        self.pause_play_btn.setText("")
        self.fast_forward_btn.setText("")
        self.end_btn.setText("")
        self.graph_title_lbl.setText(QCoreApplication.translate("graph_widget", u"Graph Title", None))
    # retranslateUi

