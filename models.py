from typing import Iterator, NamedTuple, List 
# import tinydb                  


class PlantSpecies(NamedTuple):
    species_name: str
    species_id: int
    products_and_services: List[str]
    nativity: str
    native_range: List[str]
