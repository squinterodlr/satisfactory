class Part:
    def __init__(self, name: str, kind: str):
        self.name = name
        self.kind = kind
        self.recipes = []

    def add_recipe(self, inputs, output_rate, building=None):
        '''Adds a recipe for the part.
        Parameters
        ----------
        inputs: Array of shape (n, 2)
            Each entry of the array is of the form [part, number],
            where part is a Part and number is the number consumed per minute
        output_rate: float
            The output per minute
        building: str or list of str, optional
            The buildings where this recipe can be made
        '''

        recipe = Recipe(inputs, outputs=[[self, output_rate]], building=building)
        self.recipes.append(recipe)
        return recipe
    
    def get_default_recipe(self):
        if len(self.recipes ) > 0:
            return self.recipes[0]
        else:
            return None

    def __repr__(self) -> str:
        return self.name


class Recipe:

    def __init__(self, inputs, outputs, building):
        '''
        Parameters
        ----------
        
        inputs: Array of shape (n, 2)
            Each entry of the array is of the form [part, number],
            where part is a Part and number is the number consumed per minute
        outputs: Array of shape (n, 2)
            Same as above but with outputs (I think it's usually just one object!)
        building: str or list of str, optional
            The buildings where this recipe can be made'''
        
        self.inputs = inputs
        self.outputs = outputs
        self.building = building
    
    def __repr__(self) -> str:

        if len(self.inputs) > 1:
            output_str = "Inputs:\n"
        else:
            output_str = "Input:\n"
        
        for part, number in self.inputs:
            if number > 1:
                output_str += f"{number:>8}  {part}s\n"
            else:
                output_str += f"{number:>8}  {part}\n"
        
        if len(self.outputs) > 1:
            output_str += "Outputs:\n"
        else:
            output_str += "Output:\n"
        
        for part, number in self.outputs:
            if number > 1:
                output_str += f"{number:>8}  {part}s\n"
            else:
                output_str += f"{number:>8}  {part}\n"
        
        return output_str
