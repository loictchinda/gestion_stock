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


class Employe:
    def __init__(self,root):
        self.root=root
        self.root.title("EMPLOYE")
        self.root.geometry("1100x590+90+90")
        self.root.config(bg="white")
        self.root.focus_force()
   

        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS employe(e_id text PRIMARY KEY,nom text,prenom text,e_mail text,sexe text,contact text,date_naissance text,date_adhesion text,password text,type_compte text,adresse text,salaire integer)")
        con.commit()

        ### mes variables

        self.var_recherche_type = StringVar()
        self.var_recherche_txt = StringVar()
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

        #rechercher employe

        reche_frame = LabelFrame(self.root, text="Recherche Employe", font=("goudy old style",15,"bold"),bd=2,relief=RIDGE,bg="white")
        reche_frame.place(x=440,y=10,width=520,height=90)

        #option recherche

        reche_option = ttk.Combobox(reche_frame,textvariable=self.var_recherche_type,values=("code","nom","prenom","email","contact"),font=("times new roman",15),state="r",justify=CENTER)
        reche_option.current(0)
        reche_option.place(x=10,y=4,width=100)

        reche_txt = Entry(reche_frame,textvariable=self.var_recherche_txt,font=("times new roman",15),bg="lightyellow").place(x=120,y=4,width=120)

        btn_reche = Button(reche_frame,text="RECHERCHER",command=self.recherche,font=("times new roman",15),cursor="hand2",bg="blue",fg="white").place(x=250,y=4,height=30)
        btn_tous = Button(reche_frame,command=self.afficher,text="TOUS",font=("times new roman",15),cursor="hand2",bg="lightgray").place(x=420,y=4,height=30)


        #titre

        titre = Label(self.root,text="FORMULAIRE EMPLOYE",font=("times new roman",15),cursor="hand2",bg="cyan").place(x=0,y=120,width=1100)

        #contenu
        ##1Ligne

        lbl_empid= Label(self.root,text="ID Employé :", font=("goudy old style",15),bg="white").place(x=50,y=160,width=150)
        lbl_sexe= Label(self.root,text="SEXE :", font=("goudy old style",15),bg="white").place(x=280,y=160,width=150)
        lbl_contact= Label(self.root,text="CONTACT :", font=("goudy old style",15),bg="white").place(x=520,y=160,width=150)
        lbl_nom= Label(self.root,text="NOM :", font=("goudy old style",15),bg="white").place(x=750,y=160,width=150)

        self.txt_empid = Entry(self.root,textvariable=self.var_emplo_id,font=("goudy old style",15),bg="lightyellow")
        self.txt_empid.place(x=180,y=160,width=130)
        txt_sexe = ttk.Combobox(self.root,textvariable=self.var_sexe,values=("HOMME","FEMME"),font=("goudy old style",15),state="readonly",justify=CENTER)
        txt_sexe.current(0)
        txt_sexe.place(x=390,y=160,width=130)
        txt_contact = Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=650,y=160,width=130)
        txt_nom = Entry(self.root,textvariable=self.var_nom,font=("goudy old style",15),bg="lightyellow").place(x=860,y=160,width=130)

          ##2 Lignes

        lbl_prenom= Label(self.root,text="PRENOM :", font=("goudy old style",15),bg="white").place(x=35,y=210,width=150)
        lbl_naissance= Label(self.root,text="DATE_NAISSANCE :", font=("goudy old style",15),bg="white").place(x=290,y=210,width=180)
        lbl_adehsion= Label(self.root,text="DATE_ADHESION :", font=("goudy old style",15),bg="white").place(x=690,y=210,width=180)

        txt_prenom = Entry(self.root,textvariable=self.var_prenom,font=("goudy old style",15),bg="lightyellow").place(x=160,y=210,width=110)
        txt_naissance = Entry(self.root,textvariable=self.var_date_naissance,font=("goudy old style",15),bg="lightyellow").place(x=475,y=210,width=130)
        self.btn_nai= Button(self.root,command=self.showcalendar,text="DATE", font=("goudy old style",15),bg="sky blue").place(x=610,y=210,width=60,height=30)
        txt_adhesion = Entry(self.root,textvariable=self.var_date_adhesion,font=("goudy old style",15),bg="lightyellow").place(x=870,y=210,width=130)
        self.btn_adh= Button(self.root,state="normal",command=self.showcalendares,text="DATE", font=("goudy old style",15),bg="sky blue").place(x=1010,y=210,width=60,height=30)

          ##3 Lignes

        lbl_email= Label(self.root,text="E-MAIL :", font=("goudy old style",15),bg="white").place(x=50,y=260,width=150)
        lbl_password= Label(self.root,text="PASSWORD :", font=("goudy old style",15),bg="white").place(x=350,y=260,width=150)
        lbl_type= Label(self.root,text="TYPE-COMPTE :", font=("goudy old style",15),bg="white").place(x=640,y=260,width=150)

        txt_email = Entry(self.root,textvariable=self.var_email,font=("goudy old style",15),bg="lightyellow").place(x=180,y=260,width=150)
        txt_password = Entry(self.root,textvariable=self.var_password,show="*",font=("goudy old style",15),bg="lightyellow").place(x=490,y=260,width=130)
        txt_type = ttk.Combobox(self.root,textvariable=self.var_type,values=("ADMIN","EMPLOYE"),font=("goudy old style",15),state="readonly",justify=CENTER)
        txt_type.current(0)
        txt_type.place(x=800,y=260,width=150)
            ##4 Lignes

        lbl_adresse= Label(self.root,text="ADRESSE :", font=("goudy old style",15),bg="white").place(x=50,y=300,width=150)
        lbl_salaire= Label(self.root,text="SALAIRE :", font=("goudy old style",15),bg="white").place(x=350,y=300,width=150)
       
        self.txt_adresse = Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_adresse.place(x=180,y=300,width=150,height=80)
        txt_salaire = Entry(self.root,textvariable=self.var_salaire,font=("goudy old style",15),bg="lightyellow").place(x=470,y=300,width=150)

        self.afficherajout_btn = Button(self.root,command=self.ajouter,text="AJOUTER",state="normal",font=('times news roman',15,"bold"),cursor="hand2",bg="green")
        self.afficherajout_btn.place(x=350,y=340,height=30)
        self.modif_btn = Button(self.root,command=self.modifier,text="MODIFIER",state="disable",font=('times news roman',15,"bold"),cursor="hand2",bg="yellow")
        self.modif_btn.place(x=480,y=340,height=30)
        self.supp_btn = Button(self.root,command=self.supprimer,text="SUPPRIMER",state="disable",font=('times news roman',15,"bold"),cursor="hand2",bg="red")
        self.supp_btn.place(x=610,y=340,height=30)
        renit_btn = Button(self.root,command=self.renitialiser,text="ACTUALISER",font=('times news roman',15,"bold"),cursor="hand2",bg="lightgray").place(x=760,y=340,height=30)
        impri_btn = Button(self.root,command=self.imprimer,text="IMPRIMER",font=('times news roman',15,"bold"),cursor="hand2",bg="blue").place(x=920,y=340,height=30)

        ###Listes employe

        listeFrame = Frame(self.root,bd=3, relief=RIDGE)
        listeFrame.place(x=0,y=390,height=200,relwidth=1)

        scroll_y = Scrollbar(listeFrame,orient=VERTICAL,width=30)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x = Scrollbar(listeFrame,orient=HORIZONTAL,width=30)
        scroll_x.pack(side=BOTTOM,fill=X)

        self.employeliste = ttk.Treeview(listeFrame, columns=("eid","nom","prenom","e_mail","sexe","contact","date_naissance","date_adhesion","password","type","adresse","salaire"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
        scroll_x.config(command=self.employeliste.xview)
        scroll_y.config(command=self.employeliste.yview)

        self.employeliste.heading("eid",text="ID_E",anchor="w")
        self.employeliste.heading("nom",text="NOM",anchor="w")
        self.employeliste.heading("prenom",text="PRENOM",anchor="w")
        self.employeliste.heading("e_mail",text="E_MAIL",anchor="w")
        self.employeliste.heading("sexe",text="SEXE",anchor="w")
        self.employeliste.heading("contact",text="CONTACT",anchor="w")
        self.employeliste.heading("date_naissance",text="NAISSANCE",anchor="w")
        self.employeliste.heading("date_adhesion",text="ADHESION",anchor="w")
        self.employeliste.heading("password",text="PASSWORD",anchor="w")
        self.employeliste.heading("type",text="TYPE",anchor="w")
        self.employeliste.heading("adresse",text="ADRESSE",anchor="w")
        self.employeliste.heading("salaire",text="SALAIRE",anchor="w")

        self.employeliste["show"]="headings"
        self.employeliste.bind("<ButtonRelease-1>",self.get_donne)
        self.employeliste.pack(fill=BOTH,expand=1)
        self.afficher()
    ## foction pour la date    

    def showcalendar(self):
      if(self.txt_caladar!=1):
        self.top = Toplevel()
        self.top.geometry("295x255")
        self.top.title("Date Picker")
        self.top.resizable(False, False)
        self.cal = Calendar(self.top, selectmode='day', day=280, mont=10, year=2022, width=300, height=275)
        self.cal.pack()
        self.valider = Button(self.top, text="OK", command=lambda: self.grad_date1())
        self.valider.place(x=135, y=195, width=40, height=40)
        self.txt_caladar=1
        
    def grad_date1(self):
        self.var_date_naissance.set(self.cal.get_date())
        self.txt_caladar=0

      ## fonction 2 pour la date 

    def showcalendares(self):
      if(self.txt_caladar!=1):
        self.top = Toplevel()
        self.top.geometry("295x255")
        self.top.title("Date Picker")
        self.top.resizable(False, False)
        self.cal = Calendar(self.top, selectmode='day', day=280, mont=10, year=2022, width=300, height=275)
        self.cal.pack()
        self.valider = Button(self.top, text="OK", command=lambda: self.grad_date())
        self.valider.place(x=135, y=195, width=40, height=40)
        self.txt_caladar=1
      
        

    def grad_date(self):
      
        self.var_date_adhesion.set(self.cal.get_date())
        self.txt_caladar=0
        

        ### foction sur les boutons

    def ajouter(self):
        con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
        cur=con.cursor()
        try:
            if self.var_emplo_id.get=="" or self.var_salaire.get=="" or self.var_password.get=="":
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
                self.afficher()
                self.renitialiser()
                messagebox.showinfo("succès","ajouter avec succès!")    
        except Exception as ex:
          messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")


    def afficher(self):
      con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
      cur=con.cursor()
      try:
        cur.execute("select * from employe")
        rows = cur.fetchall()
        self.employeliste.delete(*self.employeliste.get_children())
        for row in rows:
          self.employeliste.insert("",END,values=row)
      except Exception as ex:
        messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")

    def get_donne(self,ev):
      self.afficherajout_btn.config(state="disable")
      self.modif_btn.config(state="normal")
      self.supp_btn.config(state="normal")
      self.txt_empid.config(state="readonly")
      r=self.employeliste.focus()
      contenu = self.employeliste.item(r)
      row = contenu["values"]
      self.var_emplo_id.set(row[0]),
      self.var_nom.set(row[1]),
      self.var_prenom.set(row[2]),
      self.var_email.set(row[3]),
      self.var_sexe.set(row[4]),
      self.var_contact.set(row[5]),
      self.var_date_naissance.set(row[6]),
      self.var_date_adhesion.set(row[7]),
      self.var_password.set(row[8]),
      self.var_type.set(row[9]),
      self.txt_adresse.delete("1.0",END),
      self.txt_adresse.insert(END,row[10]),
      self.var_salaire.set(row[11])


    def modifier(self):
      con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
      cur=con.cursor()
      try:
        cur.execute("update employe set nom=?,prenom=?,e_mail=?,sexe=?,contact=?,date_naissance=?,date_adhesion=?,password=?,type_compte=?,adresse=?,salaire=? where e_id=?",(
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
                  self.var_salaire.get(),
                  self.var_emplo_id.get()
        ))
        con.commit()
        self.afficher()
        self.renitialiser()
        messagebox.showinfo("Succeès","Modification éffectuée avec succès!")
      except Exception as ex:
        messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")

    def supprimer(self):
      con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
      cur=con.cursor()

      try:
        op = messagebox.askyesno("Confirmer","Voulez-vous vraiment supprimer?")
        if op==TRUE:
          cur.execute("delete from employe where e_id=?",(self.var_emplo_id.get(),))
          con.commit()
          self.afficher()
          self.renitialiser()
          messagebox.showinfo("Succès","supprimer avec succès!")

      except Exception as ex:
        messagebox.showerror("Erreur",f"Erreur de connexion{str(ex)}")


    def renitialiser(self):
      self.txt_empid.config(state="normal")
      self.afficherajout_btn.config(state="normal")
      self.modif_btn.config(state="disable")
      self.supp_btn.config(state="disable")
      self.var_nom.set(""),
      self.var_prenom.set(""),
      self.var_email.set(""),
      self.var_sexe.set("HOMME"),
      self.var_contact.set(""),
      self.var_date_naissance.set(""),
      self.var_date_adhesion.set(""),
      self.var_password.set(""),
      self.var_type.set("ADMIN"),
      self.txt_adresse.delete("1.0",END),
      self.var_salaire.set(""),
      self.var_emplo_id.set(""),
      self.var_recherche_txt.set(""),
      self.var_recherche_type.set("nom")

    def recherche(self):
      con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
      cur=con.cursor()
      try:
        if self.var_recherche_txt.get()=="":
          messagebox.showerror("Erreur",'Veillez saisir dans le champs recherche!')
        else:
          cur.execute("select * from employe where nom LIKE '%"+self.var_recherche_txt.get()+"%'")  
          rows = cur.fetchall()
          if len(rows)!=0:
            self.employeliste.delete(*self.employeliste.get_children())
            for row in rows:
              self.employeliste.insert("",END,values=row)
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
          
            self.set_left_margin(2)
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

      TABLE_COL_NAMES = ("e_id","nom","prenom","e_mail","sexe","contact","date_naissance","date_adhesion","password","type_compte","adresse","salaire")
      con=sqlite3.connect(database=r"D:\new\projet python\gestion_licence\base_donnees\gest_entreprise.db")
      cur=con.cursor()
      cur.execute("select * from employe")
      val=[]
      for row in cur:
        val.append(row)
        #con.close()
      TABLE_DATA = val
      pdf.set_left_margin(2)
      def render_table_header():
        pdf.set_font(family="",style="B")
        for col_name in TABLE_COL_NAMES:
            pdf.cell(17.5,9,col_name,border=1,align='C')
        pdf.ln()
      pdf.set_font("Times",size=8)
      pdf.set_font(family="",style="B")
      pdf.set_left_margin(2)
      render_table_header()
      for _ in range(1):
        for rows in TABLE_DATA:
          #if pdf.page_break_trigger():
            pdf.set_left_margin(2)
            render_table_header
            for h in rows:
                pdf.set_left_margin(2)
                pdf.cell(17.5, 9, f'{h}', border=1, align='C')
            pdf.ln(10)
      pdf.set_font('helvetica','BUI',19)
      pdf.output('employe.pdf')
      file="employe.pdf"
      os.popen(file)
      os.startfile(file,"print")
      messagebox.showinfo("succes","Imprimer avec success")                    




        
          
      




        









if __name__=="__main__":
    root=Tk()
    obj = Employe(root)
    root.mainloop()