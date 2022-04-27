from argparse import REMAINDER
from ctypes.wintypes import PUSHORT
from pickle import POP

import sly
import re


class TetrisLexer(sly.Lexer):

    tokens = {
        # IMPORT
        IMPORT, GAME,

        ID, NUMBER, STRING_LITERAL,

        # OPERATORS AND MISCELLANEOUS
        ASSIGN, SEPARATOR, EOL,

        # #RELATIONAL OPERATORS
        EE, LTE, GTE, NE, GT, LT,

        # LOGICAL OPERATORS
        AND, OR, NOT,

        # BRACES
        LBLOCKPAREN, RBLOCKPAREN, LCURLYPAREN, RCURLYPAREN,

        # CONDITIONALS AND LOOP STRUCTURES
        IF, ELSE, WHILE, TIMEOUT,

        # DATA TYPES
        INT_TYPE, STRING_TYPE, ARRAY, BOARD, TETRO, 

        # BUILT-IN FUNCTIONS
        GET_BOARD, GET_NAME, GET_NEXT_TETROMINO, SET_SPEED,
        SET_MODE, ROTATE_RIGHT, ROTATE_LEFT, MOVE_RIGHT, MOVE_LEFT,
        HARD_DROP, CHECK_CLEARED_LINE, CLEAR_LINE, GET_CHAR, DISPLAY, DISPLAY_NEXT_TETRO,
        DISPLAY_TETRO, DISPLAY_BOARD, ADD_SCORE, CLEAR_SCREEN,
        PUSH, POP, REM, LEN,MOVE_LEFT,MOVE_RIGHT,ROTATE_LEFT,ROTATE_RIGHT,ADVANCE,PLAY_HW,SET_GAME_DIFFICULTY

        # CONTROL TRANSFER
        BREAK, EXIT,

        # FLAGS
        EASY, MEDIUM, HARD, NORMAL, SPRINT, ARROW_RIGHT,
        SOFT_DROP_FLAG, ARROW_LEFT, CLOCKWISE, ANTI_CLOCKWISE, HARD_DROP_FLAG,

        # NEWLY ADDED
        # THEN, CHECK_LINE, DOWN, SET_DIRECTION, RIGHT
    }

    literals = {'(', ')', '+', '-', '/', '*', '%'}
    # 56
    ignore = ' \t'

    STRING_LITERAL = r'\"(\\.|[^"\\])*\"'

    # Regular expressions for tokens 13+8+10+1+15+7
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ID['getBoard'] = GET_BOARD
    ID['getName'] = GET_NAME
    ID['getNextTetromino'] = GET_NEXT_TETROMINO
    ID['setSpeed'] = SET_SPEED
    # ID['setDirection'] = SET_DIRECTION
    ID['setGameMode'] = SET_MODE
    ID['rotateRight'] = ROTATE_RIGHT
    ID['rotateLeft'] = ROTATE_LEFT
    ID['moveRight'] = MOVE_RIGHT
    ID['moveLeft'] = MOVE_LEFT
    ID['hardDrop'] = HARD_DROP
    ID['checkClearedLine'] = CHECK_CLEARED_LINE
    ID['clearLine'] = CLEAR_LINE
    ID['getCharacter'] = GET_CHAR
    ID['display'] = DISPLAY
    ID['displayUpcomingTetromino'] = DISPLAY_NEXT_TETRO
    ID['displayTetromino'] = DISPLAY_TETRO
    ID['displayBoard'] = DISPLAY_BOARD
    ID['addScore'] = ADD_SCORE
    ID['clearScreen'] = CLEAR_SCREEN
    ID['import'] = IMPORT
    ID['game'] = GAME
    ID['moveLeft'] = MOVE_LEFT
    ID['moveRight'] = MOVE_RIGHT
    ID['rotateLeft']=ROTATE_LEFT
    ID['rotateRight'] = ROTATE_RIGHT
    ID['advance'] = ADVANCE
    ID['playHW'] = PLAY_HW
    ID['setGameDifficulty'] = SET_GAME_DIFFICULTY
    # 13+8+10
    ID['while'] = WHILE
    ID['if'] = IF
    # ID['then'] = THEN
    ID['else'] = ELSE
    ID['timeout'] = TIMEOUT
    # 13+8+5
    ID['int'] = INT_TYPE
    ID['str'] = STRING_TYPE
    ID['tetro'] = TETRO
    ID['board'] = BOARD
    ID['array'] = ARRAY
    # ID['position'] = POSITION

    ID['push'] = PUSH
    ID['pop'] = POP
    ID['rem'] = REM
    ID['len'] = LEN

    ID['break'] = BREAK
    ID['exit'] = EXIT

    ID['and'] = AND
    ID['or'] = OR
    ID['not'] = NOT

    # 13+8
    ID['EASY'] = EASY
    ID['MEDIUM'] = MEDIUM
    ID['HARD'] = HARD
    # ID['DOWN'] = DOWN
    # ID['RIGHT'] = RIGHT
    ID['NORMAL'] = NORMAL
    ID['SPRINT'] = SPRINT
    ID['ARROW_RIGHT'] = ARROW_RIGHT
    ID['ARROW_LEFT'] = ARROW_LEFT
    ID['CLOCKWISE'] = CLOCKWISE
    ID['ANTI_CLOCKWISE'] = ANTI_CLOCKWISE
    ID['HARD_DROP'] = HARD_DROP_FLAG
    ID['SOFT_DROP'] = SOFT_DROP_FLAG

    # 8
    NUMBER = r'[0-9][0-9]*'
    ASSIGN = r'='
    GT = r'>'
    LT = r'<'
    GTE = r'>='
    LTE = r'<='
    EE = r'=='
    NE = r'!='

    # BRACES
    LBLOCKPAREN = r'\['
    RBLOCKPAREN = r'\]'
    LCURLYPAREN = r'\{'
    RCURLYPAREN = r'\}'

    EOL = r';'
    SEPARATOR = r'[,]'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1


if __name__ == '__main__':
    data = '''
    str x = "hey";
    int i = 0;
    while (i < 10) {
        display(x);
        i = i+ 1;
    }
    '''
    lexer = TetrisLexer()
    for tok in lexer.tokenize(data):
        print(tok)

    #tokens: tokens + literals + ignore
    print("Distinct patterns : " + str(len(lexer.tokens) + len(lexer.literals) + 1))
    # token types: token lengths
    print("Distinct token types: " + str(len(lexer.tokens) + len(lexer.literals)))
    # token types are encoded into an enumerated type or a number - 3
    # Token types that are just literals
    print("Number of Token types that are the lexemes themselves: " +
          str(len(lexer.literals)))
