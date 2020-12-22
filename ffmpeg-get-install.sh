# wget https://github.com/FFmpeg/FFmpeg/releases/download/n3.0/ffmpeg-3.0.tar.gz -O ffmpeg
# tar -xzf ffmpeg

git clone https://github.com/FFmpeg/FFmpeg.git

apt install libchromaprint-dev -y
apt install yasm -y
apt install frei0r-plugins-dev -y
apt install libunistring-dev -y
apt install gnutls-dev -y
apt install ladspa-sdk-dev -y
apt install libaom-dev -y
apt install liblilv-dev -y
apt install libiec61883-dev -y
apt install libavc1394-dev -y
apt install libass-dev -y
apt install libbluray-dev -y
apt install libbs2b-dev -y
apt install libcaca-dev -y
apt install libcodec2-dev -y
apt install libdav1d-dev -y
apt install libdc1394-dev -y
apt install libdrm-dev -y

git clone https://github.com/festvox/flite.git
cd flite/
./configure
make
make install


cd ..
# apt install pd-flite -y 语音合成库

apt install timidity -y
timidity tmp43ZC.mid -Ow -o - | ffmpeg -i - -ac 1 -ar 8000 aaa.amr

wget https://versaweb.dl.sourceforge.net/project/timidity/TiMidity%2B%2B/TiMidity%2B%2B-2.15.0/TiMidity%2B%2B-2.15.0.tar.gz -O timidi.tar.gz
tar -xzf timidi.tar.xz
cd TiMidity++-2.15.0

./configure --prefix=/usr --extra-version=5 --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu;/usr/local/include --arch=amd64 --enable-gpl --disable-stripping --enable-avresample --disable-filter=resample --enable-gnutls --enable-ladspa --enable-libaom --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libcodec2 --enable-libdav1d --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libjack --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librabbitmq --enable-librsvg --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --disable-libsrt --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzmq --enable-libzvbi --enable-lv2 --enable-omx --enable-openal --enable-opencl --enable-opengl --enable-sdl2 --enable-pocketsphinx --enable-libmfx --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libx264 --enable-shared --enable-libopencore-amrnb --enable-version3
# cd ffmpeg-3.0