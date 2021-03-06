# -*- coding: utf-8 -*-
import logging

from box import Box
from qtpy import QtCore, QtWidgets

from fastflix.encoders.common.setting_panel import SettingPanel

logger = logging.getLogger("fastflix")

recommended_bitrates = [
    "500k    (320x240p @ 30fps)",
    "800k    (640x360p @ 30fps)",
    "1000k  (640x480p @ 30fps)",
    "1500k  (1280x720p @ 30fps)",
    "3000k  (1280x720p @ 60fps)",
    "5000k  (1080p @ 30fps)",
    "8000k  (1080p @ 60fps)",
    "12000k (1440p @ 30fps)",
    "20000k (1440p @ 60fps)",
    "30000k (2160p @ 30fps)",
    "45000k (2160p @ 60fps)",
    "Custom",
]

recommended_crfs = [
    "23 (x264 default - lower quality)",
    "22",
    "21",
    "20",
    "19 (480p)",
    "18 (720p)",
    "17 (1080p)",
    "16 (1440p)",
    "15 (2160p)",
    "14 (high quality)",
    "Custom",
]


pix_fmts = ["8-bit: yuv420p", "10-bit: yuv420p10le"]


class AVC(SettingPanel):
    def __init__(self, parent, main):
        super(AVC, self).__init__(parent)
        self.main = main

        grid = QtWidgets.QGridLayout()

        self.widgets = Box(remove_hdr=None, mode=None)

        self.mode = "CRF"
        self.updating_settings = False

        grid.addLayout(self.init_modes(), 0, 2, 6, 4)
        grid.addLayout(self._add_custom(), 10, 0, 1, 6)

        grid.addLayout(self.init_preset(), 1, 0, 1, 2)
        grid.addLayout(self._add_remove_hdr(), 2, 0, 1, 2)
        grid.addLayout(self.init_max_mux(), 3, 0, 1, 2)
        grid.addLayout(self.init_tune(), 4, 0, 1, 2)
        grid.addLayout(self.init_profile(), 5, 0, 1, 2)
        grid.addLayout(self.init_pix_fmt(), 6, 0, 1, 2)

        # grid.addWidget(QtWidgets.QWidget(), 8, 0)
        grid.setRowStretch(9, 1)

        guide_label = QtWidgets.QLabel(
            "<a href='https://trac.ffmpeg.org/wiki/Encode/H.264'>FFMPEG AVC / H.264 Encoding Guide</a>"
        )
        guide_label.setAlignment(QtCore.Qt.AlignBottom)
        guide_label.setOpenExternalLinks(True)
        grid.addWidget(guide_label, 11, 0, -1, 1)

        self.setLayout(grid)
        self.hide()

    def init_preset(self):
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Preset")
        label.setToolTip(
            "The slower the preset, the better the compression and quality\n"
            "Slow is highest personal recommenced, as past that is much smaller gains"
        )
        layout.addWidget(label)
        self.widgets.preset = QtWidgets.QComboBox()
        self.widgets.preset.addItems(
            ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow", "placebo"]
        )
        self.widgets.preset.setCurrentIndex(5)
        self.widgets.preset.currentIndexChanged.connect(lambda: self.main.page_update())
        layout.addWidget(self.widgets.preset)
        return layout

    def init_tune(self):
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Tune")
        label.setToolTip("Tune the settings for a particular type of source or situation")
        layout.addWidget(label)
        self.widgets.tune = QtWidgets.QComboBox()
        self.widgets.tune.addItems(
            ["default", "film", "animation", "grain", "stillimage", "psnr", "ssim", "zerolatency", "fastdecode"]
        )
        self.widgets.tune.setCurrentIndex(0)
        self.widgets.tune.currentIndexChanged.connect(lambda: self.main.page_update())
        layout.addWidget(self.widgets.tune)
        return layout

    def init_profile(self):
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Profile")
        label.setToolTip("Enforce an encode profile")
        layout.addWidget(label)
        self.widgets.profile = QtWidgets.QComboBox()
        self.widgets.profile.addItems(["default", "baseline", "main", "high", "high10", "high422", "high444"])
        self.widgets.profile.setCurrentIndex(0)
        self.widgets.profile.currentIndexChanged.connect(lambda: self.main.page_update())
        layout.addWidget(self.widgets.profile)
        return layout

    def init_max_mux(self):
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Max Muxing Queue Size")
        label.setToolTip('Only change this if you are getting the error "Too many packets buffered for output stream"')
        layout.addWidget(label)
        self.widgets.max_mux = QtWidgets.QComboBox()
        self.widgets.max_mux.addItems(["default", "1024", "2048", "4096", "8192"])
        self.widgets.max_mux.setCurrentIndex(0)
        self.widgets.max_mux.currentIndexChanged.connect(lambda: self.main.page_update())
        layout.addWidget(self.widgets.max_mux)
        return layout

    def init_pix_fmt(self):
        return self._add_combo_box(
            label="Bit Depth",
            tooltip="Pixel Format (requires at least 10-bit for HDR)",
            widget_name="pix_fmt",
            options=pix_fmts,
            default=0,
        )

    def init_modes(self):
        layout = QtWidgets.QGridLayout()
        crf_group_box = QtWidgets.QGroupBox()
        crf_group_box.setStyleSheet("QGroupBox{padding-top:5px; margin-top:-18px}")
        crf_box_layout = QtWidgets.QHBoxLayout()
        bitrate_group_box = QtWidgets.QGroupBox()
        bitrate_group_box.setStyleSheet("QGroupBox{padding-top:5px; margin-top:-18px}")
        bitrate_box_layout = QtWidgets.QHBoxLayout()
        self.widgets.mode = QtWidgets.QButtonGroup()
        self.widgets.mode.buttonClicked.connect(self.set_mode)

        bitrate_radio = QtWidgets.QRadioButton("Bitrate")
        bitrate_radio.setFixedWidth(80)
        self.widgets.mode.addButton(bitrate_radio)
        self.widgets.bitrate = QtWidgets.QComboBox()
        self.widgets.bitrate.setFixedWidth(250)
        self.widgets.bitrate.addItems(recommended_bitrates)
        self.widgets.bitrate.setCurrentIndex(6)
        self.widgets.bitrate.currentIndexChanged.connect(lambda: self.mode_update())
        self.widgets.custom_bitrate = QtWidgets.QLineEdit("3000")
        self.widgets.custom_bitrate.setFixedWidth(100)
        self.widgets.custom_bitrate.setDisabled(True)
        self.widgets.custom_bitrate.textChanged.connect(lambda: self.main.build_commands())
        bitrate_box_layout.addWidget(bitrate_radio)
        bitrate_box_layout.addWidget(self.widgets.bitrate)
        bitrate_box_layout.addStretch()
        bitrate_box_layout.addWidget(QtWidgets.QLabel("Custom:"))
        bitrate_box_layout.addWidget(self.widgets.custom_bitrate)

        crf_help = "CRF is extremely source dependant,<br>" "the resolution-to-crf are mere suggestions!<br>"
        crf_radio = QtWidgets.QRadioButton("CRF")
        crf_radio.setChecked(True)
        crf_radio.setFixedWidth(80)
        crf_radio.setToolTip(crf_help)
        self.widgets.mode.addButton(crf_radio)

        self.widgets.crf = QtWidgets.QComboBox()
        self.widgets.crf.setToolTip(crf_help)
        self.widgets.crf.setFixedWidth(250)
        self.widgets.crf.addItems(recommended_crfs)
        self.widgets.crf.setCurrentIndex(0)
        self.widgets.crf.currentIndexChanged.connect(lambda: self.mode_update())
        self.widgets.custom_crf = QtWidgets.QLineEdit("30")
        self.widgets.custom_crf.setFixedWidth(100)
        self.widgets.custom_crf.setDisabled(True)
        self.widgets.custom_crf.setValidator(self.only_int)
        self.widgets.custom_crf.textChanged.connect(lambda: self.main.build_commands())
        crf_box_layout.addWidget(crf_radio)
        crf_box_layout.addWidget(self.widgets.crf)
        crf_box_layout.addStretch()
        crf_box_layout.addWidget(QtWidgets.QLabel("Custom:"))
        crf_box_layout.addWidget(self.widgets.custom_crf)

        bitrate_group_box.setLayout(bitrate_box_layout)
        crf_group_box.setLayout(crf_box_layout)

        layout.addWidget(crf_group_box, 0, 0)
        layout.addWidget(bitrate_group_box, 1, 0)
        return layout

    def mode_update(self):
        self.widgets.custom_crf.setDisabled(self.widgets.crf.currentText() != "Custom")
        self.widgets.custom_bitrate.setDisabled(self.widgets.bitrate.currentText() != "Custom")
        self.main.build_commands()

    def setting_change(self, update=True):
        if self.updating_settings:
            return
        self.updating_settings = True

        if update:
            self.main.page_update()
        self.updating_settings = False

    def get_settings(self):
        settings = Box(
            disable_hdr=bool(self.widgets.remove_hdr.currentIndex()),
            preset=self.widgets.preset.currentText(),
            max_mux=self.widgets.max_mux.currentText(),
            profile=self.widgets.profile.currentText(),
            pix_fmt=self.widgets.pix_fmt.currentText().split(":")[1].strip(),
            extra=self.ffmpeg_extras,
        )

        tune = self.widgets.tune.currentText()
        settings.tune = tune if tune.lower() != "default" else None

        if self.mode == "CRF":
            crf = self.widgets.crf.currentText()
            settings.crf = int(crf.split(" ", 1)[0]) if crf != "Custom" else int(self.widgets.custom_crf.text())
        else:
            bitrate = self.widgets.bitrate.currentText()
            if bitrate.lower() == "custom":
                settings.bitrate = self.widgets.custom_bitrate.text()
            else:
                settings.bitrate = bitrate.split(" ", 1)[0]
        return settings

    def set_mode(self, x):
        self.mode = x.text()
        self.main.build_commands()
