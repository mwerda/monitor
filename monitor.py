from threading import Event, Condition, Thread

DEFAULT_START_THREADS = False


class Communicator:

    def __init__(self, nodes_count):
        self.canal = [{} for element in range(nodes_count)]
        self.events = [Event() for element in range(nodes_count)]



class Environment:

    def __init__(self, nodes_count, communicator):
        self.nodes = []
        for i in range(nodes_count):
            node = Node(communicator.events[i])
            node.talker.request_numbers = [0 for element in range(nodes_count)]
            self.nodes.append(node)

        self.nodes_count = Talker.new_id
        self.token = Token(self.nodes_count)
        self.canal = [{} for element in range(nodes_count)]


class Node:

    def __init__(self, event):
        self.talker = Talker(event)


class Talker(Thread):
    new_id = 0

    def __init__(self, event):
        self.id = Talker.new_id
        self.request_numbers = []
        self.token = None
        self.event = event

        Talker.new_id += 1
        Thread.__init__(self)
        if DEFAULT_START_THREADS:
            self.start()

    def run(self):
        while True:
            self.event.wait()
            print('Talker in node ' + str(self.id) + ' was awoken')



    def request(self):
        return
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
    number_of_nodes = 4
    communicator = Communicator(number_of_nodes)
    environment = Environment(4, communicator)
