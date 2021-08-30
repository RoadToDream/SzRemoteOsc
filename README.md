# SzRemoteOsc
SzRemoteOsc assists you use your GW Instek Oscilloscope more confident.

## Deploy
Require Anaconda installed, run 

```
conda create -y --name gwinstek python=3.7
eval "$(conda shell.zsh hook)"
conda activate gwinstek
conda install -y -c conda-forge pyqtads
pip install opencv-python pyvisa pyvisa-py 
```

## Contribute
Only necessary components are implemented, feel free to contribute
