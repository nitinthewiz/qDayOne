#!/usr/bin/env python

# example textview.py

import pygtk
pygtk.require('2.0')
import gtk, gobject
import os
import getpass
import platform
import xml.etree.ElementTree as ET
import datetime
import uuid
import re

#os.environ['PATH'] += ";gtk/lib;gtk/bin"

class QDayOne:
	directory = ''
	myUUID = ''

	def close_application(self, widget):
		gtk.main_quit()

	def callback(self, widget):
		print self.textbuffer.get_text(self.textbuffer.get_start_iter() , self.textbuffer.get_end_iter())

	def reset(self):
		self.label.set_text("")

	def save(self, widget):
		#print "Saving"
		self.label.set_text("Saving")
		#print self.textbuffer.get_text(self.textbuffer.get_start_iter() , self.textbuffer.get_end_iter())
		now = datetime.datetime.utcnow()
		theUUID = uuid.uuid4()
		self.myUUID = re.sub('[-]', '', str(theUUID))
		self.myUUID = self.myUUID.swapcase()

		plist = ET.Element('plist')
		plist.attrib = {'version':"1.0"}
		b = ET.SubElement(plist, 'dict')
		
		c = ET.SubElement(b, 'key')
		c.text = 'Creation Date'
		d = ET.SubElement(b, 'date')
		d.text = str(now.strftime("%Y-%m-%dT%H:%M:%SZ"))
			
		e = ET.SubElement(b, 'key')
		e.text = 'Entry Text'
		f = ET.SubElement(b, 'string')
		f.text = self.textbuffer.get_text(self.textbuffer.get_start_iter() , self.textbuffer.get_end_iter())
			
		g = ET.SubElement(b, 'key')
		g.text = 'Starred'
		h = ET.SubElement(b, 'false')
		
		i = ET.SubElement(b, 'key')
		i.text = 'UUID'
		j = ET.SubElement(b, 'string')
		j.text = self.myUUID
			
		file = open(self.directory+self.myUUID+'.doentry', 'w')
		XMLL = """<?xml version="1.0" encoding="UTF-8"?>"""
		DTD = """<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">"""
		file.write(XMLL + "\n")
		file.write(DTD + "\n")
		ET.ElementTree(plist).write(file)
		#print "saved"
		self.label.set_text("Saved")
		gobject.timeout_add_seconds(3, self.reset)

	def __init__(self):
		savefile = open('DayOne.sav', 'w+')
		try:
			tree = ET.parse(savefile)
			root = tree.getroot()
			self.directory = root.text
		except:
			#print "savefile not found"
			#print platform.system()
			if platform.system() == 'Windows':
				#print "system is windows"
				directory = 'C:\\Users\\'+getpass.getuser()+'\\Dropbox\\Apps\\Day One\\Journal.dayone\\entries\\'
				if os.path.exists(directory):
					self.directory = directory
				else:
					message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
					message.set_markup("Day One entries folder not found. Please select the entries directory of Day One. It should be under Dropbox -> Apps -> Day One -> Journal.dayone -> entries")
					response = message.run()
					message.destroy()
					dialog = gtk.FileChooserDialog("Choose entries directory:",action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
					response = dialog.run()
					if response == gtk.RESPONSE_OK:
						#print dialog.get_current_folder(), 'selected'
						self.directory = dialog.get_current_folder()
					elif response == gtk.RESPONSE_CANCEL:
						#print 'Closed, no files selected'
						message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
						message.set_markup("No folder was selected. I can't work like this!")
						response = message.run()
						message.destroy()
						gtk.main_quit()
					dialog.destroy()
			else:
				message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
				message.set_markup("Day One entries folder not found. Please select the entries directory of Day One. It should be under Dropbox->Apps->Day One->Journal.dayone->entries")
				message.run()
				dialog = gtk.FileChooserDialog("Choose entries directory:",action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
				response = dialog.run()
				if response == gtk.RESPONSE_OK:
					#print dialog.get_current_folder(), 'selected'
					self.directory = dialog.get_current_folder()
				elif response == gtk.RESPONSE_CANCEL:
					#print 'Closed, no files selected'
					message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
					message.set_markup("No folder was selected. I can't work like this!")
					response = message.run()
					message.destroy()
					gtk.main_quit()
				dialog.destroy()
			dir = ET.Element('directory')
			dir.text = self.directory
			ET.ElementTree(dir).write(savefile)

		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_resizable(True)
		window.connect("destroy", self.close_application)
		window.set_title("qDayOne - Post to Day One quickly")
		window.set_border_width(0)
		window.set_size_request(300, 300)

		box1 = gtk.VBox(False, 0)
		window.add(box1)
		box1.show()

		box2 = gtk.VBox(False, 10)
		box2.set_border_width(10)
		box1.pack_start(box2, True, True, 0)
		box2.show()

		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.textbuffer = gtk.TextBuffer()
		textview = gtk.TextView(self.textbuffer)
		textview.set_wrap_mode(gtk.WRAP_WORD)
		#textbuffer = textview.get_buffer()
		sw.add(textview)
		sw.show()
		textview.show()
		box2.pack_start(sw)
		
		separator = gtk.HSeparator()
		box1.pack_start(separator, False, True, 0)
		separator.show()

		table = gtk.Table(2, 2, True)
		box1.pack_start(table, False, True, 0)

		self.label = gtk.Label('')
		table.attach(self.label, 0, 1, 0, 1)
		self.label.show()

		# button = gtk.Button("Print")
		# button.connect("clicked", self.callback)
		# table.attach(button, 1, 2, 0, 1)
		# button.show()

		button = gtk.Button("Save")
		button.connect("clicked", self.save)
		table.attach(button, 0, 2, 1, 2)
		button.show()

		table.show()
		window.show()

def main():
	gtk.main()
	return 0

if __name__ == "__main__":
	QDayOne()
	main()
