def run(source_path: str, target_path: str = "./output"):
    compile(source_path, target_path)

def compile(source_path: str, target_path: str):
    """
    first create AST
    then run line by line
    """
    syntax_tree = create_syntax_tree(source_path)
    bytecode = convert_syntax_tree_to_byte_code(syntax_tree)

def create_syntax_tree(source_path: str):
    pass

def convert_syntax_tree_to_byte_code(syntax_tree):
    pass
