from threading import Event, Condition, Thread, Lock
import copy

DEFAULT_START_THREADS = False


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
                'receive_token': self.receive_token
            }[key]

            print('Talker in node: ' + str(self.id) + ' was awoken with ' + key + ' call')
            function_to_call(incoming_data[key])




    # params: {'id': int, 'seq': int (sequential number)
    def handle_incoming_request(self, args):
        self.event.clear()
        self.request_numbers[args['id']]\
            = args['seq'] if args['seq'] > self.request_numbers[args['id']] else self.request_numbers[args['id']]
        if self.token is not None:
            self.pass_token({'id': args['id'], 'token': copy.copy(self.token)})
            self.token = None

    def send_request(self, args):
        self.request_numbers[self.id] += 1
        for element in self.all_channels:
            element = {'id': self.id, 'seq': self.request_numbers[self.id]}
        for event in self.all_events:
            event.set()


    def receive_token(self, args):
        self.event.clear()
        self.token = copy.copy(self.channel['token'])
        self.channel = {}
        self.enter_critical_section.set()
        self.leave_critical_section.wait()
        self.token[self.id] = self.request_numbers[self.id]
        self.token.queue.pop()

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

        # skopiuj token do siebie
        # wyslij sygnal do workera, zeby ogarnal swoja sekcje i zaloz waita na event, czekaj na odblokowanie
        # wez LN[i] tokenowe = moje RN[i]
        # queue pop
        # dla kazdego id, ktorego nie ma w kolejce, dodaj jesli LN jest mniejsze od RN
        # wywal token do pierwszego w kolejce - skopiuj i usun lokalna kopie
        return


    # params: {'id': int, 'token': token}
    def pass_token(self, args):
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
    number_of_nodes = 4
    communicator = Communicator(number_of_nodes)
    environment = Environment(4, communicator)
