import os
import argparse
import subprocess
import unittest
import sys
import requests
from bs4 import BeautifulSoup
import types


class Tester(unittest.TestCase):
    pass

SRC_FORMAT = "{contest_id}/{problem}.py"
SRC_TEMPLATE = "if __name__ == \"__main__\":\n    print \"\""
OUT_FORMAT = "{contest_id}/out_{problem}_{test_num}.txt"
IN_FORMAT = "{contest_id}/in_{problem}_{test_num}.txt"


def test_generator(contest_id, problem, test_num):

    def get_expected_out(contest_id, problem):
        out_file = OUT_FORMAT.format(contest_id=contest_id, problem=problem, test_num=test_num)
        with open(out_file, 'r') as f:
            return f.read()

    def test(self):
        src_file = SRC_FORMAT.format(contest_id=contest_id, problem=problem)
        in_file = IN_FORMAT.format(contest_id=contest_id, problem=problem, test_num=test_num)
        run_output = subprocess.check_output("python {0} < {1}".format(src_file, in_file), shell=True)
        self.assertEqual(get_expected_out(contest_id, problem), run_output)
    return test


def download_contest(contest_id, problem):
    url = "http://codeforces.com/contest/{contest}/problem/{problem}".format(contest=contest_id, problem=problem)
    print "Downloading url = ", url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    html_inputs = soup.find_all('div', attrs={'class': 'input'})
    html_outputs = soup.find_all('div', attrs={'class': 'output'})
    formatted_inputs = []
    formatted_outputs = []

    def get_pre_text(pre_tag):
        text = ''
        for elem in pre_tag.recursiveChildGenerator():
            if isinstance(elem, types.StringTypes):
                text += elem
            elif elem.name == 'br':
                text += '\n'
        return text.strip()

    for idx, html_input in enumerate(html_inputs):
        formatted_inputs.append(get_pre_text(html_input.pre))
        html_output = html_outputs[idx]
        formatted_outputs.append(get_pre_text(html_output.pre))

    return zip(formatted_inputs, formatted_outputs)


def create_files(contest_id, problem):
    """
    creates src and test files for a given contest/problem
    :param contest_id: contest id
    :param problem: problem
    :return:
    """
    # create source file

    # create directory with contest_id
    dir_name = str(contest_id)
    if not os.path.exists(dir_name):
        print "Create directory: ", dir_name
        os.mkdir(dir_name)

    # create file if not exists
    src_file = SRC_FORMAT.format(contest_id=contest_id, problem=problem)
    if not os.path.isfile(src_file):
        print "Create source file: ", src_file
        with os.fdopen(os.open(src_file, os.O_WRONLY | os.O_CREAT, 0777), 'w') as fd:
            fd.write(SRC_TEMPLATE)

    # create test files.
    # fixme => should only if not exists (maybe?)
    test_cases = download_contest(contest_id, problem)

    for test_num, (formatted_input, formatted_output) in enumerate(test_cases):
        in_file = IN_FORMAT.format(contest_id=contest_id, problem=problem, test_num=test_num)
        with open(in_file, 'w') as f:
            print "Create input file: ", in_file
            f.write(formatted_input)
        out_file = OUT_FORMAT.format(contest_id=contest_id, problem=problem, test_num=test_num)
        with open(out_file, 'w') as f:
            print "Create output file: ", out_file
            f.write(formatted_output)

    return test_cases


def get_problems(contest_id):
    contest_url = "http://codeforces.com/contest/{contest}".format(contest=contest_id)
    print "Downloading contest url: ", contest_url
    response = requests.get(contest_url)
    soup = BeautifulSoup(response.text, "html.parser")
    problem_ids = soup.find_all('td', attrs={'class': 'id'})
    return [problem_id.a.text.strip().lower() for problem_id in problem_ids]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", action="store_true")
    parser.add_argument("-c", "--contest", action="store", type=int, required=True)
    parser.add_argument("-p", "--problem", action="store", required=True)

    args = parser.parse_args()
    contest_id = args.contest
    problem = args.problem

    if args.init:
        # if requested, create files for *all* problems
        problem_ids = get_problems(contest_id)
        for problem_id in problem_ids:
            test_cases = create_files(contest_id, problem_id)

    # get num tests for this problem
    num_tests = 0
    for root, dirs, filenames in os.walk(str(contest_id)):
        for filename in filenames:
            if filename.startswith("in_{problem}".format(problem=problem)):
                num_tests += 1

    for test_num in range(num_tests):
        test_name = 'test_%s' % test_num
        test = test_generator(contest_id, problem, test_num)
        setattr(Tester, test_name, test)

    # trim argv to not include params to this script
    # these are directly passed to the unittest runner.py to confuse things!
    sys.argv = sys.argv[0:1]

    # run unittest runner
    unittest.main()
