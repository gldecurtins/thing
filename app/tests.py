import unittest


class Tests(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)


def main():
    unittest.main(module="tests")


if __name__ == "__main__":
    unittest.main()