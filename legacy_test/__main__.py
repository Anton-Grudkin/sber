import unittest
from Animal import AnimalFactory
import json, os

class TestSequence(unittest.TestCase):
    pass 

def get_skill_test(animal, skill, energy_change):
    def test_skill(self):
        energy_before = animal.get_energy
        animal.__getattribute__(skill)()
        self.assertEqual(animal.get_energy, energy_before - energy_change, \
            f'Skill {skill} caused incorrect energy change for {animal.__name__} {animal.get_name}')
    return test_skill

def tests_generator(animal_type, init_energy, skills):
    animal = AnimalFactory(animal_type, init_energy, skills)(f'{animal_type}_Sample')
    def test_factory(self):
        self.assertEqual(animal.__name__, animal_type, \
            f'{animal.__name__} {animal.get_name} has incorrect type')
    
    def test_energy(self):
        self.assertEqual(animal.get_energy, init_energy, \
            f'{animal.__name__} {animal.get_name} was initilized with incorrect energy')

    skill_tests = []
    for skill, energy_change in skills.items():
        test_skill = get_skill_test(animal, skill, energy_change)
        test_skill.__name__ += f'_{skill}'
        skill_tests.append(test_skill)

    return [test_factory, test_energy] + skill_tests


if __name__ == '__main__':
    if 'animals.json' in os.listdir():
        with open('animals.json', 'r') as f:
            animals = json.load(f)
    else:
        print('File animals.json not found; no animals will be created')
        animals = {}

    # for animal, params in animals.items():
    #     exec(f"{animal} = AnimalFactory('{animal}', *{params})")

    for animal_type, params in animals.items():
        tests = tests_generator(animal_type, *params)
        for test in tests:
            setattr(TestSequence, f'{test.__name__}_{animal_type}', test)

    unittest.main()
    