#  dictentry.py

class Dictentry:

	def __init__(self, pline: str):
		items = (pline.split('\t'))
		if len(items) > 1:
			key = items[0]
			self.key = key.strip()
			self.data = '\n'.join(items[1:])
		else:
			self.key = pline.strip()
			self.data = ''


	def isKeyValid(self, keys:list) -> bool:
		if self.key == '':
			return False
		elif self.key in keys:
			return False
		else:
			return True


	def __str__(self) -> str:
		return self.key + '\t' + '\t'.join(self.data.split('\n'))


	def __repr__(self) -> str:
		return 'key=' + self.key + ', data=' + '|'.join(self.data.split('\n'))


# Tests

if __name__ == '__main__':
	d1 = Dictentry('')
	print(repr(d1))
	print('validkey=' + str(d1.isKeyValid(['a','b','c'])))

	d1 = Dictentry('a')
	print(repr(d1))
	print('validkey=' + str(d1.isKeyValid(['a','b','c'])))

	d1 = Dictentry('a\tb')
	print(repr(d1))
	print('validkey=' + str(d1.isKeyValid(['a','b','c'])))

	d1 = Dictentry('d \tb\tc')
	print(repr(d1))
	print('validkey=' + str(d1.isKeyValid(['a','b','c'])))

	d1 = Dictentry(' a\t b \t c \n  k')
	print(repr(d1))
	print('validkey=' + str(d1.isKeyValid(['a','b','c'])))

	d1 = Dictentry('b  ' + '\t' + ' b \n c \n  k')
	print(repr(d1))
	print('validkey=' + str(d1.isKeyValid(['a','b','c'])))

