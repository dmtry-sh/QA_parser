from big_parser import *

try:
	answer = parse_answer_big('ffffggfbrgjjr')
	if answer is None:
		raise ValueError('')
except ValueError:
	pass