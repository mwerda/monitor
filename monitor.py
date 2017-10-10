class Environment:

    def __init__(self, nodes_count):
        self.nodes = []
        for i in range(nodes_count):
            node = Node()
            node.talker.request_numbers = [0 for element in range(nodes_count)]
            self.nodes.append(node)

        self.nodes_count = Talker.new_id
        self.token = Token(self.nodes_count)


class Node:

    def __init__(self):
        self.talker = Talker()

class Talker:
    new_id = 0

    def __init__(self):
        self.id = Talker.new_id
        self.request_numbers = []
        self.token = None

        Talker.new_id += 1

    def request(self):
        #for element in ra
        # TODO implement sending requests

    def nodes_count_in_environment(self):
        return len(self.request_numbers)


    #def request


class Token:

    def __init__(self, nodes_count):
        self.request_numbers = [0 for element in range(nodes_count)]
        self.queue = []


def main():
    environment = Environment(4)
