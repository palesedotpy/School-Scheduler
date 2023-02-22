import tkinter as tk
import mysql.connector as mc
from tkinter import ttk
from tkinter import GROOVE, messagebox


try:
    db = mc.connect(        # Connect the database
        host = 'localhost',
        username = 'root',
        password = '',
        database = 'students_database'
    )
    cursor = db.cursor()
except:
    db = mc.connect(        # Connect the database
        host = 'localhost',
        username = 'root',
        password = ''
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE students_database")
    db.commit()

try:
    cursor.execute("CREATE TABLE students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), surname VARCHAR(255), gender VARCHAR(255))")
    db.commit()
except:
    print('esiste')


root = tk.Tk()
root.title('School Mangment')
root.resizable(False, False)      # Inizializing the window
root.geometry('800x500')
root.config(bg= '#2C3333')


def visualizeStudent():     # Command to visualize the student

    rootVisualize = tk.Tk()
    rootVisualize.title('')
    rootVisualize.config(bg= '#2C3333')
    rootVisualize.resizable(False, False)

    column = ('id', 'name', 'surname', 'gender')
    table = ttk.Treeview(rootVisualize, columns = column, show= 'headings')
    table.heading('id', text= 'ID')
    table.heading('name', text= 'Name')
    table.heading('surname', text= 'Surname')
    table.heading('gender', text= 'Gender')
    

    scrollbar = tk.Scrollbar(rootVisualize, orient= 'vertical', command= table.yview)
    scrollbar.grid(row= 0, column= 1, sticky= 'ns')

    table['yscrollcommand'] = scrollbar.set
    
    sql = 'SELECT * FROM students'
    cursor.execute(sql)
    result = cursor.fetchall()
    l = 1
    for p in result:
        l+=1

    rows = []

    for i in result:
        rows.append((i[0], i[1], i[2], i[3]))

    for row in rows:
        table.insert('', tk.END, values= row)

    table.grid(row= 0, column= 0, sticky= 'nsew')


def addStudent():           # Command to add the student

    def submitAddFunction():
        global nameStudent, surnameStudent, genderStudent

        x = True

        nameStudent = entryNameStudent.get()
        surnameStudent = entrySurameStudent.get()
        genderStudent = gender.get()

        invalidSimbols = '1234567890!"£$%&/()=?^\'[]@#_:;,.-<>'
        invalidSimbolsList = list(invalidSimbols)
        if len(nameStudent) != 0 or len(surnameStudent) != 0:
            for char in invalidSimbolsList:
                if (char in nameStudent) or (char in surnameStudent):
                    messagebox.showwarning(title = 'ERROR', message= 'Invalid name')
                    x = False
        else:
            messagebox.showwarning(title = 'ERROR', message= 'Empty name')
        if x:
            sql = 'INSERT INTO students (name, surname, gender) VALUES (%s, %s, %s)'
            values = nameStudent, surnameStudent, genderStudent
            cursor.execute(sql, values)
            db.commit()
            rootAdd.destroy()
            messagebox.showinfo(title='SUCCESS', message='Student added successfully!')


    rootAdd = tk.Tk()
    rootAdd.title('Add Students')
    rootAdd.config(bg= '#2C3333')
    rootAdd.resizable(False, False)
    
    tk.Label(root, text='Add Student', font=('Lucida Console', 20, 'bold'), bg= '#2B4646', fg= 'white')

    tk.Label(rootAdd, text= 'Insert the student\'s name', font= ('Trebuchet MS', 20, 'bold'), bg= '#2C3333', fg= 'white').pack()

    sNameStudent = tk.StringVar()   # StringVar of Name Student
    entryNameStudent = tk.Entry(rootAdd, textvariable= sNameStudent)
    entryNameStudent.pack()


    tk.Label(rootAdd, text= 'Insert the student\'s surname', font= ('Trebuchet MS', 20, 'bold'), bg= '#2C3333', fg= 'white').pack()
    sSurnameStudent = tk.StringVar()   # StringVar of surname Student
    entrySurameStudent = tk.Entry(rootAdd, textvariable= sSurnameStudent)
    entrySurameStudent.pack()

    tk.Label(rootAdd, bg= '#2C3333').pack(pady= 10)
    
    gender = tk.StringVar(rootAdd)
    maleRadiobutton = tk.Radiobutton(rootAdd, text= 'Male', value= 'Male', font= ('Trebuchet MS', 10, 'bold'), variable= gender, bg= '#2C3333', fg= 'white', selectcolor= 'black')
    maleRadiobutton.pack(pady= 10)
    femaleRadiobutton = tk.Radiobutton(rootAdd, text= 'Female', value= 'Female', font= ('Trebuchet MS', 10, 'bold'), variable= gender, bg= '#2C3333', fg= 'white', selectcolor= 'black')
    femaleRadiobutton.pack()


    submitAddButton = tk.Button(rootAdd, text= 'Submit', command= submitAddFunction)
    submitAddButton['activebackground'] = '#C6ECAE'
    submitAddButton['font'] = ('Trebuchet MS'), 10, 'bold'
    submitAddButton['activebackground'] = '#C6ECAE'
    submitAddButton['relief'] = GROOVE
    submitAddButton.pack(pady= 20)


def delStudent():           # Command to delete the student

    def submitDelFunction():
        x = True
        sql = f'SELECT * FROM students WHERE id = {entryIdStudent.get()}'
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()

        try:
            if int(entryIdStudent.get()) == result[0][0]:
                x = True
        except:
            messagebox.showerror(title= 'ERROR', message= 'Student didn\'t found ')
            delRoot.destroy()
            x = False

        if x:
            sql = f'DELETE FROM students WHERE id = {entryIdStudent.get()}'
            cursor.execute(sql)
            db.commit()
            messagebox.showinfo(title='SUCCESS', message='Student deleted successfully!')
            delRoot.destroy()
            

    delRoot = tk.Tk()
    delRoot.title('Delete Students')
    delRoot.config(bg= '#2C3333')
    delRoot.resizable(False, False)

    tk.Label(root, text='Add Student', font=('Lucida Console', 20, 'bold'), bg= '#2B4646', fg= 'white')

    tk.Label(delRoot, text= 'Insert the student\'s id', font= ('Trebuchet MS', 20, 'bold'), bg= '#2C3333', fg= 'white').pack()

    entryIdStudent = tk.Entry(delRoot)
    entryIdStudent.pack()


    tk.Label(delRoot, bg= '#2C3333').pack(pady= 10)

    submitAddButton = tk.Button(delRoot, text= 'Submit', command= submitDelFunction)
    submitAddButton['activebackground'] = '#C6ECAE'
    submitAddButton['font'] = ('Trebuchet MS'), 10, 'bold'
    submitAddButton['activebackground'] = '#C6ECAE'
    submitAddButton['relief'] = GROOVE
    submitAddButton.pack(pady= 20)


def modStudent():        # Command to modify the student
    def submitModFunction():
        def updateIdFunction():
            validInput = True
            o = True
            a = True
            try:   # Check if user use valid ID
                newId = int(updateId.get())
                updateId.delete(0,tk.END)
                a = True
                                
            except:
                labelMessage['text'] = 'Invalid ID'
                labelMessage['font'] = ('Trebuchet MS', 15, 'bold')
                labelMessage['bg'] = '#9a031e'
                labelMessage['fg'] = '#fb8b24'
                validInput = False
                
            if validInput:
                sql = 'SELECT id FROM students'
                cursor.execute(sql)
                result = cursor.fetchall()
                db.commit()

                for j in range(len(result)):
                    if o:   # Check if the new ID is univoque
                        for i in result[j]:
                            if newId != i:
                                print(newId, i, 'OK')
                                validInput = True
                                a = True
                                break
                            else:
                                print(newId, i,'NO')
                                labelMessage['text'] ='ID already assigned'
                                labelMessage['font'] = ('Trebuchet MS', 15, 'bold')
                                labelMessage['bg'] = '#9a031e'
                                labelMessage['fg'] = '#fb8b24'
                                labelMessage.place(x=260, y=250)
                                validInput = False
                                o = False
                                a = False

                if a:
                    try:
                        sql = 'UPDATE students SET id = %s WHERE id = %s'
                        values = newId, newInputId[0]
                        cursor.execute(sql, values)
                        db.commit()
                        print(inputId)
                        print('DONE')
                        print('nw', newId)
                        print(f'UPDATE students SET id = {newId} WHERE id = {inputId}')
                        values = newId, inputId

                        tk.Label(rootMod2, bg= '#2C3333').grid(row=6, column=0)
                        tk.Label(rootMod2, bg= '#2C3333').grid(row=7, column=0)
                        tk.Label(rootMod2, bg= '#2C3333').grid(row=8, column=0)
                        tk.Label(rootMod2, bg= '#2C3333').grid(row=9, column=0)

                        labelMessage['text'] = 'ID updated successfully'
                        labelMessage['font'] = ('Trebuchet MS', 15, 'bold')
                        labelMessage['bg'] = '#90e0ef'
                        labelMessage['fg'] = '#023e8a'

                        idStudent['text'] = newId
                        updateId.delete(0,tk.END)
                        newInputId.append(newId)
                        newInputId.pop(0)
                        

                    except:
                        tk.Label(rootMod2, bg= '#2C3333').grid(row=6, column=0)
                        tk.Label(rootMod2, bg= '#2C3333').grid(row=7, column=0)
                        tk.Label(rootMod2, bg= '#2C3333').grid(row=8, column=0)
                        tk.Label(rootMod2, bg= '#2C3333').grid(row=9, column=0)
                        labelMessage['text'] = 'ID already assigned'
                        labelMessage['font'] = ('Trebuchet MS', 15, 'bold')
                        labelMessage['bg'] = '#9a031e'
                        labelMessage['fg'] = '#fb8b24'
                    
        def updateNameFunction():
            validInput = True

            try:
                newName = updateName.get()
                sql = 'SELECT * FROM students'
                cursor.execute(sql)
                result = cursor.fetchall()
                db.commit()

                if newName != result[0][1]:
                    print(newName, 'OK')
                    validInput = True
            except:
                messagebox.showerror(rootMod2, title='ERROR', message= 'Invalid input')
                validInput = False
            
            if validInput:

                sql = 'UPDATE students SET name = %s WHERE id = %s'
                values = newName, inputId
                cursor.execute(sql, values)
                db.commit()
                tk.Label(rootMod2, bg= '#2C3333').grid(row=6, column=0)
                tk.Label(rootMod2, bg= '#2C3333').grid(row=7, column=0)
                tk.Label(rootMod2, bg= '#2C3333').grid(row=8, column=0)
                tk.Label(rootMod2, bg= '#2C3333').grid(row=9, column=0)
                labelMessage = tk.Label(rootMod2)
                labelMessage['text'] = 'NAME updated successfully'
                labelMessage['font'] = ('Trebuchet MS', 15, 'bold')
                labelMessage['bg'] = '#90e0ef'
                labelMessage['fg'] = '#023e8a'
                labelMessage.place(x=260, y=250)

                nameStudent['text'] = updateName.get()
                updateName.delete(0,tk.END)

        def updateSurnameFunction():
            validInput = True

            try:
                newSurname = updateSurname.get()
                sql = 'SELECT * FROM students'
                cursor.execute(sql)
                result = cursor.fetchall()
                db.commit()

                if newSurname != result[0][0]:
                    print(newSurname, 'OK')
                    validInput = True
            except:
                messagebox.showerror(rootMod2, title='ERROR', message= 'Invalid input')
                validInput = False
            
            if validInput:

                sql = 'UPDATE students SET surname = %s WHERE id = %s'
                values = newSurname, inputId
                cursor.execute(sql, values)
                db.commit()
                tk.Label(rootMod2, bg= '#2C3333').grid(row=6, column=0)
                tk.Label(rootMod2, bg= '#2C3333').grid(row=7, column=0)
                tk.Label(rootMod2, bg= '#2C3333').grid(row=8, column=0)
                tk.Label(rootMod2, bg= '#2C3333').grid(row=9, column=0)
                labelMessage = tk.Label(rootMod2)
                labelMessage['text'] = 'SURNAME updated successfully'
                labelMessage['font'] = ('Trebuchet MS', 15, 'bold')
                labelMessage['bg'] = '#90e0ef'
                labelMessage['fg'] = '#023e8a'
                labelMessage.place(x=260, y=250)

                surnameStudent['text'] = updateSurname.get()
                updateSurname.delete(0,tk.END)

        def updateGenderFunction():
            validInput = True
            x = True

            sql = f'SELECT gender FROM students WHERE id = {inputId}'
            cursor.execute(sql)
            result = cursor.fetchall()
            db.commit()

            newGender = updateGender.get()

            if (newGender != 'Male' or newGender == 'male') or (newGender != 'Female' or newGender == 'Female'):
                x = False
                labelMessage['text'] = 'Invalid Gender'
                labelMessage['font'] = ('Trebuchet MS', 15, 'bold')
                labelMessage['bg'] = '#9a031e'
                labelMessage['fg'] = '#fb8b24'
                labelMessage.place(x=260, y=250)
            x = True

            if x:
                if (newGender == 'Male' or newGender == 'male') and (result[0] == 'Male' or result[0] == 'male'):
                    labelMessage['text'] = 'GENDER is already Male'
                    labelMessage['font'] = ('Trebuchet MS', 15, 'bold')
                    labelMessage['bg'] = '#9a031e'
                    labelMessage['fg'] = '#fb8b24'
                    labelMessage.place(x=260, y=250)
                    validInput = False
                elif (newGender == 'Female' or newGender == 'female') and (result[0] == 'Female' or result[0] == 'female'):
                    labelMessage['text'] = 'GENDER is already Female'
                    labelMessage['font'] = ('Trebuchet MS', 15, 'bold')
                    labelMessage['bg'] = '#9a031e'
                    labelMessage['fg'] = '#fb8b24'
                    labelMessage.place(x=260, y=250)
                    validInput = False
                else:
                    validInput = True

                if validInput:
                    newGender = updateGender.get()
                    sql = 'UPDATE students SET gender = %s WHERE id = %s'
                    values = newGender.capitalize(), inputId
                    cursor.execute(sql, values)
                    db.commit()
                    tk.Label(rootMod2, bg= '#2C3333').grid(row=6, column=0)
                    tk.Label(rootMod2, bg= '#2C3333').grid(row=7, column=0)
                    tk.Label(rootMod2, bg= '#2C3333').grid(row=8, column=0)
                    tk.Label(rootMod2, bg= '#2C3333').grid(row=9, column=0)
                    labelMessage['text'] = 'GENDER updated successfully'
                    labelMessage['font'] = ('Trebuchet MS', 15, 'bold')
                    labelMessage['bg'] = '#90e0ef'
                    labelMessage['fg'] = '#023e8a'
                    labelMessage.place(x=260, y=250)

                    genderStudent['text'] = updateGender.get()
                    updateGender.delete(0,tk.END)
       
        global newInputId
        y = True
        try:
            inputId = int(entryIdStudent.get())
            sql = f'SELECT * FROM students WHERE id = {inputId}'
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            db.commit()
            y = True
        except:
            messagebox.showerror(title= 'ERROR', message= 'Invalid input')
            y = False

        if y:
            x = True
            try:
                if inputId == result[0][0]:
                    x = True
            except:
                messagebox.showerror(title= 'ERROR', message= 'Student didn\'t found ')
                rootMod.destroy()
                x = False


            if x:
                rootMod.destroy()
                rootMod2 = tk.Tk()
                rootMod2.title('Modify Student')
                rootMod2.config(bg= '#2C3333')
                rootMod2.resizable(False, False)
                
                newInputId = []
                newInputId.append(inputId)

                labelMessage = tk.Label(rootMod2)
                labelMessage['font'] = ('Trebuchet MS', 15, 'bold')
                labelMessage.place(x=260, y=250)

                sql = f'SELECT * FROM students WHERE id = {inputId}'
                cursor.execute(sql)
                result = cursor.fetchall()
                db.commit()


                id = tk.Label(rootMod2, text= 'ID', font= 'Trebuchet 20 bold', bg= '#2C3333', fg= '#017365').grid(row=0, column=0, padx= 15)
                name = tk.Label(rootMod2, text= 'NAME', font= 'Trebuchet 20 bold', bg= '#2C3333', fg= '#017365').grid(row=0, column=1, padx= 15)
                surname = tk.Label(rootMod2, text= 'SURNAME', font= 'Trebuchet 20 bold', bg= '#2C3333', fg= '#017365').grid(row=0, column=2, padx= 15)
                gender = tk.Label(rootMod2, text= 'GENDER', font= 'Trebuchet 20 bold', bg= '#2C3333', fg= '#017365').grid(row=0, column=3, padx= 15)

                idStudent = tk.Label(rootMod2)
                idStudent['text'] = result[0][0]
                idStudent['font'] = ('Trebuchet MS', 20, 'bold')
                idStudent['bg'] = '#2C3333'
                idStudent['fg'] = 'white'
                idStudent.grid(row=1, column=0, padx= 15)

                nameStudent = tk.Label(rootMod2)
                nameStudent['text'] = result[0][1]
                nameStudent['font'] = ('Trebuchet MS', 20, 'bold')
                nameStudent['bg'] = '#2C3333'
                nameStudent['fg'] = 'white'
                nameStudent.grid(row=1, column=1, padx= 15)

                surnameStudent = tk.Label(rootMod2)
                surnameStudent['text'] = result[0][2]
                surnameStudent['font'] = ('Trebuchet MS', 20, 'bold')
                surnameStudent['bg'] = '#2C3333'
                surnameStudent['fg'] = 'white'
                surnameStudent.grid(row=1, column=2, padx= 15)

                genderStudent = tk.Label(rootMod2)
                genderStudent['text'] = result[0][3]
                genderStudent['font'] = ('Trebuchet MS', 20, 'bold')
                genderStudent['bg'] = '#2C3333'
                genderStudent['fg'] = 'white'
                genderStudent.grid(row=1, column=3, padx= 15)

                tk.Label(rootMod2, bg= '#2C3333').grid(row=2, column=0)

                newIdStudent = tk.Label(rootMod2)
                newIdStudent['text'] = 'Insert new ID'
                newIdStudent['font'] = ('Trebuchet MS', 15, 'bold')
                newIdStudent['bg'] = '#2C3333'
                newIdStudent['fg'] = '#017365'
                newIdStudent.grid(row=3, column= 0, padx= 5)

                newNameStudent = tk.Label(rootMod2)
                newNameStudent['text'] = 'Insert new Name'
                newNameStudent['font'] = ('Trebuchet MS', 15, 'bold')
                newNameStudent['bg'] = '#2C3333'
                newNameStudent['fg'] = '#017365'
                newNameStudent.grid(row=3, column= 1, padx= 5)

                newSurnameStudent = tk.Label(rootMod2)
                newSurnameStudent['text'] = 'Insert new Surname'
                newSurnameStudent['font'] = ('Trebuchet MS', 15, 'bold')
                newSurnameStudent['bg'] = '#2C3333'
                newSurnameStudent['fg'] = '#017365'
                newSurnameStudent.grid(row=3, column= 2, padx= 5)

                newGenderStudent = tk.Label(rootMod2)
                newGenderStudent['text'] = 'Insert new Gender'
                newGenderStudent['font'] = ('Trebuchet MS', 15, 'bold')
                newGenderStudent['bg'] = '#2C3333'
                newGenderStudent['fg'] = '#017365'
                newGenderStudent.grid(row=3, column= 3, padx= 5)

                sIdStudent = tk.StringVar()
                updateId = tk.Entry(rootMod2, textvariable= sIdStudent)
                updateId['font'] = ('Calibri'), 10, 'bold'
                updateId.grid(row=4, column= 0, padx= 15)

                sNameStudent = tk.StringVar()
                updateName = tk.Entry(rootMod2, textvariable= sNameStudent)
                updateName['font'] = ('Calibri'), 10, 'bold'
                updateName.grid(row= 4, column= 1, padx= 15)

                sSurnameStudent = tk.StringVar()
                updateSurname = tk.Entry(rootMod2, textvariable= sSurnameStudent)
                updateSurname['font'] = ('Calibri'), 10, 'bold'
                updateSurname.grid(row= 4, column= 2, padx= 15)
                
                sGenderStudent = tk.StringVar()
                updateGender = tk.Entry(rootMod2, textvariable= sGenderStudent)
                updateGender['font'] = ('Calibri'), 10, 'bold'
                updateGender.grid(row= 4, column= 3, padx= 15)

                updateIdButton = tk.Button(rootMod2, text= 'Change ID', relief= GROOVE, activebackground= '#C6ECAE', font= 'Trebuchet 10 bold', command= updateIdFunction).grid(row= 5,column= 0, pady= 20)
                updateNameButton = tk.Button(rootMod2, text= 'Change Name', relief= GROOVE, activebackground= '#C6ECAE', font= 'Trebuchet 10 bold', command= updateNameFunction).grid(row= 5,column= 1)
                updateSurnameButton = tk.Button(rootMod2, text= 'Change Surname', relief= GROOVE, activebackground= '#C6ECAE', font= 'Trebuchet 10 bold', command= updateSurnameFunction).grid(row= 5,column= 2, pady= 20)
                updateGenderButton = tk.Button(rootMod2, text= 'Change Gender', relief= GROOVE, activebackground= '#C6ECAE', font= 'Trebuchet 10 bold', command= updateGenderFunction).grid(row= 5,column= 3)


    rootMod = tk.Tk()
    rootMod.title('Choose Student')
    rootMod.config(bg= '#2C3333')
    rootMod.resizable(False, False)
    
    tk.Label(root, text='Choose Student', font=('Lucida Console', 20, 'bold'), bg= '#2B4646', fg= 'white')

    tk.Label(rootMod, text= 'Insert the student\'s id', font= ('Trebuchet MS', 20, 'bold'), bg= '#2C3333', fg= 'white').pack(pady= 5, ipadx= 5)

    entryIdStudent = tk.Entry(rootMod)
    entryIdStudent['font'] = ('Calibri'), 10, 'bold'
    entryIdStudent.pack()


    submitModButton = tk.Button(rootMod, text= 'Submit', command= submitModFunction)
    submitModButton['activebackground'] = '#C6ECAE'
    submitModButton['font'] = ('Trebuchet MS'), 10, 'bold'
    submitModButton['activebackground'] = '#C6ECAE'
    submitModButton['relief'] = GROOVE
    submitModButton.pack(pady= 15, ipadx= 10)


titleLabel = tk.Label(root, text='School schedule v0.1', font=('Trebuchet', 20, 'bold'), bg= '#526969', fg= 'white')     # Title
titleLabel.pack(pady= 50)

visualizeButton = tk.Button(root, text= 'Visualize student')        # The student's who visualize button
visualizeButton['font'] = ('Trebuchet MS'), 10, 'bold'
visualizeButton['activebackground'] = '#C6ECAE'
visualizeButton['relief'] = GROOVE
visualizeButton['command'] = visualizeStudent
visualizeButton.pack(ipady=4)

modButton = tk.Button(root, text= 'Add student')
modButton['font'] = ('Trebuchet MS'), 10, 'bold'
modButton['activebackground'] = '#C6ECAE'
modButton['relief'] = GROOVE
modButton['command'] = addStudent
modButton.pack(pady= 50, ipady=4)

delButton = tk.Button(root, text= 'Del student')
delButton['font'] = ('Trebuchet MS'), 10, 'bold'
delButton['activebackground'] = '#C6ECAE'
delButton['relief'] = GROOVE
delButton['command'] = delStudent
delButton.pack(ipady=4)

modifyButton = tk.Button(root, text= 'Modify student')
modifyButton['font'] = ('Trebuchet MS'), 10, 'bold'
modifyButton['activebackground'] = '#C6ECAE'
modifyButton['relief'] = GROOVE
modifyButton['command'] = modStudent
modifyButton.pack(pady= 50, ipady=4)

credits = tk.Label(root)
credits['text'] = 'Created by palese.py'
credits['font'] = ('Trebuchet MS'), 10, 'italic'
credits['bg'] = '#3b4444'
credits['fg'] = '#2c6664'
credits.place(x=660, y=465)

if __name__ == '__main__':
    root.mainloop()