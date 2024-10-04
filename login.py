import email
import http
from http.client import responses
from msilib.schema import ComboBox, Component, MsiDigitalCertificate
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
from time import strftime, time
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
import smtplib
import email_pass


class Login:
    def __init__(self,root):
        self.root=root
        self.root.title("CONNEXION")
        self.root.geometry("550x310+200+210")
        self.root.config(bg="white")
        self.root.focus_force()


        self.code_envoie=""

        login_frame = Frame(self.root,bg="cyan")
        login_frame.place(x=120,y=20,width=320,height=250)

        title = Label(login_frame,text="CONNEXION",font=("Algerian",20,"bold"),bg="cyan",fg="black").pack(side=TOP,fill=X)

        label_id =Label(login_frame,text="ID-EMPLOYE",font=("times new roman",15),bg="cyan").place(x=110,y=50)
        label_id =Label(login_frame,text="MOT DE PASSE",font=("times new roman",15),bg="cyan").place(x=100,y=110)

        self.txt_id_employe = Entry(login_frame,font=("times new roman",20),bg="lightgray")
        self.txt_id_employe.place(x=80,y=80,width=180,height=25)

        self.txt_password_employe = Entry(login_frame,show="*",font=("times new roman",20),bg="lightgray")
        self.txt_password_employe.place(x=80,y=140,width=180,height=25)

        connecter_btn = Button(login_frame,command=self.connection,text="Connexion",cursor="hand2",font=("times new roman",15,"bold"),bg="lightgray",fg="green").place(x=110,y=170,height=35,width=110)

        oublie_btn = Button(login_frame,command=self.password_oublie_fnentre,text="Mot de passe oublié",cursor="hand2",font=("times new roman",12,"bold"),bg="cyan",bd=0,fg="red",activebackground="cyan").place(x=10,y=220)
        creercompte_btn = Button(login_frame,command=self.creer_compte,text="Créer_compte",cursor="hand2",font=("times new roman",12,"bold"),bg="cyan",bd=0,fg="black",activebackground="cyan").place(x=200,y=220)

    def password_oublie_fnentre(self):
        if self.txt_id_employe.get()=="":
            messagebox.showerror("Erreur","Veillez saisir votre idendifiant ")
        else:
            con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
            cur=con.cursor()
            try:
                cur.execute("select e_mail from employe where e_id=?",(self.txt_id_employe.get(),))
                e_mail = cur.fetchone()
                if e_mail==None:
                    messagebox.showerror("Erreur","identifiant de l'employe invalide")
                else:
                    #chk = self.envoie_mail(email[0])
                    chk=""
                    if chk=="f":
                        messagebox.showerror("Erreur","Veillez vérifier votre connexion!")
                    else:
                        self.var_code = StringVar()
                        self.var_new_pass = StringVar()
                        self.var_confirm_pass= StringVar()

                        self.root2=Toplevel	()
                        self.root2.title("Reinitialiser mot de passe")
                        self.root2.config(bg="white")
                        self.root2.geometry("350x300+300+300")
                        self.root2.focus_force()
                        self.root2.grab_set()

                        title = Label(self.root2,text="Mot De Passe oublié",font=("algerian",20,"bold"),bg="red").pack(side=TOP,fill=X)
                        

                        ######### afficher le code
                        aff_code = Label(self.root2,text="Saisir le code réçu par mail",font=("times new roman",15,"bold"),bg="white").place(x=50,y=50)
                        txt_reset = Entry(self.root2,textvariable=self.var_code,font=("times new roman",15),bg="lightgray").place(x=70,y=80,width=200)
                        self.code_tn=Button(self.root2,command=self.code_valide,text="VALIDER",cursor="hand2",font=("times new roman",15,"bold"),bg="lightgray",fg="green")
                        self.code_tn.place(x=220,y=110,width=95,height=35)

                        ######## Nouveau mot de passe
                        nouveau_password = Label(self.root2,text="Nauveau password:",font=("times new roman",15,"bold"),bg="white").place(x=3,y=160)
                        txt_new_passwor = Entry(self.root2,font=("times new roman",15),textvariable=self.var_new_pass,bg="lightgray").place(x=180,y=160,width=150)
                        confirm_password = Label(self.root2,text="Confirme password:",font=("times new roman",15,"bold"),bg="white").place(x=3,y=200)
                        txt_confirm_passwor = Entry(self.root2,font=("times new roman",15),textvariable=self.var_confirm_pass,bg="lightgray").place(x=180,y=200,width=150)

                        ###### Modifier le mot de passe 
                        self.changer_btn = Button(self.root2,text="Modifier",cursor="hand2",state=DISABLED,command=self.modifier_password,font=("times new roman",15,"bold"),bg="lightblue")
                        self.changer_btn.place(x=180,y=240,width=95,height=35)

                        self.quitter_tn=Button(self.root2,command=self.quitter_f,text="QUITTER",cursor="hand2",font=("times new roman",15,"bold"),bg="lightgray",fg="red")
                        self.quitter_tn.place(x=20,y=240,width=100,height=35)


            except Exception as ex:
                messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")


    def creer_compte(self):
        self.var_emplo_id = StringVar()
        self.var_sexe = StringVar()
        self.var_contact = StringVar()
        self.var_nom = StringVar()
        self.var_prenom = StringVar()
        self.var_date_naissance = StringVar()
        self.var_date_adhesion = StringVar()
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_type = StringVar()
        self.var_salaire = IntVar()
        self.txt_caladar= 0

        self.root3=Toplevel	()
        self.root3.title("Créer un compte")
        self.root3.config(bg="white")
        self.root3.geometry("900x350+90+90")
        self.root3.focus_force()
        self.root3.grab_set()
        titre = Label(self.root3,text="FORMULAIRE POUR CREER UN COMPTE EMPLOYE",font=("times new roman",15),cursor="hand2",bg="cyan").place(x=0,y=10,width=1100)

        lbl_empid= Label(self.root3,text="ID Employé :", font=("goudy old style",15),bg="white").place(x=40,y=80,width=150)
        lbl_sexe= Label(self.root3,text="SEXE :", font=("goudy old style",15),bg="white").place(x=280,y=80,width=150)
        lbl_contact= Label(self.root3,text="CONTACT :", font=("goudy old style",15),bg="white").place(x=520,y=80,width=150)
        lbl_nom= Label(self.root3,text="NOM :", font=("goudy old style",15),bg="white").place(x=10,y=130,width=150)

        self.txt_empid = Entry(self.root3,textvariable=self.var_emplo_id,font=("goudy old style",15),bg="lightyellow")
        self.txt_empid.place(x=180,y=80,width=130)
        txt_sexe = ttk.Combobox(self.root3,textvariable=self.var_sexe,values=("HOMME","FEMME"),font=("goudy old style",15),state="readonly",justify=CENTER)
        txt_sexe.current(0)
        txt_sexe.place(x=390,y=80,width=130)
        txt_contact = Entry(self.root3,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=650,y=80,width=130)
        txt_nom = Entry(self.root3,textvariable=self.var_nom,font=("goudy old style",15),bg="lightyellow").place(x=120,y=130,width=130)

          ##2 Lignes

        lbl_prenom= Label(self.root3,text="PRENOM :", font=("goudy old style",15),bg="white").place(x=0,y=180,width=150)
        lbl_naissance= Label(self.root3,text="DATE_NAISSANCE :", font=("goudy old style",15),bg="white").place(x=260,y=130,width=180)
        lbl_adehsion= Label(self.root3,text="DATE_ADHESION :", font=("goudy old style",15),bg="white").place(x=580,y=130,width=180)

        txt_prenom = Entry(self.root3,textvariable=self.var_prenom,font=("goudy old style",15),bg="lightyellow").place(x=130,y=180,width=130)
        txt_naissance = Entry(self.root3,textvariable=self.var_date_naissance,font=("goudy old style",15),bg="lightyellow").place(x=445,y=130,width=130)
        #self.btn_nai= Button(self.root3,command=self.showcalendar,text="DATE", font=("goudy old style",15),bg="sky blue").place(x=410,y=130,width=60,height=30)
        txt_adhesion = Entry(self.root3,textvariable=self.var_date_adhesion,font=("goudy old style",15),bg="lightyellow").place(x=760,y=130,width=130)
        #self.btn_adh= Button(self.root3,state="normal",command=self.showcalendares,text="DATE", font=("goudy old style",15),bg="sky blue").place(x=1010,y=130,width=60,height=30)

          ##3 Lignes

        lbl_email= Label(self.root3,text="E-MAIL :", font=("goudy old style",15),bg="white").place(x=265,y=180,width=80)
        lbl_password= Label(self.root3,text="PASSWORD :", font=("goudy old style",15),bg="white").place(x=340,y=230,width=150)
        lbl_type= Label(self.root3,text="TYPE-COMPTE :", font=("goudy old style",15),bg="white").place(x=500,y=180,width=150)

        txt_email = Entry(self.root3,textvariable=self.var_email,font=("goudy old style",15),bg="lightyellow").place(x=350,y=180,width=130)
        txt_password = Entry(self.root3,textvariable=self.var_password,show="*",font=("goudy old style",15),bg="lightyellow").place(x=480,y=230,width=130)
        txt_type = ttk.Combobox(self.root3,textvariable=self.var_type,values=("ADMIN","EMPLOYE"),font=("goudy old style",15),state="readonly",justify=CENTER)
        txt_type.current(0)
        txt_type.place(x=670,y=180,width=150)
            ##4 Lignes

        lbl_adresse= Label(self.root3,text="ADRESSE :", font=("goudy old style",15),bg="white").place(x=50,y=230,width=150)
        lbl_salaire= Label(self.root3,text="SALAIRE :", font=("goudy old style",15),bg="white").place(x=630,y=230,width=90)
       
        self.txt_adresse = Text(self.root3,font=("goudy old style",15),bg="lightyellow")
        self.txt_adresse.place(x=180,y=230,width=150,height=80)
        txt_salaire = Entry(self.root3,textvariable=self.var_salaire,font=("goudy old style",15),bg="lightyellow").place(x=730,y=230,width=150)
        
        ###### Boutton
        self.afficherajout_btn = Button(self.root3,command=self.ajoutercompte,text="CREER",state="normal",font=('times news roman',15,"bold"),cursor="hand2",bg="green",fg="lightgray")
        self.afficherajout_btn.place(x=350,y=290,height=30)
        self.quit_btn = Button(self.root3,command=self.retour,text="RETOUR",state="normal",font=('times news roman',15,"bold"),cursor="hand2",bg="red",fg="lightgray")
        self.quit_btn.place(x=500,y=290,height=30)

    def retour(self):
        self.root.destroy()
        os.popen("login.py")    


    def ajoutercompte(self):
        con=sqlite3.connect(database=r"C:\Users\jaure\OneDrive\Bureau\projet licence\gestion_licence\base_donnees")
        cur=con.cursor()
        try:
            if self.var_emplo_id.get()=="" or self.var_salaire.get()=="" or self.var_password.get()=="":
              messagebox.showerror("Erreur","Veillez remplir tous les champs!")
            else:
              cur.execute("select * from employe where e_id =?",(self.var_emplo_id.get(),))
              row = cur.fetchone()
              if row!=None:
                messagebox.showerror("Erreur","l'ID_employe existe déja!")
              else:
                cur.execute("insert into employe(e_id,nom,prenom,e_mail,sexe,contact,date_naissance,date_adhesion,password,type_compte,adresse,salaire) values(?,?,?,?,?,?,?,?,?,?,?,?)",(
                  self.var_emplo_id.get(),
                  self.var_nom.get(),
                  self.var_prenom.get(),
                  self.var_email.get(),
                  self.var_sexe.get(),
                  self.var_contact.get(),
                  self.var_date_naissance.get(),
                  self.var_date_adhesion.get(),
                  self.var_password.get(),
                  self.var_type.get(),
                  self.txt_adresse.get("1.0",END),
                  self.var_salaire.get()
                ))
                con.commit()
                messagebox.showinfo("succès","Compte crée avec succès!")
                self.root3.destroy()    
        except Exception as ex:
          messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")





    def connection(self):
        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        try:
            if self.txt_id_employe.get()=="" or self.txt_password_employe.get()=="":
                messagebox.showerror("Erreur","Veillez entrer l'id et le mot de passe de l'employe!")
            else:
                cur.execute("select type_compte from employe where e_id=? AND password=?",(self.txt_id_employe.get(),self.txt_password_employe.get()))
                user = cur.fetchone()
                if user ==None:
                    messagebox.showerror("Erreur","l'Id ou mot de passe n'existe pas!")
                else:
                    if user[0]=="ADMIN":
                        self.root.destroy()
                        os.popen("accueil.py")
                    else:
                        self.root.destroy()
                        os.popen("caisse.py")

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")


    def modifier_password(self):
        if self.var_new_pass.get()=="" or self.var_confirm_pass.get()=="":
            messagebox.showerror("Erreur","Veillez saisir votre mot de passe!")
        elif self.var_new_pass.get()!=self.var_confirm_pass.get():
            messagebox.showerror("Erreur","Les deux mots de passes doivent être identique")    
        else:
            try:
                con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
                cur=con.cursor()
                cur.execute("update employe set password=? where e_id=?",(self.var_new_pass.get(),self.var_confirm_pass.get(),))
                con.commit
                messagebox.showinfo("Succès","Mot de passe modifier avec succès!")
                self.root2.destroy()

            except Exception as ex:
                messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")
     

    def code_valide(self):
        if int(self.code_envoie)==int(self.var_code.get()):
            self.changer_btn.config(state=NORMAL)
            self.code_tn.config(state=DISABLED)
        else:
            messagebox.showerror("Erreur","Le code saisi est invalide!")    



    def quitter_f(self) :
        self.root.destroy()
        os.popen("login.py")   


    def envoie_mail(self,to_):
        ##### pour utilise le protocole gmail
        s=smtplib.SMTP("smtp.gmail.com",587)
        #### pour le transfert de couche
        s.starttls()
        email_ = email_pass.email_
        pass_ = email_pass.pass_

        s.login(email_,pass_)
        #### gestion du code d'envoie
        self.code_envoie = int(strftime("%H%S%M"))+int(strftime("%S"))
        subj = "ENTREPRISE HASSAN|LOIC code de reinitialisation"
        msg=f"Bonjour Monsieur/Madame\n\n votre code de reinitialisation est: {self.code_envoie}\nMerci d'avoir utilise notre service"
        msg="Subject: {}\n\n".format(subj,msg)
        s.sendmail(email_,to_,msg)
        ck = s.ehlo()
        if ck[0]==250:
            return "s"
        else:
            return "f"    





if __name__=="__main__":
    root=Tk()
    obj = Login(root)
    root.mainloop()