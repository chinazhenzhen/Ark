import docker

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