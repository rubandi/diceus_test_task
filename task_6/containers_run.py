import sys
import docker
import requests
import json
import time
import os

client = docker.from_env()

GRID_NET = "grid"
if GRID_NET not in [net.name for net in client.networks.list()]:
    client.networks.create(GRID_NET).name
    print("net created")

def run_tests():
    client.images.build(path = "./", tag = "tests")
    host_report_path = os.getcwd() = '/report'
    container_logs = client.containers.run("tests", volumes={host_report_path: {'bind': '/app/report', 'mode': 'rw'}},network=GRID_NET)
    print(str(container_logs, "utf-8"))

def run_se_grid(nodes_number=1):
    client.containers.run("selenium/hub:4", detach=True, name="selenium-hub", ports={'4442/tcp':4442, '4443/tcp':4443, '4444/tcp':4444}, network=GRID_NET)
    for i in range(1, nodes_number + 1):
        container_name = "selenium-node-chrome-" + str(i)
        client.containers.run("selenium/node-chrome:89.0", detach=True, name=container_name, environment=["SE_EVENT_BUS_HOST=selenium-hub", "SE_EVENT_BUS_PUBLISH_PORT=4442", "SE_EVENT_BUS_SUBSCRIBE_PORT=4443"], volumes={'/dev/shm': {'bind': '/dev/shm', 'mode': 'rw'}}, network=GRID_NET)
    time.sleep(10)

def remove_se_grid():
    for container in client.containers.list(filters={'name': "selenium"}):
        container.stop()
        container.remove()

def grid_status():
    response = requests.get("http://localhost:4444/wd/hub/status")
    if response.status_code != 200:
        return False

    response_json = json.loads(response.text)
    nodes_status = [node['availability'] if node['availability'] == 'UP' else 'DOWN' for node in response_json['value']['nodes']]

    if response_json['value']['ready'] != True or 'DOWN' in nodes_status:
        return False
    else:
        return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        nodes_number = int(sys.argv[1])
    else:
        nodes_number = 1

    if len(client.containers.list(filters={'name': "selenium"})) == 0:
        run_se_grid(nodes_number)
    elif len(client.containers.list(filters={'name': "selenium"})) != nodes_number + 1:
        remove_se_grid()
        run_se_grid(nodes_number)

    if grid_status():
        run_tests()
    else:
        remove_se_grid()
        run_se_grid(nodes_number)
        run_tests()