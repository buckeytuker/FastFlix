# -*- coding: utf-8 -*-
import logging

from box import Box

from fastflix.shared import QtWidgets, QtCore

logger = logging.getLogger("fastflix")

recommended_bitrates = [
    "100k   (320x240p @ 24,25,30)",
    "200k   (640x360p @ 24,25,30)",
    "400k   (640x480p @ 24,25,30)",
    "800k  (1280x720p @ 24,25,30)",
    "1200k (1280x720p @ 50,60)",
    "1200k (1920x1080p @ 24,25,30)",
    "2000k (1920x1080p @ 50,60)",
    "4000k (2560x1440p @ 24,25,30)",
    "6000k (2560x1440p @ 50,60)",
    "9000k (3840x2160p @ 24,25,30)",
    "13000k (3840x2160p @ 50,60)",
    "Custom",
]

recommended_qps = ["80", "90", "100", "110", "120", "130", "140", "150", "Custom"]


class RAV1E(QtWidgets.QWidget):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.main = main

        grid = QtWidgets.QGridLayout()

        self.widgets = Box(fps=None, remove_hdr=None, mode=None)

        self.mode = "bitrate"

        grid.addLayout(self.init_speed(), 0, 0, 1, 2)
        grid.addLayout(self.init_remove_hdr(), 1, 0, 1, 2)
        grid.addLayout(self.init_range(), 2, 0, 1, 2)
        grid.addLayout(self.init_tune(), 3, 0, 1, 2)
        grid.addLayout(self.init_color_primaries(), 4, 0, 1, 2)
        grid.addLayout(self.init_transfer(), 5, 0, 1, 2)
        grid.addLayout(self.init_matrix(), 6, 0, 1, 2)

        grid.addLayout(self.init_modes(), 0, 2, 3, 3)

        grid.addWidget(QtWidgets.QWidget(), 5, 0)
        grid.setRowStretch(5, 1)
        guide_label = QtWidgets.QLabel(f"<a href='https://github.com/xiph/rav1e'>rav1e github page</a>")
        guide_label.setAlignment(QtCore.Qt.AlignBottom)
        guide_label.setOpenExternalLinks(True)
        grid.addWidget(guide_label, 9, 0, -1, 1)

        self.setLayout(grid)
        self.hide()

    def init_remove_hdr(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Remove HDR"))
        self.widgets.remove_hdr = QtWidgets.QComboBox()
        self.widgets.remove_hdr.addItems(["No", "Yes"])
        self.widgets.remove_hdr.setCurrentIndex(0)
        self.widgets.remove_hdr.setDisabled(True)
        self.widgets.remove_hdr.currentIndexChanged.connect(lambda: self.main.page_update())
        layout.addWidget(self.widgets.remove_hdr)
        return layout

    def init_range(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Pixel Range"))
        self.widgets.pixel_range = QtWidgets.QComboBox()
        self.widgets.pixel_range.addItems(["Limited", "Full"])
        self.widgets.pixel_range.setCurrentIndex(0)
        self.widgets.pixel_range.currentIndexChanged.connect(lambda: self.main.page_update())
        layout.addWidget(self.widgets.pixel_range)
        return layout

    def init_speed(self):
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Speed")
        label.setToolTip("lower = high quality, slower speed")
        layout.addWidget(label)
        self.widgets.speed = QtWidgets.QComboBox()
        self.widgets.speed.addItems([str(i) for i in range(11)])
        self.widgets.speed.setCurrentIndex(6)
        self.widgets.speed.currentIndexChanged.connect(lambda: self.main.page_update())
        layout.addWidget(self.widgets.speed)
        return layout

    def init_tune(self):
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Tune")
        label.setToolTip("Quality tuning")
        layout.addWidget(label)
        self.widgets.speed = QtWidgets.QComboBox()
        self.widgets.speed.addItems(["Psychovisual", "Psnr"])
        self.widgets.speed.setCurrentIndex(0)
        self.widgets.speed.currentIndexChanged.connect(lambda: self.main.page_update())
        layout.addWidget(self.widgets.speed)
        return layout

    def init_color_primaries(self):
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Tune")
        label.setToolTip("Quality tuning")
        layout.addWidget(label)
        self.widgets.color_primaries = QtWidgets.QComboBox()
        self.widgets.color_primaries.addItems(
            [
                "Auto",
                "BT709",
                "BT470M",
                "BT470BG",
                "BT601",
                "SMPTE240",
                "GenericFilm",
                "BT2020",
                "XYZ",
                "SMPTE431",
                "SMPTE432",
                "EBU3213",
            ]
        )
        self.widgets.color_primaries.setCurrentIndex(0)
        self.widgets.color_primaries.currentIndexChanged.connect(lambda: self.main.page_update())
        layout.addWidget(self.widgets.color_primaries)
        return layout

    def init_transfer(self):
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Transfer Characteristics")
        label.setToolTip("Transfer Characteristics used to describe color parameters")
        layout.addWidget(label)
        self.widgets.transfer = QtWidgets.QComboBox()
        self.widgets.transfer.addItems(
            [
                "Auto",
                "BT709",
                "BT470M",
                "BT470BG",
                "BT601",
                "SMPTE240",
                "Linear",
                "Log100",
                "Log100Sqrt10",
                "IEC61966",
                "BT1361",
                "SRGB",
                "BT2020_10Bit",
                "BT2020_12Bit",
                "SMPTE2084",
                "SMPTE428",
                "HLG",
            ]
        )
        self.widgets.transfer.setCurrentIndex(0)
        self.widgets.transfer.currentIndexChanged.connect(lambda: self.main.page_update())
        layout.addWidget(self.widgets.transfer)
        return layout

    def init_matrix(self):
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Matrix Coefficients")
        label.setToolTip("Matrix coefficients used to describe color parameters")
        layout.addWidget(label)
        self.widgets.matrix = QtWidgets.QComboBox()
        self.widgets.matrix.addItems(
            [
                "Auto",
                "Identity",
                "BT709",
                "FCC",
                "BT470BG",
                "BT601",
                "SMPTE240",
                "YCgCo",
                "BT2020NCL",
                "BT2020CL",
                "SMPTE2085",
                "ChromatNCL",
                "ChromatCL",
                "ICtCp",
            ]
        )
        self.widgets.matrix.setCurrentIndex(0)
        self.widgets.matrix.currentIndexChanged.connect(lambda: self.main.page_update())
        layout.addWidget(self.widgets.matrix)
        return layout

    def init_modes(self):
        layout = QtWidgets.QGridLayout()
        qp_group_box = QtWidgets.QGroupBox()
        qp_group_box.setFixedHeight(40)
        qp_group_box.setStyleSheet("QGroupBox{padding-top:5px; margin-top:-18px}")
        qp_box_layout = QtWidgets.QHBoxLayout()
        bitrate_group_box = QtWidgets.QGroupBox()
        bitrate_group_box.setFixedHeight(40)
        bitrate_group_box.setStyleSheet("QGroupBox{padding-top:5px; margin-top:-18px}")
        bitrate_box_layout = QtWidgets.QHBoxLayout()
        # rotation_dir = Path(base_path, 'data', 'rotations')
        # group_box.setStyleSheet("QGroupBox{padding-top:15px; margin-top:-15px; padding-bottom:-5px}")
        self.widgets.mode = QtWidgets.QButtonGroup()
        self.widgets.mode.buttonClicked.connect(self.set_mode)

        bitrate_radio = QtWidgets.QRadioButton("Bitrate")
        self.widgets.mode.addButton(bitrate_radio)
        self.widgets.bitrate = QtWidgets.QComboBox()
        self.widgets.bitrate.addItems(recommended_bitrates)
        self.widgets.bitrate.setCurrentIndex(6)
        self.widgets.bitrate.currentIndexChanged.connect(lambda: self.mode_update())
        self.widgets.custom_bitrate = QtWidgets.QLineEdit("3000")
        self.widgets.custom_bitrate.setFixedWidth(100)
        self.widgets.custom_bitrate.setDisabled(True)
        self.widgets.custom_bitrate.textChanged.connect(lambda: self.main.build_commands())
        bitrate_box_layout.addWidget(bitrate_radio)
        bitrate_box_layout.addWidget(self.widgets.bitrate)
        bitrate_box_layout.addWidget(QtWidgets.QLabel("Custom:"))
        bitrate_box_layout.addWidget(self.widgets.custom_bitrate)

        qp_radio = QtWidgets.QRadioButton("qp")
        qp_radio.setChecked(True)
        self.widgets.mode.addButton(qp_radio)

        self.widgets.qp = QtWidgets.QComboBox()
        self.widgets.qp.addItems(recommended_qps)
        self.widgets.qp.setCurrentIndex(2)
        self.widgets.qp.currentIndexChanged.connect(lambda: self.mode_update())
        self.widgets.custom_qp = QtWidgets.QLineEdit("30")
        self.widgets.custom_qp.setFixedWidth(100)
        self.widgets.custom_qp.setDisabled(True)
        self.widgets.custom_qp.textChanged.connect(lambda: self.main.build_commands())
        qp_box_layout.addWidget(qp_radio)
        qp_box_layout.addWidget(self.widgets.qp)
        qp_box_layout.addWidget(QtWidgets.QLabel("Custom:"))
        qp_box_layout.addWidget(self.widgets.custom_qp)

        bitrate_group_box.setLayout(bitrate_box_layout)
        qp_group_box.setLayout(qp_box_layout)

        layout.addWidget(qp_group_box, 0, 0)
        layout.addWidget(bitrate_group_box, 1, 0)
        return layout

    def mode_update(self):
        self.widgets.custom_qp.setDisabled(self.widgets.qp.currentText() != "Custom")
        self.widgets.custom_bitrate.setDisabled(self.widgets.bitrate.currentText() != "Custom")
        self.main.build_commands()

    def get_settings(self):
        settings = Box(
            disable_hdr=bool(self.widgets.remove_hdr.currentIndex()),
            speed=int(self.widgets.speed.currentText()),
            tune=self.widgets.tune.currentText(),
            pixel_range=self.widgets.pixel_range.currentText(),
            color_primaries=self.widgets.color_primaries.currentText(),
            matrix=self.widgets.matrix.currentText(),
            transfer=self.widgets.transfer.currentText(),
        )
        if self.mode == "qp":
            settings.qp = int(self.widgets.qp.currentText().split(" ", 1)[0])
        else:
            settings.bitrate = self.widgets.bitrate.currentText().split(" ", 1)[0]
        return settings

    def new_source(self):
        if not self.main.streams:
            return
        if self.main.streams["video"][self.main.video_track].get("color_space", "").startswith("bt2020"):
            self.widgets.remove_hdr.setDisabled(False)
        else:
            self.widgets.remove_hdr.setDisabled(True)

    def set_mode(self, x):
        self.mode = x.text()
