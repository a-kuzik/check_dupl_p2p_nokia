from scrapli.driver import GenericDriver
import yaml
import datetime
import getpass
import logging
import os
import time

port = 22
user = input("Username: ")
password = getpass.getpass(prompt="Password: ", stream=None)
res_directory = "results"
log_directory = "debug"

if not os.path.exists(res_directory):
    os.makedirs(res_directory)
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
log_file = f"{log_directory}/file.log"


cmd = "show router route-table protocol local"

with open("hosts_lab.yml", "r") as f:
    data = yaml.safe_load(f)

hosts = []
for d1 in data:
    for k1, v1 in d1.items():
        ip = v1["IP_address"]
        hosts.append(ip)

logger = logging.getLogger("Debug")
logger.setLevel(logging.DEBUG)
logfile = logging.FileHandler(log_file)
logfile.setLevel(logging.WARNING)
formatter = logging.Formatter(
    "{asctime} - {name} - {levelname} - {message}", datefmt="%H:%M:%S", style="{"
)
logfile.setFormatter(formatter)
logger.addHandler(logfile)


def send_cmd(hosts, port, user, password, command):
    for host in hosts:
        date_time = datetime.datetime.now()
        time_now = date_time.strftime("%d_%m_%y_%H_%M_%S")
        try:
            conn = GenericDriver(host, port, user, password, auth_strict_key=False)
            conn.open()
            print(f"Open connection to host {host}")
            file = open(f"{res_directory}/{host}_{command}_{time_now}", "w")
            file.write(conn.get_prompt())
            conn.send_command("environment no more")
            reply = conn.send_command(command)
            file.write("\n" + reply.result)
            file.close()
            conn.close()
            print(f"Close connection to host {host}")
        except Exception as err:
            print(err)
            logger.error(f"{host} - {err}")


send_cmd(hosts, port, user, password, cmd)
