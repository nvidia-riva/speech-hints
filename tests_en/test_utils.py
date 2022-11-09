import os

def parse_test_case_file(file_name: str):
    """
    Prepares tests pairs for ITN and TN tests
    """
    test_pairs = []
    with open(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + file_name, 'r') as f:
        for line in f:
            spoken, written, hint = line.split('~')
            test_pairs.append((spoken, written, hint.strip("\n")))
    return test_pairs