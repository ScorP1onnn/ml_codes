This is the code implementing probabilistic random forest on SDSS DR18 data containing 100,000 sources. It also inlcudes creating query files that is used to get the from Sciserver. 

Note: The downloaded CSV file from kaggle is more than 25 MB (it is around 32 MB). I am storing it in google drive

To download SciServer to jupyter, just save the git clone of this website: https://github.com/sciserver/SciScript-Python in the jupyter notebook file. Then follow the steps for installation.
In /py2/SciServer/Config.py and /py3/SciServer/Config.py I only added DR18. Then I followed step 3b, which is manual installation. You don't have to do step 5 (I haven't and it still worked me).

Similarly, you clone PRF git: https://github.com/ireis/PRF.git in the jupyter file and just follow the installation.

