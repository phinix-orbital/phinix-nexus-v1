import os

class GenericHelpers:

    @classmethod
    def get_base_path(cls) -> str:
        return os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))