from game import *
from tetris_lexer import *
from tetris_parser import *
import glob

def main():
    print("_____RUNNING ALL TESTS_____")
    #just for testing.
    # while True:
    #     try:
    #         text = input('tetris > ')
    #         tokens = lexer.tokenize(text)
    #         print(tokens)
    #         result = parser.parse(tokens)
    #         print(result)
    #     except EOFError:
    #         break
    for i in glob.glob("./tests/*"):
        lexer = TetrisLexer()
        parser = TetrisParser()
        print("\n\n____IN TEST: " + i.split('/')[-1].split('.')[0].upper()+ "____")
        data = open(i, 'r').read()
        tokens = lexer.tokenize(data)
        result = parser.parse(tokens)
        print(result)
        print("_____END____" + i.split('/')[-1].split('.')[0].upper()+ "____")


    print("_____TESTS COMPLETE_____\n\n")
if __name__ == "__main__":
    main()