
import sys
import ast
import jsonpickle

class ASTSerializer( ast.NodeTransformer ):
	"""
	The ASTSerializer class is a NodeTransformer
	that replaces each AST Node with a JSON representation
	for that node that adheres to the Mozilla Parser API.
	"""

	# -------- *utilities* --------

	def guard( self, node, accessor, f = lambda x: x ):
		if ( hasattr( node, accessor ) ) :
			if ( getattr( node, accessor ) is not None ) :
				return f( getattr( node, accessor ) )

		return None


	# -------- Literals --------

	def visit_Num( self, node ):
		return {
			"expr": "Literal",
			"type": "Number",
			"value": self.guard( node, "n" ),
			"position": {
				'line': self.guard( node, "lineno" )
			}
		}


	def visit_Str( self, node ): 
		return {
			"expr": "Literal",
			"type": "String",
			"value":  self.guard( node, "s" ),
			"position": {
				'line': self.guard( node, "lineno" )
			},
			"docstring": False
		}


	def visit_Bytes( self, node ): 
		return {
			"expr": "Literal",
			"type": "Bytes",
			"value": self.guard( node, "s" ),
			"position": {
				'line': self.guard( node, "lineno" )
			},
			"docstring": False
		}


	def visit_List( self, node ): 
		return {
			"expr": "Literal",
			"type": "List",
			"value": self.guard( node, "elts", f = lambda x : map( self.visit, x )  ),
			"position": {
				'line': self.guard( node, "lineno" )
			},
			"docstring": False
		}


	def visit_Tuple( self, node ): 
		return {
			"expr": "Literal",
			"type": "Tuple",
			"value": self.guard( node, "elts", f = lambda x : map( self.visit, x )  ),
			"position": {
				'line': self.guard( node, "lineno" )
			},
			"docstring": False
		}

	def visit_Set( self, node ):
		return {
			"expr": "Literal",
			"type": "Set",
			"value": self.guard( node, "elts", f = lambda x : map( self.visit, x )  ),
			"position": {
				'line': self.guard( node, "lineno" )
			},
			"docstring": False
		}

	def visit_Dict( self, node ):
		return {
			"expr": "Literal",
			"type": "Dict",
			"value": zip( self.guard( node, "keys", f = lambda x : map( self.visit, x )  ), self.guard( node, "values", f = lambda x : map( self.visit, x )  ) ),
			"position": {
				'line': self.guard( node, "lineno" )
			},
			"docstring": False
		}

	def visit_Ellipsis( self, node ):
		return {
			"expr": "Literal",
			"type": "Ellipsis",
			"position": {
				'line': self.guard( node, "lineno" )
			},
			"docstring": False
		}

	def visit_NameConstant( self, node ):
		return {
			"expr": "Literal",
			"type": "NameConstant",
			"value": self.guard( node, "value" ),
			"position": {
				'line': self.guard( node, "lineno" )
			},
			"docstring": False
		}


	# -------- Variables --------

	def visit_Name( self, node ):
		return {
			"expr": "Variable",
			"type": "Name",
			'line': self.guard( node, "id" ),
			"position": {
				'line': self.guard( node, "lineno" )
			},
			"docstring": False
		}

	def visit_Starred( self, node ):
		return {
			"expr": "Variable",
			"type": "Starred",
			"value": self.guard( node, "value", f = self.visit ),
			"position": {
				'line': self.guard( node, "lineno" )
			},
			"docstring": False
		}

	# -------- Expressions --------
	
	def visit_Expr( self, node ):
		return {
			"expr": "Expression",
			"type": "Expr",
			"value": self.guard( node, "value", f = self.visit ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	def visit_UnaryOp( self, node ):
		return {
			"expr": "Expression",
			"type": "UnaryOp",
			"operator": self.guard( node, "op", f = self.visit ),
			"operand": self.guard( node, "operand", f = self.visit ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	def visit_BinOp( self, node ):
		return {
			"expr": "Expression",
			"type": "BinOp",
			"operator": self.guard( node, "op", f = self.visit ),
			"left": self.guard( node, "left", f = self.visit ),
			"right": self.guard( node, "right", f = self.visit ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	def visit_BoolOp( self, node ):
		return {
			"expr": "Expression",
			"type": "BoolOp",
			"operator": self.guard( node, "op", f = self.visit ),
			"values": self.guard( node, "values", f = lambda x : map( self.visit, x ) ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	def visit_Compare( self, node ):
		return {
			"expr": "Expression",
			"type": "Compare",
			"left": self.guard( node, "left", f = self.visit ),
			"operators": self.guard( node, "ops", f = lambda x : map( self.visit, x ) ),
			"comparators": self.guard( node, "comparators", f = lambda x : map( self.visit, x ) ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	def visit_Call( self, node ):
		return {
			"expr": "Expression",
			"type": "Call",
			"function": self.guard( node, "func" ),
			"args": self.guard( node, "args", f = lambda x : map( self.visit, x ) ),
			"keywords": self.guard( node, "keywords", f = lambda x : map( self.visit, x ) ),
			"starargs": self.guard( node, "starargs", f = lambda x : map( self.visit, x ) ),
			"kwargs": self.guard( node, "kwargs", f = lambda x : map( self.visit, x ) ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	def visit_keyword( self, node ):
		return {
			"expr": "Expression",
			"type": "keyword",
			"arg": self.guard( node, "arg" ),
			"value": self.guard( node, "value", f = self.visit ),
			"docstring": False
		}

	def visit_IfExp( self, node ):
		return {
			"expr": "Expression",
			"type": "IfExp",
			"test": self.guard( node, "test", f = self.visit ),
			"consequent": self.guard( node, "body", f = self.visit ),
			"alternate": self.guard( node, "orelse", f = self.visit ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	def visit_Attribute( self, node ):
		return {
			"expr": "Expression",
			"type": "Attribute",
			"value": self.guard( node, "value", f = self.visit ),
			"attribute": self.guard( node, "attr" ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	# -------- Subscripting --------

	def visit_Subscript( self, node ):
		return {
			"expr": "Subscript",
			"type": "Subscript",
			"value": self.visit( node.value ),
			"slice": self.visit( node.slice ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	def visit_Slice( self, node ):
		return {
			"expr": "Subscript",
			"type": "Slice",
			"lower": self.visit( node.lower ),
			"upper": self.visit( node.upper ) if hasattr('upper', node) else None,
			"step": self.visit( node.step ) if hasattr('step', node) else None,
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	def visit_Index( self, node ):
		return {
			"expr": "Subscript",
			"type": "Index",
			"value": self.visit( node.value ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	def visit_ExtSlice( self, node ):
		return {
			"expr": "Subscript",
			"type": "Slice",
			"dims": map( self.visit, node.dims ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	# -------- Comprehensions --------

	def visit_ListComp( self, node ):
		return {
			"expr": "Comprehension",
			"type": "ListComp",
			"element": self.visit( node.elt ),
			"generators": map( self.visit, node.generators ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	def visit_ListComp( self, node ):
		return {
			"expr": "Comprehension",
			"type": "SetComp",
			"element": self.visit( node.elt ),
			"generators": map( self.visit, node.generators ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	def visit_GeneratorExp( self, node ):
		return {
			"expr": "Comprehension",
			"type": "GeneratorExp",
			"element": self.visit( node.elt ),
			"generators": map( self.visit, node.generators ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	def visit_DictComp( self, node ):
		return {
			"expr": "Comprehension",
			"type": "GeneratorExp",
			"key": self.visit( node.key ),
			"value": self.visit( node.value ),
			"generators": map( self.visit, node.generators ),
			"position": {
				'line': node.lineno
			},
			"docstring": False
		}

	def visit_comprehension( self, node ):
		return {
			"expr": "Comprehension",
			"type": "Comprehension",
			"target": self.visit( node.key ),
			"iter": self.visit( node.iter ),
			"ifs": map( self.visit, node.ifs ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	# -------- Statements --------
	
	def visit_Assign( self, node ):
		return {
			"expr": "Statement",
			"type": "Assign",
			"targets": map( self.visit, node.targets ),
			"value": self.visit( node.value ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	def visit_AugAssign( self, node ):
		return {
			"expr": "Statement",
			"type": "AugAssign",
			"target": self.visit( node.target ),
			"operator": self.visit( node.op ),
			"value": self.visit( node.value ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	def visit_Print( self, node ):
		return {
			"expr": "Statement",
			"type": "Print",
			"dest": self.visit( node.dest ),
			"values": map( self.visit, node.value ),
			"newline": node.nl,
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	def visit_Assert( self, node ):
		return {
			"expr": "Statement",
			"type": "Assert",
			"test": self.visit( node.dest ),
			"msg": self.visit( node.value ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	def visit_Raise( self, node ):
		if ( sys.version >= 3 ):
			return {
				"expr": "Statement",
				"type": "Raise",
				"exc": self.visit( node.exc ),
				"cause": self.visit( node.cause ) if node.cause is not None else None,
				"position": {
					'line': node.lineno
				},
				"docstring": False		
			}
		else:
			return {
				"expr": "Statement",
				"type": "Raise",
				"excType": self.visit(node.type),
				"inst":  self.visit(node.inst),
				"tback": self.visit(node.tback),
				"position": {
					'line': node.lineno
				},
				"docstring": False		
			}


	def visit_Delete( self, node ):
		return {
			"expr": "Statement",
			"type": "Delete",
			"targets": map( self.visit, node.targets ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	def visit_Pass( self, node ):
		return {
			"expr": "Statement",
			"type": "Pass",
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	# -------- Imports --------
	

	def visit_Import( self, node ):
		return {
			"expr": "Import",
			"type": "Import",
			"names": map( self.visit, node.names ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}	

	def visit_ImportFrom( self, node ):
		return {
			"expr": "Import",
			"type": "ImportFrom",
			"module": node.module,
			"names": map( self.visit, node.names ),
			"level": node.level,
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	def visit_alias( self, node ):
		return {
			"expr": "Import",
			"type": "ImportFrom",
			"name": node.name,
			"asname": node.asname,
			"docstring": False		
		}	 

	# -------- ControlFlow --------
	
	def visit_If( self, node ):
		return {
			"expr": "ControlFlow",
			"type": "If",
			"test": self.visit( node.test ),
			"consequent": map( self.visit, node.body ),
			"alternate": map( self.visit, node.orelse ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	def visit_For( self, node ):
		return {
			"expr": "ControlFlow",
			"type": "For",
			"target": self.visit( node.target ),
			"iter": self.visit( node.iter ),
			"body": map( self.visit, node.body ),
			"orelse": map( self.visit, node.orelse ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}


	def visit_While( self, node ):
		return {
			"expr": "ControlFlow",
			"type": "While",
			"test": self.visit( node.test ),
			"body": map( self.visit, node.body ),
			"orelse": map( self.visit, node.orelse ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	def visit_Break( self, node ):
		return {
			"expr": "ControlFlow",
			"type": "Break",
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	def visit_Continue( self, node ):
		return {
			"expr": "ControlFlow",
			"type": "Continue",
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	def visit_Try( self, node ):
		return {
			"expr": "ControlFlow",
			"type": "Try",
			"body": map( self.visit, node.body ),
			"handlers": map( self.visit, node.handlers ),
			"orelse": map( self.visit, node.orelse ),
			"finalbody": map( self.visit, node.finalbody ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}	

	def visit_TryFinally( self, node ):
		return {
			"expr": "ControlFlow",
			"type": "TryFinally",
			"body": map( self.visit, node.body ),
			"finalbody": map( self.visit, node.finalbody ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		} 
	
	def visit_TryExcept( self, node ):
		return {
			"expr": "ControlFlow",
			"type": "TryExcept",
			"body": map( self.visit, node.body ),
			"handlers": map( self.visit, node.handlers ),
			"orelse": map( self.visit, node.orelse ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		} 

	def visit_ExceptHandler( self, node ):
		return {
			"expr": "ControlFlow",
			"type": "ExceptHandler",
			"exnType": self.visit( node.type ),
			"name": node.name,
			"body": map( self.visit, node.body ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		} 	

	def visit_With( self, node ):
		return {
			"expr": "ControlFlow",
			"type": "With",
			"items": map( self.visit, node.type ),
			"body": map( self.visit, node.body ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		} 	

	def visit_withitem( self, node ):
		return {
			"expr": "ControlFlow",
			"type": "WithItem",
			"context_expr": self.visit( node.context_expr ),
			"optional_vars": self.visit( node.type ) if node.optional_vars is not None else None,
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		} 

	# -------- Function and Module Definitions --------

	def visit_FunctionDef( self, node ):
		return {
			"expr": "Definitions",
			"type": "FunctionDef",
			"name": node.name,
			"args": self.visit( node.args ),
			"body": map( self.visit, node.body ),
			"decorators": map( self.visit, node.decorator_list),
			"returns": self.visit( node.returns ) if hasattr(node, 'returns') else None,
			"position": {
				'line': node.lineno
			},
			"docstring": ast.get_docstring( node )		
		}

	def visit_Lambda( self, node ):
		return {
			"expr": "Definitions",
			"type": "Lambda",
			"args": self.visit( node.args ),
			"body": self.visit( node.body ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	def visit_arguments( self, node ):
		return {
			"expr": "Definitions",
			"type": "Arguments",
			"args": map( self.visit, node.args ),
			"kwonlyargs": map( self.visit, node.kwonlyargs ) if hasattr(node, "kwonlyargs") else None,
			"vararg": self.visit( node.vararg ) if node.vararg is not None else None,
			"kwarg": self.visit( node.kwarg ) if node.kwarg is not None else None,
			"defaults": map( self.visit, node.defaults ),
			"kw_defaults": map( self.visit, node.kw_defaults ) if hasattr(node, "kw_defaults") else None,  
			"docstring": False		
		} 

	def visit_arg( self, node ):
		return {
			"expr": "Definitions",
			"type": "arg",
			"arg": node.arg,
			"annotation": self.visit( node.annotation ),
			"docstring": False		
		} 

	def visit_Return( self, node ):
		return {
			"expr": "Definitions",
			"type": "Return",
			"value": self.visit( node.value ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}  	

	def visit_Yield( self, node ):
		return {
			"expr": "Definitions",
			"type": "Yield",
			"value": self.visit( node.value ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	def visit_YieldFrom( self, node ):
		return {
			"expr": "Definitions",
			"type": "YieldFrom",
			"value": self.visit( node.value ),
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		}

	def visit_Global( self, node ):
		return {
			"expr": "Definitions",
			"type": "Global",
			"names": node.names,
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		} 	

	def visit_Nonlocal( self, node ):
		return {
			"expr": "Definitions",
			"type": "Nonlocal",
			"names": node.names,
			"position": {
				'line': node.lineno
			},
			"docstring": False		
		} 

	def visit_ClassDef( self, node ):
		return {
			"expr": "Definitions",
			"type": "ClassDef",
			"name": node.name,
			"bases": map( self.visit, node.bases ),
			"keywords": map( self.visit, node.keywords ) if hasattr(node, "keywords") else None,
			"starargs": self.visit( node.starargs ) if hasattr(node, "starargs") else None,
			"kwargs": self.visit( node.kwargs ) if hasattr(node, "kwargs") else None,
			"body": map( self.visit, node.body ),
			"decorator_list": map( self.visit, node.decorator_list ),
			"position": {
				'line': node.lineno
			},
			"docstring": ast.get_docstring( node )		
		}

	def visit_Module( self, node ):
		return {
			"expr": "Definitions",
			"type": "Module",
			"body": map( self.visit, node.body ),
			"position": {
				'line': 0
			},
			"docstring": ast.get_docstring( node )		
		}  

	# -------- Operators --------
	
	def visit_UAdd( self, node ): return "+"

	def visit_USub( self, node ): return "-"

	def visit_Not( self, node ): return "!"

	def visit_Invert( self, node ): return "~"

	def visit_Add( self, node ): return "+"

	def visit_Sub( self, node ): return "-"

	def visit_Mult( self, node ): return "*"

	def visit_Div( self, node ): return "/"

	def visit_FloorDiv( self, node ): return "/"

	def visit_Mod( self, node ): return "%"

	def visit_Pow( self, node ): return "**"

	def visit_LShift( self, node ): return "<<"

	def visit_RShift( self, node ): return ">>"

	def visit_BitOr( self, node ): return "|"

	def visit_BitXor( self, node ): return "^"

	def visit_BitAnd( self, node ): return "&"

	def visit_And( self, node ): return "&&"

	def visit_Or( self, node ): return "||"

	def visit_Eq( self, node ): return "=="

	def visit_NotEq( self, node ): return "!="

	def visit_Lt( self, node ): return "<"

	def visit_Gt( self, node ): return ">"

	def visit_GtE( self, node ): return ">="

	def visit_LtE( self, node ): return "<="

	def visit_Is( self, node ): return "is"

	def visit_isNot( self, node ): return "is not"

	def visit_In( self, node ): return "in"

	def visit_NotIn( self, node ): return "not in"




	
