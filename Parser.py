
import os
import ast
import json

from Serializer import ASTSerializer



class ASTParser:
	"""
	This module reads a file into memory and 
	parses it as a python AST. Following that,
	it transforms the AST into a JSON representation.
	"""


	def __init__( self, filepath ):
		self.filepath = filepath


	def parse( self ):
		try:

			f = open( self.filepath, 'r' )
			self.quote = f.read()
			f.close()

		except (OSError, IOError) as e:

			return json.dumps({
				"success": False,
				"message": os.strerror( e.errno ),
				"filepath": self.filepath
			});

		try:

			serialized = self.serialize( ast.parse( self.quote ) )

			return json.dumps({
				"success": True,
				"message": None,
				"filepath": self.filepath,
				"ast": serialized
			});

		except (SyntaxError) as e:

			return json.dumps({
				"success": False,
				"message": str( e ),
				"context": e.text,
				"filepath": self.filepath,
				"position": {
					"line": e.lineno,
					"offset": e.offset
				}

			});


	def serialize( self, result ):
		return ASTSerializer().visit( result )
