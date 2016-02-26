from gi.repository import Gtk, GObject
from webcrawler import showBooks
from time import gmtime, strftime
from exam import listTT


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
    deps={"01":"CSE","02":"ECE","03":"ME","04":"CE","06":"BT","07":"CL","08":"EEE","21":"EPh","22":"CST","23":"MC"}
    return deps[dep]

def displayResult(dept, sem): #result display fuction
	win = MainNotebook(dept,sem) #calling notebookview
	win.connect("delete-event", Gtk.main_quit)
	win.show_all()
	Gtk.main()


class MainNotebook(Gtk.Window):

    def __init__(self,dept="CSE",sem=3):

        Gtk.Window.__init__(self, title="Acad-Hub")
        self.set_border_width(3)

        self.notebook = Gtk.Notebook() #init. new notebook view
        self.add(self.notebook)

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
            column.set_sort_column_id(i) #allowing sortable columns
            books_tree_view.append_column(column) 

        self.page1.pack_start(books_tree_view, True, True, 0)
        self.notebook.append_page(self.page1, Gtk.Label('Books Info'))
        #adding books page

        self.page2 = Gtk.Box()
        self.page2.set_border_width(10)
        examtt= listTT(dept,sem) #fetching exam time table array
        exams_list_store = Gtk.ListStore(str, str,str, str,str,str,str) #creating liststore for the same
        for exam in examtt:
            exams_list_store.append(list(exam))

        exams_tree_view = Gtk.TreeView(exams_list_store)

        for i, col_title in enumerate(["Course", "Day","Mid-Sem Date","Mid-Sem Day","End-Sem Date","End-Sem Day", "Venue"]): #rendering data
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
        displayResult(self.dept, self.sem)

win = MainBox() #calling the mainbox
win.connect("delete-event", Gtk.main_quit) #adding the quit event listener
win.show_all()
Gtk.main()