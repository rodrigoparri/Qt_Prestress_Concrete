from StructEng.Materials.class_Material import Material


class PrestressSteel():

    def __init__(self, fpk):
        self.fpk = fpk

    def __str__(self):
        str = f"""
        fpk: pre-stress steel characteristic strength..............................{self.fpk} Mpa
        
        """