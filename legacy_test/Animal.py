def AnimalFactory(animal_type, initial_energy = 100, skills = {'run' : 5, 'swim' : -1}):
    class Animal(object):
        def __init__(self, name, energy = initial_energy):
            self.__name = name
            self.__energy = energy
            self.__skills = skills
            self.__name__ = animal_type
            for skill, energy_change in skills.items():
                self.__add_skill_method(skill, energy_change)
        
        def __add_skill_method(self, skill, energy_change):
            def skill_method(self):
                if energy_change > 0:
                    print(f"My name is {self.__name} and i {skill}")
                    self.__energy -= energy_change
                else:
                    print(f"My name is {self.__name} and i can't {skill}")
            setattr(Animal, skill, skill_method)
        
        @property
        def get_energy(self):
            return self.__energy
        
        @property
        def get_name(self):
            return self.__name
            
        def say(self):
            print(f"Hello, i'm {self.__name__} and my name is {self.__name}")
            
    return Animal
