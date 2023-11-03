
## Requirements
Python3

## Statup
Install libs
```bash
pip3 install -r requirements.txt
```

launch voicevox docker  
```bash
docker pull voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
docker run --rm --gpus all -p '50021:50021' voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
```