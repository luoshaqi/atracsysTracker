# install SDK
## SDK Linux download and unzip
1. download fusionTrack_v4.7.4_gcc-5.4.tar.xz
2. unzip it
```
cd ~
mkdir Atracsys
cd Atracsys
tar -xJvf fusionTrack_v4.7.4_gcc-5.4.tar.xz
cd fusionTrack_SDK-v4.7.4-linux64
```
## SDK Linux version installation
```
cd ~/Atracsys/fusionTrack_SDK-v4.7.4-linux64
mkdir build
cd build

cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release ~/Atracsys/fusionTrack_SDK-v4.7.4-linux64/samples

echo -e 'export ATRACSYS_SDK_HOME=~/Atracsys/fusionTrack_SDK-v4.7.4-linux64
export ATRACSYS_FTK_HOME=~/Atracsys/fusionTrack_SDK-v4.7.4-linux64
export ATRACSYS_STK_HOME=~/Atracsys/fusionTrack_SDK-v4.7.4-linux64' >>~/.bashrc

source ~/.bashrc
```
# Python wrapper
```
cd ~/Atracsys/fusionTrack_SDK-v4.7.4-linux64/python
pip install atracsys-4.7.1.1.tar.gz
```
