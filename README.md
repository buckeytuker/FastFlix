# FastFlix

![preview](./docs/gui_preview.png)

FastFlix is a simple and friendly GUI for encoding videos.

It needs `FFmpeg` (version 4.3 or greater) under the hood for the heavy lifting, and can work with a variety of encoders.

#  Encoders

 FastFlix supports the following encoders when their required libraries are found in FFmpeg:

* HEVC (libx265) &nbsp;&nbsp;&nbsp; <img src="./fastflix/data/encoders/icon_x265.png" height="30" alt="x265" >
* AVC (libx264) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="./fastflix/data/encoders/icon_x264.png" height="30" alt="x264" >
* AV1 (librav1e) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="./fastflix/data/encoders/icon_rav1e.png" height="30" alt="rav1e" >
* AV1 (libaom-av1) &nbsp; <img src="./fastflix/data/encoders/icon_av1_aom.png" height="30" alt="av1_aom" >
* AV1 (libsvtav1) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="./fastflix/data/encoders/icon_svt_av1.png" height="30" alt="svt_av1" >
* VP9 (libvpx) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="./fastflix/data/encoders/icon_vp9.png" height="30" alt="vpg" >
* GIF (gif) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="./fastflix/data/encoders/icon_gif.png" height="30" alt="gif" >

Most builds do not have all these encoders available by default and may require custom compiling FFmpeg for a specific encoder.

* [Window FFmpeg (and more) auto builder](https://github.com/m-ab-s/media-autobuild_suite)
* [Windows cross compile FFmpeg (build on linux)](https://github.com/rdp/ffmpeg-windows-build-helpers)
* [FFmpeg compilation guide](https://trac.ffmpeg.org/wiki/CompilationGuide)

# Releases

## Windows
[![Build status](https://ci.appveyor.com/api/projects/status/208k29cvoq8xwf8j/branch/master?svg=true)](https://ci.appveyor.com/project/cdgriffith/fastflix/branch/master)

View the [releases](https://github.com/cdgriffith/FastFlix/releases) for 64 bit Windows binaries (Generated via Appveyor and also [available there](https://ci.appveyor.com/project/cdgriffith/fastflix)).

## MacOS and Linux

Please use [pipx](https://pipxproject.github.io/pipx/installation/) to install as a properly virtualized app

```
pipx install fastflix
```

You will need to have `ffmpeg` and `ffprobe` executables on your PATH and they must be executable. Version 4.3 or greater is required. The one in your in your package manager system may not support all encoders or options.
Check out the [FFmpeg download page for static builds](https://ffmpeg.org/download.html) for Linux and Mac.

## Running from source code

```
git clone https://github.com/cdgriffith/FastFlix.git
cd FastFlix
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python -m fastflix
```

# License

Copyright (C) 2019-2020 Chris Griffith

The code itself is licensed under the MIT which you can read in the `LICENSE` file. <br>
Read more about the release licensing in the [docs](docs/README.md) folder. <br>
Encoder icons for [VP9](https://commons.wikimedia.org/wiki/File:Vp9-logo-for-mediawiki.svg) and [AOM AV1](https://commons.wikimedia.org/wiki/File:AV1_logo_2018.svg) are from Wikimedia Commons all others are self created.
