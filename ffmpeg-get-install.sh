#!/bin/sh
apt install -y cmake git g++ timidity flite1-dev libgsm* libsdl2-dev libcdio-paranoia-dev libcdio-dev libcdio-dev libjack-dev libpocketsphinx-dev libomxil-bellagio-dev libopenal-dev libzvbi-dev libzmq3-dev libxvidcore-dev libx265-dev libx264-dev libwebp-dev libvpx-dev libvidstab-dev libtwolame-dev libtheora-dev libspeex-dev libssh-dev libsoxr-dev libsnappy-dev libshine-dev librubberband-dev librsvg2-dev librabbitmq-dev libpulse-dev libopus-dev libopenmpt-dev libopenjp2-7-dev libopencore-amrnb-dev libopencore-amrwb-dev libmysofa-dev libmp3lame-dev libchromaprint-dev libmfx-dev libgme* yasm frei0r-plugins-dev libunistring-dev gnutls-dev ladspa-sdk-dev libaom-dev liblilv-dev libiec61883-dev libavc1394-dev libass-dev libbluray-dev libbs2b-dev libcaca-dev libcodec2-dev libdav1d-dev libdc1394-dev libdrm-dev pkg-config
git clone https://github.com/FFmpeg/FFmpeg.git

cd FFmpeg
./configure --prefix=/usr --enable-static --extra-version=5 --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --arch=amd64 --enable-gpl --disable-stripping --enable-avresample --disable-filter=resample --enable-gnutls --enable-ladspa --enable-libaom --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libcodec2 --enable-libdav1d --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libjack --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librabbitmq --enable-librsvg --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --disable-libsrt --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzmq --enable-libzvbi --enable-lv2 --enable-omx --enable-openal --enable-sdl2 --enable-pocketsphinx --enable-libmfx --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libx264 --enable-shared --enable-libopencore-amrnb --enable-version3

# timidity tmp43ZC.mid -Ow -o - | ffmpeg -i - -ac 1 -ar 8000 aaa.amr