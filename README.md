Welcome to StarQuant
==================

<p align="left">
   <img src ="https://img.shields.io/badge/language-c%2B%2B%7Cpython-orange.svg"/>
   <img src ="https://img.shields.io/badge/c%2B%2B-%3E11-blue.svg"/>
    <img src ="https://img.shields.io/badge/python-3.7-blue.svg" />
    <img src ="https://img.shields.io/badge/platform-linux%7Cwindows-brightgreen.svg"/>
    <img src ="https://img.shields.io/badge/build-passing-green.svg" />
    <img src ="https://img.shields.io/badge/license-MIT-blue.svg"/>
</p>

**StarQuant** is light-weighted, integrated algo-backtest/trade system/platform for individual trader, it is mainly used for future trading at present, stock and other commodity will be included in future.

## Features
* decoupled module design, namely strategy, marketdatafeed, trade run by different processes, communicate by message queue(nanomsg), low-latency(30 -100 microsenconds);
* event-driven based backtest system(same as vnpy), strategy bactested in python, run directly in live；support multiple data source, i.e. data can be loaded from MongoDB, CSV file; support multiple  timescale data such as tick ,1min bar, 1h bar; 
* support strategy parameter optimization through multi-process or  genetic algorithm;
* marketdata record;
* simulated trading(paper brokerage);
* support multiple API and accounts, autoconnect/logout/reset, working in 7*24h；support self-defined instructions, such as cancel all; support local stop orders;
* strategy can be dynamically managed, i.e. init/start/stop/edit/remove at will;
* pyQt5 based GUI interface for monitoring and manual control；
* risk manage, flow control;
* realtime message notify through wechat(itchat) ...

## Architecture

C++ 11 based, client-server, event-driven, decoupled module design.




## Development Environment

Manjaro（arch，Linux 4.14)，python 3.7.2，gcc 8.2, anaconda 5.2

**third party softwares:**

* boost 1.69
* nanomsg
* log4cplus
* yamlcpp
* libmongoc-1.0
* ...

**python modules:**

* pandas-datareader
* psutil
* pyyaml
* pyqt
* qdarkstyle
* tushare
* pyfolio
* itchat
* ...


## How to Run


compile files in cppsrc:

```
$ cd cppsrc
$ mkdir build
$ cd build
$ cmake ..
$ make
$ cp StarQuant/apiserver.exe ../../
```
start apiserver and gui, strategy, recorder:
```
$ ./apiserver
```
```
$ python gui.py
$ python strategy.py
$ python recorder.py
```


## User Guide

To be continued


## Demo

![ ](demos/livepro.png  "trade mode")

![](demos/bt3.png  "backtest mode")

![ ](demos/btpro2.png  "backtest results ")


## Current State

Currently StarQuant is under test, v1.0-alpha version has been released.




