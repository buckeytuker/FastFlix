# -*- coding: utf-8 -*-
import re
import secrets
from pathlib import Path

from box import Box

from fastflix.encoders.common.audio import build_audio
from fastflix.encoders.common.helpers import Command, generate_ending, generate_ffmpeg_start, generate_filters, null
from fastflix.encoders.common.subtitles import build_subtitle


def build(
    source,
    video_track,
    ffmpeg,
    temp_dir,
    output_video,
    bitrate=None,
    crf=None,
    preset="fast",
    audio_tracks=(),
    subtitle_tracks=(),
    disable_hdr=False,
    side_data=None,
    x265_params=None,
    intra_encoding=False,
    pix_fmt="yuv420p10le",
    tune=None,
    profile="default",
    attachments="",
    **kwargs,
):
    filters = generate_filters(disable_hdr=disable_hdr, **kwargs)
    audio = build_audio(audio_tracks)
    subtitles = build_subtitle(subtitle_tracks)
    ending = generate_ending(audio=audio, subtitles=subtitles, cover=attachments, output_video=output_video, **kwargs)

    if not side_data:
        side_data = Box(default_box=True)

    beginning = generate_ffmpeg_start(
        source=source,
        ffmpeg=ffmpeg,
        encoder="libx265",
        video_track=video_track,
        filters=filters,
        pix_fmt=pix_fmt,
        **kwargs,
    )

    beginning += f'{f"-tune {tune}" if tune else ""} '

    if profile and profile != "default":
        beginning += f"-profile {profile} "

    if not x265_params:
        x265_params = []

    if not disable_hdr:
        if side_data and side_data.get("color_primaries") == "bt2020":
            x265_params.extend(
                ["hdr-opt=1", "repeat-headers=1", "colorprim=bt2020", "transfer=smpte2084", "colormatrix=bt2020nc"]
            )

        if side_data.master_display:
            x265_params.append(
                "master-display="
                f"G{side_data.master_display.green}"
                f"B{side_data.master_display.blue}"
                f"R{side_data.master_display.red}"
                f"WP{side_data.master_display.white}"
                f"L{side_data.master_display.luminance}"
            )

        if side_data.cll:
            x265_params.append(f"max-cll={side_data.cll}")

    if intra_encoding:
        x265_params.append("keyint=1")

    if side_data.cll:
        pass

    pass_log_file = Path(temp_dir) / f"pass_log_file_{secrets.token_hex(10)}.log"

    def get_x265_params(params=()):
        if not isinstance(params, (list, tuple)):
            params = [params]
        all_params = x265_params + list(params)
        return '-x265-params "{}" '.format(":".join(all_params)) if all_params else ""

    if bitrate:
        command_1 = (
            f'{beginning} {get_x265_params(["pass=1"])} '
            f'-passlogfile "{pass_log_file}" -b:v {bitrate} -preset {preset} -an -sn -dn -f mp4 {null}'
        )
        command_2 = (
            f'{beginning} {get_x265_params(["pass=2"])} -passlogfile "{pass_log_file}" '
            f"-b:v {bitrate} -preset {preset} "
        ) + ending
        return [
            Command(
                re.sub("[ ]+", " ", command_1), ["ffmpeg", "output"], False, name="First pass bitrate", exe="ffmpeg"
            ),
            Command(
                re.sub("[ ]+", " ", command_2), ["ffmpeg", "output"], False, name="Second pass bitrate", exe="ffmpeg"
            ),
        ]

    elif crf:
        command = (f"{beginning} {get_x265_params()}  -crf {crf} " f"-preset {preset} ") + ending
        return [
            Command(re.sub("[ ]+", " ", command), ["ffmpeg", "output"], False, name="Single pass CRF", exe="ffmpeg")
        ]

    else:
        return []
