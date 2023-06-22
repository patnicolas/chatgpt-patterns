__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from typing import AnyStr, Dict, List, TypeVar, Any

Instancetype = TypeVar('Instancetype', bound='Contractors')


class Contractors(object):
    def __init__(self, _contractors: List[Dict[AnyStr, Any]] = None):
        self.contractors = _contractors

    @classmethod
    def build(cls, filename: str) -> Instancetype:
        _contractors = Contractors.load(filename)
        return cls(_contractors)

    @property
    def __len__(self) -> int:
        return len(self.contractors)

    def __str__(self) -> str:
        return '\n'.join([f'{k}:{v}' for c in self.contractors for k, v in c.items()])

    def save(self, filename: str) -> bool:
        import json
        try:
            json_contractors = [json.dumps(c) for c in self.contractors]
            with open(filename, 'w') as f:
                content = "\n".join(json_contractors)
                f.write(content)
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def load(filename: str) -> List[Dict[AnyStr, Any]]:
        import json
        try:
            with open(filename, 'r') as f:
                entries = f.readlines()
                _contractors_list = [json.loads(entry) for entry in entries]
                return _contractors_list
        except json.JSONDecodeError as e:
            print(f'JSON Decoder error {str(e)}')
            return []

        except Exception as e:
            print(str(e))
            return []

    def query(self, criteria: Dict[AnyStr, Any]) -> List[Dict[AnyStr, Any]]:
        return [c for c in self.contractors if Contractors.__key_action_map(c, criteria)]

        # -------------------  Supporting methods -------------------------
    @staticmethod
    def __key_action_map(contractor: Dict[AnyStr, Any], criteria: Dict[AnyStr, Any]) -> bool:
        return not (False in [Contractors.__key_action(contractor, k, v) for k, v in criteria.items()])

    @staticmethod
    def __key_action(contractor: Dict[AnyStr, Any], key: AnyStr, value: Any) -> bool:
        if key == 'location':
            return contractor['location'] == value
        elif key == 'bid_price':
            return contractor[key] < float(value)
        elif key == 'specialty':
            return contractor['specialty'] == value
        elif key == 'rating':
            return contractor['rating'] >= int(value)
        else:
            return True



if __name__ == '__main__':
    """
    contractors_list = [
        Contractor("John doe", "San Jose", "plumbing", 95.6, "July 2nd, 2023", 7200, 4),
        Contractor("Gary abc Inc.", "San Leandro", "plumbing", 87.6, "June 25nd, 2023", 7560, 5),
        Contractor("Temple woods corp", "Palo Alto", "cabinets", 102.0, "July 8th 2023", 3200, 4),
        Contractor("Francis Beacon LLC", "San Jose", "plumbing", 105.6, "June 16th, 2023", 8200, 4),
        Contractor("Los Gatos happy painters", "Los Gatos", "painting", 80.0, "July 2nd, 2023", 2100, 3),
        Contractor("Menlo Park Cabinets Inc", "Menlo Park", "cabinets", 110.0, "July 11th, 2023", 3500, 5),
        Contractor("Sunnyvale Electricians", "Sunnyvale", "electrical", 110.0, "June 19th 2023", 2800, 3),
        Contractor("Allied Plumbers Inc", "San Jose", "plumbing", 99.5, "June 25th, 2023", 7700, 5),
        Contractor("Cupertino Electrical Supplies", "Cupertino", "electrical", 109.0, "July 5nd, 2023", 3000, 4),
        Contractor("Exact Plumbing how tInc", "Menlo Park", "plumbing", 98.0, "July 11th, 2023", 7550, 4)
    ]

    contractors = Contractors(contractors_list)

    contractors.save('../data/contractors.json')
    """
    contractors = Contractors.build('../data/contractors.json')
    print(str(contractors))
    san_jose_contractors = contractors.query({'location': 'San Jose'})
    print('\n'.join([str(c) for c in  san_jose_contractors]))

