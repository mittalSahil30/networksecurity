from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
  "this function will return list of requiremnts"
  
  requirementList:List[str]= []
  try:
    with open('requirements.txt', 'r') as file:
      lines = file.readlines()
      
      for line in lines:
        requirement = line.strip()
        
        if requirement and requirement != '-e .':
          requirementList.append(requirement)
          
  except FileNotFoundError:
    print("requirements.txt file does not found")
    
  return requirementList

setup(
  name = "NetworkSecurity",
  version = "0.0.1",
  author="sahil",
  author_email = "sahilmittal3003@gmail.com",
  packages=find_packages(),
  install_requires= get_requirements()
)
