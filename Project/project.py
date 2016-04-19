from gi.repository import Gtk, GObject, GdkPixbuf
from webcrawler import showBooks
from time import gmtime, strftime
from exam import listTT
from notes import uploadFile, listUploads
from Tkinter import Tk
from tkFileDialog import askopenfilename

def semFinder(roll): #simple function to parse the roll number and get sem
	a=str(roll)
	year=a[0:2]
	m=strftime("%m", gmtime())
	y=strftime("%y", gmtime())
	ans = ((float(m)-1)/12)+int(y)-int(year)
	return int(ans*2)

def depFinder(roll): #simple function to parse the roll number and get dept.

	a=str(roll)
	dep=a[4:6]
	deps={"01":"CSE","02":"ECE","03":"ME","04":"CE","05":"bdes","06":"BT","07":"CL","08":"EEE","21":"EPh","22":"CST","23":"MC"}
	return deps[dep]

def displayResult(dept, sem, roll): #result display fuction
	win = MainNotebook(dept,sem,roll) #calling notebookview
	win.connect("delete-event", Gtk.main_quit)
	win.show_all()
	Gtk.main()


class MainNotebook(Gtk.Window):

	def __init__(self,dept="CSE",sem=3,roll='140101063'):
		Gtk.Window.__init__(self, title="Acad-Hub")
		self.set_default_size(300, 300)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.set_border_width(10)

		self.notebook = Gtk.Notebook() #init. new notebook view
		self.add(self.notebook)
		self.notebook.set_scrollable(True)

		courseBooks = showBooks(dept, sem) #getting an array of coursebooks and rel. info
		self.page1 = Gtk.Box() 
		self.page1.set_border_width(10)
		books_list_store = Gtk.ListStore(str, str, str, str, str, str, str) #new liststore for books
		for book in courseBooks:
			books_list_store.append(list(book))

		books_tree_view = Gtk.TreeView(books_list_store) #adding to treeview

		#adding columns
		for i, col_title in enumerate(["Course", "Code", "Title", "Author", "Publications/Edition", "Library Availability", "Download link"]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(col_title, renderer, text=i)
			column.set_max_width(150)
			column.set_sort_column_id(i) #allowing sortable columns
			books_tree_view.append_column(column) 
			

		

		self.page1.pack_start(books_tree_view, True, True, 0)

		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

		for book in courseBooks:
			button = Gtk.LinkButton(book[6],label="Download")
			vbox.pack_start(button, True, True, 0)

		self.page1.pack_start(vbox,True,True,0)

		self.notebook.append_page(self.page1, Gtk.Label('Books Info'))
		#adding books page

		self.page2 = Gtk.Box()
		self.page2.set_border_width(10)
		examtt= listTT(dept,sem) #fetching exam time table array
		exams_list_store = Gtk.ListStore(str,str, str,str,str,str) #creating liststore for the same
		for exam in examtt:
			exams_list_store.append(list(exam))

		exams_tree_view = Gtk.TreeView(exams_list_store)

		for i, col_title in enumerate(["Course", "Course Name","Day","End-Sem Date","End-Sem Day", "Venue"]): #rendering data
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(col_title, renderer, text=i)
			column.set_sort_column_id(i)

			exams_tree_view.append_column(column)

		self.page2.pack_start(exams_tree_view, True, True, 0)
		self.notebook.append_page(self.page2, Gtk.Label('Exam Time Table'))

		#adding exam time table

		self.page3 = Gtk.Box()
		self.page3.set_border_width(10)
		courses= showBooks(dept,sem,"courses") #fetching course info and credits
		course_list_store = Gtk.ListStore(str, str, str, str, str , str)
		for course in courses:
			course_list_store.append(list(course))
		course_tree_view = Gtk.TreeView(course_list_store)

		for i, col_title in enumerate(["Course-Code", "Course Name", "L", "T", "P" , "C"]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(col_title, renderer, text=i)
			column.set_sort_column_id(i)
			course_tree_view.append_column(column)

		self.page3.pack_start(course_tree_view, True, True, 0)
		self.notebook.append_page(self.page3, Gtk.Label('Course Information'))
		#adding the course page to notebook view

		self.page4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.page4.set_border_width(10)
		grid = Gtk.Grid(column_homogeneous=True, column_spacing=10, row_spacing=10)

		self.scrolledwindow = Gtk.ScrolledWindow()
		self.scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
									   Gtk.PolicyType.AUTOMATIC)

		self.liststore_files = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str, str)


		self.course_combo = Gtk.ComboBoxText()
		self.course_combo.set_entry_text_column(0)
		self.courseList = []
		for course in courses:
			self.courseList.append(str(course[0]))
		for course in self.courseList:
			self.course_combo.append_text(course)
		self.course_combo.connect('changed', self.on_course_combo_changed)

		self.course_combo.set_active(0)

		buttonbox = Gtk.ButtonBox(Gtk.Orientation.HORIZONTAL)
		buttonbox.set_layout(Gtk.ButtonBoxStyle.EDGE)

		buttonbox.add(self.course_combo)
	
		button_choose_file = Gtk.Button("Choose File")
		button_choose_file.connect("clicked", self.on_file_clicked)
		buttonbox.add(button_choose_file)

		button_upload = Gtk.Button("Upload")
		button_upload.connect("clicked", self.on_upload_clicked,roll)
		buttonbox.add(button_upload)

		self.updateFileList()
		grid.attach(self.scrolledwindow, 0, 0, 1, 1)
		grid.attach_next_to(buttonbox, self.scrolledwindow,
								 Gtk.PositionType.BOTTOM, 1, 1)

		self.page4.pack_start(grid, True, True, 0)
		self.notebook.append_page(self.page4, Gtk.Label('Notes'))


	def on_course_combo_changed(self, combo):
		self.updateFileList()
		index = combo.get_active()
		combo.set_active(index)

	def on_upload_clicked(self, widget,roll):
		try:
			if self.fileToUpload != "":
				index = self.course_combo.get_active()
				course=self.courseList[index]
				uploadFile(self.fileToUpload, roll, course)
				self.updateFileList()
		except:
			pass

	def on_file_clicked(self, widget):
		dialog = Gtk.FileChooserDialog("Please choose a file", self,
			Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

		self.add_filters(dialog)
		self.fileToUpload = ""
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.fileToUpload = dialog.get_filename()
		dialog.destroy()


	def add_filters(self, dialog):
		filter_text = Gtk.FileFilter()
		filter_text.set_name("Text files")
		filter_text.add_mime_type("text/plain")
		dialog.add_filter(filter_text)

		filter_py = Gtk.FileFilter()
		filter_py.set_name("Python files")
		filter_py.add_mime_type("text/x-python")
		dialog.add_filter(filter_py)

		filter_any = Gtk.FileFilter()
		filter_any.set_name("Any files")
		filter_any.add_pattern("*")
		dialog.add_filter(filter_any)

	def updateFileList(self):
		pics_list,pics_name,uploader_list,upload_time = listUploads(self.courseList[self.course_combo.get_active()])
		self.liststore_files.clear()
		for name, pic, uploader, time in zip(pics_name, pics_list, uploader_list, upload_time):
			pxbf = GdkPixbuf.Pixbuf.new_from_file_at_scale(pic, 50, 50, True)
			self.liststore_files.append([pxbf, name, uploader, time])

		treeview = Gtk.TreeView(model=self.liststore_files)
		treeview.set_hexpand(True)
		treeview.set_vexpand(True)
		# creamos las columnas del TreeView
		renderer_pixbuf = Gtk.CellRendererPixbuf()
		column_pixbuf = Gtk.TreeViewColumn('Preview', renderer_pixbuf, pixbuf=0)
		column_pixbuf.set_alignment(0.5)
		treeview.append_column(column_pixbuf)

		renderer_text = Gtk.CellRendererText(weight=600)
		renderer_text.set_fixed_size(200, -1)
		column_text = Gtk.TreeViewColumn('Filename', renderer_text, text=1)
		column_text.set_sort_column_id(1)
		column_text.set_alignment(0.5)
		treeview.append_column(column_text)

		renderer_text = Gtk.CellRendererText(weight=600)
		renderer_text.set_fixed_size(200, -1)
		column_text = Gtk.TreeViewColumn('Uploaded By', renderer_text, text=2)
		# column_text.set_sort_column_id(1)
		column_text.set_alignment(0.5)
		treeview.append_column(column_text)

		renderer_text = Gtk.CellRendererText()
		renderer_text.set_fixed_size(200, -1)
		column_text = Gtk.TreeViewColumn('Upload time', renderer_text, text=3)
		column_text.set_sort_column_id(3)
		column_text.set_alignment(0.5)
		treeview.append_column(column_text)      

		self.scrolledwindow.add_with_viewport(treeview)  

	# def on_folder_clicked(self, widget):
	#     dialog = Gtk.FileChooserDialog("Please choose a folder", self,
	#         Gtk.FileChooserAction.SELECT_FOLDER,
	#         (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
	#          "Select", Gtk.ResponseType.OK))
	#     dialog.set_default_size(800, 400)

	#     response = dialog.run()
	#     if response == Gtk.ResponseType.OK:
	#         print("Select clicked")
	#         print("Folder selected: " + dialog.get_filename())
	#     elif response == Gtk.ResponseType.CANCEL:
	#         print("Cancel clicked")
	#     dialog.destroy()

class MainBox(Gtk.Window):

	def __init__(self):
		
		Gtk.Window.__init__(self, title="SemBegins!") #main window
		self.set_default_size(200, 100) #setting default size
		self.set_border_width(10)		

		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		label = Gtk.Label("Enter Your Roll Number:")
		vbox.pack_start(label, True, True, 0)
		
		self.entry = Gtk.Entry() #entry box
		self.entry.set_max_length(9) 
		self.entry.set_text("140101063") #default text value
		vbox.pack_start(self.entry, True, True, 0)

		button = Gtk.Button(label="Submit")
		button.connect("clicked", self.buttonClicked) #button click event
		vbox.pack_start(button, True, True, 0)
		self.add(vbox)

	def buttonClicked(self, widget):
		self.roll=self.entry.get_text()
		self.sem=semFinder(self.roll)
		self.dept=depFinder(self.roll)
		displayResult(self.dept, self.sem, self.roll)

win = MainBox() #calling the mainbox
win.connect("delete-event", Gtk.main_quit) #adding the quit event listener
win.show_all()
Gtk.main()