# ASPECTA-Server
The ASPECTA server side program for running on the projector-connected Ubuntu PC.

### Dependencies
Install in the order listed so as to avoid problems.
* python-dev (```sudo apt-get install python-dev```)
* pip (```sudo apt-get install python-pip```)
* python-opengl (```sudo apt-get install python-opengl```)
* python-pygame (```sudo apt-get install python-pygame```)
* ujson (```sudo pip install ujson```)
* FTGL (```sudo apt-get install ftgl-dev``` If there are libcheese dependency issues see below)
* scipy (```sudo apt-get install python-scipy```)
* FreeType (http://www.freetype.org See instructions for installing the contents of the tar.gz package below)
* boost::python (```sudo apt-get install libboost-python-dev```)
* PyFTGL (https://bitbucket.org/jp438/pyftglforaspecta/ See installation instructions below)

### Recommended

* Ubuntu or Ubuntu-based Linux distribution (Tested with regular Ubuntu and Ubuntu Mate)
* Jetbrains PyCharm Community (https://www.jetbrains.com/pycharm/download/#section=linux)

### FreeType Installation

After downloading extract the ```freetype-X.X.X``` folder and inside it run the following commands:
```
./configure
make
sudo make install
```

### PyFTGL Installation

Once you have downloaded and extracted the modified version of pyFTGL linked to above you can install it using the following commands:
```
sudo python setup.py build
sudo python setup.py install
```
