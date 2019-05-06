# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui/face_registry_view.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FaceRegistryUI(object):
    def setupUi(self, FaceRegistryUI):
        FaceRegistryUI.setObjectName("FaceRegistryUI")
        FaceRegistryUI.resize(763, 499)
        icon = QtGui.QIcon.fromTheme("face-cool")
        FaceRegistryUI.setWindowIcon(icon)
        self.groupBox = QtWidgets.QGroupBox(FaceRegistryUI)
        self.groupBox.setGeometry(QtCore.QRect(490, 70, 247, 291))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.loadButton = QtWidgets.QPushButton(self.groupBox)
        self.loadButton.setObjectName("loadButton")
        self.gridLayout.addWidget(self.loadButton, 1, 1, 1, 3)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.registryNameSelect = QtWidgets.QComboBox(self.groupBox)
        self.registryNameSelect.setObjectName("registryNameSelect")
        self.gridLayout.addWidget(self.registryNameSelect, 0, 1, 1, 3)
        self.nextFaceButton = QtWidgets.QPushButton(self.groupBox)
        self.nextFaceButton.setObjectName("nextFaceButton")
        self.gridLayout.addWidget(self.nextFaceButton, 3, 3, 1, 1)
        self.prevFaceButton = QtWidgets.QPushButton(self.groupBox)
        self.prevFaceButton.setObjectName("prevFaceButton")
        self.gridLayout.addWidget(self.prevFaceButton, 3, 0, 1, 2)
        self.faceName = QtWidgets.QLineEdit(self.groupBox)
        self.faceName.setReadOnly(True)
        self.faceName.setObjectName("faceName")
        self.gridLayout.addWidget(self.faceName, 2, 2, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 2)
        self.faceImageArea = QtWidgets.QWidget(FaceRegistryUI)
        self.faceImageArea.setGeometry(QtCore.QRect(80, 40, 321, 301))
        self.faceImageArea.setObjectName("faceImageArea")
        self.closeViewButton = QtWidgets.QPushButton(FaceRegistryUI)
        self.closeViewButton.setGeometry(QtCore.QRect(640, 440, 85, 27))
        self.closeViewButton.setObjectName("closeViewButton")
        self.label.setBuddy(self.registryNameSelect)
        self.label_2.setBuddy(self.faceName)

        self.retranslateUi(FaceRegistryUI)
        self.loadButton.clicked.connect(FaceRegistryUI.load_face_registry)
        self.nextFaceButton.clicked.connect(FaceRegistryUI.show_next_face)
        self.prevFaceButton.clicked.connect(FaceRegistryUI.show_prev_face)
        self.closeViewButton.clicked.connect(FaceRegistryUI.close)
        self.registryNameSelect.currentIndexChanged['QString'].connect(FaceRegistryUI.set_current_face_registry)
        QtCore.QMetaObject.connectSlotsByName(FaceRegistryUI)

    def retranslateUi(self, FaceRegistryUI):
        _translate = QtCore.QCoreApplication.translate
        FaceRegistryUI.setWindowTitle(_translate("FaceRegistryUI", "Face Album"))
        self.loadButton.setText(_translate("FaceRegistryUI", "Load"))
        self.label.setText(_translate("FaceRegistryUI", "Album"))
        self.nextFaceButton.setText(_translate("FaceRegistryUI", "Next >>"))
        self.prevFaceButton.setText(_translate("FaceRegistryUI", "<< Prev"))
        self.label_2.setText(_translate("FaceRegistryUI", "Name"))
        self.closeViewButton.setText(_translate("FaceRegistryUI", "Close"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FaceRegistryUI = QtWidgets.QDialog()
    ui = Ui_FaceRegistryUI()
    ui.setupUi(FaceRegistryUI)
    FaceRegistryUI.show()
    sys.exit(app.exec_())
