import pickle
from typing import ByteString, Any

def make_pickle(data:Any):
    return pickle.dumps(data)


def load_pickle(data:ByteString):
    return pickle.loads(data)
