__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from typing import List, AnyStr, Dict, Any, Type, Optional
from langchain.tools import BaseTool
from pydantic import Field, BaseModel


class ListContractorsInput(BaseModel):
    """ Wraps the input for loading the contractor list with condition"""
    condition: str = Field(..., description="Load and list all the contractors")


class ListContractors(BaseTool):
    name = "query_contractors"
    description = "Useful to list all the contractors from a JSON file loaded from data folder"

    def _run(self, condition: str) -> List[Dict[AnyStr, Any]]:
        list_result = list_contractors(condition)
        return list_result

    def _arun(self, condition: str) -> List[Dict[AnyStr, Any]]:
        raise NotImplementedError("ListContractors does not support async")

    args_schema: Optional[Type[BaseModel]] = None


def list_contractors(condition: str) -> List[Dict[AnyStr, Any]]:
    from domain.contractors import Contractors
    contractors_instance = Contractors.build('data/contractors.json')
    return contractors_instance.contractors
