"""
This code is adapted from the following repository:
https://github.com/hendrycks/apps

Original work by the authors of the repository. All rights and credits belong to them.
Used under the terms of the applicable license specified in the repository.
"""

import multiprocessing

from utilities.testing_util import run_test

def _temp_run(problem, generation, eval, debug, result):
    try:
        if debug:
            print(f"Running test for problem: {problem}")
        result.append(run_test(problem=problem, test=generation, eval=eval, debug=debug))
        if debug:
            print(f"Test completed with result: {result}")
    except Exception as e:
        if debug:
            print(f"Error in _temp_run: {e}")

def run_test_cases(problem: dict, generation: str, timeout: int, eval: bool = False, debug: bool = False) -> list[bool]:
    """Check correctness of code generation with a global timeout.
    The global timeout is to catch some extreme/rare cases not handled by the timeouts
    inside `run_test`"""


    manager = multiprocessing.Manager()
    result = manager.list()
    p = multiprocessing.Process(target=_temp_run, args=(problem, generation, eval, debug, result))
    p.start()
    p.join(timeout=timeout + 1)

    if p.is_alive():
        if debug:
            print(f"Process is still alive. Killing the process.")
        p.kill()
    if not result:
        # Remark: ideally we would consider that all tests failed but we can't access number of tests here easily
        # so we use 21=the average number of tests for a smaple in the test split instead 
        avg_number_tests = 21
        result = [[-1] * avg_number_tests]
        if debug:
            print(f"Global timeout occurred, returning default result.")
    if debug:
        print(f"Final result: {result}")

    return result[0]