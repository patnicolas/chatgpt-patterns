__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from typing import List, AnyStr, Dict, Any

"""
class Contractor(dict):
    def __init__(self,
                 _name: str,
                 _location: str,
                 _specialty: str,
                 _hourly_rate: float,
                 _availability: str,
                 _bid_price: float,
                 _rating: int):
        super(Contractor, self).__init__(
            name=_name,
            location=_location,
            specialty=_specialty,
            hourly_rate=_hourly_rate,
            availability=_availability,
            bid_price=_bid_price,
            review_score=_rating)

    def __str__(self):
        return ' '.join([f'{k}:{v}' for k, v in self.items()])
"""

def load_contractors(filename: AnyStr) -> List[Dict[AnyStr, Any]]:
    from domain.contractors import Contractors
    return Contractors.load(filename)

