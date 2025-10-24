#  mainwindow.py

import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkFont
from dict import Dict
from editdialog import EditDialog

class MainWindow(Tk):

	def __init__(self, assetsdir:str, iconfilename:str, datadir:str, d:Dict):

		super().__init__(className='dictionary-python')
		defaultFont = tkFont.Font(root=self, name='TkDefaultFont', exists=True)
		defaultFont.configure(family='Noto Sans', size=11)

		self.menubar = None
		self.appmenu = None
		self.datamenu = None
		self.assetsdir = assetsdir
		self.iconfilename = iconfilename
		self.datadir = datadir
		self.dict = d
		self.editdialog = None

		self.option_add('*tearOff', False)
		self.protocol('WM_DELETE_WINDOW', self.appexit)
		iconpath = os.path.join(os.getcwd(), assetsdir, iconfilename)
		self.iconphoto(False, PhotoImage(file=iconpath))
		self.title('Dictionary Manager')

		self.menubar = Menu(self, font=defaultFont)
		self.config(menu=self.menubar)

		self.appmenu = Menu(self.menubar, font=defaultFont)
		self.menubar.add_cascade(label='Application', menu=self.appmenu)
		self.appmenu.add_command(label='About', command=self.appabout, accelerator='Ctrl+H')
		self.appmenu.add_command(label='Quit', command=self.appexit, accelerator='Ctrl+Q')

		self.bind('<Control-h>', self.appabout)
		self.bind('<Control-q>', self.appexit)
		self.bind('<Alt-F4>', self.appexit)

		self.datamenu = Menu(self.menubar, font=defaultFont)
		self.menubar.add_cascade(label='Dictionary', menu=self.datamenu)
		self.datamenu.add_command(label='New', command=self.clear, accelerator='Ctrl+N')
		self.datamenu.add_command(label='Open', command=self.loaddict, accelerator='Ctrl+O')
		self.datamenu.add_command(label='Save', command=self.savedict, accelerator='Ctrl+S')
		self.datamenu.add_command(label='Save as', command=self.savedictas, accelerator='Ctrl+Shift+S')

		self.bind('<Control-n>', self.clear)
		self.bind('<Control-o>', self.loaddict)
		self.bind('<Control-s>', self.savedict)
		self.bind('<Control-S>', self.savedictas)

		self.menubar.add_command(label='View/Edit', command=self.startedit)

		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()
		w = 600
		h = 300
		x = (screen_width / 2) - (w / 2)
		y = (screen_height / 2) - (h / 2)
		self.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.resizable(True, True)

		content = ttk.Frame(self, padding=(5))
		content.grid(column=0, row=0, sticky=(N,W,E,S), padx=5, pady=5)
		content.columnconfigure(0, weight=1)
		content.rowconfigure(0, weight=1)

		self.textbox = ttk.Label(content, text='', anchor='nw', justify='left', font=('Noto Sans', 12))
		self.textbox.grid(column=0, row=0, sticky=NSEW)
		self.textbox.columnconfigure(0, weight=1)
		self.textbox.rowconfigure(0, weight=1)

		self.editdialog = EditDialog(self,d)


	def run(self):
		dummy = self.clear()
		self.mainloop()


	def appexit(self, *args):
		if self.dict.dirty:
			if not messagebox.askokcancel('Are you sure?', 'The application will quit and all changes will be lost.\n\nAre you sure?'):
				return
		self.quit()


	def appabout(self, *args):
		messagebox.showinfo(title='About', message='Dictionary Manager Version 1.0\n(2025-10, Python/Tkinter Version)')
		

	def newtitle(self):
		if self.dict.filename == '' and self.dict.len() == 0 and (not self.dict.dirty):
			t = 'New dictionary'
		elif self.dict.filename == '' and self.dict.dirty:
			t = ('New dictionary' +
					'\nNumber of entries: ' + str(self.dict.len()) +
					'\n*** CHANGES MUST BE SAVED ***')
		else:
			t = ('Dictionary path name: ' + os.path.dirname(self.dict.filename) +
			     '\nDictionary file name: ' + os.path.basename(self.dict.filename) +
			     '\nNumber of entries: ' + str(self.dict.len()))
			if self.dict.dirty:
				t = t + '\n*** CHANGES MUST BE SAVED ***'
			else:
				t = t + '\n(UNCHANGED)'
		self.textbox['text'] = t


	def clear(self, *args) -> bool:
		if self.dict.dirty:
			if not messagebox.askokcancel('Are you sure?', 'Changes will be lost.\n\nAre you sure?'):
				return False
		self.dict.__init__()
		self.newtitle()
		self.datamenu.entryconfigure(2, state=DISABLED)
		return True


	def loaddict(self, *args):
		if self.clear():
			filename = filedialog.askopenfilename(title='Open Dictionary',
			                                      initialdir=self.datadir,
			                                      filetypes=[('Text files', '*.txt'),('CSV files', '*.csv'),('All files', '*.*')])
			if type(filename) is str:
				if filename != '':
					if self.dict.file_import(filename):
						self.datamenu.entryconfigure(2, state=NORMAL)
						self.newtitle()
						return
			messagebox.showerror(title='Error', message='No file chosen or file error')


	def savedict(self, *args):
		if self.dict.filename != '':
			if self.dict.file_export_old():
				self.newtitle()
				messagebox.showinfo(title='OK', message='Data saved: ' + self.dict.filename)
				return
		else:
			self.savedictas()
			return
		messagebox.showerror(title='Error', message='No file chosen or file error')


	def savedictas(self, *args):
		try:
			fileid = filedialog.asksaveasfile(title='Save Dictionary As ...',
			                                  initialdir=self.datadir,
			                                  filetypes=[('Text files', '*.txt'),('CSV files', '*.csv'),('All files', '*.*')],
			                                  defaultextension='.txt')
			if fileid:
				filename = fileid.name
				fileid.close()
				if self.dict.file_export_new(filename):
					self.datamenu.entryconfigure(2, state=NORMAL)
					self.newtitle()
					messagebox.showinfo(title='OK', message='Data saved: ' + filename)
					return
			messagebox.showerror(title='Error', message='Save was aborted')
		except:
			messagebox.showerror(title='Error', message='Error saving data')


	def startedit(self):
		self.editdialog.run()

