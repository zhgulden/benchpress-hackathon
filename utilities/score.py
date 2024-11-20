from copy import deepcopy
from typing import Callable, Tuple
from tqdm import tqdm

from aleph_alpha_client import Client, CompletionRequest, Prompt
from utilities import load_sample, run_test_cases


def score(generation_func: Callable, client: Client, dataset_path: str, length: int = 200) -> Tuple[float, float]:
    """
    Score the generation function on a given test set.
    
    Args:
        generation_func (Callable): The generation function to score.
        dataset_path (str): The path to the test set.
        length (int): The number of problems to score.
        
    Returns:
        Tuple[float, float]: The percentage of problems that were solved correctly and the 
                             percentage of test cases that were solved correctly.
    """
    passed_problems = 0
    total_problems = length
    
    passed_test_cases = 0
    total_test_cases = 0
    
    for i in tqdm(range(length)):
        problem = load_sample(index=i, dataset_path=dataset_path)
        problem_wo_test_cases = deepcopy(problem)
        del problem_wo_test_cases["test_cases"]
        generated_code = generation_func(
            problem=problem_wo_test_cases, 
            client=client
        )

        result = run_test_cases(
            problem=problem,
            generation=generated_code,
            eval=True,
            timeout=10,
        )
        
        print(result)
        passed = [r["passed"] for r in result]
        passed_test_cases += sum(passed)
        total_test_cases += len(passed)
        
        if all(passed):
            passed_problems += 1
            
    return (
        passed_problems / total_problems,
        passed_test_cases / total_test_cases,
    )