# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui/create_registry.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateRegistry(object):
    def setupUi(self, CreateRegistry):
        CreateRegistry.setObjectName("CreateRegistry")
        CreateRegistry.resize(400, 147)
        icon = QtGui.QIcon.fromTheme("address-book-new")
        CreateRegistry.setWindowIcon(icon)
        self.createButton = QtWidgets.QDialogButtonBox(CreateRegistry)
        self.createButton.setGeometry(QtCore.QRect(40, 100, 341, 32))
        self.createButton.setOrientation(QtCore.Qt.Horizontal)
        self.createButton.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.createButton.setObjectName("createButton")
        self.layoutWidget = QtWidgets.QWidget(CreateRegistry)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 30, 341, 29))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.registryNameInput = QtWidgets.QLineEdit(self.layoutWidget)
        self.registryNameInput.setObjectName("registryNameInput")
        self.gridLayout.addWidget(self.registryNameInput, 0, 1, 1, 1)
        self.layoutWidget.raise_()
        self.createButton.raise_()
        self.label.setBuddy(self.registryNameInput)

        self.retranslateUi(CreateRegistry)
        self.createButton.accepted.connect(CreateRegistry.create_registry)
        self.createButton.rejected.connect(CreateRegistry.reject)
        self.registryNameInput.textChanged['QString'].connect(CreateRegistry.set_registry_name)
        QtCore.QMetaObject.connectSlotsByName(CreateRegistry)

    def retranslateUi(self, CreateRegistry):
        _translate = QtCore.QCoreApplication.translate
        CreateRegistry.setWindowTitle(_translate("CreateRegistry", "New Album"))
        self.label.setText(_translate("CreateRegistry", "Album Name"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CreateRegistry = QtWidgets.QDialog()
    ui = Ui_CreateRegistry()
    ui.setupUi(CreateRegistry)
    CreateRegistry.show()
    sys.exit(app.exec_())
