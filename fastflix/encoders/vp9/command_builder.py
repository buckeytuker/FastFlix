# -*- coding: utf-8 -*-
import re
import secrets
from pathlib import Path

import reusables

from fastflix.encoders.common.audio import build_audio
from fastflix.encoders.common.helpers import Command, generate_filters


def build(
    source,
    video_track,
    ffmpeg,
    temp_dir,
    output_video,
    bitrate=None,
    crf=None,
    start_time=0,
    duration=None,
    single_pass=False,
    quality="good",
    audio_tracks=(),
    speed=1,
    row_mt=0,
    force420=True,
    **kwargs,
):
    filters = generate_filters(**kwargs)
    audio = build_audio(audio_tracks)

    ending = "/dev/null"
    if reusables.win_based:
        ending = "NUL"

    beginning = (
        f'"{ffmpeg}" -y '
        f'-i "{source}" '
        f' {f"-ss {start_time}" if start_time else ""}  '
        f'{f"-t {duration}" if duration else ""} '
        f"-map 0:{video_track} "
        f"-c:v:0 libvpx-vp9 "
        f'{f"-vf {filters}" if filters else ""} '
        f'{"-pix_fmt yuv420p" if force420 else ""} '
        f'{"-row-mt 1" if row_mt else ""} '
        "-map_metadata -1 "
    )

    if not single_pass:
        pass_log_file = Path(temp_dir) / f"pass_log_file_{secrets.token_hex(10)}.log"
        beginning += f'-passlogfile "{pass_log_file}" '

    beginning = re.sub("[ ]+", " ", beginning)

    if bitrate:
        command_1 = f"{beginning} -b:v {bitrate} -quality good -pass 1 -an -f webm {ending}"
        command_2 = f'{beginning} -b:v {bitrate}  -quality {quality} -speed {speed} -pass 2 {audio} "{output_video}"'

    elif crf:
        command_1 = f"{beginning} -b:v 0 -crf {crf} -quality good -pass 1 -an -f webm {ending}"
        command_2 = (
            f"{beginning} -b:v 0 -crf {crf} -quality {quality} -speed {speed} "
            f'{"-pass 2" if not single_pass else ""} {audio} "{output_video}"'
        )

    else:
        return []

    if crf and single_pass:
        return [Command(command_2, ["ffmpeg", "output"], False, name="Single pass CRF", exe="ffmpeg")]
    pass_type = "bitrate" if bitrate else "CRF"
    return [
        Command(command_1, ["ffmpeg", "output"], False, name=f"First pass {pass_type}", exe="ffmpeg"),
        Command(command_2, ["ffmpeg", "output"], False, name=f"Second pass {pass_type} ", exe="ffmpeg"),
    ]
