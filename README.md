# ZedProject
### Zed 프로젝트 (주)비타소프트

> # 파트라슈 프로젝트 Zed2 카메라 데이터수집 센서 개발
> > ### 담당자 강대현

# main.py   
## Zed2 카메라 센서로 Left, Right, Depth, 거리배열를 저장하는 코드입니다   
### 저장 / 저장종료 : SpaceBar
### 프로그램 종료 : ESC   
```python
> # 저장경로
>> Left : saved_imgs/시간/left_{str(count).zfill(4)}.jpg   
>> Right : saved_imgs/시간/right_{str(count).zfill(4)}.jpg   
>> Depth : saved_imgs/시간/depth_{str(count).zfill(4)}.jpg   
>> distance : saved_imgs/시간/dis_{str(count).zfill(4)}.npz   
```


# Ubuntu 18.04 환경설정   

# Cuda 11.5

CUDA 버전 확인 
> nvcc --version
```bash 
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pinsudo 
mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.5.0/local_installers/cuda-repo-ubuntu1804-11-5-local_11.5.0-495.29.05-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1804-11-5-local_11.5.0-495.29.05-1_amd64.debsudo apt-key add /var/cuda-repo-ubuntu1804-11-5-local/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda
```

# ZED SDK 11.5
https://www.stereolabs.com/docs/installation/linux/









# Windows 환경설정   
#### GTX1650 GPU 호환 버전 환경설정 (아주 낮은 GPU가 아니라면 대부분 문제없음)

# Cuda 11.5

CUDA 버전 확인 
> nvcc --version

기존 CUDA 삭제
> 만약 기존에 쿠다가 설치되어 있다면 프로그램 추가/제거 들어가서 NVIDIA에 관련된 프로그램을 모두 지웁니다.

# cuda 11.5
[cuda 11.5]   
https://developer.nvidia.com/cuda-11-5-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local

# ZED SDK 11.5
[ZED_SDK (CUDA 11.X)]   
https://www.stereolabs.com/developers/release/


# PYTHON
[PYTHON]    
https://www.python.org/downloads/

# Anaconda3
[Anaconda3]   
https://www.anaconda.com/

먼저 미리 아나콘다에서 Zed를 만든후

# PIP 라이브러리 설치
```Bash
conda activate Zed
pip install cython numpy opencv-python pyopengl
cd C:\Program Files (x86)\ZED SDK
python get_python_api.py
```
get_python_api.py는 ZED SDK이 의존하는 라이브러리를 설치해주는것입니다.   
의존 라이브러리를 설치하지 않으면 pyzed를 제대로 불러올수없습니다.   
get_python_api.py실행시 관리자권한으로 실행합니다.
관리자권한을 하지않으면 권한오류가 발생됩니다.

# FFMPEG 라이브러리 설치
https://ffmpeg.org/download.html
설치후 bin 폴더 환경변수 설정

ZED가 메모리를 먹고있는지 확인
> ndivia-smi


5/23
이미지 > 영상변환 추가
파일저장 큐 자료구조 방식 변경

