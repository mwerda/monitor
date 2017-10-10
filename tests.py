import unittest
from monitor import Environment, Node, Talker, Token


class TestEnvironment(unittest.TestCase):
    def test_create_environment(self):
        e = Environment(5)
        self.assertTrue(e.nodes_count == 5)
        self.assertTrue(len(e.nodes) == 5)
        self.assertTrue(Talker.new_id == 5)
        for element in e.nodes:
            self.assertTrue(element.talker.request_numbers == [0, 0, 0, 0, 0])


class TestToken(unittest.TestCase):
    def test_create_token(self):
        token = Token(5)
        self.assertTrue(token.request_numbers == [0, 0, 0, 0, 0])



if __name__ == '__main__':
    unittest.main(exit=False)