import sys, getopt

def parse( filepath ):
	print 'Input file path is', filepath

def main( argv ):
	helpstring = argv[ 0 ] + " {-p|--parse} <input filepath>"
	filepath = ''

	if len( argv ) == 1:
		print helpstring
		sys.exit( 2 ) 

	try:
		opts, args = getopt.getopt( argv[ 1: ], "hp:", ['parse='])

	except getopt.GetoptError:
		print helpstring
		sys.exit( 2 )

	for opt, arg in opts:
		if opt == '-h':
			print helpstring
			sys.exit()

		elif opt in ('-p', '--parse'):
			filepath = arg

	parse( filepath )


if __name__ == "__main__":
	main( sys.argv )