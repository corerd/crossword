import argparse
import ast
from .constants import *
import cli.printers.crossword as crossword_printer

# helping methods
def evalTF(string):
	return ast.literal_eval(string.title())

# Default parser
DEFAULT_PARSER = argparse.ArgumentParser(
	# prog = 'crossword.py'
	# usage (generated by default)
	description = """Given a crossword puzzle as a file input, uses CSP AI
	algorithms to solve the crossword and returns the same puzzle solved (if it
	can be solved ;)""",
	epilog = "Made with love in ETSE UAB by ccebrecos, joel.sanz & davidlj95",
	add_help = True,
	allow_abbrev = True
)
DEFAULT_PARSER.add_argument("-v","--version",
	action="version",
	version="Crossword 3.141592")
DEFAULT_PARSER.add_argument("--itemset",
	action="store",
	nargs="?",
	help="""specifies the crossword & wordlist to load (default is %s)"""%\
		ITEMSET_DEFAULT["name"],
	type=str,
	choices=[ITEMSET_SMALL["name"],ITEMSET_BIG["name"]],
	default=ITEMSET_DEFAULT["name"]
)
DEFAULT_PARSER.add_argument("--show-crossword",
	metavar="true|false",
	action="store",
	nargs="?",
	help="""enables or disables printing the crossword information (%s
	by default)"""%("enabled" if SHOW_CROSSWORD_DEFAULT else "disabled"),
	type=evalTF,
	const=True,
	default=SHOW_CROSSWORD_DEFAULT
)
DEFAULT_PARSER.add_argument("--show-wordlist",
	metavar="true|false",
	action="store",
	nargs="?",
	help="""enables or disables printing the wordlist information (%s
	by default)"""%("enabled" if SHOW_WORDLIST_DEFAULT else "disabled"),
	type=evalTF,
	const=True,
	default=SHOW_WORDLIST_DEFAULT
)
DEFAULT_PARSER.add_argument("-w","--wordlist",
	metavar="filename",
	action="store",
	nargs="?",
	help="""specifies the wordlist file to use to solve the crossword. It has
	to be a file with a word per line, all uppercase or lowercase. Default is
	%s"""%(ITEMSET_DEFAULT["wordlist"]),
	type=str,
	default=None
)
DEFAULT_PARSER.add_argument("--use-thesaurus",
	metavar="true|false",
	action="store",
	nargs="?",
	help="""The file specified by wordlist option is an an Hunspell thesaurus
	(%s	by default)"""%("TRUE" if USE_THESAURUS_DEFAULT else "FALSE"),
	type=evalTF,
	const=True,
	default=USE_THESAURUS_DEFAULT
)
DEFAULT_PARSER.add_argument("-c","--crossword",
	metavar="filename",
	action="store",
	nargs="?",
	help="""specifies the crossword file to use to load the problem. It has to
	be a file with values of the crossword separed by columns with a tabulation
	character and by rows with a row meaning a line. Default is '%s'"""%\
		(ITEMSET_DEFAULT["crossword"]),
	type=str,
	default=None
)
DEFAULT_PARSER.add_argument("--solution",
	metavar="true|false",
	action="store",
	nargs="?",
	help="""enables or disables printing the solution as crossword (%s
	by default)"""%("enabled" if SHOW_SOLUTION_DEFAULT else "disabled"),
	type=evalTF,
	const=True,
	default=SHOW_SOLUTION_DEFAULT
)
DEFAULT_PARSER.add_argument("-t","--timers",
	action="count",
	help="""records the algorithm's computation time and shows them. You can
	add levels of timings by specifying repeating argument. Default timing
	level is %d"""%TIMERS_DEFAULT,
	default = TIMERS_DEFAULT
)
DEFAULT_PARSER.add_argument("--algorithm",
	action="store",
	nargs="?",
	help="""specifies the algorithm implementation to use. Use %s to show """
	"""how the variables go assigning while algorithm runs. Live algorithm"""
	"""uses the fastest algorithm found. (default is %s)"""%\
		(ALG_BACKTRACKING_LIVE,ALG_DEFAULT),
	type=str,
	choices=[ALG_BACKTRACKING_FC,ALG_BACKTRACKING_SIMPLE,ALG_BACKTRACKING_LIVE],
	default=ALG_DEFAULT
)
DEFAULT_PARSER.add_argument("--play","-p",
	action="store_const",
	help="""sets play mode: we'll find the solution and give you definitions so
	you can fill the crossword yourself, rendering all together
	in an HTML file""",
	const=True,
	default=False
)
DEFAULT_PARSER.add_argument("--style","-s",
	action="store",
	nargs="?",
	help="""style of the beautiful crossword in the CLI (default is %s)"""%\
		crossword_printer.CHAR_TABLESETS_DEFAULT_NAME,
	type=str,
	choices=list(crossword_printer.CHAR_TABLESETS.keys()),
	default=crossword_printer.CHAR_TABLESETS_DEFAULT_NAME
)
DEFAULT_PARSER.add_argument("--frames","-f",
	action="store",
	nargs="?",
	help="""when using %s algorithm that prints live status, tells the frames"""
	"""per second to update the crossword & save compute time """
	"""(default is %d)"""%\
		(ALG_BACKTRACKING_LIVE,crossword_printer.FRAMES_DEFAULT),
	type=int,
	default=crossword_printer.FRAMES_DEFAULT
)
