# summary 

method to initialize an environment to run sample codeforces tests for a given contest.

can do the following: 

1. download all the problems along with their test cases
2. create stub source files and test files 
3. run tests using auto-generated python unittest tests

## script usage: 

```
usage: runner.py [-h] [-i] -c CONTEST -p PROBLEM

optional arguments:
  -h, --help            show this help message and exit
  -i, --init
  -c CONTEST, --contest CONTEST
  -p PROBLEM, --problem PROBLEM
```  

## examples: 

### generate files for contest 596

```
codeforces> ls
runner.py
codeforces> python runner.py --init --contest 596 --problem c
Downloading contest url:  http://codeforces.com/contest/596
Create directory:  596
Create source file:  596/a.py
Downloading url =  http://codeforces.com/contest/596/problem/a
Create input file:  596/in_a_0.txt
Create output file:  596/out_a_0.txt
Create input file:  596/in_a_1.txt
Create output file:  596/out_a_1.txt
Create source file:  596/b.py
Downloading url =  http://codeforces.com/contest/596/problem/b
Create input file:  596/in_b_0.txt
Create output file:  596/out_b_0.txt
Create input file:  596/in_b_1.txt
Create output file:  596/out_b_1.txt
Create source file:  596/c.py
Downloading url =  http://codeforces.com/contest/596/problem/c
Create input file:  596/in_c_0.txt
Create output file:  596/out_c_0.txt
Create input file:  596/in_c_1.txt
Create output file:  596/out_c_1.txt
Create source file:  596/d.py
Downloading url =  http://codeforces.com/contest/596/problem/d
Create input file:  596/in_d_0.txt
Create output file:  596/out_d_0.txt
Create input file:  596/in_d_1.txt
Create output file:  596/out_d_1.txt
Create source file:  596/e.py
Downloading url =  http://codeforces.com/contest/596/problem/e
Create input file:  596/in_e_0.txt
Create output file:  596/out_e_0.txt
Create input file:  596/in_e_1.txt
Create output file:  596/out_e_1.txt
FF
======================================================================
FAIL: test_0 (__main__.Tester)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "runner.py", line 31, in test
    self.assertEqual(get_expected_out(contest_id, problem), run_output)
AssertionError: 'YES\n0 0\n1 0\n2 0\n0 1\n1 1' != '\n'

======================================================================
FAIL: test_1 (__main__.Tester)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "runner.py", line 31, in test
    self.assertEqual(get_expected_out(contest_id, problem), run_output)
AssertionError: 'NO' != '\n'

----------------------------------------------------------------------
Ran 2 tests in 0.046s

FAILED (failures=2)

```

### only run tests for a contest + problem

```
codeforces> python runner.py --contest 596 --problem c
FF
======================================================================
FAIL: test_0 (__main__.Tester)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "runner.py", line 31, in test
    self.assertEqual(get_expected_out(contest_id, problem), run_output)
AssertionError: 'YES\n0 0\n1 0\n2 0\n0 1\n1 1' != '\n'

======================================================================
FAIL: test_1 (__main__.Tester)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "runner.py", line 31, in test
    self.assertEqual(get_expected_out(contest_id, problem), run_output)
AssertionError: 'NO' != '\n'

----------------------------------------------------------------------
Ran 2 tests in 0.045s

FAILED (failures=2)
```
