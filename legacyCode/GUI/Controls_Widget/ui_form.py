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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Controls_Widget(object):
    def setupUi(self, Controls_Widget):
        if not Controls_Widget.objectName():
            Controls_Widget.setObjectName(u"Controls_Widget")
        Controls_Widget.resize(300, 517)
        self.layoutWidget = QWidget(Controls_Widget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 301, 521))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.layoutWidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.layoutWidget1 = QWidget(self.frame)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(0, 20, 301, 91))
        self.verticalLayout = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.beginning_btn = QPushButton(self.layoutWidget1)
        self.beginning_btn.setObjectName(u"beginning_btn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.beginning_btn.sizePolicy().hasHeightForWidth())
        self.beginning_btn.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u"../Icons/begin.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.beginning_btn.setIcon(icon)

        self.horizontalLayout.addWidget(self.beginning_btn)

        self.fast_backward_btn = QPushButton(self.layoutWidget1)
        self.fast_backward_btn.setObjectName(u"fast_backward_btn")
        sizePolicy.setHeightForWidth(self.fast_backward_btn.sizePolicy().hasHeightForWidth())
        self.fast_backward_btn.setSizePolicy(sizePolicy)
        icon1 = QIcon()
        icon1.addFile(u"../Icons/fast-backward.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.fast_backward_btn.setIcon(icon1)

        self.horizontalLayout.addWidget(self.fast_backward_btn)

        self.pause_play_btn = QPushButton(self.layoutWidget1)
        self.pause_play_btn.setObjectName(u"pause_play_btn")
        sizePolicy.setHeightForWidth(self.pause_play_btn.sizePolicy().hasHeightForWidth())
        self.pause_play_btn.setSizePolicy(sizePolicy)
        icon2 = QIcon()
        icon2.addFile(u"../Icons/pause.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pause_play_btn.setIcon(icon2)

        self.horizontalLayout.addWidget(self.pause_play_btn)

        self.fast_forward_btn = QPushButton(self.layoutWidget1)
        self.fast_forward_btn.setObjectName(u"fast_forward_btn")
        sizePolicy.setHeightForWidth(self.fast_forward_btn.sizePolicy().hasHeightForWidth())
        self.fast_forward_btn.setSizePolicy(sizePolicy)
        icon3 = QIcon()
        icon3.addFile(u"../Icons/fast-forward.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.fast_forward_btn.setIcon(icon3)

        self.horizontalLayout.addWidget(self.fast_forward_btn)

        self.end_btn = QPushButton(self.layoutWidget1)
        self.end_btn.setObjectName(u"end_btn")
        sizePolicy.setHeightForWidth(self.end_btn.sizePolicy().hasHeightForWidth())
        self.end_btn.setSizePolicy(sizePolicy)
        icon4 = QIcon()
        icon4.addFile(u"../Icons/end.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.end_btn.setIcon(icon4)

        self.horizontalLayout.addWidget(self.end_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addWidget(self.frame)

        self.frame_2 = QFrame(self.layoutWidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.layoutWidget2 = QWidget(self.frame_2)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(40, 20, 211, 91))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.glue_btn = QPushButton(self.layoutWidget2)
        self.glue_btn.setObjectName(u"glue_btn")
        self.glue_btn.setEnabled(False)
        icon5 = QIcon()
        icon5.addFile(u"../Icons/liquid-glue.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.glue_btn.setIcon(icon5)
        self.glue_btn.setIconSize(QSize(24, 24))

        self.verticalLayout_3.addWidget(self.glue_btn)

        self.report_btn = QPushButton(self.layoutWidget2)
        self.report_btn.setObjectName(u"report_btn")
        self.report_btn.setEnabled(False)
        icon6 = QIcon()
        icon6.addFile(u"../Icons/seo-report.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.report_btn.setIcon(icon6)
        self.report_btn.setIconSize(QSize(24, 24))

        self.verticalLayout_3.addWidget(self.report_btn)


        self.verticalLayout_2.addWidget(self.frame_2)


        self.retranslateUi(Controls_Widget)

        QMetaObject.connectSlotsByName(Controls_Widget)
    # setupUi

    def retranslateUi(self, Controls_Widget):
        Controls_Widget.setWindowTitle(QCoreApplication.translate("Controls_Widget", u"Controls_Widget", None))
        self.label.setText(QCoreApplication.translate("Controls_Widget", u"Control all graphs", None))
        self.beginning_btn.setText("")
        self.fast_backward_btn.setText("")
        self.pause_play_btn.setText("")
        self.fast_forward_btn.setText("")
        self.end_btn.setText("")
        self.glue_btn.setText(QCoreApplication.translate("Controls_Widget", u"Glue Signals", None))
        self.report_btn.setText(QCoreApplication.translate("Controls_Widget", u"Report Selected Signal", None))
    # retranslateUi

