from threading import Event, Condition, Thread, Lock
import copy

history = []

DEFAULT_START_THREADS = True

shared_variable = 0

class Communicator:

    def __init__(self, nodes_count):
        self.channels = [{} for element in range(nodes_count)]
        self.events = [Event() for element in range(nodes_count)]



class Environment:

    def __init__(self, nodes_count, communicator):
        self.nodes = []
        for i in range(nodes_count):
            node = Node(communicator.events, communicator.channels)
            node.talker.request_numbers = [0 for element in range(nodes_count)]
            self.nodes.append(node)

        self.nodes_count = Talker.new_id
        self.token = Token(self.nodes_count)


class Node:

    def __init__(self, events, channels):
        self.enter_critical_section = Event()
        self.leave_critical_section = Event()
        self.talker = Talker(events, channels, self.enter_critical_section, self.leave_critical_section)





class Talker(Thread):
    new_id = 0

    def __init__(self, events, channels, enter_critical_section, leave_critical_section):
        self.id = Talker.new_id
        self.request_numbers = []
        self.token = None
        self.event = events[self.id]
        self.all_events = events
        self.channel = channels[self.id]
        self.all_channels = channels
        self.enter_critical_section = enter_critical_section
        self.leave_critical_section = leave_critical_section

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
            # if len(incoming_data) > 0:
            #     # This means, that more data comes to the buffer than expected at the moment of implementation -
            #     # in order to properly handle this case, this block should be updated / reimplemented to avoid data loss
            #     raise Exception

            print('Node no ' + str(self.id) + ' sets up a thread waiting for calls.' )
            self.event.wait()
            self.event.clear()

            # Preventing data races
            lock = Lock()
            with lock:
                incoming_data = dict(self.all_channels[self.id])
            self.channel = {}

            function_name = incoming_data['call']
            function_to_call = {
                'receive_request': self.handle_incoming_request,
                'receive_token': self.receive_token
            }[function_name]

            print('Talker in node: ' + str(self.id) + ' was awoken with "' + function_name + '" call')
            function_to_call(incoming_data)


    # params: {'id': int, 'seq': int (sequential number)
    def handle_incoming_request(self, args):
        print('Node no ' + str(self.id) + ' handling a request')
        self.event.clear()
        self.request_numbers[args['id']]\
            = args['seq'] if args['seq'] > self.request_numbers[args['id']] else self.request_numbers[args['id']]
        if self.token is not None:
            self.pass_token({'call': 'receive_token', 'id': args['id'], 'token': copy.copy(self.token)})
            self.token = None

    def send_request(self):
        print('THREAD NO ' + str(self.id) + ' REQUESTED TO BE GRANTED WITH TOKEN')
        self.request_numbers[self.id] += 1
        i = 0
        for element in self.all_channels:
            self.all_channels[i] = {'call': 'receive_request', 'id': self.id, 'seq': self.request_numbers[self.id]}
            i += 1
        for event in self.all_events:
            event.clear()
            event.set()


    def receive_token(self, args):
        self.event.clear()
        self.token = copy.copy(self.all_channels[self.id]['token'])
        self.all_channels[self.id] = {}
        self.enter_critical_section.set()
        self.leave_critical_section.wait()
        self.token[self.id] = self.request_numbers[self.id]
        self.token.queue.pop()


        print('CURRENT TOKEN QUEUE: ' + str(self.token.queue))

        i = 0
        for token_element, request_element in zip(self.token.queue, self.request_numbers):
            if request_element > token_element:
                token_element = request_element
                self.token.queue.append(i)
                i += 1

        if len(self.token.queue) > 0:
            token_copy = copy.copy(self.token)
            args = {'id': token_copy.queue[0], 'token': token_copy}
            self.token = None
            self.pass_token(args)


    # params: {'id': int, 'token': token}
    def pass_token(self, args):
        print('TOKEN was held by node ' + str(self.id) + ' and is being passed to node ' + str(args['id']))
        self.all_channels[args['id']] = args
        self.all_events[args['id']].set()

    def nodes_count_in_environment(self):
        return len(self.request_numbers)

    #def request


class Token:

    def __init__(self, nodes_count):
        self.request_numbers = [0 for element in range(nodes_count)]
        self.queue = []


def main():
    communicator = Communicator(2)
    environment = Environment(2, communicator)
    environment.token.queue.append(1)
    environment.nodes[1].talker.token = copy.copy(environment.token)
    environment.nodes[0].talker.send_request()

    print()
    Talker.new_id = 0



if __name__ == '__main__':
    main()