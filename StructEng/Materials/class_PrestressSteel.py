# from StructEng.Materials.class_Material import Material


class PrestressSteel:

    kwDefaults = {
        'fpk': 1860,
        'gp': 1.5,
        'Es': 195E3
    }

    def __init__(self, **kwargs):
        self.fpk = kwargs.get('fpk', self.kwDefaults['fpk'])
        self.gp = kwargs.get('gp', self.kwDefaults['gp'])
        self.Ep = kwargs.get('Ep', self.kwDefaults['Ep'])

    def __str__(self):
        string = f"""
        fpk: pre-stress steel characteristic strength..............................{self.fpk} Mpa
        Ep: pre-stress steel Young's modulus.......................................{self.Ep} Mpa
        gp: pre-stress steel safety coefficient....................................{self.gp} -adim-
        """

        return string
