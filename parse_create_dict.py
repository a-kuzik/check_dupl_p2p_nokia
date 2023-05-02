import textfsm
import os
import re
from pprint import pprint

drctr = "results"
files = os.listdir(drctr)


def parse_textfsm(template, raw):
    templ = open(template)
    re_table = textfsm.TextFSM(templ)
    parse_data = re_table.ParseText(raw)
    return parse_data


dict1 = {}

for file in files:
    regexp = "(\d+\.){3}\d+"
    ip = re.search(regexp, file).group()
    #    print(ip)
    #    pprint(file)
    raw = open(f"{drctr}/{file}").read()
    parsed = parse_textfsm("sh_routes_local.template", raw)
    dict1[ip] = {}
    for l1 in parsed:
        try:
            dict1[ip].update(
                {
                    l1[1]: {
                        "type": l1[2],
                        "proto": l1[3],
                        "age": l1[4],
                        "pref": l1[5],
                        "ifname": l1[6],
                        "metric": l1[7],
                    }
                }
            )
        except Exception as err:
            pass

# pprint(dict1)

ips = []
dupl_p2p = []

for k1, v1 in dict1.items():
    for k2, v2 in v1.items():
        ips.append(k2)

for l3 in ips:
    n = ips.count(l3)
    # Set number of matches. For p2p networks > 2
    if n >= 2:
        dupl_p2p.append(l3)
dupl_p2p = list(dict.fromkeys(dupl_p2p))
print(dupl_p2p)

for l4 in dupl_p2p:
    for k3, v3 in dict1.items():
        for k4, v4 in v3.items():
            if l4 == k4:
                print("Here is a duplicating p2p network on the next hosts:")
                print("P2P network: ", l4)
                print("Host:        ", k3)
