FROM centos:latest

MAINTAINER mazhen "578233897@qq.com"

WORKDIR /

# 安装golang1.11
#RUN yum update -y \
RUN yum install wget -y
RUN yum -y install git
RUN wget https://studygolang.com/dl/golang/go1.11.1.linux-amd64.tar.gz
RUN tar -xvf go1.11.1.linux-amd64.tar.gz
RUN rm -rf go1.11.1.linux-amd64.tar.gz
# 配置golang环境
ENV GOROOT /go
ENV GOPATH /gopath
ENV PATH $PATH:$GOROOT/bin:$GOPATH/bin
# 启动tty服务
RUN go get github.com/yudai/gotty
ENTRYPOINT gotty -w -p "9000" bash

EXPOSE 9000

#### 构建镜像
#   docker build -t centos7:ark .
#### 创建测试容器
#   docker run -p 9001:9000 --name test  -d centos7:ark

