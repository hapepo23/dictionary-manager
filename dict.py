#  dict.py

from dictentry import Dictentry

class Dict:

	def __init__(self):
		self.data = {}
		self.filename = ''
		self.dirty = False


	def getkeyslist(self) -> list:
		return list(self.data.keys())


	def addde(self, de: Dictentry) -> bool:
		if de.isKeyValid(self.getkeyslist()):
			self.data[de.key] = de
			self.dirty = True
			r = True
		else:
			r = False
		return r


	def addstr(self, kv: str) -> bool:
		return self.addde(Dictentry(kv))


	def remove(self, key: str) -> bool:
		if self.keyexists(key):
			self.data.pop(key)
			self.dirty = True
			r = True
		else:
			r = False
		return r


	def file_import(self, filepath: str) -> bool:
		self.__init__()
		try:
			with open(filepath, 'r') as fileid:
				filetext = fileid.read()
			lines = filetext.split('\n')
			for line in lines:
				self.addstr(line)
			self.filename = filepath
			self.dirty = False
			return True
		except:
			return False


	def file_export_new(self, filepath: str) -> bool:
		try:
			fileid = open(filepath, 'w')
			fileid.write(str(self))
			fileid.close()
			self.filename = filepath
			self.dirty = False
			return True
		except:
			return False


	def file_export_old(self) -> bool:
		return self.file_export_new(self.filename)


	def keyexists(self, key: str) -> bool:
		return key in self.getkeyslist()


	def len(self) -> int:
		return len(self.data)


	def getsortedkeylist(self) -> list:
		return sorted(list(self.data.keys()), key=str.casefold)


	def __str__(self) -> str:
		result = ''
		for key, entry in self.data.items():
			result = result + str(entry) + '\n'
		return result


# Test

if __name__ == '__main__':
	d = Dict()
	print(str(d),end='')
	print('len=' + str(d.len()))

	print(d.addstr('a \tb\tc'))
	print(str(d),end='')
	print('len=' + str(d.len()))

	print(d.addde(Dictentry(' z\t b \t c \n  k  \n')))
	print(str(d),end='')
	print('len=' + str(d.len()))

	print(d.addstr('f'))
	print(str(d),end='')
	print('len=' + str(d.len()))

	print(d.addde(Dictentry('z\t b \t c \n  k  ')))
	print(str(d),end='')
	print('len=' + str(d.len()))

	print(d.getsortedkeylist())

