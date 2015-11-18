
import os
import ast
import json
import jsonpickle

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

			return {
				"success": False,
				"message": os.strerror( e.errno ),
				"filepath": self.filepath
			};

		return self.serialize( ast.parse( self.quote ) )


	def serialize( self, result ):
		#return json.dumps( result, default = lambda o: o.__dict__ )
		return json.dumps( ASTSerializer().visit( result ), default = lambda o: o.__dict__ )
