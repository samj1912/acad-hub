from gi.repository import Gtk, GObject
from webcrawler import showBooks
from time import gmtime, strftime
from exam import listTT


def semFinder(roll):
    a=str(roll)
    year=a[0:2]
    m=strftime("%m", gmtime())
    y=strftime("%y", gmtime())
    ans = ((float(m)-1)/12)+int(y)-int(year)
    return int(ans*2)

def depFinder(roll):

    a=str(roll)
    dep=a[4:6]
    deps={"01":"CSE","02":"ECE","03":"ME","04":"CE","06":"BT","07":"CL","08":"EEE","21":"EPh","22":"CST","23":"MC"}
    return deps[dep]

def displayResult(dept, sem):
	win = MyWindow(dept,sem)
	win.connect("delete-event", Gtk.main_quit)
	win.show_all()
	Gtk.main()


# class TreeViewWindow(Gtk.Window):
    
#     def __init__(self, dept="CE", sem=3):
#         Gtk.Window.__init__(self, title="Course Books")
#         courseBooks = showBooks(dept, sem)
#         layout = Gtk.Box()
#         self.add(layout)
#         books_list_store = Gtk.ListStore(str, str, str, str, str, str)
#         for book in courseBooks:
#             books_list_store.append(list(book))

#         books_tree_view = Gtk.TreeView(books_list_store)

#         for i, col_title in enumerate(["Course", "code", "Title", "Author", "Publications/Edition", "Download link"]):
#             renderer = Gtk.CellRendererText()
#             column = Gtk.TreeViewColumn(col_title, renderer, text=i)
#             books_tree_view.append_column(column)

#         layout.pack_start(books_tree_view, True, True, 0)

class MyWindow(Gtk.Window):

    def __init__(self,dept="CSE",sem=3):
        Gtk.Window.__init__(self, title="Acad-Hub")
        self.set_border_width(3)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        courseBooks = showBooks(dept, sem)
        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        books_list_store = Gtk.ListStore(str, str, str, str, str, str)
        for book in courseBooks:
            books_list_store.append(list(book))

        books_tree_view = Gtk.TreeView(books_list_store)

        for i, col_title in enumerate(["Course", "Code", "Title", "Author", "Publications/Edition", "Download link"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            books_tree_view.append_column(column)

        self.page1.pack_start(books_tree_view, True, True, 0)


        self.notebook.append_page(self.page1, Gtk.Label('Course Info'))

        self.page2 = Gtk.Box()
        self.page2.set_border_width(10)
        examtt= listTT(dept,sem)
        exams_list_store = Gtk.ListStore(str, str, str)
        for exam in examtt:
            exams_list_store.append(list(exam))

        exams_tree_view = Gtk.TreeView(exams_list_store)

        for i, col_title in enumerate(["Course", "Date", "Venue"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            exams_tree_view.append_column(column)

        self.page2.pack_start(exams_tree_view, True, True, 0)


        self.notebook.append_page(self.page2, Gtk.Label('Exam Time Table'))

# win = MyWindow()
# win.connect("delete-event", Gtk.main_quit)
# win.show_all()
# Gtk.main()

class ComboBoxWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="SemBegins!")
        self.set_size_request(200, 100)

        self.timeout_id = None


        self.set_border_width(10)		

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        label = Gtk.Label("Enter Your Roll Number:")
        vbox.pack_start(label, True, True, 0)
                        
        self.dept = "CSE"
        self.sem = "3"
        self.entry = Gtk.Entry()
        self.entry.set_max_length(9)
        self.entry.set_text("140101063")
        vbox.pack_start(self.entry, True, True, 0)

        button = Gtk.Button(label="Submit")
        button.connect("clicked", self.buttonClicked)
        vbox.pack_start(button, False, False, 0)
        self.add(vbox)

    def buttonClicked(self, widget):
        self.roll=self.entry.get_text()
        self.sem=semFinder(self.roll)
        self.dept=depFinder(self.roll)
        displayResult(self.dept, self.sem)
        self.destroy()

win = ComboBoxWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()