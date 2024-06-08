from PySide6.QtWidgets import *
from PySide6.QtMultimediaWidgets import *
from PySide6.QtMultimedia import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from functools import lru_cache
import os
import logging
from config import BASE_DIR, MEDIA_PLAYER_HEIGHT, MEDIA_PATH, MEDIA_PLAYER_WIDTH

class MediaCache:
    def __init__(self):
        self.cache = {}

    def get_media(self, path):
        if path not in self.cache:
            if path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                pixmap = QPixmap(path)
                self.cache[path] = pixmap
                logging.info(f"Loaded image from disk: {path}")
            elif path.lower().endswith(('.mp4', '.avi', '.mkv')):
                media_url = QUrl.fromLocalFile(path)
                self.cache[path] = media_url
                logging.info(f"Loaded video from disk: {path}")
        return self.cache[path]


class MediaDisplayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing MediaDisplayWidget")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.video_widget = QVideoWidget()
        self.image_label = QLabel()

        self.video_widget.setMaximumWidth(MEDIA_PLAYER_WIDTH)
        self.video_widget.setMaximumHeight(MEDIA_PLAYER_HEIGHT)

        self.image_label.setMaximumWidth(MEDIA_PLAYER_WIDTH)
        self.image_label.setMaximumHeight(MEDIA_PLAYER_HEIGHT)

        self.video_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.image_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.image_label.setScaledContents(False)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.video_widget)
        self.layout.addWidget(self.image_label)
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)  # Verbinde AudioOutput mit MediaPlayer
        self.player.setVideoOutput(self.video_widget)

        if not self.player.isAvailable():
            self.logger.error("QMediaPlayer is not available")
            available_backends = QMediaPlayer.availableMediaEngines()
            self.logger.error(f"Available media engines: {available_backends}")
        if not self.video_widget.isEnabled():
            self.logger.error("QVideoWidget is not available")

        self.audio_output.setVolume(0.0)

        self.media_cache = MediaCache()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.switch_media)
        self.current_media = "image"
        self.load_media_files(MEDIA_PATH)
    
    def load_media_files(self, relative_directory):
        directory = os.path.join(BASE_DIR, relative_directory)
        
        try: 
            self.media_files = []
            for file in os.listdir(directory):
                media = self.media_cache.get_media(os.path.join(directory, file))
                if isinstance(media, QPixmap):
                    self.media_files.append((media, 10000))  # 10 seconds for images
                else:
                    self.media_files.append((media, 0))  # Duration handled by video metadata
            if self.media_files:
                self.current_media_index = 0
                self.load_media()
        except Exception as e:
            error_message = f"Failed to load media files from directory {directory}: {str(e)}"
            self.logger.error(error_message)
        '''
        try: 
            self.media_files = []
            for file in os.listdir(directory):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    self.media_files.append((QUrl.fromLocalFile(os.path.join(directory, file)), 10000))
                elif file.lower().endswith(('.mp4', '.avi', '.mkv')):
                    self.media_files.append((QUrl.fromLocalFile(os.path.join(directory, file)), 0))
            if self.media_files:
                self.current_media_index = 0
                self.load_media()
        except Exception as e:
            error_message = f"Failed to load media files from directory {directory}: {str(e)}"
            logging.error(error_message)
        '''
    
    def load_media(self):
        try:
            media, duration = self.media_files[self.current_media_index]
            if isinstance(media, QPixmap):
                self.load_image(media, duration)
            elif isinstance(media, QUrl):
                self.load_video(media)
        except Exception as e:
            logging.error(f"Failed to load media {str(e)}")

    def load_video(self, video_url):
        try:
            self.player.setSource(video_url)
            self.player.play()
            self.video_widget.show()
            #print(f"Video Widget wh: {self.video_widget.width()} / {self.video_widget.height()}")
            self.image_label.hide()
            self.player.durationChanged.connect(self.set_video_duration)
        except Exception as e:
            logging.error(f"Failed to play video: {str(e)}")


    def load_image(self, pixmap, display_duration):
        try:
            self.player.stop()
            #self.image_label.setPixmap(pixmap)
            #pixmap = QPixmap(image_url.toLocalFile())
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(self.image_label.maximumWidth(), self.image_label.maximumHeight(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
            else:
                logging.error("Received a null QPixmap, cannot display image.")
            self.image_label.show()
            #print(f"Image Label wh: {self.image_label.width()} / {self.image_label.height()}")
            self.video_widget.hide()
            self.timer.start(display_duration)
        except Exception as e:
            logging.error(f"Failed to display image: {str(e)}")
    
    def set_video_duration(self, duration):
        if duration > 0:
            self.media_files[self.current_media_index] = (self.media_files[self.current_media_index][0], duration)
            self.timer.start(duration)

    def switch_media(self):
        try:
            self.current_media_index = (self.current_media_index + 1) % len(self.media_files)
            self.load_media()
        except Exception as e:
            logging.error(f"Failed to switch media: {str(e)}")

