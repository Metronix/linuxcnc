#!/usr/bin/python
import sys
from interpreter import *
from Tkinter import *
from stdglue import *

list = []

def m10(self, **words):
	global list
	if not self.task: return INTERP_OK
	list.append(self.blocks[self.remap_level].comment)
	return INTERP_OK

def done(self, dialog, entries):
	for entry in entries:
		val = entry[1].get()
		if val.isdigit:
			self.params[entry[0]] = float(val)
	dialog.update()
	dialog.destroy()

# Show the entries
def m11(self, **words):
	if not self.task: return INTERP_OK
	dir(self)
	global list
	entries = []
	row = 1
	if not hasattr(sys, 'argv'):
		sys.argv  = ['']
	dialog = Tk()
	dialog.title(self.blocks[self.remap_level].comment)
	for item in list:
		ret = item.split(";")
		prompt = ret[0]
		if len(ret) == 1:
			param = "_" + prompt.replace(" ", "")
		else:
			param = "_" + ret[1].replace(" ", "")
		Label(dialog, text=prompt).grid(row=row)
		entry = Entry(dialog)
		entry.grid(column=1, row=row)
		try:
			entry.insert(0, self.params[param])
		except:
			pass
		entries.append((param, entry))
		row += 1
	Button(dialog, text='OK', command=lambda: done(self, dialog, entries)).grid(row=row, column=0, sticky=W, pady=4)
	mainloop()
	return INTERP_OK

def m12(self, **words):
	global list
	list = []
	return INTERP_OK
