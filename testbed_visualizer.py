import argparse
import os

import xmltodict
import yaml
from pyvis.network import Network


class Pretty:
    @staticmethod
    def nodeTitle(title):
        return "<p>" + "<br>".join(f"{i}: {j}" for i, j in title.items()) + "</p>"

    @staticmethod
    def edgeTitle(title):
        string = "<p>"
        title = [(i, j) for i, j in sorted(title.items(), key=lambda x: x[1][1])]
        for c_name, c_det in title:
            string += "<p>"
            string += "<b>" + c_name + "</b><br>"
            string += "<br>".join(f"{i}: {j}" for i, j in c_det)
            string += "</p>"
        string += "</p>"
        return string


class PlotMe:
    def __init__(self, filename: str) -> None:
        with open(filename, "r") as f:
            if filename.endswith(".xml"):
                self.hm = xmltodict.parse(f.read())
            elif filename.endswith(".yml") or filename.endswith(".yaml"):
                self.hm = yaml.safe_load(f)
        self.op_name = os.path.basename(filename).split(".")[0] + ".html"
        self.net = Network(height="95vh", width="98vw")
        self.conn = {}

    def plot(self):
        self.tabulateConnection()
        self.plotHosts()
        self.plotSwitches()
        self.plotSwitchEdges()
        self.net.show(self.op_name)
        print(f"[i] Saving as {self.op_name} in cwd")

    def tabulateConnection(self):
        if "switch" in self.hm["testbed"]:
            for switch_name, switch_det in self.hm["testbed"]["switch"].items():
                for connection in list(switch_det.keys())[1:]:
                    src, dest, *_ = connection.split("-")
                    connection_det = switch_det[connection]
                    self.conn[(src, dest)] = self.conn.get((src, dest), {})
                    self.conn[(src, dest)][connection] = self.conn[(src, dest)].get(
                        connection, []
                    )
                    for key, value in connection_det.items():
                        entry = (f"{switch_name} {key}", value)
                        self.conn[(src, dest)][connection].append(entry)
        if "host" in self.hm["testbed"]:
            for host_name, host_det in self.hm["testbed"]["host"].items():
                for connection in list(host_det.keys())[1:]:
                    src, dest, *_ = connection.split("-")
                    connection_det = host_det[connection]
                    self.conn[(src, dest)] = self.conn.get((src, dest), {})
                    self.conn[(src, dest)][connection] = self.conn[(src, dest)].get(
                        connection, []
                    )
                    for key, value in connection_det.items():
                        entry = (f"{host_name} {key}", value)
                        self.conn[(src, dest)][connection].append(entry)

    def plotSwitches(self):
        if "switch" not in self.hm["testbed"]:
            return
        for i, j in self.hm["testbed"]["switch"].items():
            title = Pretty.nodeTitle(j["property"])
            # obsolete when used with 'box' shape, use 'square' to visualize the val
            # tmp = {"shape": "image", "image": "./icons/switch.png"}
            tmp = {"shape": "box"}
            self.net.add_node(i, label=i, color="#9a31a8", title=title, **tmp)

    def plotHosts(self):
        if "host" not in self.hm["testbed"]:
            return
        for i, j in self.hm["testbed"]["host"].items():
            title = Pretty.nodeTitle(j["property"])
            # tmp = {"shape": "image", "image": "./icons/server.png"}
            tmp = {"shape": "ellipse"}
            self.net.add_node(i, label=i, title=title, **tmp)

    def plotSwitchEdges(self):
        for connection, connection_det in self.conn.items():
            src, dest = connection
            width = len(connection_det) * 0.75
            try:
                tmp = {"title": Pretty.edgeTitle(connection_det), "width": width}
                self.net.add_edge(src, dest, color="magenta", **tmp)
            except Exception as e:
                print(
                    f"[!] Omiting an edge: One of the nodes is not available for {connection}"
                )


class PlotMeDir:
    """Plot Me Directed Graph"""

    def __init__(self, filename: str) -> None:
        with open(filename, "r") as f:
            if filename.endswith(".xml"):
                self.hm = xmltodict.parse(f.read())
            elif filename.endswith(".yml") or filename.endswith(".yaml"):
                self.hm = yaml.safe_load(f)
        self.op_name = os.path.basename(filename).split(".")[0] + ".html"
        self.net = Network(height="95vh", width="98vw")
        self.conn = {}

    def plot(self):
        self.tabulateConnection()
        self.plotHosts()
        self.plotSwitches()
        self.plotSwitchEdges()
        self.net.show(self.op_name)
        print(f"[i] Saving as {self.op_name} in cwd")

    def tabulateConnection(self):
        if "switch" in self.hm["testbed"]:
            for switch_name, switch_det in self.hm["testbed"]["switch"].items():
                for connection in list(switch_det.keys())[1:]:
                    src, dest, *_ = connection.split("-")
                    connection_det = switch_det[connection]
                    self.conn[(src, dest)] = self.conn.get((src, dest), {})
                    self.conn[(src, dest)][connection] = self.conn[(src, dest)].get(
                        connection, {}
                    )
                    self.conn[(src, dest)][connection].update(connection_det)
        if "host" in self.hm["testbed"]:
            for host_name, host_det in self.hm["testbed"]["host"].items():
                for connection in list(host_det.keys())[1:]:
                    src, dest, *_ = connection.split("-")
                    connection_det = host_det[connection]
                    self.conn[(src, dest)] = self.conn.get((src, dest), {})
                    self.conn[(src, dest)][connection] = self.conn[(src, dest)].get(
                        connection, {}
                    )
                    self.conn[(src, dest)][connection].update(connection_det)

    def plotSwitches(self):
        if "switch" not in self.hm["testbed"]:
            return
        for i, j in self.hm["testbed"]["switch"].items():
            title = Pretty.nodeTitle(j["property"])
            # obsolete when used with 'box' shape, use 'square' to visualize the val
            self.net.add_node(i, label=i, color="#9a31a8", shape="box", title=title)

    def plotHosts(self):
        if "host" not in self.hm["testbed"]:
            return
        for i, j in self.hm["testbed"]["host"].items():
            title = Pretty.nodeTitle(j["property"])
            self.net.add_node(i, label=i, shape="ellipse", title=title)

    def plotSwitchEdges(self):
        for connection, connection_det in self.conn.items():
            src, dest = connection
            width = len(connection_det) * 0.75
            try:
                self.net.add_edge(
                    src, dest, title=Pretty.edgeTitle(connection_det), width=width
                )
            except:
                print(
                    f"[!] Omiting an edge: One of the nodes is not avaiable for {connection}"
                )


def argument_owner():
    a = argparse.ArgumentParser()
    a.add_argument(
        "filepath",
        help="Testbed path for any of (.xml / .yml / .yaml)",
        default=None,
    )
    return a


ao = argument_owner()
a = ao.parse_args()

PlotMe(a.filepath).plot()
