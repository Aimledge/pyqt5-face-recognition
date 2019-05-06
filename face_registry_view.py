"""
Copyright (C) 2018, AIMLedge Pte, Ltd.
All rights reserved.

"""

from PyQt5.QtWidgets import QDialog, QApplication
from gui.face_registry_view_ui import Ui_FaceRegistryUI

SAMPLE_FACE_REGISTRIES = ['Demo_face_1', 'Demo_face_2']


class FaceRegistryView(QDialog):
  def __init__(self, parent=None, face_recognizer=None):
    QDialog.__init__(self, parent=parent)

    self.ui = Ui_FaceRegistryUI()
    self.ui.setupUi(self)
    self.cur_registry = None
    self.face_recognizer = face_recognizer

    for registry in SAMPLE_FACE_REGISTRIES:
      self.ui.registryNameSelect.addItem(registry)

  def load_face_registry(self):
    print('Loading face registry {} ...'.format(self.cur_registry))

  def show_next_face(self):
    print('Next face')

  def show_prev_face(self):
    print('Prev face')

  def set_current_face_registry(self, registry):
    self.cur_registry = registry
    print(registry)



if __name__ == "__main__":
  import sys
  app = QApplication(sys.argv)
  registry_view = FaceRegistryView()
  registry_view.show()
  sys.exit(app.exec_())
