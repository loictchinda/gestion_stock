from employe import Employe
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


class Accueil:
    def __init__(self,root):
        self.root=root
        self.root.title("ACCUEIL")
        self.root.geometry("1358x700+0+0")
        self.root.config(bg="white")

        self.icon_title=ImageTk.PhotoImage(file=r"D:\new\projet python\gestion_licence\image\logo.png")
        titre =Label(self.root, text="BIENVENUE A L'ENTREPRISE HASSAN",image=self.icon_title,font=("times nnew roman",40,"bold"), bg="cyan",anchor="w",padx=30,compound=LEFT).place(x=0,y=0, relwidth=1, height=100 )
        
        #button deconnection
        
        btn_deconnecte= Button(self.root,text="Deconnecter",command=self.deconnecter, font=("times new roman",20,"bold"),bd="5", cursor="hand2",bg="orange").place(x=1180,y=20)
        
        #heure

        self.lbl_heure=Label(self.root,text="Bienvenue chez Hassan\t\t Date :DD-MM-YYYY\t\t Heure: HH:MM:SS",font=("times new roman",15), bg="black",fg="white")
        self.lbl_heure.place(x=0,y=100, relwidth=1,height=40)
        self.modifier_heure()
        # MENU
        self.menulogo= Image.open(r"D:\new\projet python\gestion_licence\image\ordi.jpeg")
        self.menulogo = self.menulogo.resize((350,170)) #,Image.ANTIALIAS)
        self.menulogo = ImageTk.PhotoImage(self.menulogo)

        Menu_Frame = Frame(self.root, bd=2, relief=RIDGE,bg="white")
        Menu_Frame.place(x=0,y=140,width=300,height=500)

        lbl_menulogo = Label(Menu_Frame,image=self.menulogo)
        lbl_menulogo.pack(side=TOP,fill=X)

        self.icon_menu = ImageTk.PhotoImage(file=r"D:\new\projet python\gestion_licence\image\per.png")

        lbl_menu = Label(Menu_Frame,text="Menu",font=('times new roman',20,"bold"),bg="orange").pack(side=TOP,fill=X)

        btn_employe = Button(Menu_Frame, text="Employé",command=self.employe,image=self.icon_menu,padx=10,anchor="w",compound=LEFT,font=("times new roman",15),bd=7,cursor="hand2",bg="white",height=30).pack(side=TOP,fill=X)
        btn_fournisseur = Button(Menu_Frame, text="Fournisseur",command=self.fournisseur,image=self.icon_menu,padx=10,anchor="w",compound=LEFT,font=("times new roman",15),bd=7,cursor="hand2",bg="white",height=30).pack(side=TOP,fill=X)
        btn_categories = Button(Menu_Frame, text="Catégories",command=self.categorie,image=self.icon_menu,padx=10,anchor="w",compound=LEFT,font=("times new roman",15),bd=7,cursor="hand2",bg="white",height=30).pack(side=TOP,fill=X)
        btn_peoduit = Button(Menu_Frame, text="produit",command=self.produit,image=self.icon_menu,padx=10,anchor="w",compound=LEFT,font=("times new roman",15),bd=7,cursor="hand2",bg="white",height=30).pack(side=TOP,fill=X)
        btn_vente = Button(Menu_Frame, text="vente",command=self.vente,image=self.icon_menu,padx=10,anchor="w",compound=LEFT,font=("times new roman",15),bd=7,cursor="hand2",bg="white",height=30).pack(side=TOP,fill=X)
        btn_quitter = Button(Menu_Frame, text="Quitter",command=self.quitter,image=self.icon_menu,padx=10,anchor="w",compound=LEFT,font=("times new roman",15),bd=7,cursor="hand2",bg="white",height=30).pack(side=TOP,fill=X)

        #contenu du menu

        self.lbl_totlalemploye= Label(self.root,text="Total Employés \n[0]",bg="green",bd=5, relief=RAISED,fg="white",font=("goudy old style",20,"bold"))
        self.lbl_totlalemploye.place(x=310,y=200,height=120,width=200)

        
        self.lbl_totlalfournisseur= Label(self.root,text="Total Fournisseurs \n[0]",bg="red",bd=5, relief=RAISED,fg="white",font=("goudy old style",20,"bold"))
        self.lbl_totlalfournisseur.place(x=530,y=200,height=120,width=220)

        self.lbl_totlalcategorie= Label(self.root,text="Total Catégories \n[0]",bg="blue",bd=5, relief=RAISED,fg="white",font=("goudy old style",20,"bold"))
        self.lbl_totlalcategorie.place(x=765,y=200,height=120,width=195)
        
        self.lbl_totlalproduit= Label(self.root,text="Total Produits \n[0]",bg="gray",bd=5, relief=RAISED,fg="white",font=("goudy old style",20,"bold"))
        self.lbl_totlalproduit.place(x=970,y=200,height=120,width=180)
        
        self.lbl_totlalvente= Label(self.root,text="Total Ventes \n[0]",bg="purple",bd=5, relief=RAISED,fg="white",font=("goudy old style",20,"bold"))
        self.lbl_totlalvente.place(x=1160,y=200,height=120,width=180)

        self.modifier()

        #footer
        lbl_footer = Label(self.root,text="Developper par Hassan\t\t\twilliamshassan@gmail.com\t\t\t +237698554821\t\t\t &&\t\t\t  Loic\t\t\loictchinda13@gmail.com\t\t\t +237673668737",font=("times new roman",10), bg="green",fg="white").pack(side=BOTTOM,fill=X)

    def employe(self):
        self.obj = os.popen("employe.py")
    def vente(self):
        self.obj = os.popen("vente.py")

    def categorie(self):
        self.obj= os.popen("categories.py")

    def fournisseur(self):
       self.obj = os.popen("fournisseur.py")

    def produit(self):
       self.obj = os.popen("produit.py")
         
    def quitter(self):
        self.root.destroy() 

    def deconnecter(self):
        self.root.destroy()
        self.obj = os.popen("login.py")

    def modifier_heure(self):
        heure_ = (strftime("%H:%M:%S"))
        date_= (strftime("%d/%m/%Y"))
        self.lbl_heure.config(text=f"BIENVENUE CHEZ HASSAN \t\t Date: {str(date_)} \t\t Heure:{str(heure_)}")
        self.lbl_heure.after(200,self.modifier_heure)

    def modifier(self):
        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()

        try:
            cur.execute("select * from produit")
            produit= cur.fetchall()
            self.lbl_totlalproduit.config(text=f"Total Produits \n[{str(len(produit))}]")

            cur.execute("select * from categorie")
            categorie= cur.fetchall()
            self.lbl_totlalcategorie.config(text=f"Total Catégories \n[{str(len(categorie))}]")

            cur.execute("select * from fournisseur")
            fournisseur= cur.fetchall()
            self.lbl_totlalfournisseur.config(text=f"Total Fournisseurs \n[{str(len(fournisseur))}]")

            cur.execute("select * from employe")
            employe= cur.fetchall()
            self.lbl_totlalemploye.config(text=f"Total Employés \n[{str(len(employe))}]")

            nombre_factre=len(os.listdir(r"D:\new\projet python\gestion_licence\Facture"))
            self.lbl_totlalvente.config(text=f"Total Ventes \n[{str(nombre_factre)}]")


        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")    






if __name__=="__main__":
    root=Tk()
    obj = Accueil(root)
    root.mainloop()
