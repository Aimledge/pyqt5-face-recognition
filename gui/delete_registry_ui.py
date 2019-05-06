# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui/delete_registry.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DeleteRegistry(object):
    def setupUi(self, DeleteRegistry):
        DeleteRegistry.setObjectName("DeleteRegistry")
        DeleteRegistry.resize(400, 147)
        icon = QtGui.QIcon.fromTheme("edit-delete")
        DeleteRegistry.setWindowIcon(icon)
        self.deleteButton = QtWidgets.QPushButton(DeleteRegistry)
        self.deleteButton.setGeometry(QtCore.QRect(280, 100, 85, 27))
        self.deleteButton.setObjectName("deleteButton")
        self.label = QtWidgets.QLabel(DeleteRegistry)
        self.label.setGeometry(QtCore.QRect(60, 40, 74, 17))
        self.label.setObjectName("label")
        self.faceRegistryBox = QtWidgets.QComboBox(DeleteRegistry)
        self.faceRegistryBox.setGeometry(QtCore.QRect(170, 40, 201, 27))
        self.faceRegistryBox.setObjectName("faceRegistryBox")

        self.retranslateUi(DeleteRegistry)
        self.deleteButton.clicked.connect(DeleteRegistry.delete_registry)
        QtCore.QMetaObject.connectSlotsByName(DeleteRegistry)

    def retranslateUi(self, DeleteRegistry):
        _translate = QtCore.QCoreApplication.translate
        DeleteRegistry.setWindowTitle(_translate("DeleteRegistry", "Delete Album"))
        self.deleteButton.setText(_translate("DeleteRegistry", "Delete"))
        self.label.setText(_translate("DeleteRegistry", "Album Name"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DeleteRegistry = QtWidgets.QDialog()
    ui = Ui_DeleteRegistry()
    ui.setupUi(DeleteRegistry)
    DeleteRegistry.show()
    sys.exit(app.exec_())
