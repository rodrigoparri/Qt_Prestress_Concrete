#from StructEng.Materials.class_Material import Material

class ReinforcementSteel():
    """passive reinforcement steel"""
    def __init__(self, fyk, **kwargs):
        self.fyk = fyk

    def __str__(self):
        str = f"""
        fyk: passive steel characteristic strength.................................{self.fyk} Mpa
        
        """