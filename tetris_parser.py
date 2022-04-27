from tetris_lexer import TetrisLexer
from sly import Parser
from game import *
from pieces import *


class TetrisParser(Parser):
    VARIABLE_EXISTS_ERROR = "Variable name already exists, cannot re initialise"
    VARIABLE_MISMATCH_ERROR = "Variable Type mismatch with value"
    VARIABLE_NOT_FOUND_ERROR = "Variable not found"
    debugfile = 'parser1.out'

    # start = 'init_stmt'

    tokens = TetrisLexer.tokens
    literals = TetrisLexer.literals

    var_val_map = {}
    var_type_map = {}

    indentation = ''

    # TODO UTILITY FUNCTIONS
    def pop(self, array_val=None):

        popped = array_val[len(array_val)-1]
        array_val.pop(len(array_val)-1)
        return [array_val, popped]

    def error(self, err, lineno=0):
        print(f"Syntax Error at line {1}: {err}")

    precedence = (
        ('left', OR),
        ('left', AND),
        ('left', NOT),
        ('nonassoc', GT, LT, GTE, LTE, NE, EE),
        ('left', "+", "-"),
        ('left', "*", "/", "%"),
        ('right', UMINUS)
    )



    # compound_stmt
    @_('statement')
    def compound_stmt(self, p):
        return p.statement

    # ask
    @_('compound_stmt all_stmt')
    def compound_stmt(self, p):
        return


    ##(check)
    @_('init_stmt', 'reass_stmt', 'expr', 'birf', 'rem_call','import_stmt')
    def statement(self, p):
        return p[0]

    
    #import stmt

    @_('IMPORT GAME EOL')
    def import_stmt(self, p):
        return "from game import *\nimport curses\nfrom time import time,sleep\nfrom collections import defaultdict\n\n"

    # reass_stmt

    @_('ID ASSIGN val EOL')
    def reass_stmt(self, p):
        if self.var_val_map.get(p.ID) == None:
            self.error(self.VARIABLE_NOT_FOUND_ERROR, p.lineno)
            return self.VARIABLE_NOT_FOUND_ERROR
        else:
            if self.var_type_map[p.ID] == p.val['type']:
                self.var_val_map[p.ID] = p.val['value']
                return f"{p.ID} {p.ASSIGN} {p.val['value']}\n"
            else:
                self.error(self.VARIABLE_MISMATCH_ERROR, p.lineno)
                return self.VARIABLE_MISMATCH_ERROR

    @_('ID ASSIGN array_val EOL')
    def reass_stmt(self, p):
        if self.var_val_map.get(p.ID) == None:
            self.error(self.VARIABLE_NOT_FOUND_ERROR, p.lineno)
            return self.VARIABLE_NOT_FOUND_ERROR
        else:
            if self.var_type_map[p.ID] == 'array':
                self.var_val_map[p.ID] = p.array_val
                return f"{p.ID} {p.ASSIGN} {p.array_val}\n"
            else:
                self.error(self.VARIABLE_MISMATCH_ERROR, p.lineno)
                return self.VARIABLE_MISMATCH_ERROR

    @_('ID ASSIGN expr EOL')
    def reass_stmt(self, p):
        if self.var_val_map.get(p.ID) == None:
            self.error(self.VARIABLE_NOT_FOUND_ERROR, p.lineno)
            return self.VARIABLE_NOT_FOUND_ERROR
        else:
            if self.var_type_map[p.ID] == 'int':
                self.var_val_map[p.ID] = p.expr
                return f"{p.ID} {p.ASSIGN} {p.expr}\n"
            else:
                self.error(self.VARIABLE_MISMATCH_ERROR, p.lineno)
                return self.VARIABLE_MISMATCH_ERROR

    # INITIALISATION  & RE-ASSIGNMENT STATEMENT GRAMMAR

    @_('data_type ID ASSIGN val EOL')
    def init_stmt(self, p):
        if self.var_val_map.get(p.ID) is not None:
            self.error(self.VARIABLE_EXISTS_ERROR, p.lineno)
            return self.VARIABLE_EXISTS_ERROR
        else:
            if p.data_type == p.val['type']:
                self.var_val_map[p.ID] = p.val['value']
                self.var_type_map[p.ID] = p.data_type
                return f"{p.ID} {p.ASSIGN} {p.val['value']}\n"
            else:
                self.error(self.VARIABLE_MISMATCH_ERROR, p.lineno)
                return self.VARIABLE_MISMATCH_ERROR

    @_('data_type ID ASSIGN expr EOL')
    def init_stmt(self, p):
        if self.var_val_map.get(p.ID) is not None:
            self.error(self.VARIABLE_EXISTS_ERROR, p.lineno)
            return self.VARIABLE_EXISTS_ERROR
        else:
            if p.data_type == 'int':
                self.var_val_map[p.ID] = p.expr
                self.var_type_map[p.ID] = p.data_type
                return f"{p.ID} {p.ASSIGN} {p.expr}\n"
            else:
                self.error(self.VARIABLE_MISMATCH_ERROR, p.lineno)
                return self.VARIABLE_MISMATCH_ERROR

    @_('ARRAY ID ASSIGN array_val EOL')
    def init_stmt(self, p):
        if self.var_val_map.get(p.ID) is not None:
            self.error(self.VARIABLE_EXISTS_ERROR, p.lineno)
            return self.VARIABLE_EXISTS_ERROR
        else:
            self.var_val_map[p.ID] = p.array_val
            self.var_type_map[p.ID] = p.ARRAY
            return f"{p.ID} {p.ASSIGN} {p.array_val}\n"

    # data_type

    @_('INT_TYPE')
    def data_type(self, p):
        return p.INT_TYPE

    @_('STRING_TYPE')
    def data_type(self, p):
        return p.STRING_TYPE

    @_('ARRAY')
    def data_type(self, p):
        return p.ARRAY

    @_('BOARD')
    def data_type(self, p):
        return p.BOARD

    @_('TETRO')
    def data_type(self, p):
        return p.TETRO

    # array_val
    @_('LBLOCKPAREN RBLOCKPAREN')
    def array_val(self, p):
        return []

    @_('LBLOCKPAREN set RBLOCKPAREN')
    def array_val(self, p):
        return p.set

    # set(check)
    @_('val')
    def set(self, p):
        vals = [p.val['value']]
        return vals

    @_('set SEPARATOR val')
    def set(self, p):
        p.set.append(p.val['value'])

        return p.set

    # val(define birf)
    @_('NUMBER')
    def val(self, p):
        number = {}
        number['type'] = 'int'
        number['value'] = p.NUMBER
        return number

    @_('STRING_LITERAL')
    def val(self, p):
        number = {}
        number['type'] = 'str'
        number['value'] = p.STRING_LITERAL
        return number

    @_(' "-" factor %prec UMINUS')
    def expr(self, p):
        return -p.factor

    @_(' factor ')
    def expr(self, p):
        return p.factor

    # @_(' factor_ws ')
    # def term(self,p):
    #     return p.factor_ws

    @_(' expr "*" expr ')
    def expr(self, p):
        return int(p.expr0)*int(p.expr1)

    @_(' expr "/" expr ')
    def expr(self, p):
        if int(p.expr1) != 0:
            return int(p.expr0)/int(p.expr1)
        else:
            self.error("Divide by zero error", p.lineno)

    @_(' expr "%" expr ')
    def expr(self, p):
        if int(p.expr1) != 0:
            return int(p.expr0) % int(p.expr1)
        else:
            self.error("Modulus by zero error", p.lineno)

    # @_(' term ')
    # def sums(self,p):
    #     return p.term

    @_(' expr "+" expr ')
    def expr(self, p):
        return int(p.expr0)+int(p.expr1)

    @_(' expr "-" expr ')
    def expr(self, p):
        return int(p.expr0)-int(p.expr1)

    @_(' expr GT expr ')
    def expr(self, p):
        if int(p.expr0) > int(p.expr1):
            return 1
        else:
            return 0

    @_(' expr LT expr ')
    def expr(self, p):
        if int(p.expr0) < int(p.expr1):
            return 1
        else:
            return 0

    @_(' expr LTE expr ')
    def expr(self, p):
        if int(p.expr0) <= int(p.expr1):
            return 1
        else:
            return 0

    @_(' expr GTE expr ')
    def expr(self, p):
        if int(p.expr0) >= int(p.expr1):
            return 1
        else:
            return 0

    @_(' expr NE expr ')
    def expr(self, p):
        if int(p.expr0) != int(p.expr1):
            return 1
        else:
            return 0

    @_(' expr EE expr ')
    def expr(self, p):
        if int(p.expr0) == int(p.expr1):
            return 1
        else:
            return 0

    @_(' NOT expr ')
    def expr(self, p):
        if int(p.expr) > 0:
            return 1
        else:
            return 0

    @_(' expr AND expr ')
    def expr(self, p):
        if int(p.expr0) > 0 and int(p.expr1) > 0:
            return 1
        else:
            return 0

    @_(' expr OR expr ')
    def expr(self, p):
        if int(p.expr0) > 0 or int(p.expr1) > 0:
            return 1
        else:
            return 0

    @_('operand')
    def factor(self, p):
        return p.operand

    @_(' "(" expr ")" ')
    def factor(self, p):
        return p.expr

    @_('ID')
    def operand(self, p):
        if self.var_type_map[p.ID] == 'int':
            return self.var_val_map[p.ID]
        else:
            self.error('This type cannot be in an expression', p.lineno)

    @_('NUMBER')
    def operand(self, p):
        return p.NUMBER

    # INITIALISATION  & RE-ASSIGNMENT STATEMENT GRAMMAR

    # @_('birf')
    # def val(self, p):
    #     return p.birf

    # init_stmt

    # FUNCTION STATEMENT GRAMMAR

    # params(ask)

    @_(' param ')
    def params(self, p):
        parameters = [p.param]
        return parameters

    @_('params SEPARATOR param')
    def params(self, p):
        p.params.append(p.param)
        return p.params

    # param

    @_('ID')
    def param(self, p):
        if self.var_val_map.get(p.ID) == None:
            self.error(self.VARIABLE_NOT_FOUND_ERROR, p.lineno)
            return self.VARIABLE_NOT_FOUND_ERROR

        number = {}
        number['type'] = self.var_type_map[p.ID]
        number['value'] = self.var_val_map[p.ID]
        return number

    @_('val')
    def param(self, p):
        return p.val

    # birf_wop

    @_('GET_NEXT_TETROMINO')
    def birf_wop(self, p):
        return p.GET_NEXT_TETROMINO

    @_('GET_BOARD')
    def birf_wop(self, p):
        return p.GET_BOARD

    @_('GET_CHAR')
    def birf_wop(self, p):
        return p.GET_CHAR

    # birf_wop_call

    @_('birf_wop "(" ")" ')
    def birf_wop_call(self, p):
        if p.birf_wop == 'getNextTetromino':
            return {'type':'tetro','value':f"getNextTetromino()"}

        elif p.birf_wop == 'getBoard':
           
            return {'type':'board','value':f"getBoard(stdscr)"}

        elif p.birf_wop == 'getChar':
            return {'type':'string','value':f"getChar(stdscr)"}
            # else:
            #     return {'type': 'err', 'value': ' getBoard: Params format mismatch'}

        
        # elif p.birf_wop == 'getChar':
        #     return {'type': 'str', 'value': self.getChar()}

    # birf_wp

    @_('CHECK_CLEARED_LINE')
    def birf_wp(self, p):
        return p.CHECK_CLEARED_LINE

    @_('MOVE_LEFT')
    def birf_wp(self, p):
        return p.MOVE_LEFT
    @_('MOVE_RIGHT')  
    def birf_wp(self, p):
        return p.MOVE_RIGHT

    @_('ROTATE_RIGHT')
    def birf_wp(self, p):
        return p.ROTATE_RIGHT
    
    @_('ROTATE_LEFT')
    def birf_wp(self, p):
        return p.ROTATE_LEFT
    
    @_('ADVANCE')
    def birf_wp(self, p):
        return p.ADVANCE
    

    # pop_call
    @_('POP "(" ID ")"')
    def pop_call(self, p):
        # Check if ID is array or no in the self.pop function only.
        if self.var_type_map[p.ID] == 'array':
            retval = self.pop(self.var_val_map[p.ID])
            self.var_val_map[p.ID] = retval[0]
            return {'type': 'int', 'value': retval[1]}
        else:
            self.error("Pop expected an array identifier", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}

    @_('POP "(" array_val ")"')
    def pop_call(self, p):
        return {'type': 'int', 'value': self.pop(p.array_val)[1]}

    # len_call(define self.len function)
    @_('LEN "(" ID ")"')
    def len_call(self, p):
        if self.var_type_map[p.ID] == 'array':

            return {'type': 'int', 'value': len(self.var_val_map[p.ID])}
        else:
            self.error("Pop expected an array identifier", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}

    @_('LEN "(" array_val ")"')
    def len_call(self, p):
        return {'type': 'int', 'value': len(p.array_val)}

    # birf_wp_call
    @_('birf_wp "(" params ")" ')
    def birf_wp_call(self, p):

        if p.birf_wp == 'checkClearedLine':
            if len(p.params) == 1 and p.params[0]['type'] == 'int':
                # clearedLine = checkClearedLines([p.params[0]['value']])

                return {'type': 'int', 'value': f"len(checkClearedLines([{p.params[0]['value']}]))"}
            else:
                return {'type': 'err', 'value': ' checkClearedLine: Params format mismatch'}
        elif p.birf_wp == 'moveLeft':
            if len(p.params) == 1 and p.params[0]['type'] == 'array':
                return {'type': 'array', 'value': f"moveLeft({p.params[0]['value']})"}
            else:
                return {'type': 'err', 'value': ' moveLeft: Params format mismatch'}
        elif p.birf_wp == 'moveRight' and p.params[0]['type'] == 'array':
            if len(p.params) == 1:
                return {'type': 'array', 'value': f"moveRight({p.params[0]['value']})"}
            else:
                return {'type': 'err', 'value': ' moveRight: Params format mismatch'}
        elif p.birf_wp == 'rotateRight':
            if len(p.params) == 1 and p.params[0]['type'] == 'array':
                return {'type': 'array', 'value': f"rotateRight({p.params[0]['value']})"}
            else:
                return {'type': 'err', 'value': ' rotateRight: Params format mismatch'}
        elif p.birf_wp == 'rotateLeft':
            if len(p.params) == 1 and p.params[0]['type'] == 'array':
                return {'type': 'array', 'value': f"rotateLeft({p.params[0]['value']})"}
            else:
                return {'type': 'err', 'value': ' rotateLeft: Params format mismatch'}
        elif p.birf_wp == 'advance':
            if len(p.params) == 1 and p.params[0]['type'] == 'array':
                return {'type': 'array', 'value': f"advance({p.params[0]['value']})"}
            else:
                return {'type': 'err', 'value': ' advance: Params format mismatch'}

    @_('pop_call')
    def birf_wp_call(self, p):
        return p.pop_call

    @_('len_call')
    def birf_wp_call(self, p):
        return p.len_call

    # @_('ID LBLOCKPAREN NUMBER RBLOCKPAREN')
    # def birf_wp_call(self,p):

    @_('birf_wop_call')
    def birf(self, p):
        return p.birf_wop_call

    @_('birf_wp_call')
    def birf(self, p):
        return p.birf_wp_call

    # Void functions

    # bivf_wop

    

    @_('GET_NAME')
    def bivf_wop(self, p):
        return p.GET_NAME

    @_('DISPLAY_BOARD')
    def bivf_wop(self, p):
        return p.DISPLAY_BOARD

    @_('CLEAR_SCREEN')
    def bivf_wop(self, p):
        return p.CLEAR_SCREEN
    
    @_('PLAY_HW')
    def bivf_wop(self, p):
        return p.PLAY_HW

    @_('SET_GAME_DIFFICULTY')
    def bivf_wop(self, p):
        return p.SET_GAME_DIFFICULTY

    @_('SET_MODE')
    def bivf_wop(self, p):
        return p.SET_MODE
    # bivf_wp

    @_('HARD_DROP')
    def bivf_wp(self, p):
        return p.HARD_DROP

    @_('CLEAR_LINE')
    def bivf_wp(self, p):
        return p.CLEAR_LINE

    @_('DISPLAY')
    def bivf_wp(self, p):
        return p.DISPLAY

    @_('DISPLAY_TETRO')
    def bivf_wp(self, p):
        return p.DISPLAY_TETRO

    @_('DISPLAY_NEXT_TETRO')
    def bivf_wp(self, p):
        return p.DISPLAY_NEXT_TETRO

    @_('ADD_SCORE')
    def bivf_wp(self, p):
        return p.ADD_SCORE

    @_('REM')
    def bivf_wp(self, p):
        return p.REM

    @_('PUSH')
    def bivf_wp(self, p):
        return p.PUSH

    # set_speed_call
    @_('SET_SPEED "(" EASY ")"')
    def set_speed_call(self, p):
        return f"setSpeed({p.EASY})"

    @_('SET_SPEED "(" MEDIUM ")"')
    def set_speed_call(self, p):
        return f"setSpeed({p.MEDIUM})"

    @_('SET_SPEED "(" HARD ")"')
    def set_speed_call(self, p):
        return f"setSpeed({p.HARD})"


    # rem_call
    @_('REM "(" array_val SEPARATOR NUMBER ")"')
    def rem_call(self, p):
        if len(p.array_val) == 0:
            self.error("Array should not be empty", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        deleted = p.array_val[p.NUMBER]
        del p.array_val[p.NUMBER]
        return {'type': 'int', 'value': 1}

    @_('REM "(" array_val SEPARATOR ID ")"')
    def rem_call(self, p):
        if len(p.array_val) == 0:
            self.error("Array should not be empty", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        if p.ID not in self.var_val_map:
            self.error(f"Variable {p.ID} not declared ", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        if self.var_type_map[p.ID] != 'int':
            self.error(f"Variable {p.ID} not declared ", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        if self.var_type_map[p.ID] > len(p.array_val):
            self.error(
                f"Index {self.var_type_map[p.ID]['value']} out of bounds", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        deleted = p.array_val[self.var_val_map[p.ID]['value']]
        del p.array_val[self.var_val_map[p.ID]['value']]
        return {'type': 'int', 'value': 1}

    @_('REM "(" ID SEPARATOR NUMBER ")"')
    def rem_call(self, p):
        if len(p.ID) == 0:
            self.error("Array should not be empty", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        if p.ID not in self.var_val_map:
            self.error(f"Variable {p.ID} not declared ", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        if self.var_type_map[p.ID] != 'array':
            self.error(f"Variable {p.ID} not declared ", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        deleted = self.var_val_map[p.ID][p.NUMBER]
        del self.var_val_map[p.ID][p.NUMBER]
        return {'type': 'int', 'value': 1}

    @_('REM "(" ID SEPARATOR ID ")"')
    def rem_call(self, p):
        if len(p.ID0) == 0:
            self.error("Array should not be empty", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        if p.ID1 not in self.var_val_map:
            self.error(f"Variable {p.ID1} not declared ", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        if self.var_type_map[p.ID1] != 'int':
            self.error(f"Variable {p.ID1} not declared ", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        if self.var_val_map[p.ID1] >= len(self.var_val_map[p.ID0]):
            self.error(
                f"Index {self.var_type_map[p.ID1]['value']} out of bounds", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        if p.ID0 not in self.var_val_map:
            self.error(f"Variable {p.ID0} not declared ", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        if self.var_type_map[p.ID0] != 'array':
            self.error(f"Variable {p.ID0} not declared ", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        deleted = self.var_val_map[p.ID0][p.ID1]
        del self.var_val_map[p.ID0][p.ID1]
        return {'type': 'int', 'value': 1}

    @_('PUSH "(" ID SEPARATOR val ")"')
    def push_call(self, p):
        if p.ID not in self.var_val_map:
            self.error(f"Variable {p.ID} not declared ", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        if self.var_type_map[p.ID] != 'array':
            self.error(f"Variable {p.ID} not declared ", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        self.var_val_map[p.ID].append(p.val['value'])
        return {'type': 'int', 'value': 1}

    @_('PUSH "(" ID SEPARATOR ID ")"')
    def push_call(self, p):
        if p.ID1 not in self.var_val_map:
            self.error(f"Variable {p.ID1} not declared ", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        if self.var_type_map[p.ID1] == 'array':
            self.error(f"Variable {p.ID1} cannot be appended to array ", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        if p.ID0 not in self.var_val_map:
            self.error(f"Variable {p.ID0} not declared ", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        if self.var_type_map[p.ID0] != 'array':
            self.error(f"Variable {p.ID0} not declared ", p.lineno)
            return {'type': 'err', 'value': 'Type mismatch'}
        self.var_val_map[p.ID0].append(self.var_val_map[p.ID1])
        return {'type': 'int', 'value': 1}

    ## bivf_wop_call
    @_('bivf_wop "(" ")"')
    def bivf_wop_call(self, p):
        if(p.bivf_wop == 'clearScreen'):
            return f"endAnimation(stdscr)"
        elif (p.bivf_wop == 'displayBoard'):
            return f"displayBoard()"
        elif (p.bivf_wop == 'getName'):
            return f"getName()"
        elif (p.bivf_wop == 'playHW'):
            return f"playHW()"
        elif (p.bivf_wop == 'setGameDifficulty'):
            return f"setGameDifficulty()"
        elif (p.bivf_wop == 'setGameMode'):
            return f"setGameMode()"

    ## bivf_wp_call
    @_('bivf_wp "(" params ")"')
    def bivf_wp_call(self,p):
        if p.bivf_wp=='hardDrop':
            if len(p.params)==2 and p.params[0]['type']=='tetro' and p.params[1]['type']=='board':
                return f"hardDrop({p.params[0]['value']}, {p.params[1]['value']})"
            else:
                return {'type': 'err', 'value': ' hardDrop: Params format mismatch'}
        elif p.bivf_wp == 'clearLine':
            if len(p.params)==2 and p.params[0]['type']=='int' and p.params[1]['type']=='board':
                return f"clearLine({p.params[0]['value']}, {p.params[1]['value']})"
            else:
                return {'type': 'err', 'value': ' clearLine: Params format mismatch'}
            

        
           
    # Jump Statement Grammar

    # break statement

    @_('BREAK EOL')
    def break_stmt(self, p):
        return f"{p.BREAK} \n"

    # exit statement(find)
    @_('EXIT EOL')
    def exit_stmt(self, p):
        pass

    # Compound Statements
    # all_stmt
    @_('init_stmt')
    def all_stmt(self, p):
        return p.init_stmt

    @_('reass_stmt')
    def all_stmt(self, p):
        return p.reass_stmt

    @_('break_stmt')
    def all_stmt(self, p):
        return p.break_stmt

    @_('exit_stmt')
    def all_stmt(self, p):
        return p.exit_stmt

    # @_('bivf')
    # def all_stmt(self,p):
    #     return p.bivf

    @_('if_else')
    def all_stmt(self, p):
        return p.if_else

    # @_('while_loop')
    # def all_stmt(self,p):
    #     return p.while_loop

    # ###check timeoout loop
    # @_('timeout_loop')
    # def all_stmt(self,p):
    #     return p.timeout_loop



    # Conditional Grammar

    # empty

    @_('')
    def empty(self, p):
        pass

    # if_stmt(big confusion)
    @_('IF "(" expr ")" LCURLYPAREN compound_stmt RCURLYPAREN')
    def if_stmt(self, p):
        if p.expr:
            return p.compound_stmt
        else:
            return "No"

    # else_stmt
    @_('IF "(" expr ")" LCURLYPAREN compound_stmt RCURLYPAREN ELSE LCURLYPAREN compound_stmt RCURLYPAREN')
    def if_else_stmt(self, p):
        if p.expr>0:
            return p.compound_stmt0
        else:
            return p.compound_stmt1

    @_('IF "(" expr ")" LCURLYPAREN compound_stmt RCURLYPAREN ELSE if_stmt')
    def if_elseif_stmt(self, p):
        if p.expr>0:
            return p.compound_stmt0
        else:
            return p.if_stmt

    @_('IF "(" expr ")" LCURLYPAREN compound_stmt RCURLYPAREN ELSE if_else_stmt')
    def if_elseif_stmt(self, p):
        if p.expr > 0:
            return p.compound_stmt0
        else:
            return p.if_else_stmt


    @_('empty')
    def else_stmt(self, p):
        return p.empty

    # if_else

    @_('if_stmt else_stmt')
    def if_else(self, p):
        pass
    
    

    @_('SOFT_DROP_FLAG')
    def soft_drop(self,p):
        return "curses.KEY_DOWN"

    @_('HARD_DROP_FLAG')
    def hard_drop(self,p):
        return "ord(' ')"

    @_('ARROW_RIGHT')
    def arrow_right(self,p):
        return "curses.KEY_RIGHT"

    @_('ARROW_LEFT')
    def arrow_left(self, p):
        return "curses.KEY_LEFT"
        
    @_('CLOCKWISE')
    def clockwise(self,p):
        return "ord('a')"

    @_('ANTI_CLOCKWISE')
    def anticlockwise(self, p):
        return "ord('d')"



if __name__ == "__main__":
    lexer = TetrisLexer()
    parser = TetrisParser()

    while True:
        try:
            text = input('tetris > ')
            tokens = lexer.tokenize(text)
            print(tokens)
            result = parser.parse(tokens)
            print(result)
        except EOFError:
            break
