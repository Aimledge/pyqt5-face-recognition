# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui/face_registration_view.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FaceRegistrationUI(object):
    def setupUi(self, FaceRegistrationUI):
        FaceRegistrationUI.setObjectName("FaceRegistrationUI")
        FaceRegistrationUI.resize(774, 485)
        icon = QtGui.QIcon.fromTheme("face-cool")
        FaceRegistrationUI.setWindowIcon(icon)
        self.groupBox = QtWidgets.QGroupBox(FaceRegistrationUI)
        self.groupBox.setGeometry(QtCore.QRect(530, 40, 241, 271))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.registryNameSelect = QtWidgets.QComboBox(self.groupBox)
        self.registryNameSelect.setObjectName("registryNameSelect")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.registryNameSelect)
        self.captureButton = QtWidgets.QPushButton(self.groupBox)
        self.captureButton.setObjectName("captureButton")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.captureButton)
        self.retakeButton = QtWidgets.QPushButton(self.groupBox)
        self.retakeButton.setObjectName("retakeButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.retakeButton)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.nameInput = QtWidgets.QLineEdit(self.groupBox)
        self.nameInput.setObjectName("nameInput")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.nameInput)
        self.registerButton = QtWidgets.QPushButton(self.groupBox)
        self.registerButton.setObjectName("registerButton")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.registerButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(FaceRegistrationUI)
        self.buttonBox.setGeometry(QtCore.QRect(400, 430, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.stackedWidget = QtWidgets.QStackedWidget(FaceRegistrationUI)
        self.stackedWidget.setGeometry(QtCore.QRect(30, 10, 481, 361))
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.stackedWidget.setObjectName("stackedWidget")
        self.viewFinderPage = QtWidgets.QWidget()
        self.viewFinderPage.setObjectName("viewFinderPage")
        self.viewFinder = QCameraViewfinder(self.viewFinderPage)
        self.viewFinder.setGeometry(QtCore.QRect(0, 0, 481, 361))
        self.viewFinder.setObjectName("viewFinder")
        self.stackedWidget.addWidget(self.viewFinderPage)
        self.previewPage = QtWidgets.QWidget()
        self.previewPage.setObjectName("previewPage")
        self.picturePreview = QtWidgets.QLabel(self.previewPage)
        self.picturePreview.setGeometry(QtCore.QRect(0, 0, 481, 361))
        self.picturePreview.setFrameShape(QtWidgets.QFrame.Box)
        self.picturePreview.setObjectName("picturePreview")
        self.stackedWidget.addWidget(self.previewPage)
        self.label.setBuddy(self.registryNameSelect)

        self.retranslateUi(FaceRegistrationUI)
        self.buttonBox.accepted.connect(FaceRegistrationUI.accept)
        self.buttonBox.rejected.connect(FaceRegistrationUI.reject)
        self.nameInput.textChanged['QString'].connect(FaceRegistrationUI.handle_face_name)
        self.registerButton.clicked.connect(FaceRegistrationUI.register_face)
        self.retakeButton.clicked.connect(FaceRegistrationUI.retake_picture)
        self.captureButton.clicked.connect(FaceRegistrationUI.capture_picture)
        self.registryNameSelect.currentIndexChanged['QString'].connect(FaceRegistrationUI.set_current_face_registry)
        QtCore.QMetaObject.connectSlotsByName(FaceRegistrationUI)

    def retranslateUi(self, FaceRegistrationUI):
        _translate = QtCore.QCoreApplication.translate
        FaceRegistrationUI.setWindowTitle(_translate("FaceRegistrationUI", "Face Registration"))
        self.label.setText(_translate("FaceRegistrationUI", "Album"))
        self.captureButton.setText(_translate("FaceRegistrationUI", "Capture"))
        self.retakeButton.setText(_translate("FaceRegistrationUI", "Retake"))
        self.label_2.setText(_translate("FaceRegistrationUI", "Name"))
        self.registerButton.setText(_translate("FaceRegistrationUI", "Register"))
        self.picturePreview.setText(_translate("FaceRegistrationUI", "TextLabel"))


from PyQt5.QtMultimediaWidgets import QCameraViewfinder


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FaceRegistrationUI = QtWidgets.QDialog()
    ui = Ui_FaceRegistrationUI()
    ui.setupUi(FaceRegistrationUI)
    FaceRegistrationUI.show()
    sys.exit(app.exec_())
