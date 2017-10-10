class Environment:

    def __init__(self, nodes_count):
        self.nodes = []
        for i in range(nodes_count):
            self.nodes.append(Node())
        self.nodes_count = Talker.last_id + 1


class Node:

    def __init__(self):
        self.talker = Talker()


class Talker:
    last_id = 0

    def __init__(self):
        self.id = Talker.last_id
        self.request_numbers = []
        self.token = None

        Talker.last_id += 1


    def request


class Token:

    def __init__(self):
        self.request_numbers = []
        self.queue = []