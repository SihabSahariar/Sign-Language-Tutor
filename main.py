from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject, QTimer
from yolov8 import YOLOv8  # Import your YOLOv8 class

class DetectionThread(QThread):
    change_pixmap_signal = pyqtSignal(bytes)
    character_signal = pyqtSignal(int)
    recognition_accuracy = pyqtSignal(float)
    next_character = pyqtSignal(int)

    def __init__(self, model_path, parent=None):
        super().__init__(parent)
        self.model_path = model_path
        self.stopped = False
        self.lst_character = []
        self.count = 0
        self.char = 1

    def run(self):
        cap = cv2.VideoCapture(0)
        yolov8_detector = YOLOv8(self.model_path, conf_thres=0.6, iou_thres=0.5)

        while not self.stopped:
            ret, frame = cap.read()
            if ret:
                boxes, scores, class_ids = yolov8_detector(frame)
                if len(class_ids) > 0:
                        if class_ids[0] not in self.lst_character:
                                if class_ids[0] == self.count:
                                        print("Before->",class_ids[0],self.count)
                                        self.lst_character.append(class_ids[0])
                                        self.character_signal.emit(class_ids[0])
                                        self.recognition_accuracy.emit(scores[0])
                                        self.count += 1
                                        self.char += 1
                                        self.next_character.emit(self.char)
                                        if self.count == 49:
                                                self.count = 0
                                                self.lst_character = []
                                        print("After->",class_ids[0],self.count)

                                        

                combined_img = yolov8_detector.draw_detections(frame)
                img_bytes = cv2.imencode('.jpg', combined_img)[1].tobytes()
                self.change_pixmap_signal.emit(img_bytes)

    def stop(self):
        self.stopped = True

class Ui_Form(object):
    def __init__(self):
        self.thread = None
        self.count_img = 1
        self.record = []
        self.bengali_characters = {
        0: 'অ',
        1: 'আ',
        2: 'ই',
        3: 'উ',
        4: 'এ',
        5: 'ও',
        6: 'ক',
        7: 'খ',
        8: 'গ',
        9: 'ঘ',
        10: 'চ',
        11: 'ছ',
        12: 'জ',
        13: 'ঝ',
        14: 'ট',
        15: 'ঠ',
        16: 'ড',
        17: 'ঢ',
        18: 'ত',
        19: 'থ',
        20: 'দ',
        21: 'ধ',
        22: 'প',
        23: 'ফ',
        24: 'ব',
        25: 'ভ',
        26: 'ম',
        27: 'য়',
        28: 'র',
        29: 'ল',
        30: 'ন',
        31: 'স',
        32: 'হ',
        33: 'ড়',
        34: 'ং',
        35: 'ঃ',
        36: '০',
        37: '১',
        38: '২',
        39: '৩',
        40: '৪',
        41: '৫',
        42: '৬',
        43: '৭',
        44: '৮',
        45: '৯',
        46: '_্',
        47: 'space',
        48: 'ঞ'
        }
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(1140, 700)
        Form.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 761, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color:white;\n"
"background-color: rgb(100, 185, 127);")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(770, 0, 371, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white;\n"
"background-color: rgb(100, 185, 127);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.img1 = QtWidgets.QLabel(self.frame)
        self.img1.setGeometry(QtCore.QRect(0, 30, 761, 461))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.img1.setFont(font)
        self.img1.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.img1.setText("")
        self.img1.setObjectName("img1")
        self.img2 = QtWidgets.QLabel(self.frame)
        self.img2.setGeometry(QtCore.QRect(770, 30, 371, 221))
        self.img2.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.img2.setText("")
        self.img2.setScaledContents(True)
        self.img2.setObjectName("img2")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(770, 270, 371, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color:white;\n"
"background-color: rgb(100, 185, 127);")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.statusFrame = QtWidgets.QFrame(self.frame)
        self.statusFrame.setGeometry(QtCore.QRect(770, 300, 371, 191))
        self.statusFrame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.statusFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.statusFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.statusFrame.setObjectName("statusFrame")
        self.label_6 = QtWidgets.QLabel(self.statusFrame)
        self.label_6.setGeometry(QtCore.QRect(10, 10, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color:white;")
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.statusFrame)
        self.label_7.setGeometry(QtCore.QRect(10, 50, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color:white;")
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.statusFrame)
        self.label_8.setGeometry(QtCore.QRect(10, 90, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color:white;")
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.lbl_accuracy = QtWidgets.QLabel(self.statusFrame)
        self.lbl_accuracy.setGeometry(QtCore.QRect(290, 10, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_accuracy.setFont(font)
        self.lbl_accuracy.setStyleSheet("color:white;")
        self.lbl_accuracy.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_accuracy.setObjectName("lbl_accuracy")
        self.lbl_char = QtWidgets.QLabel(self.statusFrame)
        self.lbl_char.setGeometry(QtCore.QRect(290, 50, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Siyam Rupali ANSI")
        font.setPointSize(18)
        self.lbl_char.setFont(font)
        self.lbl_char.setStyleSheet("color:white;")
        self.lbl_char.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_char.setObjectName("lbl_char")
        self.lbl_count = QtWidgets.QLabel(self.statusFrame)
        self.lbl_count.setGeometry(QtCore.QRect(290, 90, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_count.setFont(font)
        self.lbl_count.setStyleSheet("color:white;")
        self.lbl_count.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_count.setObjectName("lbl_count")
        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet("color:white;\n"
"font: 32pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(0, 85, 127);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet("color:white;\n"
"font: 32pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(0, 85, 127);")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/image/training_80px.png"))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("BSL Smart Avator Tutor")
        self.label_3.setText( "Live Camera")
        self.label_4.setText("Mimic Sign")
        self.label_5.setText( "Learning Status")
        self.label_6.setText( "Recognition Accuracy : ")
        self.label_7.setText( "Character :")
        self.label_8.setText( "Learning Count :")


        self.lbl_accuracy.setText( "100%")
        self.lbl_char.setText( "-")
        self.lbl_count.setText( "0/49")
        self.label.setText( "BSL Smart Avator Tutor\n")
        self.start_detection()

        

    def start_detection(self):
        model_path = "models/best.onnx"
        self.thread = DetectionThread(model_path)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.character_signal.connect(self.update_character)
        self.thread.recognition_accuracy.connect(self.update_accuracy)
        self.thread.next_character.connect(self.update_sample)
        self.thread.start()
        self.update_sample(1)
  
    def update_accuracy(self, accuracy):
        self.lbl_accuracy.setText(f"{round(accuracy*100, 2)}%")

    def update_character(self, character):
        self.lbl_count.setText(f"{character+1}/49")
        self.lbl_char.setText(self.bengali_characters.get(character))
        # self.update_sample(int(character+1))

    def update_sample(self,val):
        print(f"Show {val}.png")
        img = QtGui.QPixmap(f"signs/{val}.png")
        img = img.scaled(370, 220, Qt.KeepAspectRatio)
        self.img2.setPixmap(img)

    def update_image(self, img_bytes):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(img_bytes)
        self.img1.setPixmap(pixmap)

    def closeEvent(self, event):
        if self.thread is not None:
            self.thread.stop()
            self.thread.wait()
        event.accept()



import ui.res
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

