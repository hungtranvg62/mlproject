from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = "-e ."
def get_requirements(file_path: str) -> List[str]:
    '''
    This function returns the LIST of requirements
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines() # read the file and return a list of requirements
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT) # removed so that it is not considered as a package
    
    return requirements

setup(
    name = "mlproject",
    version = "0.0.1",
    author = "Hung",
    author_email = "hungtv11224567@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')

)