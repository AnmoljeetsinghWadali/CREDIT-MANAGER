from tkinter import *
import tkinter  as tk
from tkinter.ttk import Combobox as cb
from tkinter import messagebox
from tkinter import ttk 
import datetime
import pandas as pd
from tkcalendar import Calendar, DateEntry

#global variables
tv=''
search=''
top=''
s1=''
sort_alphabets='' # alphabetically search combox
alphaSearch='' #button
entryname='' # name based search
nameSearch=''

root=Tk()
root.geometry("950x300+100+100")
root.title('WADALI JEWELLERS')
root.configure(background='Cadet Blue')
root.resizable(width=False,height=False)

f1=Frame(root,bg='Cadet Blue',bd=10,relief=RIDGE)
f1.pack()

f2=Frame(f1,bg='Cadet Blue',bd=10,relief=RIDGE)
f2.pack(side=TOP)

f3=Frame(f1,bg='powder blue',bd=10,relief=RIDGE)
f3.pack(side=LEFT)

f4=Frame(f1,bg='powder blue',bd=5,relief= GROOVE)
f4.pack(side=BOTTOM)

#functions
def ADD():
	NAME=e1.get()
	DATE=cal.get()
	AMOUNT=e2.get()
	MOBILE_NO=e3.get()
	if NAME!='' and AMOUNT!='' and MOBILE_NO!=0:
		data=[DATE,NAME,MOBILE_NO,AMOUNT]
		print(data)
		data='\n'+DATE+','+NAME.lower()+','+MOBILE_NO+','+AMOUNT
		f=open('details.csv','a+')
		f.write(data)
		f.close()
		messagebox.showinfo("SUCCESS","DATA ADDED!!!")
		e1.delete(0,END)
		e2.delete(0,END)
		e3.delete(0,END)
	else:
		messagebox.showerror("Error!!","All Data is not filled Properly!!")


def EXIT():
	a=messagebox.askyesno("QUIT!!!",'Do you want to Quit?')
	print(a)
	if a:
		root.destroy()
		return  

def DELETE():
	def selected():
		print(l.curselection())
		t=l.curselection()
		LIST=[i for i in t]
		print(LIST)
		df=pd.read_csv('details.csv')
		df.index+=1
		if 0 in LIST:
			LIST.remove(0)
		df.drop(LIST,inplace=True)
		df.reset_index(inplace=True)
		df.drop(["index"], axis = 1, inplace = True) 
		df.to_csv('details.csv',index=False)
		messagebox.showinfo("SUCCESS","Entries Deleted Successfully")
    
	DEL = tk.Toplevel(root)
	DEL.geometry('600x400+100+100')
	DEL.configure(background='cadet blue',bd=10,relief=RIDGE)
	l=Listbox(DEL,width=60,height=20,selectmode=MULTIPLE)
	df=pd.read_csv("details.csv")
	L=df.values.tolist()
	a=['DATE ',' NAME ',' MOBILE_NO ',' AMOUNT ']
	l.insert(0,a)
	for i in range(1,len(L)+1):
		l.insert(i,L[i-1])
	l.pack()
	btn = Button(DEL, text ='DELETE',command =selected) 
	btn.pack(side = TOP, pady = 10) 


def alphashow():
	global sort_alphabets,tv,search
	tv.delete(*tv.get_children())
	if sort_alphabets.get()!='SELECT ALPHABETS TO SHOW' or sort_alphabets.get()!='':
		df1=pd.read_csv("details.csv")
		newdata=df1.dropna(axis=0,how="any")
		data=newdata.values.tolist()
		count=0
		lis=[]
		for i in data:
			if i[1][0]==sort_alphabets.get():
				count+=1
				lis.append(i)
		if count==0:
			messagebox.showerror("RESULT","NO MATCH FOUND")
		else:
			for i in lis:
				tv.insert("",'end',values=i )
		search.set("SELECT OPTION SEARCH")
	else:
		messagebox.showerror("Problem!!","No Alphabet is Selected!!")

def nameshow():
	global entryname,tv,search
	tv.delete(*tv.get_children())
	if entryname.get()!='':
		df1=pd.read_csv("details.csv")
		newdata=df1.dropna(axis=0,how="any")
		data=newdata.values.tolist()
		count=0
		lis=[]
		for i in data:
			if i[1]==entryname.get().lower():
				count+=1
				lis.append(i)
		if count==0:
			messagebox.showinfo("RESULT","NO MATCH FOUND")
		else:
			for i in lis:
				tv.insert("",'end',values=i)
		search.set("SELECT OPTION SEARCH")

	else:
		messagebox.showerror("Problem!!",'No name has been Entered!!')





def show():
	global tv,search,top,s1,alphaSearch,sort_alphabets,entryname,nameSearch
	if search.get()=="ALL":
		if sort_alphabets!='':
			sort_alphabets.grid_forget()
			sort_alphabets=''
		if alphaSearch!='':
			alphaSearch.grid_forget()
			alphaSearch=''
		if nameSearch!='':
			nameSearch.grid_forget()
			nameSearch=''
		if entryname!="":
			entryname.grid_forget()
			entryname=''

		tv.delete(*tv.get_children())
		df=pd.read_csv("details.csv")
		data=df.dropna(axis=0,how='any')
		l=data.values.tolist()
		for i in l:
			if i!='':
				tv.insert("",'end',values=i )
		messagebox.showinfo("ENTRIES COUNT",'TOTAL NUMBER OF ENTRIES - '+str(len(l)))
	elif search.get()=='ALPHABETICALLY':
		print('hello')
		if nameSearch!='':
			nameSearch.grid_forget()
			nameSearch=''
		if entryname!='':
			entryname.grid_forget()
			entryname=''
		alphabet=[chr(97+i) for i in range(26)]
		sort_alphabets=cb(s1,value=alphabet,width=25)
		sort_alphabets.set('SELECT ALPHABETS TO SHOW')
		sort_alphabets.grid(row=4,column=3)
		alphaSearch=Button(s1,width=15,fg='blue',activeforeground='black',text='SHOW BY LETTER',command=alphashow)
		alphaSearch.grid(row=6,column=3)

	elif search.get()=='NAME':
		if sort_alphabets!='':
			sort_alphabets.grid_forget()
			sort_alphabets=''
		if alphaSearch!='':
			alphaSearch.grid_forget()
			alphaSearch=''
		entryname=Entry(s1,width=25,font=('arial',14,'bold'),bg="white")
		entryname.grid(row=4,column=3)
		entryname.insert(0, 'ENTER PARTY NAME!!!!')
		nameSearch=Button(s1,width=15,fg='green',activeforeground='black',text='SHOW BY NAME',command=nameshow)
		nameSearch.grid(row=6,column=3)
		search.set("SELECT OPTION SEARCH")





	else:
		if sort_alphabets!='':
			sort_alphabets.grid_forget()
			sort_alphabets=''
		if alphaSearch!='':
			alphaSearch.grid_forget()
			alphaSearch=''
		if nameSearch!='':
			nameSearch.grid_forget()
			nameSearch=''
		if entryname!='':
			entryname.grid_forget()
			entryname=''
		search.set("CHOOSE OPTION")

        



def SHOW():
	global tv,search,s1
	top=Toplevel(root)
	top.config(background='Cadet Blue')
	top.geometry('1000x500+100+100')
	top.resizable(width=False,height=False)
	top.title('PAYMENTS DUE')
	s1=Frame(top,bg='Cadet Blue',bd=10,relief=RIDGE)
	s1.pack(side=TOP)

	label1=Label(s1,text='SHOW PAYMENTS DUES',bg='white',fg='red',bd=5  ,font=('arial',20,'bold'))
	label1.grid(row=1,column=3)

	menu=['ALL',"ALPHABETICALLY",'NAME']
	search=StringVar()
	LD=OptionMenu(s1,search,*menu)
	search.set("SELECT OPTION SEARCH")
	LD.config(width=20)
	LD.grid(row=2,column=0)
	b1=Button(s1,text='PRESS TO CHOOSE',width=15,fg='red',activeforeground='black',command=show,relief=GROOVE)
	b1.grid(row=2,column=8)

	frm=Frame(top,bg='Cadet Blue',bd=10,relief=RIDGE)
	frm.pack(side=tk.LEFT,padx=30)
	tv=ttk.Treeview(frm,columns=(1,2,3,4),show="headings",height="15")
	tv.pack()
	tv.heading(1,text="DATE",anchor=tk.W)
	tv.heading(2,text="NAME")
	tv.heading(3,text="MOBILE_NO")
	tv.heading(4,text="AMOUNT")
  




# widgets

l1=Label(f2,width=40,fg="red",bd=5  ,font=('arial',30,'bold'),text='PAYMENTS-MANAGER')
l1.grid(row=0,column=0) 

#txt=Text(f3,width=84,height=24,bg='white',bd=4,font=('arial',12,'bold'))
#txt.grid(row=1,column=0)

date=Label(f3,width=20,bg='powder blue',fg="red" ,bd=4  ,font=('arial',18,'bold'),text='DATE')
date.grid(row=0,column=0) 
cal = DateEntry(f3, width=20, background='darkblue',
                    foreground='white', borderwidth=4, year=2020,date_pattern='dd/MM/yyyy')
cal.grid(row=0,column=3) 


name=Label(f3,width=20,fg="red" ,bg='powder blue',font=('arial',18,'bold'),text='NAME OF PERSON')
name.grid(row=1,column=0)   
e1=Entry(f3,width=25,font=('arial',14,'bold'),bg="white")
e1.grid(row=1,column=3) 
#e1.insert(0, 'ENTER NAME')

phoneno=Label(f3,width=20,bg='powder blue',fg="red",bd=4  ,font=('arial',18,'bold'),text='MOBILE NO')
phoneno.grid(row=2,column=0) 

e3=Entry(f3,width=25,font=('arial',14,'bold'),bg="white")
e3.grid(row=2,column=3) 

amount=Label(f3,width=20,bg='powder blue',fg="red",bd=4  ,font=('arial',18,'bold'),text='AMOUNT')
amount.grid(row=3,column=0) 
e2=Entry(f3,width=25,font=('arial',14,'bold'),bg="white")
e2.grid(row=3,column=3) 

#e2.insert(0, 'ENTER AMOUNT')

#e3.insert(0, 'ENTER MOBILE NO')

b1=Button(f4,fg='red',	
activeforeground='black',width=15,text='ADD',command=ADD)
b1.grid(row=6,column=0)

b2=Button(f4,fg='red',activeforeground='black',width=15,text='SHOW',command=SHOW)
b2.grid(row=6,column=1)

b3=Button(f4,width=15,fg='red',activeforeground='black',text='DELETE',command=DELETE)
b3.grid(row=6,column=2 )

b4=Button(f4,width=15,fg='red',activeforeground='black',text='EXIT!!',command=EXIT)
b4.grid(row=7,column=1)


root.mainloop()

