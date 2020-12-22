wget https://github.com/FFmpeg/FFmpeg/releases/download/n3.0/ffmpeg-3.0.tar.gz -O ffmpeg
tar -xzf ffmpeg

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

# apt install pd-flite -y 语音合成库

apt install timidity -y
timidity tmp43ZC.mid -Ow -o - | ffmpeg -i - -ac 1 -ar 8000 aaa.amr

wget https://versaweb.dl.sourceforge.net/project/timidity/TiMidity%2B%2B/TiMidity%2B%2B-2.15.0/TiMidity%2B%2B-2.15.0.tar.gz -O timidi.tar.gz
tar -xzf timidi.tar.xz
cd TiMidity++-2.15.0

cd ffmpeg-3.0