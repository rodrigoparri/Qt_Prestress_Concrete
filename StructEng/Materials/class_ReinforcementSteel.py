# from StructEng.Materials.class_Material import Material

class ReinforcementSteel:
    """passive reinforcement steel"""
    kwDefaults = {
        'fyk': 500,
        'gs': 1.15,
        'Es': 200E3
    }

    def __init__(self, **kwargs):
        self.fyk = kwargs.get('fyk', self.kwDefaults['fyk'])
        self.gs = kwargs.get('gs', self.kwDefaults['gs'])
        self.Es = kwargs.get('Es', self.kwDefaults['Es'])

    def __str__(self):
        string = f"""
        fyk: passive steel characteristic strength.................................{self.fyk} Mpa
        Es: passive steel Young's modulus..........................................{self.Es} Mpa
        gs: passive steel safety coefficient.......................................{self.gs} -adim-
        
        """
        return string
