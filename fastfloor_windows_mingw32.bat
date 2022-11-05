cd raycaster
%UserProfile%\AppData\Roaming\Python\Python38\Scripts\cython.exe -o fastfloor.c fastfloor.pyx
cd C:\MinGW\bin\
mingw32-gcc.exe -c -m32 -DMS_WIN32 -Ofast -I"C:\Program Files (x86)\Python38-32\include" -I"%UserProfile%\AppData\Roaming\Python\Python38\site-packages\numpy\core\include" -o %UserProfile%\GitHub\raycaster\raycaster\fastfloor.o %UserProfile%\GitHub\raycaster\raycaster\fastfloor.c
mingw32-gcc.exe -m32 -shared -L"C:\Program Files (x86)\Python38-32\libs" -o %UserProfile%\GitHub\raycaster\raycaster\fastfloor.pyd %UserProfile%\GitHub\raycaster\raycaster\fastfloor.o -lpython38
cd %UserProfile%\GitHub\raycaster
python raycaster
pause
