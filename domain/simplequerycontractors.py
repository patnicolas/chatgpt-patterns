__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from typing import List, AnyStr, Dict, Any, Type, Optional
from langchain.tools import BaseTool
from pydantic import Field, BaseModel


class SimpleQueryContractorsInput(BaseModel):
    """ Wraps the input for loading the contractor list with condition"""
    condition_list: List[AnyStr] = Field(..., description="Condition applied to the query the contractor list")


class SimpleQueryContractors(BaseTool):
    name = "simple_query_contractors"
    description = "Useful to select contractors from data/contractors.json file according to condition"

    def _run(self, condition_list: List[AnyStr]) -> AnyStr:
        query_result = simple_query_contractors(condition_list)
        return query_result

    def _arun(self, condition_list: List[AnyStr]) -> AnyStr:
        raise NotImplementedError("QueryContractors does not support async")

    args_schema: Optional[Type[BaseModel]] = SimpleQueryContractorsInput

    def schema(self):
        return self.args_schema.schema()


def simple_query_contractors(_conditions: List[str]) -> AnyStr:
    from domain.contractors import Contractors
    from domain.htmltable import format_html
    contractors = Contractors.build('data/contractors.json')
    conditions_dictionary: Dict[AnyStr, Any] = {}
    for condition in _conditions:
        c = str(condition)
        key, value = c.split("=") if c.__contains__("=") else c.split(":")
        conditions_dictionary.update({key.rstrip(): value.lstrip()})

    selected_contractors: List[Dict[AnyStr, Any]] = contractors.query(conditions_dictionary)
    return format_html(selected_contractors)




if __name__ == '__main__':
    input_str = "location#San Jose"
    args = input_str.split(":")

    conditions_list = ["location:San Jose", "specialty:plumbing"]
    results: list[dict[str, Any]] = simple_query_contractors(conditions_list)
    print(results)
    print(SimpleQueryContractors().schema())

