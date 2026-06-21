from aergia.lexer import tokenize
from aergia.parser import parse
from aergia.nodes import *

def get_ast(code):
    """Helper to bypass boilerplate and return the parsed AST."""
    return parse(tokenize(code))

def test_parse_literals_and_variables():
    ast = get_ast('42 "string" x')
    
    assert len(ast) == 3
    assert isinstance(ast[0], LiteralNode)
    assert ast[0].value == 42
    
    assert isinstance(ast[1], LiteralNode)
    assert ast[1].value == "string"
    
    assert isinstance(ast[2], VariableNode)
    assert ast[2].name == 'x'

def test_parse_assignment():
    ast = get_ast('= x 10')
    
    assert len(ast) == 1
    node = ast[0]
    assert isinstance(node, AssignNode)
    assert node.name == 'x'
    assert isinstance(node.child, LiteralNode)
    assert node.child.value == 10

def test_parse_binary_op_assignment():
    ast = get_ast('= x +y 10')
    
    assert len(ast) == 1
    node = ast[0]
    assert isinstance(node, AssignNode)
    assert node.name == 'x'
    
    # Should wrap the assignment in a BinaryOpNode
    assert isinstance(node.child, BinaryOpNode)
    assert node.child.op == '+'
    assert isinstance(node.child.left, VariableNode)
    assert node.child.left.name == 'y'

def test_parse_prefix_math():
    ast = get_ast('+5 *2 3')
    
    node = ast[0]
    assert isinstance(node, BinaryOpNode)
    assert node.op == '+'
    assert node.left.value == 5
    
    # Right child should be the nested multiplication
    assert isinstance(node.right, BinaryOpNode)
    assert node.right.op == '*'
    assert node.right.left.value == 2
    assert node.right.right.value == 3

def test_parse_arrays():
    ast = get_ast('< 1 2 3 >')
    
    node = ast[0]
    assert isinstance(node, ArrayNode)
    assert len(node.elements) == 3
    assert node.elements[0].value == 1
    assert node.elements[2].value == 3

def test_parse_array_operations():
    ast = get_ast('+: arr 4')
    
    node = ast[0]
    assert isinstance(node, PushNode)
    assert isinstance(node.arrayn, VariableNode)
    assert node.arrayn.name == 'arr'
    assert isinstance(node.itemn, LiteralNode)
    assert node.itemn.value == 4

def test_parse_if_else_block():
    code = '(== x 1 > "true") -> (> "false")'
    ast = get_ast(code)
    
    node = ast[0]
    assert isinstance(node, IfNode)
    assert isinstance(node.cond, BinaryOpNode)
    
    # Check main body
    assert len(node.mainbody) == 1
    assert isinstance(node.mainbody[0], OutputNode)
    
    # Check else body
    assert len(node.elsebody) == 1
    assert isinstance(node.elsebody[0], OutputNode)

def test_parse_while_loop():
    code = '[<< x 10 =+ x 1]'
    ast = get_ast(code)
    
    node = ast[0]
    assert isinstance(node, WhileNode)
    assert isinstance(node.cond, BinaryOpNode)
    assert node.cond.op == '<<'
    assert len(node.body) == 1
    assert isinstance(node.body[0], AssignNode)

def test_parse_for_loop():
    code = '[`arr item > item]'
    ast = get_ast(code)
    
    node = ast[0]
    assert isinstance(node, ForNode)
    assert isinstance(node.array, VariableNode)
    assert node.array.name == 'arr'
    assert node.iname == 'item'
    assert len(node.body) == 1

def test_parse_function_definition_and_call():
    code = """
    {add :a b: 
        ? +a b 
    }
    @add:5 10:
    """
    ast = get_ast(code)
    
    # Test Function Node
    func_node = ast[0]
    assert isinstance(func_node, FunctionNode)
    assert func_node.name == 'add'
    assert func_node.para == ['a', 'b']
    
    # Test Call Node
    call_node = ast[1]
    assert isinstance(call_node, CallNode)
    assert isinstance(call_node.target, VariableNode)
    assert call_node.target.name == 'add'
    assert len(call_node.args) == 2
    
def test_parse_string_escape_sequences():
    """Checks that string escape transformations evaluate to true control sequences."""
    ast = get_ast('"line1\\nline2\\tends"')
    node = ast[0]
    
    assert isinstance(node, LiteralNode)
    assert "\n" in node.value
    assert "\t" in node.value
    assert "\\" not in node.value

def test_parse_deeply_nested_prefix_math():
    """Tests an expansive prefix evaluation branch tree to ensure proper associativity rules."""
    ast = get_ast("+5 *2 -10 7")
    node = ast[0]
    
    # Structure should match: 5 + (2 * (10 - 7))
    assert isinstance(node, BinaryOpNode)
    assert node.op == '+'
    assert node.left.value == 5
    
    assert isinstance(node.right, BinaryOpNode)
    assert node.right.op == '*'
    assert node.right.left.value == 2
    
    assert isinstance(node.right.right, BinaryOpNode)
    assert node.right.right.op == '-'
    assert node.right.right.left.value == 10
    assert node.right.right.right.value == 7

def test_parse_advanced_array_operators():
    """Examines complex structural mutations from the ARROPS table."""
    # Slice operator ::
    ast_slice = get_ast("^: arr 0 2")
    assert isinstance(ast_slice[0], SliceNode)
    
    # Insert operator *:
    ast_insert = get_ast("*: arr 1 \"item\"")
    assert isinstance(ast_insert[0], InsertNode)
    
    # Remove operator $:
    ast_remove = get_ast("$: arr \"item\"")
    assert isinstance(ast_remove[0], RemoveItemNode)
    
    # Set index operator =:
    ast_set = get_ast("=: arr 0 99")
    assert isinstance(ast_set[0], SetIndexNode)
    
    # Pop index operator ~:
    ast_pop_idx = get_ast("~: arr 3")
    assert isinstance(ast_pop_idx[0], PopIndexNode)