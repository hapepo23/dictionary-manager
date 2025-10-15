#  utils.py

from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

def ButtonEnable(b:ttk.Button, yes:bool):
	if yes:
		b.state(['!disabled'])
	else:
		b.state(['disabled'])


def EntryEnable(e:ttk.Entry, yes:bool):
	if yes:
		e.configure(state='normal')
	else:
		e.state(['readonly'])


def TextboxEnable(tb:scrolledtext.ScrolledText, yes:bool):
	if yes:
		tb.config(state=NORMAL)
		tb.configure(bg='white')
	else:
		tb.config(state=DISABLED)
		tb.configure(bg='lightgrey')


def TextboxDeleteAndEnable(tb:scrolledtext.ScrolledText, yes:bool):
	if yes:
		tb.config(state=NORMAL)
		tb.configure(bg='white')
		tb.delete('1.0', 'end')
	else:
		tb.config(state=NORMAL)
		tb.delete('1.0', 'end')
		tb.config(state=DISABLED)
		tb.configure(bg='lightgrey')


def combineKeyAndDataWithTabs(key:str, data:str) -> str:
	r = key.strip() + '\t' + '\t'.join(data[:-1].split('\n'))  # data from textbox contains always extra \n that is removed here
	return r


def getTreeviewNextIID(tv:ttk.Treeview, currIID) -> str:
	nextIID = tv.next(currIID)
	if nextIID:
		return nextIID
	else:
		nextIID = tv.prev(currIID)
		if nextIID:
			return nextIID
		else:
			return ''

