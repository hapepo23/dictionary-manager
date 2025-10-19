# editdialog.py

import os
import utils
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from dict import Dict
from dictentry import Dictentry

class EditDialog(Toplevel):

	def __init__(self, parent, d:Dict):
		super().__init__(parent)

		self.parent = parent
		self.dict:Dict = d
		self.add_mode = False

		# self.transient(self.parent)
		self.title('View/Edit Dictionary')
		iconpath = os.path.join(os.getcwd(), self.parent.assetsdir, self.parent.iconfilename)
		self.iconphoto(False, PhotoImage(file=iconpath))
		self.protocol('WM_DELETE_WINDOW', self.close)
		self.bind('<Escape>', self.close)

		self.columnconfigure(0, weight=1) # to adjust to win size
		self.rowconfigure(0, weight=1) # to adjust to win size

		content = ttk.Frame(self, padding=(5))
		content.grid(column=0, row=0, sticky=NSEW, padx=5, pady=5)
		# columns and rows to be extended
		content.columnconfigure(2, weight=1)
		content.columnconfigure(6, weight=1)
		content.rowconfigure(3, weight=1)

		#  line 0
		ttk.Label(content, text='Filter:').grid(column=0, row=0, sticky=E, padx=0, pady=0)

		self.filtervalue = StringVar(name='filtervalue', master=self)
		self.filtervalue.set('')
		self.filterentry = ttk.Entry(content, width=15, textvariable=self.filtervalue)
		self.filterentry.grid(column=1, row=0, columnspan=3, sticky=EW, padx=5)
		self.filtervalue.trace_add('write', self.trace_filtervalue)

		self.filterclear = ttk.Button(content, width=3, text=' X ', command=self.click_filter)
		self.filterclear.grid(column=4, row=0, padx=0, pady=0, sticky=W )

		ttk.Label(content, text='  ').grid(column=5, row=0, sticky=EW, padx=5, pady=5)

		ttk.Label(content, text='Key:').grid(column=6, row=0, sticky=W, padx=0, pady=0)

		# line 1
		self.mykeylist = None
		keysframe = ttk.Frame(content, padding=(0))
		keysframe.grid(column=0, row=1, columnspan=5, rowspan=3, sticky=NSEW, padx=0, pady=0)
		keysframe.columnconfigure(0, weight=1) # to adjust to win size
		keysframe.rowconfigure(0, weight=1) # to adjust to win size
		self.keyslist = ttk.Treeview(keysframe, columns=('keys'), show='', selectmode='extended')  # or browse
		self.keyslist.heading('keys', text='Keys')
		self.keyslist.column('keys', minwidth=0, width=200, stretch=YES)
		self.keyslist.bind('<<TreeviewSelect>>', self.show)
		scrollbar = ttk.Scrollbar(keysframe, orient=VERTICAL, command=self.keyslist.yview)
		self.keyslist.configure(yscroll=scrollbar.set)
		self.keyslist.grid(column=0, row=0, sticky=NSEW, padx=0, pady=5)
		scrollbar.grid(column=1, row=0, sticky='NSE', padx=0, pady=5)

		self.keyvalue = StringVar(name='keyvalue', master=self)
		self.keyvalue.set('')
		self.keyvalueentry = ttk.Entry(content, width=30, textvariable=self.keyvalue, font=('Noto Sans', 12))
		self.keyvalueentry.grid(column=6, row=1, columnspan=5, sticky=EW, pady=5)
		self.keyvalueentry.bind('<Tab>', self.no_tab_in_keyvalueentry)
		self.keyvalue.trace_add('write', self.trace_keyvalue)

		# line 2
		ttk.Label(content, text='Data:').grid(column=6, row=2, sticky=W, padx=0, pady=0)

		# line 3
		self.textbox = scrolledtext.ScrolledText(content, width=40, height=20, wrap='word', font=('Noto Sans', 12))
		self.textbox.grid(column=6, row=3, columnspan=5, sticky=NSEW, pady=5)
		self.textbox.bind('<Tab>', self.no_tab_in_textbox)

		# line 4
		self.addbutton = ttk.Button(content, text='Add', command=self.click_add)
		self.addbutton.grid(column=0, row=4, sticky=W, padx=0, pady=0)

		self.updbutton = ttk.Button(content, text='Update', command=self.click_update)
		self.updbutton.grid(column=2, row=4, padx=0, pady=0)

		self.delbutton = ttk.Button(content, text='Delete', command=self.click_delete)
		self.delbutton.grid(column=4, row=4, sticky=E, padx=0, pady=0)

		self.savebutton = ttk.Button(content, text='Save', command=self.click_save)
		self.savebutton.grid(column=10, row=4, sticky=E, padx=0, pady=0)

		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()
		w = 700
		h = 500
		x = (screen_width / 2) - (w / 2)
		y = (screen_height / 2) - (h / 2)
		self.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.minsize(w,h)

		self.withdraw()


	def run(self):
		self.deiconify()
		self.title('View/Edit Dictionary ' + os.path.basename(self.dict.filename))
		topkey = self.redo_keyslist()
		self.grab_set()
		utils.ButtonEnable(self.delbutton, False)
		utils.ButtonEnable(self.updbutton, False)
		utils.ButtonEnable(self.savebutton, False)
		utils.TextboxEnable(self.textbox, False)
		utils.EntryEnable(self.keyvalueentry, False)
		self.add_mode = False
		if topkey != '':
			self.keyslist.selection_set(topkey)


	def close(self, *args):
		self.grab_release()
		self.parent.deiconify()
		self.click_filter()
		self.withdraw()
		self.parent.newtitle()


	def no_tab_in_textbox(self, event):
		self.savebutton.focus()
		return 'break'


	def no_tab_in_keyvalueentry(self, event):
		self.textbox.focus()
		return 'break'


	def item_selected(self):
		r = ''
		for r in self.keyslist.selection():
			break
		return r


	def item_selected_count(self) -> int:
		return len(self.keyslist.selection())


	def redo_keyslist(self) -> str:
		self.keyslist.delete(*self.keyslist.get_children())
		self.mykeylist = self.dict.getsortedkeylist()
		fv = self.filtervalue.get().lower()
		if fv == '':
			for v in self.mykeylist:
				self.keyslist.insert('', END, iid=v, values=[v])
		else:
			for v in self.mykeylist:
				if fv in str(self.dict.data[v]).lower():
					self.keyslist.insert('', END, iid=v, values=[v])
		r = ''
		for v in self.mykeylist:
			r = v
			break
		return r  # first key or ''


	def show(self, *args):
		self.keyvalue.set('')
		utils.EntryEnable(self.keyvalueentry, False)
		utils.TextboxDeleteAndEnable(self.textbox, False)
		utils.ButtonEnable(self.updbutton, False)
		utils.ButtonEnable(self.delbutton, False)
		utils.ButtonEnable(self.savebutton, False)
		self.add_mode = False
		if self.item_selected_count() == 1:
			key = self.item_selected()
			if self.dict.keyexists(key):
				de:Dictentry = self.dict.data[key]
				val = de.data
				utils.TextboxEnable(self.textbox, True)
				self.textbox.insert('1.0',val)
				utils.TextboxEnable(self.textbox, False)
				self.keyvalue.set(key)
				utils.ButtonEnable(self.delbutton, True)
				utils.ButtonEnable(self.updbutton, True)
		elif self.item_selected_count() > 1:
			utils.ButtonEnable(self.delbutton, True)


	def trace_filtervalue(self, *args):
		self.redo_keyslist()


	def trace_keyvalue(self, *args):
		if self.add_mode:
			str = utils.combineKeyAndDataWithTabs(self.keyvalue.get(), self.textbox.get("1.0", "end"))
			de = Dictentry(str)
			utils.ButtonEnable(self.savebutton, de.isKeyValid(self.dict.getkeyslist()))


	def click_filter(self):
		self.filtervalue.set('')


	def click_add(self):
		self.keyvalue.set('')
		utils.EntryEnable(self.keyvalueentry, True)
		utils.TextboxDeleteAndEnable(self.textbox, True)
		utils.ButtonEnable(self.savebutton, False)
		self.add_mode = True
		self.keyvalueentry.focus()


	def click_update(self):
		self.show()
		utils.TextboxEnable(self.textbox, True)
		utils.ButtonEnable(self.savebutton, True)
		self.add_mode = False
		self.textbox.focus()


	def click_delete(self):
		cnt = 0
		nextkey = ''
		for key in self.keyslist.selection():
			nextkey = utils.getTreeviewNextIID(self.keyslist, key)
			if self.dict.remove(key):
				cnt = cnt + 1
		if cnt > 0:
			self.redo_keyslist()
		if cnt == 1:
			self.keyvalue.set('')
			utils.TextboxDeleteAndEnable(self.textbox, False)
			utils.ButtonEnable(self.delbutton, False)
			utils.ButtonEnable(self.updbutton, False)
			utils.ButtonEnable(self.savebutton, False)
			if nextkey != '':
				self.keyslist.selection_set(nextkey)


	def click_save(self):
		str = utils.combineKeyAndDataWithTabs(self.keyvalue.get(), self.textbox.get("1.0", "end"))
		de = Dictentry(str)
		if self.add_mode:
			if de.isKeyValid(self.dict.getkeyslist()):
				self.dict.addde(de)
				self.redo_keyslist()
				utils.TextboxEnable(self.textbox, False)
				utils.EntryEnable(self.keyvalueentry, False)
				utils.ButtonEnable(self.savebutton, False)
				utils.ButtonEnable(self.updbutton, False)
				utils.ButtonEnable(self.delbutton, False)
				self.keyslist.selection_set(de.key)
			else:
				messagebox.showerror("Error", "The key exists (use UPDATE) or is empty!")
		else:
			if self.dict.keyexists(de.key):
				self.dict.remove(de.key)
				self.dict.addde(de)
				utils.TextboxEnable(self.textbox, False)
				utils.ButtonEnable(self.updbutton, True)
				utils.ButtonEnable(self.delbutton, True)
			else:
				messagebox.showerror("Error", "The key is invalid!")

