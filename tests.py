import unittest
from monitor import Environment, Node, Talker, Token, Communicator, DEFAULT_START_THREADS


class TestEnvironment(unittest.TestCase):
    def test_create_environment(self):
        communicator = Communicator(5)
        e = Environment(5, communicator)
        self.assertTrue(e.nodes_count == 5)
        self.assertTrue(len(e.nodes) == 5)
        self.assertTrue(Talker.new_id == 5)
        for element in e.nodes:
            self.assertTrue(element.talker.request_numbers == [0, 0, 0, 0, 0])
        Talker.new_id = 0


class TestToken(unittest.TestCase):
    def test_create_token(self):
        token = Token(5)
        self.assertTrue(token.request_numbers == [0, 0, 0, 0, 0])
        Talker.new_id = 0


class TestEnvironmentCommunicatorTalkers:   # if DEFAULT_START_THREADS, awaken thread should print something out
    def test_create_communicator_environment_check_talkers(self):
        communicator = Communicator(4)
        environment = Environment(4, communicator)
        # communicator.events[1].set()
        # communicator.events[1].clear()
        Talker.new_id = 0

class TestTalkers:
    communicator = Communicator(2)
    environment = Environment(2, communicator)
    environment.nodes[0].talker.send_request()
    print()
    Talker.new_id = 0

if __name__ == '__main__':
    unittest.main(exit=False)