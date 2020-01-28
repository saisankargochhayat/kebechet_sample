
from thamos import lib
import yaml
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)

def advise_wrap():
    with open("Pipfile", "r") as pipfile, \
         open("Pipfile.lock", "r") as piplock:

        res = lib.advise(pipfile.read(), "")
        pp.pprint(res)
        pip_info = res[0]["report"][0][1]["requirements"]
        lock_info = res[0]["report"][0][1]["requirements_locked"]
        pp.pprint(pip_info)
        pp.pprint(lock_info)

    return res


def advise_and_write():
    res = advise_wrap()

    pip_info = res[0]["report"][0][1]["requirements"]
    lock_info = res[0]["report"][0][1]["requirements_locked"]
    with open("Pipfile", "w+") as f:
        f.write("[dev-packages]\n")
        for entry in pip_info["dev-packages"]:
            f.write("{} = \"{}\"\n".format(entry, pip_info["dev-packages"][entry]))

        f.write("\n[packages]\n")
        for entry in pip_info["packages"]:
            f.write("{} = \"{}\"\n".format(entry, pip_info["packages"][entry]))
            
        f.write("\n[requires]\n")
        for entry in pip_info["requires"]:
            f.write("{} = \"{}\"\n".format(entry, pip_info["requires"][entry]))

        for index in pip_info["source"]:
            f.write("\n[[source]]\n")
            for entry in index:
                if entry == "verify_ssl":
                    f.write("{} = {}\n".format(entry, str(index[entry]).lower()))
                else:
                    f.write("{} = \"{}\"\n".format(entry, index[entry]))

    with open("Pipfile.lock", "w+") as f:
        f.write(json.dumps(lock_info))

        
