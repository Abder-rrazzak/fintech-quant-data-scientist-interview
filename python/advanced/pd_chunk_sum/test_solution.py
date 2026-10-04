import os
import tempfile
import pandas as pd
from solution import pd_chunk_sum

def test_chunk():
    handle, name = tempfile.mkstemp(suffix='.csv')
    os.close(handle)
    try:
        with open(name, 'w', encoding='utf-8') as out:
            out.write('amount\n1\n2\n3\n')
        assert pd_chunk_sum(name, chunksize=2) == 6.0
    finally:
        os.remove(name)
