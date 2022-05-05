"""
Utility function to generate the string that will then be called as python code.
Test cases:
["a = []", ["b = {}"]]

"""

class ProgramGenerator:

    def __init__(self) -> None:
        self.program_variable = ""
    
    
    def printProgram(self, arr):
        self.getProgram(arr)
        print(self.program_variable)

 
    def getProgram(self, arr = None, current_level = 0):
        if arr == None:
            return
        for element in arr:
            # print(type(element))
            if isinstance(element, list):
                self.getProgram(element, current_level + 1)
            elif isinstance(element, str):
                # print("String found : " + element)
                # print("Level : " + str(current_level))
                for _ in range(1,current_level):
                    self.program_variable += '    '
                self.program_variable += element
                self.program_variable += '\n'

        
        

arr = [["a = 3"], ["if a == 3:", ["print(a)"]]]    
ProgramGenerator().printProgram(arr)

    