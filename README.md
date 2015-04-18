sImulAcre
=========

[![logo](https://raw.github.com/bizalu/sImulAcre/master/core/client/images/logo.png)](https://github.com/bizalu/sImulAcre/)


sImulAcre is a try to make an Intelligence Artificial.  
This goal is not realistic for the moment, but we can try to develop a fake IA who make we think computer can be "intelligent"


Introduction
------------
sImulAcre is a client-server application develop with python 3 and pyQT 5.  
I test it on Ubuntu 14.10, but can run on every linux OS with python.

For the moment, this application can just communicate with existing API or package to run :
* Text to speech (voices) : Google trad API , espeak & mbrola
* Speech to text (ears) : Google chrome API
* bot (brain) : cleverbot, jabberwacky and pandora


Installation
------------

sImulAcre need dependency to work : 
```bash
sudo apt-get install python3 python3-pyqt5 python3-sip python3-pip python3-setuptools mbrola mbrola-fr1 espeak  
sudo pip3 install pydub
```


How to run
----------
You have to run the server before the client. You can do it with this set of command :  
```bash
./core/server/main.py  
./core/client/main.py
```

License
--------
See [LICENSE](LICENSE) file.
