# install SDK
## unzip the fusionTrack_SDK-v4.7.4-linux64.zip
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
```
