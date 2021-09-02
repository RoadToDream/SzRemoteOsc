# SzRemoteOsc
SzRemoteOsc assists you use your GW Instek Oscilloscope more confident.

![SzRemoteOsc Screenshot](./images/screenshot-1.png)

**Please note this project is still at an early stage, please use with care. Hope it will be helpful**

## Usage

Download from [latest release](https://github.com/RoadToDream/SzRemoteOsc/releases/latest) and run, app is packaged with PyInstaller, macOS and Windows version provided. 

## Deploy
Require Anaconda installed, run following to setup environment

```
conda create -y --name gwinstek python=3.7
conda activate gwinstek
conda install -y -c conda-forge pyqtads
pip install opencv-python pyvisa pyvisa-py 
```

After setting the environment, you may run program by 
```
python SzRemoteOsc.py
```

Enjoy

## Contribute
Only necessary components are implemented, feel free to contribute
