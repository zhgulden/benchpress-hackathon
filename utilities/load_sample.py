import json

from pathlib import Path
from typing import Any


def load_sample(index: int, dataset_path: str = "./data/dev") -> dict[str, Any]:
    """
    Load an item from the development sample of the APPS dataset.
    
    Args:
        index (int): The index of the item to load.
    
    Returns:
        dict: A dictionary containing the problem, test cases, starter code.
    """

    sample_path = Path(dataset_path) / f"{index:04d}.json"
    if not sample_path.exists():
        raise FileNotFoundError(f"Sample '{sample_path}' does not exist.")
    
    with open(sample_path, "r") as f:
        sample_data = json.load(f)
    
    return sample_data