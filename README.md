# ASPECTA-Server
The ASPECTA server side program for running on the projector-connected Ubuntu PC.

###Dependencies
Install in the order listed so as to avoid problems.
* python-dev (```sudo apt-get install python-dev```)
* pip (```sudo apt-get install python-pip```)
* python-opengl (```sudo apt-get install python-opengl```)
* python-pygame (```sudo apt-get install python-pygame```)
* ujson (```sudo pip install ujson```)
* FTGL (```sudo apt-get install ftgl-dev``` If there are libcheese dependency issues see below)
* FreeType (http://www.freetype.org See instructions for installing the contents of the tar.gz package below)
* boost::python (```sudo apt-get install libboost-python-dev```)
* PYFTGL (https://bitbucket.org/jp438/pyftglforaspecta/ See installation instructions below)

###Recommended

These have been used for development and testing, so are recommended but not required.
* Eclipse (https://www.eclipse.org/downloads/ See eclipse notes below if eclipse won't run due to Java Runtime Environment issues)
* PyDev for Eclipse (see instructions below on how to download and install)

###FTGL LibCheese Depencency Issues
There has been one report of failure when trying to install ftgl-dev due to issues fulfilling the depencency for libcheese. In this case the following commands resolved the issue:
```
sudo apt-get install xserver-xorg-dev-lts-utopic mesa-common-dev-lts-utopic
sudo apt-get install ftgl-dev
```

###FreeType Installation

After downloading extract the ```freetype-X.X.X``` folder and inside it run the following commands:
```
./configure
make
sudo make install
```

###PYFTGL Modifications

Once you have downloaded and extracted the version of pyFTGL linked to above you can install it using the following commands:
```
sudo python setup.py build
sudo python setup.py install
```

###Eclipse Notes

If elipse won't run after extraction you may need to run the following in a terminal:
```
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java7-installer
sudo apt-get install oracle-java7-set-default
```
If eclipse still doesn't start execute the following:
#####32-Bit Systems
```ln -s /usr/lib/jni/libswt-* ~/.swt/lib/linux/x86/```
#####64-Bit Systems
```ln -s /usr/lib/jni/libswt-* ~/.swt/lib/linux/x86_64/```

###Installing PyDev
#####Easy installation (For newer versions of Eclipse, attempt this first):

In the Eclipse menu go to "Help" -> "Install New Software" and use the source:

http://pydev.org/updates

To download PyDev 3.3.3. This will fail if the version of Eclipse is too old.

#####Manual Installation (For all versions of Eclipse):

Go to the PyDev website (http://pydev.org/manual_101_install.html) and download the zip file for Pydev 3.3.3

Navigate to ~/.eclipse/org.eclipse.platform_3.7.0_155965261/ (Eclipse version may be different) and create a folder called "dropins". Copy the contents of the downloaded zip file to this new folder.
