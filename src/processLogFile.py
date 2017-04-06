'''
This class reads the log line by line and stores
the log data as list of tuples in RAM so that
the data will have faster access time.
'''

import re

class processLogFile:
	
	def __init__(self):
		# initialize line number 
		self.line_number  = 1
		
	def return_tuple(self, line):
		"""
		Each tuple is a log entry. Tuple structure are as follows:
		
		tup[0]: host
		tup[1]:	timestamp
		tup[2]:	request method
		tup[3]:	URI
		tup[4]:	http version
		tup[5]: reply code
		tup[6]: reply bytes
		"""
		try:
			# regex tokenizing based on blank space or time stamp
			a = re.split(r"\[\s*(\d+/\D+/.*?)\]| ", line)

			if len(a) == 19:
				tup = (a[0], a[7], a[10].strip('"'), a[12], a[14].strip('"'), a[16], a[18].strip('\n'))
			elif len(a) == 17:
				tup = (a[0], a[7], a[10].strip('"'), a[12], "", a[14], a[16].strip('\n'))
			else:
				tup = (a[0], a[7], "","","", a[12], a[14].strip('\n'))
			self.line_number += 1
		except:
			print (self.line_number, line)
			raise Exception("Problem in log line - problem in tokenizing")
		return tup


