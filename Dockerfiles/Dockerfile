FROM golang:1.11

MAINTAINER mazhen "578233897@qq.com"
RUN go get github.com/yudai/gotty

ENTRYPOINT gotty -w -p "9000" bash
EXPOSE 9000

# gotty -p 9000 bash

#### 构建镜像
#   docker build -t ark .
#### 构建容器
#   docker run -p 9001:9000 --name ark1  -d ark
# 将容器的9000端口映射到9001端口
# name 容器名 -d 镜像名
# 删除docker
# docker stop ark
# docker rm ark
# docker image rm ark

# docker stop $(docker ps -a -q)
# docker  rm $(docker ps -a -q)