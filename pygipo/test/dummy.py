import json
import os

here = os.path.dirname(__file__)


class Dummy:
    attributes = None
    @classmethod
    def from_path(cls, path):
        with open(path) as f:
            self = cls()
            self.attributes = json.load(f)
            return self


group = Dummy.from_path(os.path.join(here, '_dummy/projects.json'))
project = Dummy()
project.attributes = group.attributes[0]
