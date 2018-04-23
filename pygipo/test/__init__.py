import os


class TestFile:

    def __init__(self, fname):
        self.fname = fname
        self.here = os.path.dirname(__file__)
        with open(os.path.join(self.here, 'expected', self.fname)) as f:
            self.expected = f.read()

    def write_actual(self, x):
        with open(os.path.join(self.here, 'actual', self.fname), 'w') as f:
            f.write(x)
