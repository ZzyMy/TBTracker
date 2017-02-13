# TBTracker

A tracker for commodities in TaoBao.

## Pre-insatll

```shell
$ wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
$ tar -zxvf phantomjs-2.1.1-linux-x86_64.tar.bz2 && sudo rm phantomjs-2.1.1-linux-x86_64.tar.bz2
$ cd phantomjs-2.1.1-linux-x86_64/bin
$ sudo mv phantomjs /usr/local/bin
$ sudo chown root:root /usr/local/bin/phantomjs
```

```shell
$ sudo apt-get install sqlite3
$ sudo apt-get install libpng-dev
$ sudo apt-get install git
$ sudo apt-get install python3-dev python3-pip python3-pyqt5
$ sudo pip3 install bs4 pillow requests selenium wordcloud xlwt pyyaml
```

```shell
$ wget http://download.savannah.gnu.org/releases/freetype/freetype-2.7.1.tar.gz
$ tar -zxvf freetype-2.7.1.tar.gz && sudo rm freetype-2.7.1.tar.gz
$ cd freetype-2.7.1
$ ./configure
$ make
$ sudo make install
```

```shell
$ git clone https://github.com/matplotlib/matplotlib.git
$ cd matplotlib
$ sudo python3 setup.py build
$ sudo python3 setup.py install
```

## First Step

```shell
$ sudo python3 TBTracker_InitDataBase.py
```

## Second Step

```shell
$ sudo python3 TBTracker_Main.py
```

just enjoy it!!!
