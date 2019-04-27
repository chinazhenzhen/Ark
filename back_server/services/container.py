import docker
import random
import string


class ContainerManager(object):
    OS_LIST = None
    CONTAINER_PREFIX = "ARK_CONTAINERS_"

    def __init__(self):
        self.client = docker.from_env()

    def create_container(self, image_name):

        container_name = self.produce_container_name() # 我们需要确定这个参数
        try:
            self.client.containers.run(
                image=image_name,
                ports={'9000/tcp': None},
                name=container_name,
                detach=True,
                tty=True
            )
        except Exception:
            return None
        else:
            return container_name

    def get_container_ports(self, container_name):
        try:
            ports = self.client.containers.get(
                container_name).attrs['NetworkSettings']['Ports']
            return {
                port: mapped_ports[0]['HostPort']
                for port, mapped_ports in ports.items()
            }
        except Exception:
            return None

    def is_rm_container(self, container_id) -> bool:
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            container.remove()
            return True
        except Exception:
            return False

    def produce_container_name(self) -> str:
        return self.CONTAINER_PREFIX + ''.join(
            random.sample(string.ascii_letters + string.digits, 16))


def create_container(u_port):
    print(u_port)
    client = docker.from_env()
    client.containers.run(
        image="ark:latest",
        name="ark"+str(u_port),
        ports={'9000/tcp': u_port},
        detach=True,
        tty=True
    )

if __name__ == "__main__":
    test = ContainerManager()
    c_name = test.create_container("ark:latest")
    print(c_name)
    print(test.get_container_ports(c_name))
    print(test.is_rm_container(c_name))
