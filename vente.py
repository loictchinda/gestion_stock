from ast import Index
import builtins
import http
from http.client import responses
from msilib.schema import ComboBox, Component
import textwrap
import tkinter
from cProfile import label
from email import message
from optparse import TitledHelpFormatter, Values
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


class Vente:
    def __init__(self,root):
        self.root=root
        self.root.title("VENTE")
        self.root.geometry("1050x510+90+90")
        self.root.config(bg="white")
        self.root.focus_force()


        self.var_nfacture = StringVar()
        self.list_facture =[]

        Title=Label(self.root, text="Consulter Facture des clients",font=("goudy old style",20),bg="cyan",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=0,pady=15)

        lbl_n_facture=Label(self.root, text="Numéro Facture:",font=("times news roman",15),bg="white").place(x=5,y=80)
        txt_n_facture = Entry(self.root,textvariable=self.var_nfacture,font=("times new roman",15),bg="lightyellow").place(x=160,y=80,width=150)

        btn_recherche = Button(self.root,command=self.recherche,text="RECHERCHER",font=("times new roman",15,"bold"),bg="green",cursor="hand2").place(x=320,y=80,width=150,height=30)
        btn_reini = Button(self.root,command=self.reini,text="ACTUALISER",font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=480,y=80,width=150,height=30)


        vente_frame = Frame(self.root,bd=3, relief=RIDGE)
        vente_frame.place(x=5,y=120,height=380,width=280)

        scroll_y = Scrollbar(vente_frame,orient=VERTICAL,width=30)

        self.liste_vente=Listbox(vente_frame,font=("goudy old style",15),bg="white",yscrollcommand=scroll_y.set)
        
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.liste_vente.yview)
        self.liste_vente.pack(fill=BOTH,expand=1)
        self.liste_vente.bind("<ButtonRelease-1>",self.recupereDonee)


        ############# espace facture a afficher

        facture_frame = Frame(self.root,bd=3, relief=RIDGE)
        facture_frame.place(x=310,y=120,height=380,width=350)

        title=Label(facture_frame,text="Facture du client",font=("goudy old style",18,"bold"),bg="orange").pack(side=TOP,fill=X)

        scroll_y2=Scrollbar(facture_frame,orient=VERTICAL,width=25)
        self.espaceFacture=Text(facture_frame,font=("goudy old style",12),bg="lightyellow",yscrollcommand=scroll_y2.set)
        scroll_y2.pack(side=RIGHT,fill=Y)
        scroll_y2.config(command=self.espaceFacture.yview)
        self.espaceFacture.pack(fill=BOTH,expand=1)

        ####### image

        self.facture_photo= Image.open(r"D:\new\projet python\gestion_licence\image\icon.ico")
        self.facture_photo=self.facture_photo.resize((385,380))
        self.facture_photo=ImageTk.PhotoImage(self.facture_photo)
        

        lbl_image=Label(self.root,image=self.facture_photo)
        lbl_image.place(x=660,y=120)

        self.afficher()

        ############ function
    def afficher(self):
            del self.list_facture[:]
            self.liste_vente.delete(0,END)
            for i in os.listdir(r"D:\new\projet python\gestion_licence\Facture"):
                if i.split(".")[-1]=="txt":
                    self.liste_vente.insert(END,i)
                    self.list_facture.append(i.split(".")[0])

    def recupereDonee(self,ev):
        index_ = self.liste_vente.curselection()  
        nom_fichier=self.liste_vente.get(index_)
        fichier_ouvert = open(fr"D:\new\projet python\gestion_licence\Facture\{nom_fichier}","r")
        self.espaceFacture.delete("1.0",END)
        for i in fichier_ouvert:
            self.espaceFacture.insert(END,i)
        fichier_ouvert.close()    


    def recherche(self):
        if self.var_nfacture.get()=="":
            messagebox.showerror("Erreur","Veillez entrer un numéro de facture!")
        else:
            if self.var_nfacture.get() in self.list_facture:
                fichier_ouvert = open(fr"D:\new\projet python\gestion_licence\Facture\{self.var_nfacture.get()}.txt","r")
                self.espaceFacture.delete("1.0",END)
                for i in fichier_ouvert:
                    self.espaceFacture.insert(END,i)
                fichier_ouvert.close()
            else:
                messagebox.showerror("Erreur","Numéro de facture invalide!")        

    def reini(self):
        self.afficher()
        self.espaceFacture.delete("1.0",END)
        self.var_nfacture.set("")










if __name__=="__main__":
    root=Tk()
    obj = Vente(root)
    root.mainloop()