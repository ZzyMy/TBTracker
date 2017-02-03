# TBTracker

A tracker for commodities in TaoBao.

## Pre-insatll

```shell
$ sudo apt-get install phantomjs
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
