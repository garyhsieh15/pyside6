# -*- coding: utf-8 -*-
from PySide6.QtCore import QObject, QEvent, Qt, QSize, QUrl
from PySide6.QtGui import QIcon, QImageReader, QPixmap
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QSizePolicy,
    QSplitter,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)


class PreviewManager(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.preview_panel = QWidget(parent)
        self.preview_layout = QVBoxLayout(self.preview_panel)
        self.preview_layout.setContentsMargins(0, 0, 0, 0)

        self.preview_controls = QWidget(self.preview_panel)
        self.preview_controls_layout = QHBoxLayout(self.preview_controls)
        self.preview_controls_layout.setContentsMargins(8, 8, 8, 8)

        self.btn_preview_single = QPushButton(self.preview_controls)
        self.btn_preview_dual = QPushButton(self.preview_controls)
        self.btn_preview_add_second = QPushButton(self.preview_controls)

        icon_size = QSize(20, 20)
        self._init_button(
            self.btn_preview_single,
            "images/toolbar_icons/view_single.svg",
            "單一",
            icon_size,
            checkable=True,
        )
        self._init_button(
            self.btn_preview_dual,
            "images/toolbar_icons/view_dual.svg",
            "雙畫面",
            icon_size,
            checkable=True,
        )
        self._init_button(
            self.btn_preview_add_second,
            "images/toolbar_icons/add_second.svg",
            "加入第二個",
            icon_size,
            checkable=False,
        )
        self.btn_preview_add_second.setStyleSheet(
            "QPushButton { border-radius: 0px; padding: 2px; border: none; }"
            "QPushButton:pressed { background-color: #D6D6D6; }"
        )

        self.preview_controls_layout.addStretch(1)
        self.preview_controls_layout.addWidget(self.btn_preview_single)
        self.preview_controls_layout.addWidget(self.btn_preview_dual)
        self.preview_controls_layout.addWidget(self.btn_preview_add_second)

        self.preview_splitter = QSplitter(Qt.Horizontal, self.preview_panel)
        self.preview_layout.addWidget(self.preview_splitter)

        self.slot1 = self._create_preview_slot()
        self.slot2 = self._create_preview_slot()
        self.preview_splitter.addWidget(self.slot1["container"])
        self.preview_splitter.addWidget(self.slot2["container"])
        self.preview_splitter.setStretchFactor(0, 1)
        self.preview_splitter.setStretchFactor(1, 1)
        self.preview_splitter.setSizes([1, 0])
        self.slot2["container"].setVisible(False)

        self.preview_mode = 1
        self.next_slot = 1
        self.preview_mode_group = QButtonGroup(self)
        self.preview_mode_group.setExclusive(True)
        self.preview_mode_group.addButton(self.btn_preview_single)
        self.preview_mode_group.addButton(self.btn_preview_dual)
        self.btn_preview_single.setChecked(True)

        self.btn_preview_single.clicked.connect(lambda: self.set_preview_mode(1))
        self.btn_preview_dual.clicked.connect(lambda: self.set_preview_mode(2))
        self.btn_preview_add_second.clicked.connect(self.select_second_slot)

    def panel_widget(self):
        return self.preview_panel

    def controls_widget(self):
        return self.preview_controls

    def handle_tree_click(self, index, fs_model):
        file_path = fs_model.filePath(index)
        if fs_model.isDir(index):
            return

        slot = self.slot1 if self.preview_mode == 1 or self.next_slot == 1 else self.slot2
        self.next_slot = 1

        slot["player"].stop()
        slot["btn_video_play"].setText("播放")
        slot["video_progress"].setValue(0)
        slot["preview_placeholder"].setText("請選擇圖片或影片檔案")
        slot["preview_stack"].setCurrentWidget(slot["preview_placeholder"])

        if QImageReader(file_path).canRead():
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                slot["current_pixmap"] = pixmap
                self._update_image_preview(slot)
                slot["preview_stack"].setCurrentWidget(slot["preview_image_frame"])
                return

        lower_path = file_path.lower()
        if lower_path.endswith((".mp4", ".mov", ".m4v", ".avi", ".mkv")):
            slot["player"].setSource(QUrl.fromLocalFile(file_path))
            slot["preview_stack"].setCurrentWidget(slot["video_page"])
            return

        slot["preview_placeholder"].setText("不支援的檔案類型")
        slot["preview_stack"].setCurrentWidget(slot["preview_placeholder"])

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Resize:
            if obj is self.slot1["preview_image"]:
                self._update_image_preview(self.slot1)
            elif obj is self.slot2["preview_image"]:
                self._update_image_preview(self.slot2)
        return super().eventFilter(obj, event)

    def set_preview_mode(self, mode):
        self.preview_mode = mode
        if mode == 1:
            self.slot2["container"].setVisible(False)
            self.preview_splitter.setSizes([1, 0])
            self._stop_slot_playback(self.slot2)
        else:
            self.slot2["container"].setVisible(True)
            self.preview_splitter.setSizes([1, 1])

    def select_second_slot(self):
        if self.preview_mode == 1:
            self.set_preview_mode(2)
        self.next_slot = 2

    def _init_button(self, button, icon_path, tooltip, icon_size, checkable):
        button.setIcon(QIcon(icon_path))
        button.setIconSize(icon_size)
        button.setText("")
        button.setToolTip(tooltip)
        if checkable:
            button.setCheckable(True)
            button.setStyleSheet(
                "QPushButton { border-radius: 0px; padding: 2px; border: none; }"
                "QPushButton:checked { background-color: #D6D6D6; border: none; }"
            )
        else:
            button.setStyleSheet(
                "QPushButton { border-radius: 0px; padding: 2px; border: none; }"
            )

    def _update_image_preview(self, slot):
        if not slot["current_pixmap"]:
            return
        target_size = slot["preview_image"].size()
        if target_size.width() <= 0 or target_size.height() <= 0:
            return
        scaled = slot["current_pixmap"].scaled(
            target_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        slot["preview_image"].setPixmap(scaled)

    def _create_preview_slot(self):
        container = QWidget(self.preview_panel)
        stack = QStackedLayout(container)
        placeholder = QLabel("請選擇圖片或影片檔案", container)
        placeholder.setAlignment(Qt.AlignCenter)

        image = QLabel(container)
        image.setAlignment(Qt.AlignCenter)
        image.setMinimumSize(0, 0)
        image.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        image.installEventFilter(self)
        image_frame = QWidget(container)
        image_frame_layout = QVBoxLayout(image_frame)
        image_frame_layout.setContentsMargins(0, 0, 0, 0)
        image_row = QWidget(image_frame)
        image_row_layout = QHBoxLayout(image_row)
        image_row_layout.setContentsMargins(0, 0, 0, 0)
        image_row_layout.addStretch(1)
        image_row_layout.addWidget(image, 4)
        image_row_layout.addStretch(1)
        image_frame_layout.addStretch(1)
        image_frame_layout.addWidget(image_row, 4)
        image_frame_layout.addStretch(1)

        video_widget = QVideoWidget(container)
        video_page = QWidget(container)
        video_layout = QVBoxLayout(video_page)
        video_layout.setContentsMargins(0, 0, 0, 0)
        video_layout.addWidget(video_widget)
        video_controls = QWidget(video_page)
        video_controls_layout = QHBoxLayout(video_controls)
        video_controls_layout.setContentsMargins(8, 8, 8, 8)
        btn_play = QPushButton("播放", video_controls)
        btn_stop = QPushButton("停止", video_controls)
        progress = QSlider(Qt.Horizontal, video_controls)
        progress.setRange(0, 0)
        progress.setSingleStep(1000)
        progress.setPageStep(5000)
        volume = QSlider(Qt.Horizontal, video_controls)
        volume.setRange(0, 100)
        volume.setValue(50)
        volume.setFixedWidth(120)
        video_controls_layout.addWidget(btn_play)
        video_controls_layout.addWidget(btn_stop)
        video_controls_layout.addWidget(progress)
        video_controls_layout.addWidget(volume)
        video_layout.addWidget(video_controls)

        stack.addWidget(placeholder)
        stack.addWidget(image_frame)
        stack.addWidget(video_page)

        player = QMediaPlayer(self)
        audio_output = QAudioOutput(self)
        audio_output.setVolume(0.5)
        player.setAudioOutput(audio_output)
        player.setVideoOutput(video_widget)

        slot = {
            "container": container,
            "preview_stack": stack,
            "preview_placeholder": placeholder,
            "preview_image": image,
            "preview_image_frame": image_frame,
            "video_page": video_page,
            "player": player,
            "audio_output": audio_output,
            "btn_video_play": btn_play,
            "btn_video_stop": btn_stop,
            "video_progress": progress,
            "video_volume": volume,
            "current_pixmap": None,
        }

        btn_play.clicked.connect(lambda: self._toggle_slot_playback(slot))
        btn_stop.clicked.connect(lambda: self._stop_slot_playback(slot))
        player.positionChanged.connect(lambda pos: self._update_slot_position(slot, pos))
        player.durationChanged.connect(lambda dur: self._update_slot_duration(slot, dur))
        progress.sliderMoved.connect(lambda pos: self._seek_slot_position(slot, pos))
        volume.valueChanged.connect(lambda val: self._update_slot_volume(slot, val))

        return slot

    def _toggle_slot_playback(self, slot):
        if slot["player"].playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            slot["player"].pause()
            slot["btn_video_play"].setText("播放")
        else:
            slot["player"].play()
            slot["btn_video_play"].setText("暫停")

    def _stop_slot_playback(self, slot):
        slot["player"].stop()
        slot["btn_video_play"].setText("播放")
        slot["video_progress"].setValue(0)

    def _update_slot_position(self, slot, position):
        if not slot["video_progress"].isSliderDown():
            slot["video_progress"].setValue(position)

    def _update_slot_duration(self, slot, duration):
        slot["video_progress"].setRange(0, duration)

    def _seek_slot_position(self, slot, position):
        slot["player"].setPosition(position)

    def _update_slot_volume(self, slot, value):
        slot["audio_output"].setVolume(value / 100.0)
