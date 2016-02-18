from gi.repository import Gtk
from webcrawler import showBooks



def displayResult(dept, sem):
	win = TreeViewWindow(dept,sem)
	win.connect("delete-event", Gtk.main_quit)
	win.show_all()
	Gtk.main()


class TreeViewWindow(Gtk.Window):
    
    def __init__(self, dept="CE", sem=3):
        Gtk.Window.__init__(self, title="Course Books")
        courseBooks = showBooks(dept, sem)
        layout = Gtk.Box()
        self.add(layout)
        books_list_store = Gtk.ListStore(str, str, str, str, str)
        for book in courseBooks:
            books_list_store.append(list(book))

        books_tree_view = Gtk.TreeView(books_list_store)

        for i, col_title in enumerate(["Course", "code", "Title", "Author", "Publications/Edition"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            books_tree_view.append_column(column)

        layout.pack_start(books_tree_view, True, True, 0)


class ComboBoxWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="SemBegins!")

        self.set_border_width(10)		

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        self.dept = "CSE"
        self.sem = "3"

        deptbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label = Gtk.Label("Choose Department: ")
        depts = ["CSE", "ECE", "EEE", "ME", "CE", "BT", "CL", "EPh", "CST", "MC"]
        dept_combo = Gtk.ComboBoxText()
        dept_combo.set_entry_text_column(0)
        dept_combo.connect("changed", self.on_dept_combo_changed)
        for dept in depts	:
            dept_combo.append_text(dept)
        dept_combo.set_active(0)
        deptbox.pack_start(label, False, False, 0)
        deptbox.pack_start(dept_combo, False, False, 0)
        vbox.pack_start(deptbox, False, False, 0)

        sembox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        label = Gtk.Label("Choose Semester: ")
        sem_combo = Gtk.ComboBoxText()
        sem_combo.set_entry_text_column(0)
        sem_combo.connect("changed", self.on_sem_combo_changed)
        for i in range(1,9)	:
            sem_combo.append_text("Semester " + str(i))
        sem_combo.set_active(2)
        sembox.pack_start(label, False, False, 0)
        sembox.pack_start(sem_combo, False, False, 0)
        vbox.pack_start(sembox, False, False, 0)

        button = Gtk.Button(label="Submit")
        button.connect("clicked", self.buttonClicked)
        vbox.pack_start(button, False, False, 0)
        self.add(vbox)

    def on_dept_combo_changed(self, combo):
        text = combo.get_active_text()
        if text != None:
        	self.dept = text

    def on_sem_combo_changed(self, combo):
        text = combo.get_active_text()
        if text != None:
        	self.sem = text[len(text)-1]

    def buttonClicked(self, widget):
    	displayResult(self.dept, self.sem)

win = ComboBoxWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()