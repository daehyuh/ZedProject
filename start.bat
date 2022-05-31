set root=C:\Users\vitasoft\anaconda3
call %root%\Scripts\activate.bat %root%

call conda env list
call conda activate Zed
call cd C:\Users\vitasoft\Desktop\ZedProject
call python main.py

pause