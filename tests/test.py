import os

"""
"""

VARIABLE_FILES = ['variables.tf', 'module_test/variables.tf',
                  '.assertions/variables.tf', '.assertions/module_test/variables.tf']
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
EXPECTED_VALUES = []
RESULT_VALUES = []


def get_results(args):
    global EXPECTED_VALUES
    global RESULT_VALUES
    EXPECTED_VALUES = []
    RESULT_VALUES = []
    for var_file in VARIABLE_FILES:
        with open(CURRENT_DIR + '/' + var_file, 'r') as file:
            text = file.read()
            if '.assertions' in var_file:
                EXPECTED_VALUES.append(text)
            else:
                RESULT_VALUES.append(text)


def run_dir_test(args):
    os.system(f"python3 {PARENT_DIR}/terraform-check-unused-variables.py --dir tests -q")
    get_results(args)
    print('dir test 1...', end='')
    assert EXPECTED_VALUES[0] == RESULT_VALUES[0]
    print('pass')
    print('dir test 2...', end='')
    assert EXPECTED_VALUES[1] != RESULT_VALUES[1]
    print('pass')
    clean_up()


def run_recursive_test(args):
    os.system(f"python3 {PARENT_DIR}/terraform-check-unused-variables.py -rq")
    get_results(args)
    for i, file in enumerate(EXPECTED_VALUES):
        print(f'recursive test {i + 1}...', end='')
        assert file == RESULT_VALUES[i]
        print('pass')
    clean_up()


def clean_up():
    os.system(f"git checkout -- {CURRENT_DIR}/*")


def parse_args():
    return {}


def test_header(text):
    whitespace = '    '
    text = whitespace + text + whitespace
    flavor = '=' * ((80 - len(text)) // 2)
    text = flavor + text + flavor + '\n'
    linebreak = '=' * (len(text)-1) + '\n'
    print(linebreak + text + linebreak)


if __name__ == '__main__':
    try:
        args = parse_args()
        test_header('Running tests')
        run_dir_test(args)
        run_recursive_test(args)
    finally:
        clean_up()
