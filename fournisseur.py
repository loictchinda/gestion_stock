import http
from http.client import responses
from msilib.schema import ComboBox, Component
from sqlite3.dbapi2 import Row
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


class Fournisseur:
    def __init__(self,root):
        self.root=root
        self.root.title("FOURNISSEUR")
        self.root.geometry("1100x580+90+90")
        self.root.config(bg="white")
        self.root.focus_force()


        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS fournisseur(forid text PRIMARY KEY,nom text,contact text,description text)")
        con.commit()

        ### variables
        self.var_recherche_txt = StringVar()
        self.var_forid = StringVar()
        self.var_nom = StringVar()
        self.var_contact = StringVar()
    #### titre
        titre = Label(self.root,text="FORMULAIRE FOURNISSEUR",font=("times new roman",15),cursor="hand2",bg="cyan").place(x=0,y=15,width=1100)


    #### option recherche
        recher_option = Label(self.root,text="Rechercher ID Fournisseur:",font=("times new roman",15),bg="white")
        recher_option.place(x=480,y=60)
        recher_text = Entry(self.root,textvariable=self.var_recherche_txt,font=("times new roman",15), bg="lightyellow").place(x=710,y=60,width=120)
        rechercher_btn = Button(self.root,command=self.recherche,text="RECHERCHER",font=("times new roman",13,"bold"),cursor="hand2",bg="blue",fg="white").place(x=840,y=60,height=30)
        tous_btn = Button(self.root,command=self.afficher,text="TOUS",font=("times new roman",13,"bold"),cursor="hand2",bg="lightgray").place(x=980,y=60,height=30)

        ##contenu
        # linge1
        lbl_fourid = Label(self.root, text="ID_FOURNISSEUR:",font=("goudy old style",15),bg="white").place(x=50,y=60)
        self.txt_fourid = Entry(self.root,textvariable=self.var_forid,font=('goudy old stylle',15),bg="lightyellow")
        self.txt_fourid.place(x=230,y=60,width=140)

        # linge2

        lbl_nom = Label(self.root, text="NOM:",font=("goudy old style",15),bg="white").place(x=50,y=100)
        txt_nom = Entry(self.root,textvariable=self.var_nom,font=('goudy old stylle',15),bg="lightyellow").place(x=230,y=100,width=140)
        # linge3

        lbl_contact = Label(self.root, text="CONTACT:",font=("goudy old style",15),bg="white").place(x=50,y=140)
        txt_contact = Entry(self.root,textvariable=self.var_contact,font=('goudy old stylle',15),bg="lightyellow").place(x=230,y=140,width=140)

        # linge4

        lbl_description = Label(self.root, text="DESCRIPTION:",font=("goudy old style",15),bg="white").place(x=50,y=180)
        self.txt_description = Text(self.root,font=('goudy old stylle',15),bg="lightyellow")
        self.txt_description.place(x=230,y=180,width=400,height=90)

        ####} Button ajouter
        self.ajout_btn = Button(self.root,command=self.ajouter, text="AJOUTER",font=("times new roman",15,"bold"),cursor="hand2",bg="green",state="normal")
        self.ajout_btn.place(x=70,y=290,width=100,height=30)

            ####} Button  modifier
        self.modifier_btn = Button(self.root,command=self.modifier, text="MODIFIER",font=("times new roman",15,"bold"),cursor="hand2",bg="yellow",state="disable")
        self.modifier_btn.place(x=180,y=290,width=120,height=30)

            ####} Button  supprimer
        self.supprimer_btn = Button(self.root,command=self.supprimer, text="SUPPRIMER",font=("times new roman",15,"bold"),cursor="hand2",bg="red",state="disable")
        self.supprimer_btn.place(x=320,y=290,width=120,height=30)

            ####} Button  reinitialiser
        self.actualiser_btn = Button(self.root,command=self.reini, text="ACTUALISER",font=("times new roman",15,"bold"),cursor="hand2",bg="lightgray")
        self.actualiser_btn.place(x=450,y=290,width=140,height=30)

            ####} Button  imprimer
        self.imprimer_btn = Button(self.root,command=self.imprimer, text="IMPRIMER",font=("times new roman",15,"bold"),cursor="hand2",bg="blue")
        self.imprimer_btn.place(x=600,y=290,width=120,height=30)

        ####### Liste fournisseur

        
        listeFrame = Frame(self.root,bd=3, relief=RIDGE)
        listeFrame.place(x=50,y=350,height=220,width=800)

        scroll_y = Scrollbar(listeFrame,orient=VERTICAL,width=30)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x = Scrollbar(listeFrame,orient=HORIZONTAL,width=30)
        scroll_x.pack(side=BOTTOM,fill=X)

        self.fournisseurliste = ttk.Treeview(listeFrame,columns=("forid","nom","contact","description"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.fournisseurliste.xview)
        scroll_y.config(command=self.fournisseurliste.yview)

        self.fournisseurliste.heading("forid",text="ID_FOURNISSEUR",anchor="w")
        self.fournisseurliste.heading("nom",text="NOM",anchor="w")
        self.fournisseurliste.heading("contact",text="CONTACT",anchor="w")
        self.fournisseurliste.heading("description",text="DESCRIPTION",anchor="w")

        self.fournisseurliste["show"]="headings"
        self.fournisseurliste.pack(fill=BOTH,expand=1)
        self.fournisseurliste.bind("<ButtonRelease-1>",self.get_donne)

        self.afficher()

        ####### creation des foctions

    def ajouter(self):
        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        try:
            if self.var_forid.get=="" and self.var_contact=="" and self.var_nom.get=="":
              messagebox.showerror("Erreur","Veillez remplir tous les champs!")
            else:
              cur.execute("select * from fournisseur where forid =?",(self.var_forid.get(),))
              row = cur.fetchone()
              if row!=None:
                messagebox.showerror("Erreur","l'ID_fournisseur existe déja!")
              else:
                  cur.execute("insert into fournisseur (forid,nom,contact,description) values(?,?,?,?)",(
                      self.var_forid.get(),
                      self.var_nom.get(),
                      self.var_contact.get(),
                      self.txt_description.get("1.0",END)
                  ))
                  con.commit()
                  self.afficher()
                  messagebox.showinfo("succès","ajouter avec succès!")
        
        except Exception as ex:
           messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")
        
    def afficher(self):
      con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
      cur=con.cursor()
      try:
        cur.execute("select * from fournisseur")
        rows = cur.fetchall()
        self.fournisseurliste.delete(*self.fournisseurliste.get_children())
        for row in rows:
          self.fournisseurliste.insert("",END,values=row)
      except Exception as ex:
        messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")


    def get_donne(self,ev):
      self.ajout_btn.config(state="disable")
      self.modifier_btn.config(state="normal")
      self.supprimer_btn.config(state="normal")
      self.txt_fourid.config(state="readonly")
      r=self.fournisseurliste.focus()
      contenu = self.fournisseurliste.item(r)
      row = contenu["values"]
      self.var_forid.set(row[0]),
      self.var_nom.set(row[1]),
      self.var_contact.set(row[2]),
      self.txt_description.delete("1.0",END),
      self.txt_description.insert(END,row[3])


    def modifier(self):
      con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
      cur=con.cursor()
      try:
          cur.execute("update fournisseur set nom=?,contact=?, description=? where forid=?",(
              self.var_nom.get(),
              self.var_contact.get(),
              self.txt_description.get("1.0",END),
              self.var_forid.get()
          ))
          con.commit()
          self.afficher()
          messagebox.showinfo("succès","modification effectué avec succès!")

      except Exception as ex:
        messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")

    def supprimer(self):
      con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
      cur=con.cursor()

      try:
        op = messagebox.askyesno("Confirmer","Voulez-vous vraiment supprimer?")
        if op==TRUE:
          cur.execute("delete from fournisseur where forid=?",(self.var_forid.get(),))
          con.commit()
          self.afficher()
          
          messagebox.showinfo("Succès","supprimer avec succès!")

      except Exception as ex:
        messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")


    def reini(self):
        self.txt_fourid.config(state="normal")
        self.ajout_btn.config(state="normal")
        self.modifier_btn.config(state="disable")
        self.supprimer_btn.config(state="disable")
        self.var_forid.set("")
        self.var_nom.set("")
        self.var_contact.set("")
        self.var_recherche_txt.set("")
        self.txt_description.delete("1.0",END)

    def recherche(self):
        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        try:
            if self.var_recherche_txt.get()=="":
                messagebox.showerror("erreur","Veillez remplir le champs de rechercher!")
            else:
                cur.execute("select * from fournisseur where forid=?",(self.var_recherche_txt.get(),))
                row= cur.fetchone()
                if row != None:
                    self.fournisseurliste.delete(*self.fournisseurliste.get_children())
                    self.fournisseurliste.insert("",END, values=row)
                else:
                    messagebox.showerror("Erreur","Aucun resultat trouves!")
    
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")

    def imprimer(self):


      class PDF(FPDF):
        def header(self):
            self.set_font("helvetica","B",10)
            self.cell(5,20,'MAGASIN HASSAN',border=False)
            self.ln(6)

            self.set_font("helvetica","B",10)
            self.cell(5,20,'TEL:698554821',border=False)
            self.ln(6)

            self.set_font("helvetica","B",10)
            self.cell(5,20,'SITE: http://www.hassan.com ',border=False)
            self.ln(6)
            self.set_font("helvetica","B",10)
            self.cell(5,20,'siege: YAOUNDE',border=False)
            self.ln(6)

            self.cell(5,20,"Statut:Entreprise privée",border=False)
            self.ln(6)
            self.set_font("helvetica","B",10)

            self.set_line_width(1)
            self.image(r"D:\new\projet python\gestion_licence\image\font.jpg",155,20,40)
            self.ln(10)
          
            self.set_left_margin(8)
            self.set_font("helvetica", "B", 20)
            self.cell(0,40,"LISTES DES EMPLOYES",border=False,align="C")
            self.ln(40)

        def footer(self):
            self.set_y(-15)
            self.set_font('helvetica','I',10)
            self.cell(0,10,f'Date:{datet}')
            self.cell(0,10,f'Page {self.page_no()}/{1}',align='C')

      pdf=PDF('P','mm','Letter')
      datet= datetime.datetime.today()
      pdf.alias_nb_pages()
      pdf.set_auto_page_break(auto=True,margin=15)
      perso=[]

      pdf.add_page()

      TABLE_COL_NAMES = ("forid","nom","contact","description")
      con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
      cur=con.cursor()
      cur.execute("select * from fournisseur")
      val=[]
      for row in cur:
        val.append(row)
        #con.close()
      TABLE_DATA = val
      pdf.set_left_margin(8)
      def render_table_header():
        pdf.set_font(family="",style="B")
        for col_name in TABLE_COL_NAMES:
            pdf.cell(17.5,9,col_name,border=1,align='C')
        pdf.ln()
      pdf.set_font("Times",size=8)
      pdf.set_font(family="",style="B")
      pdf.set_left_margin(8)
      render_table_header()
      for _ in range(1):
        for rows in TABLE_DATA:
          #if pdf.page_break_trigger():
            pdf.set_left_margin(8)
            render_table_header
            for h in rows:
                pdf.set_left_margin(2)
                pdf.cell(20, 12, f'{h}', border=1, align='C')
            pdf.ln(10)
      pdf.set_font('helvetica','BUI',19)
      pdf.output('fournisseur.pdf')
      file="fournisseur.pdf"
      os.popen(file)
      os.startfile(file,"print")
      messagebox.showinfo("succes","Imprimer avec success") 

          
           






if __name__=="__main__":
    root=Tk()
    obj = Fournisseur(root)
    root.mainloop()