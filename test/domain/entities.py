__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from typing import AnyStr, Dict, List, TypeVar, Any

Instancetype = TypeVar('Instancetype', bound='Contractors')


class Entities(object):
    def __init__(self, _entities: List[Dict[AnyStr, Any]] = None):
        self.entities = _entities

    @classmethod
    def build(cls, filename: str) -> Instancetype:
        _entities = Entities.load(filename)
        return cls(_entities)

    @property
    def __len__(self) -> int:
        return len(self.entities)

    def __str__(self) -> str:
        return '\n'.join([f'{k}:{v}' for c in self.entities for k, v in c.items()])

    def save(self, filename: str) -> bool:
        import json
        try:
            json_entities = [json.dumps(c) for c in self.entities]
            with open(filename, 'w') as f:
                content = "\n".join(json_entities)
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
                _entities_list = [json.loads(entry) for entry in entries]
                return _entities_list
        except json.JSONDecodeError as e:
            print(f'JSON Decoder error {str(e)}')
            return []

        except Exception as e:
            print(str(e))
            return []

    def query(self, criteria: Dict[AnyStr, Any]) -> List[Dict[AnyStr, Any]]:
        return [c for c in self.entities if Entities.__key_action_map(c, criteria)]

        # -------------------  Supporting methods -------------------------
    @staticmethod
    def __key_action_map(entities_map: Dict[AnyStr, Any], criteria: Dict[AnyStr, Any]) -> bool:
        return not (False in [Entities.__key_action(entities_map, k, v) for k, v in criteria.items()])

    @staticmethod
    def __key_action(entities_map: Dict[AnyStr, Any], key: AnyStr, value: Any) -> bool:
        if key == 'location':
            return entities_map['location'] == value
        elif key == 'bid_price':
            return entities_map[key] < float(value)
        elif key == 'specialty':
            return entities_map['specialty'] == value
        elif key == 'rating':
            return entities_map['rating'] >= int(value)
        else:
            return True


if __name__ == '__main__':
    entities = Entities.build('../../data/contractors.json')
    print(str(entities))
    queried_entities = entities.query({'location': 'San Jose'})
    print('\n'.join([str(c) for c in queried_entities]))

