from game import *
from tetris_lexer import *
from tetris_parser import *


def main():
    data = '''
    str x = "hey";
    int i = 0;
    while (i < 10) {
        display(x);
        i = i+ 1;
    }
    '''
    
    lexer = TetrisLexer()
    parser = TetrisParser()

    # while True:
    #     try:
    #         text = input('tetris > ')
    #         tokens = lexer.tokenize(text)
    #         print(tokens)
    #         result = parser.parse(tokens)
    #         print(result)
    #     except EOFError:
    #         break

    tokens = lexer.tokenize(data)
    result = parser.parse(tokens)
    print(result)

    