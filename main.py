#!/usr/bin/env python3

#  Copyright (C) 2015-2016 Ben Klein. All rights reserved.
#
#  This file was based upon an example class of the Qt Toolkit.
#
#  This application is licensed under the GNU GPLv3 License, included with
#  this application source.

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)


import sys

if sys.version_info >= (3, 3):
    import rython3
    print("Using Rython3: " + str(sys.version_info))
elif sys.version_info >= (2, 7):
    import rython2
    print("Using Rython2: " + str(sys.version_info))
else: sys.exit("This program requires Python 2.7+ or 3.3+, please install either of those versions.")

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QSettings

settings = QSettings('ubuntu-airplay')

class Window(QtGui.QDialog):
    def __init__(self):
        super(Window, self).__init__()

        self.createIconGroupBox()
        self.createMessageGroupBox()

        self.iconLabel.setMinimumWidth(self.durationLabel.sizeHint().width())

        self.createActions()
        self.createTrayIcon()

        self.showMessageButton.clicked.connect(self.showMessage)
        self.showIconCheckBox.toggled.connect(self.trayIcon.setVisible)
        self.iconComboBox.currentIndexChanged.connect(self.setIcon)
        self.trayIcon.messageClicked.connect(self.messageClicked)
        self.trayIcon.activated.connect(self.iconActivated)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.iconGroupBox)
        mainLayout.addWidget(self.messageGroupBox)
        self.setLayout(mainLayout)

        self.iconComboBox.setCurrentIndex(1)
        self.trayIcon.show()

        self.setWindowTitle("Ubuntu Airplay Settings")
        self.resize(400, 300)

    def setVisible(self, visible):
        self.minimizeAction.setEnabled(visible)
        self.maximizeAction.setEnabled(not self.isMaximized())
        self.restoreAction.setEnabled(self.isMaximized() or not visible)
        super(Window, self).setVisible(visible)

    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            if not settings.value('promptOnClose_systray'):
                QtGui.QMessageBox.information(self, "Systray",
                    "The program will keep running in the system tray. "
                    "To terminate the program, choose <b>Quit</b> in "
                    "the menu of the system tray airplay icon.")
            self.hide()
            event.ignore()
            print("Closing to System Tray")
        else:
            print("Tray Icon not visible, quitting.")
            sys.exit("Exit: No system tray instance to close to.")

    def setIcon(self, index):
        icon = self.iconComboBox.itemIcon(index)
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)

        self.trayIcon.setToolTip("Ubuntu Airplay")

    def iconActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            self.iconComboBox.setCurrentIndex(
                    (self.iconComboBox.currentIndex() + 1)
                    % self.iconComboBox.count())
        elif reason == QtGui.QSystemTrayIcon.MiddleClick:
            self.showMessage()

    def showMessage(self):
        icon = QtGui.QSystemTrayIcon.MessageIcon(
                self.typeComboBox.itemData(self.typeComboBox.currentIndex()))
        self.trayIcon.showMessage(self.titleEdit.text(),
                self.bodyEdit.toPlainText(), icon,
                self.durationSpinBox.value() * 1000)

    def messageClicked(self):
        QtGui.QMessageBox.information(None, "Ubuntu Airplay Help", "If you need help with Ubuntu Airplay, "
        "see the Github page to file bug reports or see further documentation and help.")

    def createIconGroupBox(self):
        self.iconGroupBox = QtGui.QGroupBox("Tray Icon")

        self.iconLabel = QtGui.QLabel("Icon:")

        self.iconComboBox = QtGui.QComboBox()
        self.iconComboBox.addItem(QtGui.QIcon('images/Airplay-Light'), "Black Icon")
        self.iconComboBox.addItem(QtGui.QIcon('images/Airplay-Dark'), "White Icon")

        self.showIconCheckBox = QtGui.QCheckBox("Show tray icon")
        self.showIconCheckBox.setChecked(True)

        iconLayout = QtGui.QHBoxLayout()
        iconLayout.addWidget(self.iconLabel)
        iconLayout.addWidget(self.iconComboBox)
        iconLayout.addStretch()
        iconLayout.addWidget(self.showIconCheckBox)
        self.iconGroupBox.setLayout(iconLayout)

    def createMessageGroupBox(self):
        self.messageGroupBox = QtGui.QGroupBox("Balloon Message")

        typeLabel = QtGui.QLabel("Type:")

        self.typeComboBox = QtGui.QComboBox()
        self.typeComboBox.addItem("None", QtGui.QSystemTrayIcon.NoIcon)
        self.typeComboBox.addItem(self.style().standardIcon(
                QtGui.QStyle.SP_MessageBoxInformation), "Information", QtGui.QSystemTrayIcon.Information)
        self.typeComboBox.addItem(self.style().standardIcon(
                QtGui.QStyle.SP_MessageBoxWarning), "Warning", QtGui.QSystemTrayIcon.Warning)
        self.typeComboBox.addItem(self.style().standardIcon(
                QtGui.QStyle.SP_MessageBoxCritical), "Critical", QtGui.QSystemTrayIcon.Critical)
        self.typeComboBox.setCurrentIndex(1)

        self.durationLabel = QtGui.QLabel("Duration:")

        self.durationSpinBox = QtGui.QSpinBox()
        self.durationSpinBox.setRange(2, 15)
        self.durationSpinBox.setSuffix("s")
        self.durationSpinBox.setValue(5)

        durationWarningLabel = QtGui.QLabel("(some systems might ignore this hint)")
        durationWarningLabel.setIndent(10)

        titleLabel = QtGui.QLabel("Title:")

        self.titleEdit = QtGui.QLineEdit("Cannot connect to network")

        bodyLabel = QtGui.QLabel("Body:")

        self.bodyEdit = QtGui.QTextEdit()
        self.bodyEdit.setPlainText("Don't believe me. Honestly, I don't have a clue.\nClick this balloon for details.")

        self.showMessageButton = QtGui.QPushButton("Show Message")
        self.showMessageButton.setDefault(True)

        messageLayout = QtGui.QGridLayout()
        messageLayout.addWidget(typeLabel, 0, 0)
        messageLayout.addWidget(self.typeComboBox, 0, 1, 1, 2)
        messageLayout.addWidget(self.durationLabel, 1, 0)
        messageLayout.addWidget(self.durationSpinBox, 1, 1)
        messageLayout.addWidget(durationWarningLabel, 1, 2, 1, 3)
        messageLayout.addWidget(titleLabel, 2, 0)
        messageLayout.addWidget(self.titleEdit, 2, 1, 1, 4)
        messageLayout.addWidget(bodyLabel, 3, 0)
        messageLayout.addWidget(self.bodyEdit, 3, 1, 2, 4)
        messageLayout.addWidget(self.showMessageButton, 5, 4)
        messageLayout.setColumnStretch(3, 1)
        messageLayout.setRowStretch(4, 1)
        self.messageGroupBox.setLayout(messageLayout)

    def createActions(self):
        self.minimizeAction = QtGui.QAction("Mi&nimize", self, triggered=self.hide)

        self.maximizeAction = QtGui.QAction("Ma&ximize", self, triggered=self.showMaximized)

        self.restoreAction = QtGui.QAction("&Restore", self, triggered=self.showNormal)

        self.quitAction = QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit)

    def createTrayIcon(self):
         self.trayIconMenu = QtGui.QMenu(self)
         self.trayIconMenu.addAction(self.minimizeAction)
         self.trayIconMenu.addAction(self.maximizeAction)
         self.trayIconMenu.addAction(self.restoreAction)
         self.trayIconMenu.addSeparator()
         self.trayIconMenu.addAction(self.quitAction)

         self.trayIcon = QtGui.QSystemTrayIcon(self)
         self.trayIcon.setContextMenu(self.trayIconMenu)

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Systray", "I couldn't detect any system tray on this system.")
        sys.exit(1)

    QtGui.QApplication.setQuitOnLastWindowClosed(False)

    window = Window()
    window.show()
    print("Goodbye")
    sys.exit(app.exec_())
