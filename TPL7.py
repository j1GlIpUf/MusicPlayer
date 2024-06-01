import time

from PyQt5 import QtWidgets
from Player1 import Ui_MainWindow  # импорт нашего сгенерированного файла
import sys
import os
from pygame import mixer
from pyglet import media
import threading
import time
from PyQt5 import QtWidgets, QtCore
from Player1 import Ui_MainWindow  # импорт нашего сгенерированного файла
import sys
import os
from pygame import mixer
from mutagen.mp3 import MP3

all_name_music_likst = os.listdir("D:\\Music")
count = 0

mixer.init()
max_size_song = 0
pause = False

class mywindow(QtWidgets.QMainWindow):
    update_progress_signal = QtCore.pyqtSignal(float)

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        mixer.music.load(f"D:\\Music\\{all_name_music_likst[count]}")

        self.ui.pushButton.clicked.connect(self._play_music)
        self.ui.pushButton_2.clicked.connect(self._stop_music)
        self.ui.pushButton_3.clicked.connect(self._next_music)
        self.ui.pushButton_4.clicked.connect(self._back_music)
        self.ui.dial.valueChanged.connect(self._reg_value_music)
        self.update_progress_signal.connect(self.update_slider)
        self.ui.horizontalSlider.sliderMoved.connect(self._set_music_pos)
        self.progress_thread = threading.Thread(target=self.update_progress)
        self.progress_thread.daemon = True
        self.progress_thread.start()

    def _play_music(self):
        global pause
        pause = False
        mixer.music.play()
        self._set_value_music()
        audio = MP3(f"D:\\Music\\{all_name_music_likst[count]}")
        global max_size_song
        max_size_song = audio.info.length
        print(max_size_song)

    def _stop_music(self):
        mixer.music.stop()
        global pause
        pause = True

    def _next_music(self):
        self.ui.horizontalSlider.setValue(0)
        global count, max_size_song
        if count == len(all_name_music_likst) - 1:
            count = 0
        else:
            count += 1
        self._load_music()
        mixer.music.play()
        self._set_value_music()

    def _back_music(self):
        global count
        if count == 0:
            count = len(all_name_music_likst) - 1
        else:
            count -= 1
        self._load_music()
        mixer.music.play()
        self._set_value_music()

    def _load_music(self):
        global count, max_size_song
        mixer.music.load(f"D:\\Music\\{all_name_music_likst[count]}")
        audio = MP3(f"D:\\Music\\{all_name_music_likst[count]}")
        max_size_song = audio.info.length

    def _reg_value_music(self):
        value = self.ui.dial.value()
        mixer.music.set_volume(value / 100)

    def _set_music_pos(self):
        global max_size_song
        pos = self.ui.horizontalSlider.value()
        mixer.music.play(start=pos * max_size_song / 100)

    def update_progress(self):
        global current_position, pause, max_size_song
        while True:
            if mixer.music.get_busy() and not pause:
                current_position = (mixer.music.get_pos() / 1000) / max_size_song * 100
                self.update_progress_signal.emit(current_position)

                if current_position >= 100:
                    self._stop_music()
                    max_size_song = 0
            time.sleep(0.1)

    def update_slider(self, current_position):
        self.ui.horizontalSlider.setValue(int(current_position))

    def _set_value_music(self):
        mixer.music.set_volume(0.1)

app = QtWidgets.QApplication([])

application = mywindow()
application.show()

sys.exit(app.exec())
