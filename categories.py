import http
from http.client import responses
from msilib.schema import ComboBox, Component
import textwrap
import tkinter
from cProfile import label
from email import message
from optparse import Values
from textwrap import fill
from tkinter import *
from subprocess import call
from tkinter import messagebox, ttk
import tempfile
import random
from time import strftime
from tkinter import font
import mysql.connector
from PIL import ImageTk, Image
import os
import re
import mysql
from tkcalendar import Calendar
from fpdf import FPDF
import datetime
import sqlite3


class Categorie:
    def __init__(self,root):
        self.root=root
        self.root.title("CATEGORIES")
        self.root.geometry("1050x510+90+90")
        self.root.config(bg="white")
        self.root.focus_force()

        ### les variables

        self.var_cat_id = StringVar()
        self.var_nom = StringVar()
        ###base de donnees

        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS categorie(cid INTEGER PRIMARY KEY AUTOINCREMENT,nom text)")
        con.commit()


        titre = Label(self.root,text="GESTION CATEGORIES",font=("times new roman",15),cursor="hand2",bg="cyan").place(x=0,y=15,width=1100)

        ##contenu
        lbl_categories=Label(self.root,text="Saisir Catégorie Produit",font=("times new roman",15),bg="white").place(x=5,y=80)
        txt_categorie = Entry(self.root,textvariable=self.var_nom,font=("times new roman",15),bg="lightyellow").place(x=5,y=110,width=200)

        btn_ajouter =Button(self.root,command=self.ajouter,text="AJOUTER",font=("times new roman",15),bg="green",cursor="hand2").place(x=220,y=130,width=150,height=40)
        btn_supprimer =Button(self.root,command=self.supprimer,text="SUPPRIMER",font=("times new roman",15),bg="red",cursor="hand2").place(x=380,y=130,width=160,height=40)

        ### liste categories

        listeFrame = Frame(self.root,bd=3, relief=RIDGE)
        listeFrame.place(x=560,y=50,height=150,width=475)

        scroll_y = Scrollbar(listeFrame,orient=VERTICAL,width=20)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x = Scrollbar(listeFrame,orient=HORIZONTAL,width=20)
        scroll_x.pack(side=BOTTOM,fill=X)

        self.cateogrieliste = ttk.Treeview(listeFrame, columns=("cid","nom"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
        scroll_x.config(command=self.cateogrieliste.xview)
        scroll_y.config(command=self.cateogrieliste.yview)

        self.cateogrieliste.heading("cid",text="ID_Catégorie",anchor="w")
        self.cateogrieliste.heading("nom",text="NOM",anchor="w")

        self.cateogrieliste["show"]="headings"

        self.cateogrieliste.pack(fill=BOTH,expand=1)
        self.cateogrieliste.bind("<ButtonRelease-1>",self.get_donne)
        self.afficher()

        self.cat1 = Image.open(r"D:\new\projet python\gestion_licence\image\im3.jpg")
        self.cat1=self.cat1.resize((490,295),)
        self.cat1=ImageTk.PhotoImage(self.cat1)

        self.lbl_img_cat1=Label(self.root,bd=7,relief=RAISED,image=self.cat1)
        self.lbl_img_cat1.place(x=5,y=190) 

        self.cat2 = Image.open(r"D:\new\projet python\gestion_licence\image\im2.jpg")
        self.cat2=self.cat2.resize((480,275),)
        self.cat2=ImageTk.PhotoImage(self.cat2)

        self.lbl_img_cat2=Label(self.root,bd=7,relief=RAISED,image=self.cat2)
        self.lbl_img_cat2.place(x=530,y=205)   
    
    def ajouter(self):
        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        try:
            if self.var_nom.get()=="":
                messagebox.showerror("erreur","veillez saisir le champ categories produit!")
            else:
                cur.execute("select * from categorie where nom=?",(self.var_nom.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("erreur","la categories existe déja!")
                else:
                    cur.execute("insert into categorie (nom) values (?)",(self.var_nom.get(),))
                    con.commit()
                    self.var_cat_id.set("")
                    self.var_nom.set("")
                    self.afficher()
                    messagebox.showinfo("succès","enregistrement effectué!")        
        except Exception as ex:
          messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")

    def afficher(self):
      con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
      cur=con.cursor()
      try:
        cur.execute("select * from categorie")
        rows = cur.fetchall()
        self.cateogrieliste.delete(*self.cateogrieliste.get_children())
        for row in rows:
          self.cateogrieliste.insert("",END,values=row)
      except Exception as ex:
        messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")

    def get_donne(self,ev):
      r=self.cateogrieliste.focus()
      contenu = self.cateogrieliste.item(r)
      row = contenu["values"]
      self.var_cat_id.set(row[0])
      self.var_nom.set(row[1])

    def supprimer(self):
      con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
      cur=con.cursor()
      try:
          if self.var_cat_id.get()=="":
              messagebox.showerror("erreur","Veillez selectionner une catégories dans la liste!")
          else:
              cur.execute("select * from categorie where cid=?",(self.var_cat_id.get(),))
              row = cur.fetchone()
              if row==None:
                  messagebox.showerror("erreur","L'id n'exciste pas!")
              else:
                  op = messagebox.askyesno("Confirmer","Voulez-vous vraiment supprimer?")
                  if op==TRUE:
                    cur.execute("delete from categorie where cid=?",(self.var_cat_id.get(),))
                    con.commit()
                    self.afficher()
                    self.var_cat_id.set("")
                    self.var_nom.set("")
                    messagebox.showinfo("Succès","supprimer avec succès!")




      except Exception as ex:
        messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")
  









if __name__=="__main__":
    root=Tk()
    obj = Categorie(root)
    root.mainloop()