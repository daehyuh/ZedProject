# ZedProject
### Zed 프로젝트 (주)비타소프트

> # 파트라슈 프로젝트 Zed2 카메라 데이터수집 센서 개발
> > ### 담당자 강대현, 황가온

# main.py   
## Zed2 카메라 센서로 Left, Right, Depth, 거리배열를 저장하는 코드입니다   
### 저장 / 저장종료 : SpaceBar
### 프로그램 종료 : ESC   

> ## 저장경로   
>> Left : saved_imgs/저장시작시간/left_{str(count).zfill(4)}.jpg   
>> Right : saved_imgs/저장시작시간/right_{str(count).zfill(4)}.jpg   
>> Depth : saved_imgs/저장시작시간/depth_{str(count).zfill(4)}.jpg   
>> 거리 : saved_imgs/저장시작시간/dis_{str(count).zfill(4)}.npz   

# ver 1.0
초기 개발 완료

# Windows 환경설정

GTX1650 그래픽 호환 버전

# Cuda 11.5

CUDA 버전 확인 
> nvcc --version

기존 CUDA 삭제
> 프로그램 추가/제거 들어가서 NVIDIA에 관련된 프로그램을 모두 지운다.

cuda 11.5
> https://developer.nvidia.com/cuda-11-5-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local

# ZED SDK 11.5
ZED_SDK (CUDA 11.X)
> https://www.stereolabs.com/developers/release/
> Program Files 폴더에서 ZED를 실행하려면 관리자 액세스 권한을 줘야한다

# PYTHON
PYTHON
> https://www.python.org/downloads/

# Anaconda
Anaconda3
> https://www.anaconda.com/

먼저 미리 아나콘다에서 Zed를 만든후

# PIP 라이브러리 설치
> conda activate Zed   
> pip install cython numpy opencv-python pyopengl   
> cd C:\Program Files (x86)\ZED SDK   
> python get_python_api.py

get_python_api.py는 ZED SDK의 의존하는 라이브러리를 설치해주는것이다 실행해주지 않으면 pyzed를 제대로 불러올수없다


Check GPU memory
> ndivia-smi

