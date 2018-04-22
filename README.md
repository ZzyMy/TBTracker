## 淘宝商品数据追踪系统.
### 安装开发库和依赖库
1. 安装轻量级浏览器--PhantomJS
```shell
$ wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
$ tar -zxvf phantomjs-2.1.1-linux-x86_64.tar.bz2 && sudo rm phantomjs-2.1.1-linux-x86_64.tar.bz2
$ cd phantomjs-2.1.1-linux-x86_64/bin
$ sudo mv phantomjs /usr/local/bin
$ sudo chown root:root /usr/local/bin/phantomjs
```

2. 升级Ubuntu14.04自带的Python3.4至3.5版本
```shell
$ sudo add-apt-repository ppa:fkrull/deadsnakes
$ sudo apt-get update
$ sudo apt-get install python3.5
$ sudo rm /usr/bin/python3
$ sudo ln -s /usr/bin/python3.5m /usr/bin/python
```

3. 安装python开发工具
```shell
$ sudo apt-get install build-essential
$ sudo apt-get install python3.5-dev
$ sudo apt-get install python3-pip
$ sudo pip3 install --upgrade pip
```

4. 安装相关开发库和依赖库
```shell
$ sudo apt-get install sqlite3 
$ sudo apt-get install libpng-dev
$ sudo pip3 install bs4
$ sudo pip3 install selenium 
$ sudo pip3 install xlwt 
$ sudo pip3 install pyyaml 
$ sudo pip3 install PyQt5 
$ sudo pip3 install numpy
$ sudo pip3 install matplotlib
```

5. 可选安装
```shell
$ wget http://download.savannah.gnu.org/releases/freetype/freetype-2.7.1.tar.gz
$ tar -zxvf freetype-2.7.1.tar.gz && sudo rm freetype-2.7.1.tar.gz
$ cd freetype-2.7.1
$ ./configure
$ make
$ sudo make install
```
### 克隆源码
```shell
$ sudo apt-get install git
$ git clone https://github.com/summychou/TBTracker.git
$ cd TBTracker/TBTracker
````
### 初始化系统数据库
```shell
$ sudo python3 TBTracker_InitDataBase.py
```
### 运行系统
```shell
$ sudo python3 TBTracker_Main.py
```

## JUST ENJOY IT!!!
