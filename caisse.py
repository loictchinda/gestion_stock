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
from time import time
from time import strftime
from tkinter import font
from typing import Union
import mysql.connector
from PIL import ImageTk, Image
import os
import re
import mysql
from tkcalendar import Calendar
from fpdf import FPDF
import datetime
import sqlite3


class Caisse:
    def __init__(self,root):
        self.root=root
        self.root.title("CAISSE")
        self.root.geometry("1358x700+0+0")
        self.root.config(bg="white")


        self.cart_liste = []
        self.ck_print = 0

    ##### titre
        self.icon_title =ImageTk.PhotoImage(file=r"D:\new\projet python\gestion_licence\image\logo.png")
        titre =Label(self.root, text="CAISSE DE PAIEMENT",image=self.icon_title,font=("times nnew roman",20,"bold"), bg="cyan",anchor="w",padx=30,compound=LEFT).place(x=0,y=0, relwidth=1, height=70)

        ## button deconnecte
        btn_deconnecte= Button(self.root,text="Deconnecter",command=self.deconnecter, font=("times new roman",20,"bold"),bd="5", cursor="hand2",bg="orange").place(x=1180,y=8)

        ##### heure
        self.lbl_heure=Label(self.root,text="BIENVENUE CHEZ HASSAN \t\t Date: DD-MM-YYYY \t\t Heure: HH:MM:SS", font=("times new roman",15),bg="black",fg="white")
        self.lbl_heure.place(x=0,y=70,relwidth=1,height=40) 
        self.modifier_heure()
        ### produit

        self.var_recherche=StringVar()

        produitframe1 = Frame(self.root,bd=4,relief=RIDGE,bg="white")
        produitframe1.place(x=10,y=115,width=500,height=550)

        ptitre =Label(produitframe1,text="Tous les produits",font=("goudy old style",15,"bold"),bg="cyan",bd=3,relief=RIDGE).pack(side=TOP,fill=X)   

        produitframe2 = Frame(self.root,bd=4,relief=RIDGE,bg="white")
        produitframe2.place(x=15,y=150,width=490,height=120)

        lbl_recherche = Label(produitframe2,text="Recherche Produit | Par Nom",font=("goudy old style",15,"bold"),bg="green",fg="white",bd=3,relief=RIDGE).place(x=5,y=8)
        lbl_nomproduit = Label(produitframe2,text="Nom Produit:",font=("goudy old style",15,"bold"),bg="white").place(x=5,y=60)

        txt_recherche = Entry(produitframe2,textvariable=self.var_recherche,font=("goudy old style",15),bg="lightyellow").place(x=125,y=60,width=120)
        recherche_btn =Button(produitframe2,command=self.rechercher,text="RECHERCHE",font=("times new roman",15),bg="lightblue",cursor="hand2").place(x=250,y=60,width=120,height=30)
        tous_btn =Button(produitframe2,command=self.afficher,text="TOUS",font=("times new roman",15),bg="lightgray",cursor="hand2").place(x=380,y=60,width=70,height=30)

  
        produitFrame3 = Frame(produitframe1,bd=3, relief=RIDGE)
        produitFrame3.place(x=2,y=160,height=380,relwidth=1)

        scroll_y = Scrollbar(produitFrame3,orient=VERTICAL,width=30)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x = Scrollbar(produitFrame3,orient=HORIZONTAL,width=30)
        scroll_x.pack(side=BOTTOM,fill=X)

        self.produit_table = ttk.Treeview(produitFrame3,columns=("pid","Nom","Prix","Quandite","Status"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.produit_table.xview)
        scroll_y.config(command=self.produit_table.yview)

        self.produit_table.heading("pid",text="ID_PRODUIT",anchor="w")
        self.produit_table.heading("Nom",text="NOM",anchor="w")
        self.produit_table.heading("Prix",text="PRIX",anchor="w")
        self.produit_table.heading("Quandite",text="QUANDITE",anchor="w")
        self.produit_table.heading("Status",text="STATUS",anchor="w")

        self.produit_table["show"]="headings"
        self.produit_table.pack(fill=BOTH,expand=1)
        self.produit_table.bind("<ButtonRelease-1>",self.get_donne)

        lbl_note =Label(produitframe1,text="Note: 'Entrer 0 Quandité pour retier le produit du panier'",anchor="w",font=("times new roman",10),bg="white",fg="red").pack(side=BOTTOM,fill=X)
        self.afficher()


        ####### Frame Client

        self.var_client_nom=StringVar()
        self.var_contact=StringVar()

        client_frame = Frame(self.root,bd=4,relief=RIDGE,bg="white")
        client_frame.place(x=520,y=120,width=450,height=75)

        ctitle =Label(client_frame,text="Informations du Client",font=("goudy old style",15,"bold"),bg="pink",bd=3,relief=RIDGE).pack(side=TOP,fill=X)

        lbl_nom =Label(client_frame,text="Nom:",font=("goudy old style",15,),bg="white").place(x=10,y=35)
        txt_nom = Entry(client_frame,textvariable=self.var_client_nom,font=("goudy old style",15),bg="lightyellow").place(x=60,y=35,width=120)

        lbl_contact =Label(client_frame,text="Contact:",font=("goudy old style",15,),bg="white").place(x=200,y=35)
        txt_contact = Entry(client_frame,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=280,y=35,width=120)

        ###### calculatrice
        self.var_cal_input = StringVar()

        calcul_cart_frame =Frame(self.root,bd=4,relief=RIDGE,bg="white")
        calcul_cart_frame.place(x=520,y=200,width=450,height=290)

        calculframe =Frame(calcul_cart_frame,bd=4,relief=RIDGE,bg="white")
        calculframe.place(x=5,y=5,width=205,height=268)

        self.txt_calc_input =Entry(calculframe,textvariable=self.var_cal_input,font=("arial",15,"bold"),justify=RIGHT,bg="lightyellow",bd=5,relief=GROOVE,state="readonly",width=15)
        self.txt_calc_input.grid(row=0,columnspan=4)

        self.btn_7=Button(calculframe,text="7",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=lambda:self.get_input(7)).grid(row=1,column=0)
        self.btn_8=Button(calculframe,text="8",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=lambda:self.get_input(8)).grid(row=1,column=1)
        self.btn_9=Button(calculframe,text="9",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=lambda:self.get_input(9)).grid(row=1,column=2)
        self.btn_add=Button(calculframe,text="+",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=lambda:self.get_input("+")).grid(row=1,column=3)

        self.btn_4=Button(calculframe,text="4",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=lambda:self.get_input(4)).grid(row=2,column=0)
        self.btn_5=Button(calculframe,text="5",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=lambda:self.get_input(5)).grid(row=2,column=1)
        self.btn_6=Button(calculframe,text="6",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=lambda:self.get_input(6)).grid(row=2,column=2)
        self.btn_sous=Button(calculframe,text="-",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=lambda:self.get_input("-")).grid(row=2,column=3)

        self.btn_1=Button(calculframe,text="1",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=lambda:self.get_input(1)).grid(row=3,column=0)
        self.btn_2=Button(calculframe,text="2",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=lambda:self.get_input(2)).grid(row=3,column=1)
        self.btn_3=Button(calculframe,text="3",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=lambda:self.get_input(3)).grid(row=3,column=2)
        self.btn_x=Button(calculframe,text="*",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=lambda:self.get_input("*")).grid(row=3,column=3)

        self.btn_0=Button(calculframe,text="0",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=lambda:self.get_input(0)).grid(row=4,column=0)
        self.btn_c=Button(calculframe,text="c",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=self.clear_cal).grid(row=4,column=1)
        self.btn_egal=Button(calculframe,text="=",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=self.resultat).grid(row=4,column=2)
        self.btn_div=Button(calculframe,text="/",font=("arial",10,"bold"),bg="gray",cursor="hand2",width=5,pady=15,command=lambda:self.get_input("/")).grid(row=4,column=3)

        cart_frame =Frame(calcul_cart_frame,bd=3,relief=RIDGE)
        cart_frame.place(x=210,y=5,height=280,width=235)

        self.ctitle =Label(cart_frame,text="Produit Total du Panier: [0]",font=("goudy old style",11,"bold"),bg="pink",bd=3,relief=RIDGE)
        self.ctitle.pack(side=TOP,fill=X)

        scroll_y = Scrollbar(cart_frame,orient=VERTICAL,width=20)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x = Scrollbar(cart_frame,orient=HORIZONTAL,width=20)
        scroll_x.pack(side=BOTTOM,fill=X)

        self.cartTable = ttk.Treeview(cart_frame,columns=("pid","Nom","Prix","Quandite","Stock"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.cartTable.xview)
        scroll_y.config(command=self.cartTable.yview)

        self.cartTable.heading("pid",text="ID_PRODUIT",anchor="w")
        self.cartTable.heading("Nom",text="NOM",anchor="w")
        self.cartTable.heading("Prix",text="PRIX",anchor="w")
        self.cartTable.heading("Quandite",text="QUANDITE",anchor="w")
        self.cartTable.heading("Stock",text="STOCK",anchor="w")

        self.cartTable["show"]="headings"
        self.cartTable.pack(fill=BOTH,expand=1)   
        self.cartTable.bind("<ButtonRelease-1>",self.get_donne_cart)

        ####### ajouter bouton cart
        self.var_pid =StringVar()
        self.pname = StringVar()
        self.var_prix=StringVar()
        self.var_qte =StringVar()
        self.var_stock=StringVar()

        Button_frame = Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Button_frame.place(x=520,y=495,width=450,height=170)

        lbl_p_nom=Label(Button_frame,text="Nom Produit",font=("goudy old style",15),bg="white").place(x=5,y=5)
        txt_p_nom =Entry(Button_frame,font=("goudy old style",15),textvariable=self.pname,bg="lightyellow",state="readonly").place(x=5,y=40,width=120,height=25)

        lbl_p_prix=Label(Button_frame,text="Prix Produit",font=("goudy old style",15),bg="white").place(x=175,y=5)
        txt_p_prix =Entry(Button_frame,font=("goudy old style",15),textvariable=self.var_prix,bg="lightyellow",state="readonly").place(x=175,y=40,width=120,height=25)

        lbl_p_qte=Label(Button_frame,text="Quandité",font=("goudy old style",15),bg="white").place(x=5,y=70)
        txt_p_qte =Entry(Button_frame,font=("goudy old style",15),textvariable=self.var_qte,bg="lightyellow").place(x=5,y=110,width=120,height=25)

        self.lbl_p_stock=Label(Button_frame,text="EN STOCK",font=("goudy old style",15),bg="white")
        self.lbl_p_stock.place(x=190,y=85)

        btn_clear_cart = Button(Button_frame,command=self.clear_cart,text="Réinitialiser",cursor="hand2",font=("times new roman",15),bg="lightgray").place(x=135,y=130,height=30,width=110)
        btn_ajouter_cart = Button(Button_frame,command=self.ajout_modifier,text="AJOUTER|MODIFIER",cursor="hand2",font=("times new roman",15),bg="yellow").place(x=250,y=130,height=30,width=190)
        
        ##### espace facture

        Factuere_frame = Frame(self.root,bd=4,relief=RIDGE, bg="white")
        Factuere_frame.place(x=980,y=115,width=365,height=400)

        ctitle =Label(Factuere_frame,text="Zone de Facture client",font=("goudy old style",15,"bold"),bg="skyblue",bd=3,relief=RIDGE).pack(side=TOP,fill=X)

        scroll_y = Scrollbar(Factuere_frame,orient=VERTICAL,width=20)
        scroll_y.pack(side=RIGHT,fill=Y)

        self.txt_espace_facture = Text(Factuere_frame,yscrollcommand=scroll_y.set)
        self.txt_espace_facture.pack(fill=BOTH,expand=1)
        scroll_y.config(command=self.txt_espace_facture.yview)

        ####### Bouton
        factureMenuframe = Frame(self.root,bd=4,relief=RIDGE,bg="white")
        factureMenuframe.place(x=980,y=520,width=365,height=145)

        self.lbl_montant_facture =Label(factureMenuframe,text="Montant facture \n [0]",font=("goudy old style",15),bg="#3f51b5",fg="black")
        self.lbl_montant_facture.place(x=3,y=5,width=130,height=45)

        self.lbl_montantHT_facture =Label(factureMenuframe,text="Montant HT \n [0]",font=("goudy old style",15),bg="#8bc34a",fg="black")
        self.lbl_montantHT_facture.place(x=140,y=5,width=110,height=45)

        self.lbl_net_payer =Label(factureMenuframe,text="Net à Payer \n [0]",font=("goudy old style",15),bg="#607d8b",fg="black")
        self.lbl_net_payer.place(x=260,y=5,width=95,height=45)

        btn_imprimer = Button(factureMenuframe,command=self.imprimer_facture,text="IMPRIMER",font=("goudy old style",15),bg="blue",fg="black").place(x=245,y=70,width=110,height=40)
        btn_genrer = Button(factureMenuframe,command=self.generer_facture,text="GENERER",font=("goudy old style",15),bg="green",fg="black").place(x=3,y=70,width=110,height=40)
        btn_reinitialiser = Button(factureMenuframe,command=self.clear_all,text="ACTUALISER",font=("goudy old style",15),bg="lightgray",fg="black").place(x=115,y=70,width=130,height=40)

         #footer

        lbl_footer = Label(self.root,text="Developper par Hassan\t\t\twilliamshassan@gmail.com\t\t\t +237698554821\t\t\t &&\t\t\t  Loic\t\t\loictchinda13@gmail.com\t\t\t +237673668737",font=("times new roman",10), bg="green",fg="white").pack(side=BOTTOM,fill=X)

    ####### fonctions

    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set("")

    def resultat(self):
        resultats = self.txt_calc_input.get()    
        self.var_cal_input.set(eval(resultats))

    def afficher(self):
      con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
      cur=con.cursor()
      try:
        cur.execute("select pid,nom,prix,quandite,status from produit where status='Active'")
        rows = cur.fetchall()
        self.produit_table.delete(*self.produit_table.get_children())
        for row in rows:
          self.produit_table.insert("",END,values=row)
      except Exception as ex:
        messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")    

    def rechercher(self):
        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        try:
            if self.var_recherche.get()=="":
              messagebox.showerror("erreur","Veillez saisir le produire a rechercher!")
            else:
                cur.execute("select pid,nom,prix,quandite,status from produit where nom LIKE '%"+self.var_recherche.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.produit_table.delete(*self.produit_table.get_children())
                    for row in rows:
                        self.produit_table.insert("", END, values=row)
                else:
                    messagebox.showerror("erreur","Aucun resultat!")        


        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")    

    def get_donne(self,ev):
      r=self.produit_table.focus()
      contenu = self.produit_table.item(r)
      row = contenu["values"]
      self.var_pid.set(row[0]) 
      self.pname.set(row[1])
      self.var_prix.set(row[2])
      self.lbl_p_stock.config(text=f"EN Stock[{str(row[3])}]")
      self.var_stock.set(row[3])
      self.var_qte.set(1)

    
    def get_donne_cart(self,ev):
      r=self.cartTable.focus()
      contenu = self.cartTable.item(r)
      row = contenu["values"]
      self.var_pid.set(row[0]) 
      self.pname.set(row[1])
      self.var_prix.set(row[2])
      self.var_qte.set(row[3])
      self.var_stock.set(row[3])
      self.lbl_p_stock.config(text=f"EN STOCK [{str(row[4])}]")
      self.var_stock.set(row[4])
     
    def ajout_modifier(self):
        if self.var_pid.get()=="":
            messagebox.showerror("erreur","Veillez selectionnez un produit!")
        elif self.var_qte.get()=="":
            messagebox.showerror("erreur","Veillez donner la quandité!")
        elif int(self.var_qte.get()) > int(self.var_stock.get()):
            messagebox.showerror("Erreur","La quandité n'est pas disponible!")
        else:
            prix_cal = self.var_prix.get()
            cart_donne=[self.var_pid.get(),self.pname.get(),self.var_prix.get(),self.var_qte.get(),self.var_stock.get()]
    
            present = "non"
            index_ = 0
            for row in self.cart_liste:
                if self.var_pid.get()==row[0]:
                    present = "oui"
                    break
                index_+=1
            if present =="oui":
                op = messagebox.askyesno("Confirmer","Le produit est déjà présent\n voulez-vous  vraiment modifier | supprimer de la liste?")
                if op ==True:
                    if self.var_qte.get()=="0":
                        self.cart_liste.pop(index_)
                    else:
                        self.cart_liste[index_][3]=self.var_qte.get()
            else:
                self.cart_liste.append(cart_donne)
                messagebox.showinfo("succès","Ajouter avec succès")
                self.afficher_cart()
                self.facture_modifier()   


    def afficher_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cart_liste:
                self.cartTable.insert("",END,values=row)
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")    


    def  facture_modifier(self):
        self.montant_facture=0
        self.net_payer = 0
        self.remise = 0
        self.montantht=0
        for row in self.cart_liste:
            self.montant_facture = self.montant_facture+(float(row[2])*int(row[3]))
            self.remise = (self.montant_facture*5/100)
            self.montantht=float(self.montant_facture*0.1925)
            self.net_payer = self.montant_facture-self.remise

            self.lbl_montant_facture.config(text=f"Montant facture \n [{str(self.montant_facture)}]")
            self.lbl_net_payer.config(text=f"Net à Payer \n [{str(self.net_payer)}]")
            self.lbl_montantHT_facture.config(text=f"Montant HT \n [{str(self.montantht)}]",)
            self.ctitle.config(text=f"Produit Total du Panier: [{str(len(self.cart_liste))}]")

    def generer_facture(self):
        if self.var_client_nom.get()=="" and self.var_contact.get()=="":
            messagebox.showerror("Erreur","Veillez saisir le nom du client")
        elif len(self.cart_liste)==0:
            messagebox.showerror("Erreur","Veillez ajouter des produits dans le panier!")
        else:
            self.entete_facture()
            self.corps_facture()
            self.footer_facture() 
            fp= open(fr"D:\new\projet python\gestion_licence\Facture\{str(self.facture)}.txt", "w")
            fp.write(self.txt_espace_facture.get("1.0",END))  
            fp.close
            messagebox.showinfo("Sauvarger","Enregistrer avec succès!")
            self.ck_print = 1

    def entete_facture(self):
        self.facture = int(strftime("%H%M%S"))+int(strftime("%d%M%Y"))
        facture_entete = f"""
         Magasin Hassan \n\t Tel: +237 652 58 45 85\n\t Adressse: Yaounde
{str("*")*41}
        Nom du client: {self.var_client_nom.get()}
        Tel du client : {self.var_contact.get()}
        Numéro Facture : {str(self.facture)}\t\t\n\tDate:{str(strftime("%d/%m/%Y"))}
{str("*")*41}
    \tNom produit: \tQuandité:\tPrix:
{str("*")*41}
        """
        self.txt_espace_facture.delete("1.0", END)
        self.txt_espace_facture.insert("1.0", facture_entete)

    def corps_facture(self):
        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        try:
            for row in self.cart_liste:
                pid = row[0]
                nom = row[1]
                quandite = int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status = "Inactive"
                if int(row[3])!=int(row[4]):
                    status="Active"
                prix=int(row[2])*int(row[3])
                prix =str(prix)
                self.txt_espace_facture.insert(END,"\n"+nom+":\t"+row[3]+":\t"+prix)
                cur.execute("update produit set quandite=?,status=? where pid=? ",(
                    quandite,
                    status,
                    pid
                ))
                con.commit()
            con.close
            self.afficher()       
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")    
    

    def footer_facture(self):
        facture_footer=f"""
{str("*"*41)}
Montant Facture: \t\t {self.montant_facture}
Montant Ht : \t\t {self.montantht}
Montant Net à Payer: \t\t {self.net_payer}
{str("*"*41)}
        """
        self.txt_espace_facture.insert(END,facture_footer)

    def clear_cart(self):
        self.var_pid.set("")
        self.pname.set("")
        self.var_prix.set("")
        self.var_qte.set("")
        self.lbl_p_stock.config(text=f"En Stock")
        self.var_stock.set("")

    def clear_all(self):
        del self.cart_liste[:]
        self.var_client_nom.set("")
        self.var_contact.set("")
        self.txt_espace_facture.delete("1.0",END)
        self.ctitle.config(text=f"Produit Total du Panier: [0]")
        self.var_recherche.set("")
        self.ck_print = 0
        self.clear_cart()
        self.afficher()
        self.afficher_cart()

    def modifier_heure(self):
        heure_ = (strftime("%H:%M:%S"))
        date_= (strftime("%d/%m/%Y"))
        self.lbl_heure.config(text=f"BIENVENUE CHEZ HASSAN \t\t Date: {str(date_)} \t\t Heure:{str(heure_)}")
        self.lbl_heure.after(200,self.modifier_heure)


    def imprimer_facture(self):
        if self.ck_print==1:
            messagebox.showinfo("Imprimer","Veillez patienter pendant l'impression")
            fichier = tempfile.mktemp(".txt")
            open(fichier,"w").write(self.txt_espace_facture.get("1.0",END))
            os.startfile(fichier,"print")
        else:
            messagebox.showerror("Erreur","Veillez générer la facture!")    

        

    
    def deconnecter(self):
        self.root.destroy()
        self.obj = os.popen("login.py")










if __name__=="__main__":
    root=Tk()
    obj = Caisse(root)
    root.mainloop()
