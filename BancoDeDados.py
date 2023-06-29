from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os

root = Tk()

class Funcs():
    def limpa_tela(self):
        self.ID_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.Diretor_entry.delete(0, END)
        self.data_entry.delete(0, END)
        self.Nota_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect('BancoDeDados.bd')
        self.cursor = self.conn.cursor(); print('Conectando ao banco de dados')
    def desconecta_bd(self):
        self.conn.close(); print('Desconectando do banco de dados')
    def montaTabelas(self):
        self.conecta_bd()

        ### criar tabela
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS BancoDeDados (
            ID INTEGER PRIMARY KEY,
            Nome CHAR(40) NOT NULL,
            Diretor CHAR(40),
            Data CHAR(10),
            Nota INTEGER(2)
            );
        """)
        self.conn.commit(); print('Banco de dados criado')
        self.desconecta_bd(), print('')
    def variaveis(self):
        self.ID = self.ID_entry.get()
        self.nome = self.nome_entry.get()
        self.Diretor = self.Diretor_entry.get()
        self.data = self.data_entry.get()
        self.Nota = self.Nota_entry.get()
    def add_filme(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute("""
        INSERT INTO BancoDeDados (Nome, Diretor, Data, Nota)
        VALUES (?, ?, ?, ?)""", (self.nome,self.Diretor, self.data, self.Nota))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def select_lista(self):
        self.listaBd.delete(*self.listaBd.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" 
        SELECT ID, Nome, Diretor, Data, Nota 
        FROM BancoDeDados
        ORDER BY ID ASC; """)
        for i in lista:
            self.listaBd.insert('', END, values=i)
        self.desconecta_bd()
    def OnDoubleClick(self,event):
        self.limpa_tela()
        self.listaBd.selection()

        for n in self.listaBd.selection():
            col1, col2, col3, col4, col5 = self.listaBd.item(n, 'values')
            self.ID_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.Diretor_entry.insert(END, col3)
            self.data_entry.insert(END, col4)
            self.Nota_entry.insert(END,col5)
    def deleta_filme(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM BancoDeDados WHERE ID = ? """,(self.ID,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()
    def altera_filme(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE BancoDeDados SET Nome = ?, Diretor = ?, Data = ?, Nota = ?
            WHERE ID = ? """, (self.nome, self.Diretor, self.data, self.Nota, self.ID))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def buscar(self):
        self.conecta_bd()
        self.listaBd.delete(*self.listaBd.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute("""
        SELECT ID, Nome, Diretor, Data, Nota FROM BancoDeDados
        WHERE Nome LIKE '%s' ORDER BY Nome ASC
        """ % nome)
        buscaNomeFilme = self.cursor.fetchall()
        for i in buscaNomeFilme:
            self.listaBd.insert("",END, values=i)
        self.limpa_tela()
        self.desconecta_bd()


class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()
    def tela(self):
        self.root.title('Filmes dos Anons')
        self.root.configure(background= '#000000')
        self.root.geometry('700x500')
        self.root.resizable(True, True)
        self.root.maxsize(width= 900, height= 700)
        self.root.minsize(width= 500, height= 400)
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd = 4, bg= '#dfe3ee',
                              highlightbackground= 'grey', highlightthickness= 3)
        self.frame_1.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.46)

        self.frame_2 = Frame(self.root, bd = 4, bg= '#dfe3ee',
                              highlightbackground= 'grey', highlightthickness= 3)
        self.frame_2.place(relx= 0.02, rely= 0.5, relwidth= 0.96, relheight= 0.46)
    def widgets_frame1(self):
        ### Criação botão de limpar
        self.bt_limpar = Button(self.frame_1, text= 'Limpar', bd=3, bg= 'brown', fg= 'white', font=('verdan', 9, 'bold'), command= self.limpa_tela)
        self.bt_limpar.place(relx=0.05, rely=0.7, relwidth=0.1, relheight=0.1)

        ### Criação botão de buscar
        self.bt_buscar = Button(self.frame_1, text= 'Buscar', bd=3, bg= 'brown', fg= 'white', font=('verdan', 9, 'bold'), command= self.buscar)
        self.bt_buscar.place(relx=0.2, rely=0.7, relwidth=0.1, relheight=0.1)
        
        ### Criação botão de novo
        self.bt_novo = Button(self.frame_1, text= 'Novo', bd=3, bg= 'brown', fg= 'white', font=('verdan', 9, 'bold'), command= self.add_filme)
        self.bt_novo.place(relx=0.55, rely=0.7, relwidth=0.1, relheight=0.1)

        ### Criação botão de alterar
        self.bt_alterar = Button(self.frame_1, text= 'Alterar', bd=3, bg= 'brown', fg= 'white', font=('verdan', 9, 'bold'), command= self.altera_filme)
        self.bt_alterar.place(relx=0.7, rely=0.7, relwidth=0.1, relheight=0.1)

        ### Criação botão de apagar
        self.bt_apagar = Button(self.frame_1, text= 'Apagar', bd=3, bg= 'brown', fg= 'white', font=('verdan', 9, 'bold'), command= self.deleta_filme)
        self.bt_apagar.place(relx=0.85, rely=0.7, relwidth=0.1, relheight=0.1)


        ## Criação da label e entrada do ID
        self.lb_ID = Label(self.frame_1, text= 'ID',bg= '#dfe3ee', fg='black',font=('verdan', 9, 'bold'))
        self.lb_ID.place(relx= 0.06, rely= 0.05)

        self.ID_entry = Entry(self.frame_1)
        self.ID_entry.place(relx= 0.06, rely= 0.15, relwidth= 0.1)

        ## Criação da label e entrada do nome
        self.lb_nome = Label(self.frame_1, text= 'Nome do filme',bg= '#dfe3ee', fg='black',font=('verdan', 9, 'bold'))
        self.lb_nome.place(relx= 0.3, rely= 0.05)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx= 0.3, rely= 0.15, relwidth= 0.64)


        ## Criação da label e entrada do diretor
        self.lb_Diretor = Label(self.frame_1, text= 'Diretor',bg= '#dfe3ee', fg='black',font=('verdan', 9, 'bold'))
        self.lb_Diretor.place(relx= 0.06, rely= 0.35)

        self.Diretor_entry = Entry(self.frame_1)
        self.Diretor_entry.place(relx= 0.06, rely= 0.45, relwidth= 0.25)

        ## Criação da label e entrada da data
        self.lb_data = Label(self.frame_1, text= 'Ano de lançamento',bg= '#dfe3ee', fg='black',font=('verdan', 9, 'bold'))
        self.lb_data.place(relx= 0.42, rely= 0.35)

        self.data_entry = Entry(self.frame_1)
        self.data_entry.place(relx= 0.42, rely= 0.45, relwidth= 0.29)

        ## Criação da label e entrada da nota
        self.lb_nota = Label(self.frame_1, text= 'Nota (0/100)',bg= '#dfe3ee', fg='black',font=('verdan', 9, 'bold'))
        self.lb_nota.place(relx= 0.82, rely= 0.35)

        self.Nota_entry = Entry(self.frame_1)
        self.Nota_entry.place(relx= 0.82, rely= 0.45, relwidth= 0.12)

    def lista_frame2(self):
        self.listaBd = ttk.Treeview(self.frame_2, height= 3, column=('col1', 'col2', 'col3', 'col4', 'col5'))
        self.listaBd.heading('#0', text='')
        self.listaBd.heading('#1', text='ID')
        self.listaBd.heading('#2', text='Nome do filme')
        self.listaBd.heading('#3', text='Diretor')
        self.listaBd.heading('#4', text='Ano')
        self.listaBd.heading('#5', text='Nota')

        self.listaBd.column('#0', width= 0)
        self.listaBd.column('#1', width= 70)
        self.listaBd.column('#2', width= 200)
        self.listaBd.column('#3', width= 150)
        self.listaBd.column('#4', width= 80)
        self.listaBd.column('#5', width= 80)
        self.listaBd.place(relx= 0.01, rely= 0.1, relwidth= 0.95, relheight= 0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient= 'vertical')
        self.scroolLista.config(command=self.listaBd.yview)
        self.listaBd.configure(yscrollcommand=self.scroolLista.set)
        self.scroolLista.place(relx= 0.96, rely= 0.1, relwidth= 0.04, relheight= 0.85)
        self.listaBd.bind('<Double-1>', self.OnDoubleClick)
    def Sobre_mim(self):
        messagebox.showinfo(title='Sobre mim', message='''Ola! me chamo João Victor Nunes e sou um programador iniciante em python.

Este é meu primeiro programa sério então peço compreenção com possiveis erros ou bugs.''')
        
    def Sobre_programa(self):
        messagebox.showinfo(title='Sobre o programa', message='''O aplicativo em questão é uma plataforma de cadastro e avaliação de filmes em banco de dados.

O usuário podera adicionar, excluir, alterar ou buscar por filmes cadastrados.''')

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)

        menubar.add_cascade(label= 'Sobre', menu= filemenu)

        filemenu.add_command(label='Sobre o Criador', command= self.Sobre_mim)
        filemenu.add_command(label='Sobre o programa',command= self.Sobre_programa)


Application()
