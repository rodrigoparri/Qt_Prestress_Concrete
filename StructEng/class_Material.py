from abc import ABC, abstractmethod

class Material(ABC):

    def __init__(self, fck, **kwargs):
        self.fck = fck