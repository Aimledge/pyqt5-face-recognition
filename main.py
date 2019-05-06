import logging
from PyQt5.QtWidgets import QApplication
import face_recognition_app

if __name__ == "__main__":
  import sys
  logging.basicConfig(level=logging.INFO)
  app = QApplication(sys.argv)
  face_rec_app = face_recognition_app.FaceRecognitionAppUI()
  face_rec_app.show()
  sys.exit(app.exec_())
