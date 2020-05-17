import tkinter.font as tkFont
import tkinter as ttk
from tkinter import *
from tkinter import messagebox
import datetime
import os.path
import os

"""
This code creates a Tkinter based Expense Tracker application which allows the user to keep a track of his/her money. 
"""

#===============Variables==================
#Storing the color for background and foreground for switching between dark and light mode
background_color = "#ffffff"
foreground_color = "#000000"

#color variables to store variants of that color
green_color= 'green'
red_color = 'red'
blue_color = 'blue'

#Store the total amount of that particular section
money_var = 0.0
expense_var = 0.0
budget_var = 0.0

#Dark mode ON/OFF
isDark = False

#Store the currency (Set as an empty string by default)
currency = ""

#dictionaries to store the categories in each section
money_items = {
    "CASH" : 0,
    "CARD" : 0
}
budget_items = {}
expense_items = {}
goal_items = {}

#name of the files which needs to be created or opened
data_filename = 'data.txt'
log_filename = 'log.txt'


def createfile():
    """Creates a file for the storing the data of the app."""
    file = open(data_filename, 'w')
    file.write('background_color = ' + background_color)
    file.write('\nforeground_color = ' + foreground_color)
    file.write('\nmoney_var = ' + str(money_var))
    file.write('\nexpense_var = ' + str(expense_var))
    file.write('\nbudget_var = ' + str(budget_var))
    file.write('\nisDark = ' + str(isDark))
    file.write('\ncurrency = ' + currency)
    file.write('\n\ndictionaries')
    file.write('\nmoney_items = ' + str(money_items))
    file.write('\nexpense_items = ' + str(expense_items))
    file.write('\nbudget_items = ' + str(budget_items))
    file.write('\ngoal_items = ' + str(goal_items))
    file.close()

def open_file():
    """Opens the file which contains the data of the file and implements that data to the app."""
    global background_color
    global foreground_color
    global money_var
    global expense_var
    global budget_var
    global isDark
    global currency

    file = open(data_filename)

    #First while-loop is to read and assign the variables
    line = file.readline()
    line = line.strip('\n')
    while line != 'dictionaries':
        words = line.split(' ')
        if words[0] == 'background_color':
            background_color = words[2]
        elif words[0] == 'foreground_color':
            foreground_color = words[2]
        elif words[0] == 'money_var':
            money_var = float(words[2])
        elif words[0] == 'expense_var':
            expense_var = float(words[2])
        elif words[0] == 'budget_var':
            budget_var = float(words[2])
        elif words[0] == 'isDark':
            if words[2] == 'True':
                isDark = True
            else:
                isDark = False
        elif words[0] == 'currency':
            currency = words[2]

        line = file.readline()
        line = line.strip('\n')
    
    #Second while-loop is to read and assign the dictionaries
    line = file.readline()
    line = line.strip('\n')
    while line != '':
        words = line.split('{')
        option = words[0].strip(' = ')
        words = words[1].strip('}')
        key_value_pairs = words.split(',')

        if len(words) != 0:
            for i in key_value_pairs:
                i = i.strip(' ')
                key_value = i.split(': ')
                key_value[0] = key_value[0].strip('"')
                
                if option == "money_items":
                    money_items[key_value[0].strip("'")] = float(key_value[1])
                elif option == "expense_items":
                    expense_items[key_value[0].strip("'")] = float(key_value[1])
                elif option == "budget_items":
                    budget_items[key_value[0].strip("'")] = float(key_value[1])
                elif option == "goal_items":
                    goal_items[key_value[0].strip("'")] = float(key_value[1])
            
        line = file.readline()
        line = line.strip('\n')

def update_file():
    """Updates the file which contains the data when the user quits the app."""
    global background_color
    global foreground_color
    global money_var
    global expense_var
    global budget_var
    global isDark
    global currency

    file = open(data_filename, 'w')
    file.write('background_color = ' + background_color)
    file.write('\nforeground_color = ' + foreground_color)
    file.write('\nmoney_var = ' + str(money_var))
    file.write('\nexpense_var = ' + str(expense_var))
    file.write('\nbudget_var = ' + str(budget_var))
    file.write('\nisDark = ' + str(isDark))
    file.write('\ncurrency = ' + currency)
    file.write('\n\ndictionaries')
    file.write('\nmoney_items = ' + str(money_items))
    file.write('\nexpense_items = ' + str(expense_items))
    file.write('\nbudget_items = ' + str(budget_items))
    file.write('\ngoal_items = ' + str(goal_items))
    file.close()

#To check if the file exists or not
file_exists = os.path.isfile(data_filename)

#If the file exists then open the file else create a new file
if file_exists:
    open_file()
else:
    createfile()

#==========================Classes=================================

class tracker_func:
    """
    This is a class to track the amount of money.

    Attributes:
        None
    """

    def callback(self, window):
        """
        The function to close a specific window and show the root window.

        Parameters:
            window (tkinter.Toplevel): The window to be closed.  
        """
    
        root.deiconify()
        window.destroy()
    
    def callback_toplevel(self, window, window_str):
        """
        The function to close a specific window and open another window.

        Parameters:
            window (tkinter.Toplevel): The window to be closed.  
            window_str (str): The name of the window to be opened. 
        """

        window.destroy()
        track.choose(window_str)

    def onFrameConfigure(self, canvas):
        """
        Reset the scroll region to encompass the inner frame.
        
        Parameters:
            canvas (tkinter.Canvas): widget which requires changes.
        """
        canvas.configure(scrollregion=canvas.bbox("all"))

    def items_select(self, option):
        """
        The function to return a dictionary according to the section.

        Parameters:
            option (str): The name of the section.

        Returns:
            dictionary: The dictionary of categories which belongs to a section.
        """

        if option == "money":
            return money_items
        elif option == "expense":
            return expense_items
        elif option == "budget":
            return budget_items
        elif option == "goal":
            return goal_items

    def choose(self, option):
        """
        The function to add specific widgets to the window and perform specific tasks according to the section.

        Parameters:
            option (str): The name of the section.  
        """
        
        dict_items = self.items_select(option)

        #Creating a Window and setting it up
        choice_win =  Toplevel(root)
        choice_win.title("Choose an Option")
        window_center(choice_win, 300, 223)
        choice_win.resizable(False, False)
        choice_win.config(background=background_color)
        choice_win.iconbitmap(logo_loc)

        def populate(frame):
            """
            The function fill the frame with specific buttons or labels depending on the section.

            Parameters:
                frame (tkinter.Frame): frame to contain the button and label widgets.
            """
            Label(frame ,text=option.upper(), font=custom_font, background=background_color, foreground=foreground_color,width=25).pack(pady=2, fill=BOTH)
            
            #Condition to add a Label if there are no categories
            if len(dict_items) == 0:
                Label(frame, text="No " + option.upper(), font='calibri 11 bold', border=0, background=background_color, foreground=foreground_color, width=25).pack(ipady=3, padx=5, pady=2, fill=BOTH)
            
            #Loop to populate the frame
            for i in dict_items:
                #Condition to check if the category is goal
                if option == 'goal':
                    Label(frame, text=i +" : DHS "+str(dict_items[i]), font='calibri 11 bold', border=0, background=background_color, foreground=foreground_color, width=25).pack(ipady=3, padx=5, pady=2, fill=BOTH)
                else:
                    Button(frame, text=i, font='calibri 11 bold', border=0, background='#00bdaa', foreground=foreground_color, width=25,command=lambda i=i: self.add(i, option)).pack(ipady=8, padx=5, pady=2, fill=BOTH)
            
            #Condition to check if the category is budget or expense to add the specific Buttons
            if option == 'budget' or option == 'expense' or option == 'goal':
                add_btn = Button(frame, text="Add a Category",font='calibri 11 bold', border=0, background='#fa744f', foreground=foreground_color, width=25, command=lambda: self.add_func(choice_win, option.upper()))
                remove_btn = Button(frame, text="Remove a Category",font='calibri 11 bold', border=0, background='#fa744f', foreground=foreground_color, width=25, command=lambda: self.remove_func(choice_win, option.upper()))

                #Disabling the remove button if there are no categories
                if len(dict_items) == 0:
                    remove_btn.config(state=DISABLED, bg='#FAB8AD')

                add_btn.pack(ipady=8, padx=5, pady=2, fill=BOTH)
                remove_btn.pack(ipady=8, padx=5, pady=2, fill=BOTH)

            Button(frame, text="BACK", font='calibri 11 bold', border=0, background='#00bdaa', foreground=foreground_color, command= lambda: self.callback(choice_win)).pack(ipady=8, padx=5, pady=2, fill=BOTH)
        
        #Certain steps to make a scrollbar for widgets
        canvas = Canvas(choice_win, borderwidth=0, border=0, background=background_color,width=280, highlightthickness=0)
        frame = Frame(canvas, border=0, background=background_color)
        vsb = Scrollbar(choice_win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4,4), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda event, canvas=canvas: self.onFrameConfigure(canvas))
        populate(frame)

        #Functions to make the window more usable
        root.withdraw()
        choice_win.focus_force()
        choice_win.protocol("WM_DELETE_WINDOW", lambda: self.callback(choice_win))

    def add(self, option_str, option):
        """
        The function to open another window depending on the category.

        Parameters:
            option_str (str): The name of the category.
            option (str): The name of the section.
        """

        #Creating a Window and setting it up
        money_win = Toplevel(root)
        money_win.title("Add Money to " + option_str)
        window_center(money_win, 300, 150)
        money_win.resizable(False, False)
        money_win.focus_force()
        money_win.config(background=background_color)
        money_win.iconbitmap(logo_loc)

        amount_text = Label(money_win, text="Enter Amount : ", font=custom_font, background=background_color, foreground=foreground_color)
        amount_text.pack()

        amount_input = Entry(money_win, font='calibri 11',border=0, justify='center', bg='#dee3e2')
        amount_input.insert(0,"Enter Amount")
        amount_input.pack(ipady=5)

        amount_input.bind("<FocusIn>", lambda args: amount_input.delete('0', 'end'))
        
        submit = Button(money_win, text="Add", font='calibri 11 bold', border=0, background='#00bdaa', foreground=foreground_color)
        submit.pack(pady=5, ipadx=10)

        #Conditions to make the submit button call different functions depending on the section
        if option == "money":
            submit.config(command=lambda: self.adding_money(option_str.upper(), amount_input, money_win, option))
        elif option == "expense":
            submit.config(command=lambda: self.adding_expense(option_str.upper(), amount_input, money_win, option))
        elif option == "budget":
            submit.config(command=lambda: self.adding_budget(option_str.upper(), amount_input, money_win, option))

        Button(money_win, text="BACK", font='calibri 11 bold', border=0, background='#00bdaa', foreground=foreground_color, command= money_win.destroy).pack(ipady=8, padx=5, pady=2, fill=BOTH)
    
    def adding_money(self, money_str, a_input, window, option):
        """
        The function to open another window depending on the category.

        Parameters:
            money_str (str): The name of the category in section 'money'.
            a_input (tkinter.Entry): The Entry widget which stores a value.
            window (tkinter.Toplevel): The window from which this function was called.
            option (str): The name of the section.
        """

        amount = 0
        amount = a_input.get()
        a_input.delete(0,END)

        #Trying to convert the amount string to float
        try:
            amount = float(amount)
        except:
            messagebox.showinfo("ERROR", "Please Input a Number")
            return

        if money_str == "CARD":
            money_items['CARD'] += amount
        elif money_str == "CASH":
            money_items['CASH'] += amount

        #Calling the method to add event to the log file
        log_file_write(option, money_str, amount)
        money_source()
        window.destroy()

    def adding_expense(self, expense_str, a_input, window, option):
        """
        The function to open another window depending on the category.

        Parameters:
            expense_str (str): The name of the category in section 'expense'.
            a_input (tkinter.Entry): The Entry widget which stores a value.
            window (tkinter.Toplevel): The window from which this function was called.
            option (str): The name of the section.
        """

        global budget_var
        global budget_items
        amount=0
        amount = a_input.get()
        a_input.delete(0,END)

        #Trying to convert the amount string to float
        try:
            amount = float(amount)
        except:
            messagebox.showinfo("ERROR", "Please Input a Number")
            return

        #Nested Conditions to check if expense can be added 
        if budget_var >= amount:
            for x,y in budget_items.items():
                if x == expense_str:
                    if y >= amount:
                        budget_items[x] -= amount
                    elif y<amount and y>=0:
                        ans = messagebox.askyesno("Are You Sure?", "Not Enough Money in " + expense_str + " Budget. Do you still want to Continue?")
                        if ans == True:
                            leftover_amt = amount - y
                            budget_items[x] = 0
                            if money_items['CASH'] >= leftover_amt and money_items['CASH'] != 0:
                                money_items['CASH'] -= leftover_amt
                            elif money_items['CARD'] >= leftover_amt and money_items['CASH'] < leftover_amt and money_items['CARD'] != 0:
                                money_items['CARD'] -= leftover_amt
                            else:
                                messagebox.showinfo("NOTE", "Not Enough Money")
                                return
                            money_source()
                        elif ans == False:
                            return
                    else:
                        return

        elif budget_var<amount and budget_var>0:
            ans = messagebox.askyesno("Are You Sure?", "Not Enough Money in " + expense_str + " Budget. Do you still want to Continue?")
            if ans == True:
                leftover_amt = amount - budget_var
                money_items['CASH'] -= leftover_amt
                for i in budget_items:
                    budget_items[i] = 0
                money_source()
            elif ans == False:
                return

        elif budget_var <= 0:
            ans = messagebox.askyesno("Are You Sure?", "Not Enough Money in Budget. Do you still want to Continue?")
            if ans == True:
                if money_items['CASH'] >= amount and money_items['CASH'] != 0:
                    money_items['CASH'] -= amount
                elif money_items['CARD'] >= amount and money_items['CARD'] != 0:
                    money_items['CARD'] -= amount
                else:
                    messagebox.showinfo("NOTE", "Not Enough Money")
                    return
                money_source()
            elif ans == False:
                return

        #loop which adds the amount to a specific categories
        for i,y in expense_items.items():
            if i == expense_str:      
                expense_items[i] += amount
        
        #Calling the method to add event to the log file
        log_file_write(option, expense_str, amount)
        expense_source()
        window.destroy()

    def adding_budget(self, budget_str, a_input, window, option):
        """
        The function to open another window depending on the category.

        Parameters:
            budget_str (str): The name of the category in section 'budget'.
            a_input (tkinter.Entry): The Entry widget which stores a value.
            window (tkinter.Toplevel): The window from which this function was called.
            option (str): The name of the section.
        """

        amount = 0
        amount = a_input.get()
        a_input.delete(0,END)

        #Trying to convert the amount string to float
        try:
            amount = float(amount)
        except:
            messagebox.showinfo("ERROR", "Please Input a Number", icon="error")
            return

        #Checks if the 'money' section has enough balance
        if amount > money_var:
            messagebox.showinfo("NOTE", "Not Enough Money")
            window.destroy()
            return

        #Loop which adds the amount to a specific categories
        for i,y in budget_items.items():
            if i == budget_str:      
                budget_items[i] += amount
        
        #Calling the method to add event to the log file
        log_file_write(option, budget_str, amount)
        budget_source(amount)
        window.destroy()

    def info(self, option):
        """
        The function to open a window with the info of the categories in that specific section.

        Parameters:
            option (str): The name of the section.  
        """

        dict_items = self.items_select(option)
        global currency

        #Creating a Window and setting it up
        info_win = Toplevel(root)
        info_win.title(option.upper() + " Info")
        window_center(info_win, 300, 200)
        info_win.resizable(False,False)
        info_win.focus_force()
        info_win.config(background=background_color)
        info_win.iconbitmap(logo_loc)

        def populate(frame):
            """
            The function fill the frame with specific labels depending on the section.

            Parameters:
                frame (tkinter.Frame): frame to contain the button and label widgets.
            """

            #Condition to add a Label if there are no categories
            if len(dict_items) == 0:
                Label(frame, text="No "+ option.upper(), font='calibri 11 bold', border=0, background=background_color, foreground=foreground_color, width=35).pack(ipady=3, padx=5, pady=2, fill=BOTH)
            
            #Loop to populate the frame with Labels    
            for x,y in dict_items.items():
                Label(frame, text=x + " : " +currency+" "+ str(y), font='calibri 11 bold', background=background_color, foreground=foreground_color, width=35).pack(pady=2)
        
        #Certain steps to make a scrollbar for widgets
        canvas = Canvas(info_win, borderwidth=0, border=0, background=background_color,width=280, highlightthickness=0)
        frame = Frame(canvas, border=0, background=background_color)
        vsb = Scrollbar(info_win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4,4), window=frame, anchor="nw")

        frame.bind("<Configure>", lambda event, canvas=canvas: self.onFrameConfigure(canvas))

        populate(frame)

    def add_func(self, window, window_str):
        """
        The function which creates a window which allows the user input a new category which he can add to a section.

        Parameters:
            window (tkinter.Toplevel): The window to be closed.  
            window_str (str): The name of the window to be opened. 
        """

        window.destroy()

        #Creating a Window and setting it up
        add_win = Toplevel(root)
        add_win.title("Add Category")
        window_center(add_win, 300, 170)
        add_win.resizable(False, False)
        add_win.config(background=background_color)
        add_win.iconbitmap(logo_loc)

        Label(add_win, text="Enter Name of " + window_str + " : ", font=custom_font, background=background_color, foreground=foreground_color).pack(pady=10)

        cat_input = Entry(add_win, font='calibri 11',border=0, justify='center', bg='#dee3e2')
        cat_input.insert(0,"Enter Category")
        cat_input.pack(ipady=5)

        cat_input.bind("<FocusIn>", lambda args: cat_input.delete('0', 'end'))
        
        #Adding some extra widgets if the section is 'goal'
        if window_str.lower() == 'goal':
            add_win.geometry("300x230")
            Label(add_win, text="Amount to Reach the Goal : ", font=custom_font, background=background_color, foreground=foreground_color).pack(pady=(5,2))

            value_input = Entry(add_win, font='calibri 11',border=0, justify='center', bg='#dee3e2')
            value_input.insert(0,"Enter Value")
            value_input.pack(ipady=5)

            value_input.bind("<FocusIn>", lambda args: value_input.delete('0', 'end'))

        submit = Button(add_win, text="Add", font='calibri 11 bold', border=0, background='#00bdaa', foreground=foreground_color, command=lambda: adding_cat())
        submit.pack(pady=5, ipadx=10)

        Button(add_win, text="BACK", font='calibri 11 bold', border=0, background='#00bdaa', foreground=foreground_color, command= lambda: self.callback_toplevel(add_win, window_str.lower())).pack(ipady=8, padx=5, pady=2, fill=BOTH)

        add_win.focus_force()
        
        add_win.protocol("WM_DELETE_WINDOW", lambda: self.callback_toplevel(add_win, window_str.lower()))

        def adding_cat():
            """The function to check if the new category is valid or not."""

            dict_items = self.items_select(window_str.lower())
            category = cat_input.get()
            category = category.upper()

            #Some if conditions to check for errors
            if category == "" or category == "ENTER CATEGORY":
                messagebox.showinfo("ERROR", "Please Input a " + window_str)
                return

            for x in dict_items:
                if x == category:
                    messagebox.showinfo("ERROR", window_str + " already Exists")
                    return

            if window_str == 'GOAL':
                goal_value = value_input.get()

                try:
                    goal_value = float(goal_value)
                except:
                    messagebox.showinfo("ERROR", "Please Input a Number")
                    return
                
                goal_items[category] = goal_value
            #if there are are no more errors then the else statement is called
            else:
                expense_items[category] = 0
                budget_items[category] = 0
            
            self.callback_toplevel(add_win, window_str.lower())

    def remove_func(self, window, window_str):
        """
        The function which creates a window which allows the user input a existing category which he can remove from a section.

        Parameters:
            window (tkinter.Toplevel): The window to be closed.  
            window_str (str): The name of the window to be opened. 
        """

        window.destroy()

        #Creating a Window and setting it up
        remove_win = Toplevel(root)
        remove_win.title("Remove From " + window_str)
        window_center(remove_win, 300, 170)
        remove_win.resizable(False, False)
        remove_win.config(background=background_color)
        remove_win.iconbitmap(logo_loc)
        remove_win.focus_force()

        Label(remove_win, text=("Enter Name of " + window_str + " : "), font=custom_font, background=background_color, foreground=foreground_color).pack(pady=10)

        cat_input = Entry(remove_win, font='calibri 11',border=0, justify='center', bg='#dee3e2')
        cat_input.insert(0,"Enter Category")
        cat_input.pack(ipady=5)

        cat_input.bind("<FocusIn>", lambda args: cat_input.delete('0', 'end'))

        submit = Button(remove_win, text="Remove", font='calibri 11 bold', border=0, background='#00bdaa', foreground=foreground_color, command=lambda: self.removing_cat(remove_win, window_str, cat_input))
        submit.pack(pady=5, ipadx=10)   

        Button(remove_win, text="BACK", font='calibri 11 bold', border=0, background='#00bdaa', foreground=foreground_color, command= lambda: self.callback_toplevel(remove_win, window_str.lower())).pack(ipady=8, padx=5, pady=2, fill=BOTH)
        remove_win.protocol("WM_DELETE_WINDOW",lambda: self.callback_toplevel(remove_win, window_str.lower()))

    def removing_cat(self, window, window_str, c_input):
        """
        The function which checks if the existing category can be removed.

        Parameters:
            window (tkinter.Toplevel): The window to be closed.  
            window_str (str): The name of the window to be opened. 
        """

        category = c_input.get()
        category = category.upper()

        #Some if conditions to check for errors
        if category == "" or category == "ENTER CATEGORY":
            messagebox.showinfo("ERROR", "Please Input a " + window_str)
            return
        
        if window_str == 'GOAL':
            try:
                del goal_items[category]
                messagebox.showinfo("SUCCESS","Goal Deleted")
            except:
                messagebox.showinfo("ERROR", "Goal Doesn't Exists")
                return
        else:
            if category in budget_items.keys():
                if budget_items[category] != 0:
                    ans = messagebox.askyesno("Warning", "Budget for this category is " + str(budget_items[category]) + ". Do you still wish to remove it?")

                    if ans:
                        budget_source(-budget_items[category])
                        money_source()
                        del expense_items[category]
                        del budget_items[category]
                        messagebox.showinfo("SUCCESS", "Category Removed")
                    else:
                        return
                #if there are are no more errors then the else statement is called
                else:
                        del expense_items[category]
                        del budget_items[category]
                        messagebox.showinfo("SUCCESS", "Category Removed")
            else:
                messagebox.showinfo("ERROR", "Category Doesn't Exist.")
 

        self.callback_toplevel(window, window_str.lower())

#===============Methods============================================
def window_center(win, width, height):
    """
    The function centres the window on the screen.
    
    Parameters:
        win (tkinter.Toplevel): window which needs to be centred.
        width (int): width of the window.
        height (int): height of the window.
    """

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    positionRight = int(screen_width/2 - width/2)
    positionDown = int(screen_height/3 - height/3)
    win.geometry("{}x{}+{}+{}".format(width,height,positionRight, positionDown))

def reset():
    """The function deletes the files which contains the data and log. Resetting the app."""

    ans = messagebox.askyesno("Are You Sure?", "Do you want to RESET everything?")
    if ans:
        if os.path.isfile(data_filename):
            os.remove(data_filename)
        if os.path.isfile(log_filename):
            os.remove(log_filename)
        root.destroy()

    return

def log_file_write(section, category, amount):
    """
    The function writes the events taking place inside the app by the user into a file.
    
    Parameters:
        section (str): name of the section.
        category (str): name of the category inside the section.
        amount (int): amount of money added/removed from that category
    """

    isfile = os.path.isfile(log_filename)
    log_file = '' 

    if isfile == False:
        log_file = open(log_filename, 'x')
    
    log_file = open(log_filename, 'a')
    log_file.write( date_value +","+ section +","+ category +","+ str(amount) + "\n")
    log_file.close()

def log_display():
    """The function displays everything inside the log file onto the screen in a readable format."""

    #Creating a Window and setting it up
    log_win = Toplevel(root)
    log_win.title("Logs")
    window_center(log_win, 400, 315)
    log_win.resizable(False, False)
    log_win.focus_force()
    log_win.config(background=background_color)
    root.withdraw()

    isfile = os.path.isfile(log_filename)

    if isfile == False:
        log_file = open(log_filename, 'x')

    #Steps to create a Listbox with a scrollbar
    log_frame = Frame(log_win, background=background_color)
    scroll_bar_y = Scrollbar(log_frame, orient='vertical')
    scroll_bar_x = Scrollbar(log_frame, orient='horizontal')
    scroll_bar_y.pack(side=RIGHT, fill=Y)
    scroll_bar_x.pack(side=BOTTOM, fill=X)

    log_list = Listbox(log_frame, border=0 , highlightthickness=0, font='calibri 11 bold', justify=LEFT, background=background_color, foreground =foreground_color,yscrollcommand = scroll_bar_y.set, xscrollcommand= scroll_bar_x.set)
    log_file = open(log_filename, 'r')

    #To make sense of the data in the log.txt and add it to the listbox
    line = log_file.readline()
    line = line.strip('\n')
    counter = 0
    while line != '':
        words = line.split(',')
        dep_with = ''

        if words[1] == 'money':
            dep_with = 'deposited to'
            fgcolor= green_color
        elif words[1] == 'expense':
            dep_with = 'withdrawn from'
            fgcolor= red_color
        elif words[1] == 'budget':
            dep_with = 'saved for'
            fgcolor= blue_color
        
        log_list.insert(END,"{} : {} {} has been {} {}".format(words[0], currency, words[3], dep_with, words[2]))
        line = log_file.readline()
        line = line.strip('\n')
        log_list.itemconfig(counter, foreground = fgcolor)
        counter += 1

    if counter == 0:
        log_list.config(justify=CENTER)
        log_list.insert(END, 'NO LOGS')

    log_file.close()

    log_list.pack(side=LEFT, fill=BOTH, expand=True, padx=(10,0), pady=(10,0))
    scroll_bar_y.config(command = log_list.yview)
    scroll_bar_x.config(command = log_list.xview)
    log_frame.pack(fill=BOTH, expand=True)

    Button(log_win, text="BACK", font='calibri 11 bold', border=0, background='#00bdaa', foreground=foreground_color, command= lambda: track.callback(log_win)).pack(ipady=8, fill=BOTH)
    log_win.protocol("WM_DELETE_WINDOW", lambda: track.callback(log_win))

def theme_change_dark():
    """The function changes the color variables to suit the Dark mode."""

    global background_color
    global foreground_color
    global green_color
    global red_color
    global blue_color
    global isDark

    isDark = True
    background_color = "#252525"
    foreground_color = "#ffffff"
    green_color = "#a7d129"
    red_color = "#ff0000"
    blue_color = "#29c7ac"
    background_color_config()

def theme_change_light():
    """The function changes the color variables to suit the Light mode."""

    global background_color
    global foreground_color
    global green_color
    global red_color
    global blue_color
    global isDark
    
    isDark = False
    background_color = "#ffffff"
    foreground_color = "#000000"
    green_color = "#2b580c"
    red_color = "#af0404"
    blue_color = "#053f5e"

    background_color_config()

def background_color_config():
    """The function configs the color of the widgets according to the theme."""

    root.config(background=background_color)
    date_label.config(background=background_color, foreground=foreground_color)
    main_frame.config(background=background_color)
    money_frame.config(background=background_color)
    expense_frame.config(background=background_color)
    budget_frame.config(background=background_color)
    money_label.config(background=background_color)
    expense_label.config(background=background_color)
    budget_label.config(background=background_color)
    money_text.config(background=background_color)
    expense_text.config(background=background_color)
    budget_text.config(background=background_color)
    log_button.config(background='#00bdaa', foreground=background_color )
    goal_button.config(background='#00bdaa', foreground=background_color )
    money_add.config(background=background_color)
    expense_add.config(background=background_color)
    budget_add.config(background=background_color)
    money_info.config(background=background_color)
    expense_info.config(background=background_color)
    budget_info.config(background=background_color)
    money_label.config(foreground= green_color)
    expense_label.config(foreground=red_color)
    budget_label.config( foreground=blue_color)
    money_text.config(foreground= green_color)
    expense_text.config(foreground=red_color)
    budget_text.config( foreground=blue_color)

def set_currency():
    """The function opens a window which allows the user to change the currency used in the app."""

    #Creating a Window and setting it up
    root.withdraw()
    win = Toplevel(root)
    win.title("Set Currency")
    window_center(win, 300, 150)
    win.resizable(False, False)
    win.config(background= background_color)
    win.iconbitmap(logo_loc)
    win.focus_force()

    amount_text = Label(win, text="Enter Currency : ", font=custom_font, background=background_color, foreground=foreground_color)
    amount_text.pack()

    amount_input = Entry(win, font='calibri 11',border=0, justify='center', bg='#dee3e2')
    amount_input.insert(0,"Currency")
    amount_input.pack(ipady=5)

    amount_input.bind("<FocusIn>", lambda args: amount_input.delete('0', 'end'))
    
    submit = Button(win, text="Save", font='calibri 11 bold', border=0, background='#00bdaa', foreground=foreground_color, command= lambda: set_c())
    submit.pack(pady=5, ipadx=10)
    
    Button(win, text="BACK", font='calibri 11 bold', border=0, background='#00bdaa', foreground=foreground_color,command = lambda: track.callback(win) ).pack(ipady=8, padx=5, pady=2, fill=BOTH)
    win.protocol('WM_DELETE_WINDOW', lambda: track.callback(win))
    
    def set_c():
        """The function checks if the input by the user is valid or not."""

        global currency
        try:
            float(amount_input.get())
            messagebox.showinfo("Error", "Dont Input a Number")
            return
        except:
            currency = amount_input.get().upper()
            set_currency_text()


def set_currency_text():
    """The function implements the currency into the app."""

    money_text.config(text = currency +" "+ str(money_var))
    expense_text.config(text = currency +" "+ str(expense_var))
    budget_text.config(text = currency +" "+ str(budget_var))

def tutorial():
    """The function which shows the tutorial on how to use the app."""

    root.withdraw()
    win = Toplevel(root)
    win.title("Tutorial")
    window_center(win, 300, 150)
    win.resizable(False, False)
    win.config(background= background_color)
    win.iconbitmap(logo_loc)
    win.focus_force()

    amount_text = Label(win, text="Coming Soon", font=custom_font, background=background_color, foreground=foreground_color)
    amount_text.pack()

    Button(win, text="BACK", font='calibri 11 bold', border=0, background='#00bdaa', foreground=foreground_color,command = lambda: track.callback(win) ).pack(ipady=8, padx=5, pady=2, fill=BOTH)
    win.protocol('WM_DELETE_WINDOW', lambda: track.callback(win))

#==============Methods for Money==============
def money_source():
    """The function which manages the money added/removed from the 'money' section."""

    global money_var
    global currency

    if money_items['CASH'] < 0:
        money_items['CARD'] += money_items['CASH']
        money_items['CASH'] = 0

    money_var = money_items['CASH'] + money_items['CARD']
    money_text.config(text= currency +" "+ str(money_var))

#==============Methods for Expense==============
def expense_source():
    """The function which manages the money added/removed from the 'expense' section."""

    global expense_var
    global budget_var
    global currency

    total_amt = 0
    budget_amt = 0
    
    for i in expense_items.values():
        total_amt += i
    
    for j in budget_items.values():
        budget_amt += j

    budget_var = budget_amt
    budget_text.config(text=currency +" "+ str(budget_var))
    expense_var = total_amt
    expense_text.config(text=currency +" "+ str(expense_var))
        
#==============Methods for Budget==============
def budget_source(amt):
    """The function which manages the money added/removed from the 'budget' section."""

    global budget_var
    global money_var
    global currency

    budget_var += amt
    budget_text.config(text = currency +" "+ str(budget_var))
    money_items['CASH'] -= amt
    money_source()
    money_text.config(text = currency +" "+ str(money_var)) 

#=================window=================================================================
root = Tk()
root.title("Spender")
root.iconbitmap('images/logo_icon.ico')
window_center(root, 400, 315)
root.resizable(False,False)

track = tracker_func()

#=============Fonts=============================
date_font = tkFont.Font(family="courier new", size=10)
custom_font = tkFont.Font(family="calibri light", size=15, weight="bold")
btn_font = tkFont.Font(family="calibri", size=11, weight="bold")

#=============Menu Options======================
menubar = Menu(root)

edit_menu = Menu(menubar, tearoff=0, bg='white')
appear = Menu(edit_menu,tearoff=0, bg='white')
edit_menu.add_cascade(label="Appeareance", menu=appear)
appear.add_command(label="Light", background="white", foreground="black", command=theme_change_light)
appear.add_command(label="Dark", background="black", foreground="white", command=theme_change_dark)
edit_menu.add_command(label="Currency", command=set_currency)
edit_menu.add_separator()
edit_menu.add_command(label="Reset",foreground="red", command=reset)

menubar.add_cascade(label="Edit", menu=edit_menu)

help_menu = Menu(menubar, tearoff=0, bg='white')
help_menu.add_command(label="Tutorial", command=tutorial)
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)

#=============Date==================
date_value = datetime.datetime.now().strftime("%d %b %Y")
date_label = Label(root, text=("Date : "+date_value), font=date_font)
date_label.grid()

#=============Frames==================
main_frame = LabelFrame(root, border=0)
main_frame.grid(sticky="WE", ipadx=3, padx=3)

money_frame = Frame(main_frame)
money_frame.grid(pady=5, padx=(15,5))

expense_frame = Frame(main_frame)
expense_frame.grid(pady=5, padx=(15,5))

budget_frame = Frame(main_frame)
budget_frame.grid(pady=5, padx=(15,5))

#=============Images=================
add_sign = PhotoImage(file="images/add_sign.png")
add_sign = add_sign.subsample(1)

info_sign = PhotoImage(file="images/info.png")
info_sign = info_sign.subsample(2)

logo_loc = 'images/logo_icon.ico'

#=============Labels==================
money_label = Label(money_frame,text="Money :   ", font=custom_font, foreground="#2b580c")
money_label.grid(column=0,row=0, sticky="W")

money_text = Label(money_frame, text=str(money_var), width=20, font=custom_font, foreground="#2b580c")
money_text.grid(column=1,row=0, padx=(0,10))

expense_label = Label(expense_frame,text="Expense : ", font=custom_font,foreground="#af0404")
expense_label.grid(column=0,row=0, sticky="W")

expense_text = Label(expense_frame, text=str(expense_var), width=20, font=custom_font, foreground="#af0404")
expense_text.grid(column=1,row=0, padx=(0,10))

budget_label = Label(budget_frame,text="Budget :  ", font=custom_font, foreground="#053f5e")
budget_label.grid(column=0,row=0, sticky="W")

budget_text = Label(budget_frame,text=str(budget_var), width=20, font=custom_font, foreground="#053f5e")
budget_text.grid(column=1,row=0, padx=(0,10))

#=============Buttons==================
money_add = Button(money_frame, image=add_sign, border=0, command=lambda: track.choose("money"))
money_add.grid(column=2,row=0, sticky="E")
money_info = Button(money_frame, image=info_sign, border=0, command=lambda: track.info('money'))
money_info.grid(column=2,row=1, sticky="E")

expense_add = Button(expense_frame, image=add_sign, border=0, command=lambda: track.choose("expense"))
expense_add.grid(column=2,row=0, sticky="E")
expense_info = Button(expense_frame, image=info_sign, border=0, command=lambda: track.info('expense'))
expense_info.grid(column=2,row=1, sticky="E")

budget_add = Button(budget_frame, image=add_sign, border=0, command=lambda: track.choose("budget"))
budget_add.grid(column=2,row=0, sticky="E")
budget_info = Button(budget_frame, image=info_sign, border=0, command=lambda: track.info('budget'))
budget_info.grid(column=2,row=1, sticky="E")

log_button = Button(root, text="LOGS", border=0, font=btn_font,  command=lambda: log_display());
log_button.grid(row=3, ipadx=30, ipady=2, pady=2, padx=(90,15), sticky="W")

goal_button = Button(root, text="GOALS", border=0, font=btn_font,  command=lambda: track.choose("goal"))
goal_button.grid(row=3, ipadx=25, ipady=2, pady=2, padx=(15,90), sticky="E")

if isDark == True:
    theme_change_dark()
else:
    theme_change_light()

set_currency_text()
#=========START=======================

def callback():
    """The function which takes confirmation from the user before closing the window."""
    ans = messagebox.askyesno("Are You Sure?", "Do you want to Exit?")
    if ans:
        update_file()
        root.destroy()
    return

root.protocol("WM_DELETE_WINDOW", callback)

root.mainloop()