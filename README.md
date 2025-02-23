# 1. 内容分析

TCP 提供了一种面向连接的、可靠的字节流服务，本次实验使用Socket TCP 通信，构建能够实现文件传输的服务器和客户端。

客户端需要建立与TCP服务器的连接，上传或者下载指定文件，同时实现一个简单的shell获取指令。

在服务器端需要能够建立一个主动的套接口，监听端口，对请求的客户端建立连接，可以接收客户端上传的文件，也可以传输客户端要求下载的文件；同时，采用多线程，可以与多个客户端建立连接。



# 2. 设计方法

使用`Python`、`socket`库及`threading`库完成该实验。设计三个文件，分别是客户端`client.py`、服务器端`server.py`和封装工具函数的文件`utils.py`。

## 2.1 TCP套接口流程

首先需要启动服务器，等待客户端的连接。客户端启动之后向服务器发送请求，等待服务器处理、建立连接之后返回响应。之后可以进行文件传输，直到客户端关闭连接。

![image-20201230011335903](https://github.com/Thooooor/SocketTcpTransfer/blob/main/README.assets/image-20201230011335903.png?raw=true)

## 2.2 客户端

首先运行一个shell，根据用户的输入建立连接，对应进行文件的上传或下载。上传和接收的文件存放在文件夹`upload_dir`中。

使用一个类实现客户端`Client`，初始化时建立socket，确定用户需要建立连接之后进行连接，之后根据具体指令调用对应的上传和下载的方法。上传或者下载时，会首先发送对应的指令和文件名称，发送之后使用`sleep`等待1秒，之后再上传或者接收数据。设置一个缓存大小，每次接收1024字节的数据，根据数据长度是否为零可以判断数据传输是否结束。



## 2.3  服务器端

构建一个服务器类`Server`，循环等待建立连接，每次连接时创建一个线程，构建一个继承`Thread`的客户端处理类`ClientThread`对连接进行处理，首先需要根据客户端第一次传输的指令检查文件夹，判断此次传输是否能进行，之后对应进行文件的接收或者传输。接收的文件存放在`files`文件夹中。



# 3. 结果分析

分别在本地一台windows系统的物理机和一台ubuntu系统的虚拟机上运行客户端，需要注意修改路径格式。在远程Linux环境服务器（`39.107.251.174:8000`）上运行服务器端。

两台客户端同时建立连接，在Ubuntu客户端上传`test.md`文件，在windows客户端上传`img.jpg`图片。之后在Ubuntu端下载`img.jpg`文件，在windows段下载`test.md`文件。

Ubuntu客户端运行情况如下，两次连接都建立成功，上传和下载命令都成功执行。

![ubuntu客户端](https://github.com/Thooooor/SocketTcpTransfer/blob/main/README.assets/image-20201230013232435.png?raw=true)

windows客户端运行情况如下，两次连接都建立成功，上传和下载命令都成功执行。

![windows客户端](https://github.com/Thooooor/SocketTcpTransfer/blob/main/README.assets/image-20201230013259872.png?raw=true)

Linux服务器端运行情况如下，根据打印的进程id能够判断多线程运行成功，同时，根据执行指令时的打印信息，能够判断两条指令交叉执行。

![image-20201230013502483](https://github.com/Thooooor/SocketTcpTransfer/blob/main/README.assets/image-20201230013502483.png?raw=true)

最终在服务器端能够得到接收的两个新文件：

![image-20201230013748587](https://github.com/Thooooor/SocketTcpTransfer/blob/main/README.assets/image-20201230013748587.png?raw=true)

两个本地的客户端也都有两个文件。