# Benchpress Hackathon

Welcome to the Benchpress Hackathon. The goal is to build an agent that excels in solving hard coding problems.

## Installation

To install the dependencies Python 3.10 is required.
Install the dependencies in an isolated environment:

```
pip install -r requirements.txt
```

## Usage

The challenge comes with a Jupyter notebook for your implementation and various utilities.
We provide a development set and a validation set you can use to develop your solution.
The development set is for testing your code and consists of 300 problems with a varying number of test cases.
You are free to use all data provided with a problem, a sample has the following structure:

```python
{
    # Unique identifier for the problem in the APPS dataset.
    "problem_id": 4424,
    # The problem statement
    "question": "Given three integers ...",
    # The expected function name and the input/output examples
    # representing test cases.
    "input_output": {
        "fn_name": "expression_matter",
        "inputs": [ ... ],
        "outputs": [ ... ]
    },
    "url": "https://www.codewars.com/kata/5ae62fcf252e66d44d00008e",
    "difficulty": "introductory",
    # The starter code for the problem.
    "starter_code": "def expression_matter(a, b, c):\n\t"
}
```

The validation set is consists of 100 problems, and includes an additional key `test_cases` which is used to score your solution with the provided scoring function.

```python
{
    ...
    "test_cases": {
        "fn_name": "expression_matter",
        "inputs": [ ... ],
        "outputs": [ ... ]
    },
    ...
}
```

### Loading Problems

Use the `load_sample` function to load a problem from the development or validation set.

```python
from utilities import load_sample

problem = load_sample(index=0, dataset_path="./data/dev")
```

### Generating Code

Use the `aleph_alpha_client` to generate code.
Make sure your `AA_TOKEN` is set.

```python
from aleph_alpha_client import Client, CompletionRequest, Prompt

client = Client(AA_TOKEN)

request = CompletionRequest(
    prompt=Prompt.from_text("Your prompt."),
    maximum_tokens=256,
)

# API reference for the client:
# https://aleph-alpha-client.readthedocs.io/en/latest/
response = client.complete(request, model=MODEL)
```

### Running Tests

Use the `run_test_cases` function to run the generated code against the test cases.
The function returns a dictionary with the test results, including the expected output, the generated output, a boolean indicating whether the test passed and a traceback in case of an error.

```python
from utilities import run_test_cases

test_results = run_test_cases(
    problem=problem, 
    generation=response.completions[0].completion, 
    timeout=10,
)
```

### Scoring

Use the `score` function to score your solution on the validation set.
It expects a function that takes a problem and a client and returns a generation.

```python
from utilities import score

passed_problems, passed_test_cases = score(
    generation_func=generate_code, 
    client=client,
    dataset_path="./data/val", 
    length=50,
)
```

## Evaluation

The evaluation is done by running the generated code against a set of test cases. 
You can evaluate your function on the provided validation set by running the scoring function in the notebook.

If you want to test your solution, you can send it to us via email and we will run it against the test set.

## Attribution

The dataset is based on the [APPS dataset](https://github.com/hendrycks/apps), which is licensed under the MIT license. 
Parts of the code are adapted from APPS.

## Caution: Important Notice

- It is forbidden to use any of the other samples besides the provided ones from the APPS dataset!
- It is forbidden to use any other LLM besides the two provided ones (llama3.1-8b. llama3.1-70b)
- Please be gentle and do not waste compute. 
  - Set max tokens
  - only have a max of ten requests in flight
  - use llama3.1-8b for debugging of your scripts (rather than 70b)
  - Please refer also to https://docs.aleph-alpha.com/docs/best-practices/
- Your solution is tested against a secret test set, which contains 200 additional samples. Keep the global timeout of 10 minutes in mind


Have fun!
