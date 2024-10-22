from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    This function will return the list of requirements.
    """
    requirement_list = []
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
        for line in lines:
            requirement = line.strip()
            if requirement and requirement != "-e .":
                requirement_list.append(requirement)
        return requirement_list
    except Exception as e:
        raise e
    
setup(
    name="Network Security",
    version="0.0.1",
    author="Jiyadh K Salim",
    author_email="jiyadh23@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()
)