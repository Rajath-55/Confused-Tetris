from tetris_lexer import TetrisLexer
from sly import Parser
from game import *
from pieces import *

class TetrisParser(Parser):
    VARIABLE_EXISTS_ERROR = "Variable name already exists, cannot re initialise"
    debugfile = 'parser.out'

    tokens = TetrisLexer.tokens
    literals = TetrisLexer.literals

    var_val_map = {}
    var_type_map = {}

    #TODO UTILITY FUNCTIONS
    def pop(self, ID = None, array_val = None):
        #TODO CHECK THIS FUNCTION
        if ID in self.symbol_table:
            return self.symbol_table.pop(ID)
        else:
            #TODO Error function check
            return None

    def error(self,err):
        print(f"Syntax Error: {err}")

    

    precedence = (
        ('left', OR),
        ('left', AND),
        ('left', NOT),
        ('nonassoc', GT, LT, GTE, LTE, NE, EE ),
        ('left', "+", "-"),
        ('left', "*", "/", "%"),
        ('right', UMINUS)
    )

    @_('ID')
    def operand(self,p):
        if self.var_type_map[p.ID] == 'int':
            return self.var_val_map[p.ID]
        else:
            self.error('This type cannot be in an expression')

    @_('NUMBER')
    def operand(self,p):
        return p.NUMBER

    @_('operand')
    def factor(self,p):
        return p.operand

    @_(' "(" expr ")" ')
    def factor(self,p):
        return p.expr

    @_(' "-" factor %prec UMINUS')
    def expr(self,p):
        return -p.factor

    @_(' factor ')
    def expr(self,p):
        return p.factor

    # @_(' factor_ws ')
    # def term(self,p):
    #     return p.factor_ws

    @_(' expr "*" expr ')
    def expr(self,p):
        return p.expr0*p.expr1

    @_(' expr "/" expr ')
    def expr(self,p):
        if p.expr1 != 0:
            return p.expr0/p.expr1
        else:
           self.error("Divide by zero error")

    @_(' expr "%" expr ')
    def expr(self,p):
        if p.expr1 != 0:
            return p.expr0%p.expr1
        else:
            self.error("Modulus by zero error")


    # @_(' term ')
    # def sums(self,p):
    #     return p.term

    @_(' expr "+" expr ')
    def expr(self,p):
        return p.expr0+p.expr1

    @_(' expr "-" expr ')
    def expr(self,p):
        return p.expr0-p.expr1

    @_(' expr GT expr ')
    def expr(self,p):
        if p.expr0>p.expr1:
            return 1
        else:
            return 0

    @_(' expr LT expr ')
    def expr(self,p):
        if p.expr0<p.expr1:
            return 1
        else:
            return 0

    @_(' expr LTE expr ')
    def expr(self,p):
        if p.expr0<=p.expr1:
            return 1
        else:
            return 0

    @_(' expr GTE expr ')
    def expr(self,p):
        if p.expr0>=p.expr1:
            return 1
        else:
            return 0

    @_(' expr NE expr ')
    def expr(self,p):
        if p.expr0!=p.expr1:
            return 1
        else:
            return 0

    @_(' expr EE expr ')
    def expr(self,p):
        if p.expr0==p.expr1:
            return 1
        else:
            return 0

    @_(' NOT expr ')
    def expr(self,p):
        if p.expr>0:
            return 1
        else:
            return 0

    @_(' expr AND expr ')
    def expr(self,p):
        if p.expr0>0 and p.expr1>0:
            return 1
        else:
            return 0

    @_(' expr OR expr ')
    def expr(self,p):
        if p.expr0>0 or p.expr1>0:
            return 1
        else:
            return 0

    # INITIALISATION  & RE-ASSIGNMENT STATEMENT GRAMMAR

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

    # @_('birf')
    # def val(self, p):
    #     return p.birf

    # set(check)
    @_('val')
    def set(self, p):
        vals = [p.val]
        return vals

    @_('set SEPARATOR val')
    def set(self, p):
        p.set.append(p.val)
        
        return p.set

    # array_val
    @_('LBLOCKPAREN RBLOCKPAREN')
    def array_val(self, p):
        return []

    @_('LBLOCKPAREN set RBLOCKPAREN')
    def array_val(self, p):
        return p.set

    # init_stmt
    @_('data_type ID ASSIGN val EOL')
    def init_stmt(self, p):
        if self.var_val_map.get(p.ID) is not None:
            self.error(self.VARIABLE_EXISTS_ERROR)
            return self.VARIABLE_EXISTS_ERROR
        else:
            if p.data_type == p.val['type']:
                self.var_val_map[p.ID] = p.val['value']
                self.var_type_map[p.ID] = p.data_type
                return (p.ID, p.ASSIGN, p.val['value'])
            else:
                self.error("Variable Type mismatch with value")
                return "Variable Type mismatch with value"

    @_('data_type ID ASSIGN expr EOL')
    def init_stmt(self, p):
        if self.var_val_map.get(p.ID) is not None:
            self.error(self.VARIABLE_EXISTS_ERROR)
            return self.VARIABLE_EXISTS_ERROR
        else:
            if p.data_type == 'int':
                self.var_val_map[p.ID] = p.expr
                self.var_type_map[p.ID] = p.data_type
                return (p.ID, p.ASSIGN, p.expr)
            else:
                self.error(" Variable Type mismatch with value")
                return "Variable Type mismatch with value"

    @_('ARRAY ID ASSIGN array_val EOL')
    def init_stmt(self, p):
        if self.var_val_map.get(p.ID) is not None:
            self.error(self.VARIABLE_EXISTS_ERROR)
            return self.VARIABLE_EXISTS_ERROR
        else:
            self.var_val_map[p.ID] = p.array_val
            self.var_type_map[p.ID] = p.ARRAY
            return (p.ID, p.ASSIGN, p.array_val)

    # reass_stmt
    @_('ID ASSIGN val EOL')
    def reass_stmt(self, p):
        if self.var_val_map.get(p.ID) == None:
            self.error(" Variable not found")
            return "Variable not found"
        else:
            if self.var_type_map[p.ID] == p.val['type']:
                self.var_val_map[p.ID] = p.val['value']
                return (p.ID, p.ASSIGN, p.val['value'])
            else:
                self.error(" Variable Type mismatch with value")
                return "Variable Type mismatch with value"

    @_('ID ASSIGN array_val EOL')
    def reass_stmt(self, p):
        if self.var_val_map.get(p.ID) == None:
            self.error(" Variable not found")
            return "Variable not found"
        else:
            if self.var_type_map[p.ID] == 'array':
                self.var_val_map[p.ID] = p.array_val
                return (p.ID, p.ASSIGN, p.array_val)
            else:
                self.error(" Variable Type mismatch with value")
                return "Variable Type mismatch with value"

    @_('ID ASSIGN expr EOL')
    def reass_stmt(self, p):
        if self.var_val_map.get(p.ID) == None:
           self.error(" Variable not found")
           return "Variable not found"
        else:
            if self.var_type_map[p.ID] == 'int':
                self.var_val_map[p.ID] = p.expr
                return (p.ID, p.ASSIGN, p.expr)
            else:
                self.error(" Variable Type mismatch with value")
                return "Variable Type mismatch with value"

    #FUNCTION STATEMENT GRAMMAR

    ##param
    @_('ID')
    def param(self,p):
        if self.var_val_map.get(p.ID) == None:
            self.error(" Variable not found")
            return "Variable not found"

        number={}
        number['type'] = var_type_map[p.ID]
        number['value'] = var_val_map[p.ID]
        return number
    
    @_('val')
    def param(self,p):
        return p.val

    ##params(ask)

    @_(' param ')
    def params(self,p):
        parameters = [p.param]
        return parameters

    @_('params SEPARATOR param')
    def params(self,p):
        p.params.append(p.param)
        return p.params

    ##birf_wop

    @_('GET_NAME')
    def birf_wop(self,p):
        return p.GET_NAME

    @_('GET_NEXT_TETROMINO')
    def birf_wop(self,p):
        return p.GET_NEXT_TETROMINO

    @_('GET_CHAR')
    def birf_wop(self,p):
        return p.GET_CHAR

    ##birf_wop_call

    @_('birf_wop "(" ")" ')
    def birf_wop_call(self,p):
        if p.birf_wop == 'getName':
            return {'type':'str', 'value': self.getName()}
        elif p.birf_wop == 'getNextTetromino':
            return {'type':'tetro', 'value': self.getNextTetromino()}
        elif p.birf_wop == 'getChar':
            return {'type':'str', 'value': self.getChar()}
    
    
    ##birf_wp

    @_('GET_BOARD')
    def birf_wp(self,p):
        return p.GET_BOARD

    @_('CHECK_CLEARED_LINE')
    def birf_wp(self,p):
        return p.CHECK_CLEARED_LINE

    ##pop_call
    @_('POP "(" ID ")"')
    def pop_call(self,p):
        #Check if ID is array or no in the self.pop function only.
        return self.pop(p.ID)

    @_('POP "(" array_val ")"')
    def pop_call(self,p):
        return self.pop(p.array_val)

    
if __name__ == "__main__":
    lexer = TetrisLexer()
    parser = TetrisParser()

    while True:
        try:
            text = input('tetris > ')
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except EOFError:
            break