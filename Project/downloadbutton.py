from gi.repository import Gtk, GObject, GdkPixbuf
import webbrowser

class MainBox(Gtk.Window):

	def __init__(self):
		
		Gtk.Window.__init__(self, title="SemBegins!") #main window
		self.set_default_size(200, 100) #setting default size
		self.set_border_width(10)		

		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		label = Gtk.Label("Enter Your Roll Number:")
		vbox.pack_start(label, True, True, 0)
		
		

		button = Gtk.LinkButton("https://www.google.com",label="Submit")	
	
		vbox.pack_start(button, True, True, 0)
		self.add(vbox)

win = MainBox() #calling the mainbox
win.connect("delete-event", Gtk.main_quit) #adding the quit event listener
win.show_all()
Gtk.main()