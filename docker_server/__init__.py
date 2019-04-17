import docker

client = docker.from_env()
# print(client.containers.run("centos:latest", detach=True))
# print(client.containers.kill())
client.containers.run("centos:latest", tty=True, detach=True)
# 创建一个新的容器
print(client.containers.list(all=True))
# client.containers 对客户端容器进行操作 client.containers.list(all=True) 返回 Container objects，然后我们再对 Container object 进行操作
for container in client.containers.list(all=True):
    print(container.id)
    print(client.containers.get(container.id))
    #container.exec_run("/bin/bash",tty=True) 执行命令
    container.stop()
    container.remove()