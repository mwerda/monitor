from threading import Event, Condition, Thread, Lock

DEFAULT_START_THREADS = False


class Communicator:

    def __init__(self, nodes_count):
        self.channel = [{} for element in range(nodes_count)]
        self.events = [Event() for element in range(nodes_count)]



class Environment:

    def __init__(self, nodes_count, communicator):
        self.nodes = []
        for i in range(nodes_count):
            node = Node(communicator.events[i], communicator.channel[i])
            node.talker.request_numbers = [0 for element in range(nodes_count)]
            self.nodes.append(node)

        self.nodes_count = Talker.new_id
        self.token = Token(self.nodes_count)
        self.channel = [{} for element in range(nodes_count)]


class Node:

    def __init__(self, event, channel):
        self.talker = Talker(event, channel)


class Talker(Thread):
    new_id = 0

    def __init__(self, event, channel):
        self.id = Talker.new_id
        self.request_numbers = []
        self.token = None
        self.event = event
        self.channel = channel

        Talker.new_id += 1
        Thread.__init__(self)
        if DEFAULT_START_THREADS:
            self.start()

    def run(self):
        # An advantage coming from copying the channel's data is scalability: if processing the request
        # shall take more time in any scenario of higher complexity, the channel should not remain blocked
        # for any longer than necessary
        incoming_data = {}
        while True:
            if len(incoming_data) > 0:
                # This means, that more data comes to the buffer than expected at the moment of implementation -
                # in order to properly handle this case, this block should be updated / reimplemented to avoid data loss
                raise Exception

            self.event.wait()
            self.event.clear()

            # Preventing data races
            lock = Lock()
            with lock:
                incoming_data = dict(self.channel)
            self.channel = {}

            key = next(iter(incoming_data.values()))
            function_to_call = {
                'incoming_request': self.handle_incoming_request,
                'receive_token': self.receive_token,
            }[key]

            print('Talker in node: ' + str(self.id) + ' was awoken with ' + key + ' call')
            function_to_call(incoming_data[key])




    # params: {'id': int, 's': int (sequential number)
    def handle_incoming_request(self, args):


    def receive_token(self, args):

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
