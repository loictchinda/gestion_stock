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


class Produit:
    def __init__(self,root):
        self.root=root
        self.root.title("PRODUIT")
        self.root.geometry("1100x580+90+90")
        self.root.config(bg="white")
        self.root.focus_force()

        ####base de donnees
        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS produit(pid INTEGER PRIMARY KEY AUTOINCREMENT,categorie text,fournisseur text,nom text,prix text,quandite text,status text)")
        con.commit()


        ### les variables
        
        self.var_recherche_type = StringVar()
        self.var_recherche_txt = StringVar()
        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_four = StringVar()
        self.var_nom = StringVar()
        self.var_prix = IntVar()
        self.var_qte = StringVar()
        self.var_status = StringVar()

        self.four_liste = []
        self.liste_four()

        produit_frame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        produit_frame.place(x=10,y=10,width=550,height=550)

        titre = Label(produit_frame,text="DETAILS DES PRODUITS",font=("goudy old style",20,"bold"),bg="cyan").pack(side=TOP,fill=X)

        lbl_categories = Label(produit_frame,text="catégories:",font=("goudy old style",18,),bg="white").place(x=20,y=50)
        lbl_fournisseur = Label(produit_frame,text="Fournisseur:",font=("goudy old style",18,),bg="white").place(x=20,y=100)
        lbl_nomproduit = Label(produit_frame,text="Nom Produit:",font=("goudy old style",18,),bg="white").place(x=20,y=150)
        lbl_Quandite = Label(produit_frame,text="Quandite:",font=("goudy old style",18,),bg="white").place(x=20,y=200)
        lbl_prix = Label(produit_frame,text="Prix:",font=("goudy old style",18,),bg="white").place(x=20,y=250)
        lbl_status = Label(produit_frame,text="Status:",font=("goudy old style",18,),bg="white").place(x=20,y=300)

        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        cur.execute("select nom from categorie")
        rows = cur.fetchall()


        txt_categories=ttk.Combobox(produit_frame,values=rows,state="r",textvariable=self.var_cat,justify=CENTER,font=("goudy old style",15))
        txt_categories.place(x=150,y=50,width=260)
        txt_categories.set("Select")

        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        cur.execute("select nom from fournisseur")
        rows = cur.fetchall()


        txt_fournisseur=ttk.Combobox(produit_frame,values=self.four_liste,state="r",textvariable=self.var_four,justify=CENTER,font=("goudy old style",15))
        txt_fournisseur.place(x=150,y=100,width=260)
        txt_fournisseur.current(0)

        txt_nom = Entry(produit_frame,textvariable=self.var_nom,font=("goudy old style",15),bg="lightyellow").place(x=160,y=150,width=260)
        txt_quanditee = Entry(produit_frame,textvariable=self.var_qte,font=("goudy old style",15),bg="lightyellow").place(x=160,y=200,width=260)
        txt_prix = Entry(produit_frame,textvariable=self.var_prix,font=("goudy old style",15),bg="lightyellow").place(x=160,y=250,width=260)

        txt_status=ttk.Combobox(produit_frame,values=["Active","Inactive"],state="r",textvariable=self.var_status,justify=CENTER,font=("goudy old style",15))
        txt_status.place(x=150,y=300,width=260)
        txt_status.current(0)

        ### buttom

        self.ajouter_btn = Button(produit_frame,command=self.ajouter,text="AJOUTER",state="normal",font=("times new roman",15),bg="green",cursor="hand2")
        self.ajouter_btn.place(x=1,y=380,height=40,width=98)

        self.modifier_btn = Button(produit_frame,command=self.modifier,text="MODIFIER",state="disabled",font=("times new roman",15),bg="red",cursor="hand2")
        self.modifier_btn.place(x=100,y=380,height=40,width=100)

        self.supprimer_btn = Button(produit_frame,command=self.supprimer,text="SUPPRIMER",state="disabled",font=("times new roman",15),bg="yellow",cursor="hand2")
        self.supprimer_btn.place(x=203,y=380,height=40,width=109)

        self.renitialiser_btn = Button(produit_frame,command=self.reini,text="ACTUALISER",font=("times new roman",15),bg="lightgray",cursor="hand2")
        self.renitialiser_btn.place(x=314,y=380,height=40,width=125)
        self.imprimer_btn = Button(produit_frame,text="IMPRIMER",font=("times new roman",15),bg="blue",cursor="hand2")
        self.imprimer_btn.place(x=440,y=380,height=40,width=105)

        ##### frame rechercher

        recher_frame = LabelFrame(self.root,text="Recherche Produit",font=("times new roman",15),bd=2,relief=RIDGE,bg="white")
        recher_frame.place(x=580,y=5,width=500,height=70)

        txt_recher_option=ttk.Combobox(recher_frame,values=["Categorie","Fournisseur","Nom_produit"],state="r",textvariable=self.var_recherche_type,justify=CENTER,font=("goudy old style",15))
        txt_recher_option.place(x=5,y=10,width=140)
        txt_recher_option.current(0)

        txt_recher = Entry(recher_frame,textvariable=self.var_recherche_txt,font=("goudy old style",15),bg="lightyellow").place(x=150,y=10,width=130)

        rechercher = Button(recher_frame,command=self.recherche,text="RECHERCHER",font=("times new roman",15),bg="blue",cursor="hand2",fg="white").place(x=285,y=10,width=135,height=30)

        tous_reche = Button(recher_frame,command=self.afficher,text="TOUS",font=("times new roman",15),bg="lightgray",cursor="hand2").place(x=430,y=10,width=60,height=30)

        ####### Listes produit

        
        listeFrame = Frame(self.root,bd=3, relief=RIDGE)
        listeFrame.place(x=580,y=90,height=460,width=515)

        scroll_y = Scrollbar(listeFrame,orient=VERTICAL,width=20)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x = Scrollbar(listeFrame,orient=HORIZONTAL,width=20)
        scroll_x.pack(side=BOTTOM,fill=X)

        self.produitliste = ttk.Treeview(listeFrame,columns=("pid","Categorie","Fournisseur","Nom","Prix","Quandite","Status"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.produitliste.xview)
        scroll_y.config(command=self.produitliste.yview)

        self.produitliste.heading("pid",text="ID_PRODUIT",anchor="w")
        self.produitliste.heading("Categorie",text="CATEGORIE",anchor="w")
        self.produitliste.heading("Nom",text="NOM",anchor="w")
        self.produitliste.heading("Fournisseur",text="FOURNISSEUR",anchor="w")
        self.produitliste.heading("Prix",text="PRIX",anchor="w")
        self.produitliste.heading("Quandite",text="QUANDITE",anchor="w")
        self.produitliste.heading("Status",text="STATUS",anchor="w")

        self.produitliste["show"]="headings"
        self.produitliste.pack(fill=BOTH,expand=1)
        self.afficher()
        self.produitliste.bind("<ButtonRelease-1>",self.get_donne)


    def liste_four(self):
        self.four_liste.append("vide")
        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()

        try:
            cur.execute("select nom from fournisseur")
            four =cur.fetchall()
            if len(four)>0:
                del self.four_liste[0]
                self.four_liste.append("Select")
                for i in four:
                    self.four_liste.append(i[0])
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")


    def ajouter(self):
        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        try:
            if self.var_cat.get=="Select" and self.var_four=="Select" and self.var_nom.get=="":
              messagebox.showerror("Erreur","Veillez remplir tous les champs!")
            else:
              cur.execute("select * from produit where nom =?",(self.var_nom.get(),))
              row = cur.fetchone()
              if row!=None:
                messagebox.showerror("Erreur","le produit existe déja!")
              else:
                  cur.execute("insert into produit (categorie,fournisseur,nom,prix,quandite,status) values(?,?,?,?,?,?)",(
                      self.var_cat.get(),
                      self.var_four.get(),
                      self.var_nom.get(),
                      self.var_prix.get(),
                      self.var_qte.get(),
                      self.var_status.get()
                  ))
                  con.commit()
                  self.afficher()
                  self.reini()
                  messagebox.showinfo("succès","ajouter avec succès!")
        
        except Exception as ex:
           messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")

    def afficher(self):
      con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
      cur=con.cursor()
      try:
        cur.execute("select * from produit")
        rows = cur.fetchall()
        self.produitliste.delete(*self.produitliste.get_children())
        for row in rows:
          self.produitliste.insert("",END,values=row)
      except Exception as ex:
        messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")

        
    def get_donne(self,ev):
      self.ajouter_btn.config(state="disable")
      self.modifier_btn.config(state="normal")
      self.supprimer_btn.config(state="normal")
      r=self.produitliste.focus()
      contenu = self.produitliste.item(r)
      row = contenu["values"]
      self.var_pid.set(row[0]) 
      self.var_cat.set(row[1])
      self.var_four.set(row[2])
      self.var_nom.set(row[3])
      self.var_prix.set(row[4])
      self.var_qte.set(row[5])
      self.var_status.set(row[6])
        
         
    def modifier(self):
        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("erreur","Veillez selectionner un produit!")
            else:
                cur.execute("select * from produit where pid=?",(self.var_pid.get(),))    
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("erreur","Veillez selectionner un produit sur la liste!")
                else:
                    cur.execute("update produit set categorie=?,fournisseur=?,nom=?,prix=?,quandite=?,status=? where pid=?",(
                      self.var_cat.get(),
                      self.var_four.get(),
                      self.var_nom.get(),
                      self.var_prix.get(),
                      self.var_qte.get(),
                      self.var_status.get(),
                      self.var_pid.get()
                    ))
                    con.commit()
                    self.afficher()
                    self.reini()
                    messagebox.showinfo("succès","Modifier avec succès!")
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")

    def supprimer(self):
      con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
      cur=con.cursor()

      try:
        op = messagebox.askyesno("Confirmer","Voulez-vous vraiment supprimer?")
        if op==TRUE:
          cur.execute("delete from produit where pid=?",(self.var_pid.get(),))
          con.commit()
          self.afficher()
          self.reini()
          messagebox.showinfo("Succès","supprimer avec succès!")

      except Exception as ex:
        messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")

    def reini(self):
        self.ajouter_btn.config(state="normal")
        self.modifier_btn.config(state="disable")
        self.supprimer_btn.config(state="disable")

        self.var_pid.set("") 
        self.var_cat.set("Select")
        self.var_four.set("Select")
        self.var_nom.set("")
        self.var_prix.set("")
        self.var_qte.set("")
        self.var_status.set("Active")
        self.var_recherche_txt.set("")

    def recherche(self):
        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()

        try:
            if self.var_recherche_txt.get()=="":
                messagebox.showerror("erreur","Veillez entrer le champs a rechercher!")
            else:
                cur.execute("select * from produit where categorie LIKE '%"+self.var_recherche_txt.get()+"%'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.produitliste.delete(*self.produitliste.get_children())
                    for row in rows:
                        self.produitliste.insert("",END,values=row)  
                else:
                    messagebox.showerror("erreur","Aucun resultat trouvé!")      
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")




if __name__=="__main__":
    root=Tk()
    obj = Produit(root)
    root.mainloop()