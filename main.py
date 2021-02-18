#---import required modules
import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk) 
from matplotlib.figure import Figure 
import base64
import calc
from datetime import (datetime, date)
#----creating the main window----
root = Tk()
root.overrideredirect(True)         
root.geometry('700x500+250+100')
root.attributes('-topmost', True)
lastClickX = 0
lastClickY = 0
#-----main code -----
def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y
def Dragging(event):
    x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
    root.geometry("+%s+%s" % (x , y))
#___conversion class___
class RealTimeCurrencyConverter():
    def convert(self,inp_curr,out_curr,input_amount):
        self.inp_code,ext1= map(str,inp_curr.split('-'))
        self.out_code,ext2= map(str,out_curr.split('-'))
        response_url = "https://api.ratesapi.io/api/latest?base={}&symbols={}".format(self.inp_code, self.out_code)
        response = requests.get(response_url)
        data = response.json()
        rates = data['rates'][self.out_code]
        self.output_amount = rates*float(input_amount)
        return self.output_amount
#____ App class____
class App(tk.Tk): 
    def __init__(self):
        #creating main window attributes
        title_bar = Frame(root,bd=5,highlightthickness=0,bg="#2e2e2e")
        title_bar.pack(expand=0, fill=X)
        close_button = Button(title_bar, text='X', command=root.destroy,bg="#2e2e2e",padx=2,pady=2,activebackground='red',bd=0,font="bold",fg='white',highlightthickness=3)
        close_button.pack(side=RIGHT)
        l = Label(title_bar,text="CURRENCY CONVERTER ",font=('algerian', 10, "bold"),fg="white",bg="#2e2e2e") 
        l.pack(side="left")
        value_out = StringVar()
        value_in = StringVar()
        amount = StringVar()
        Var_1 = Button(root,text = "Currency Converter",activebackground="light blue",activeforeground="red",bd=3,padx=30,command = self.main ) #,state=DISABLED
        Var_2 = Button(root,text = "Graphical analysis",activebackground="pink",bd=3,padx=30,command = self.graph) 
        Var_3 = Button(root,text = "OTHERS",activebackground="light blue",bd=3,padx=60,command = self.links) #,bg = "white"
        Var_4 = Button(root,text = "ADMIN Login",bd=3,padx=45,  command = self.var  ) 
        Var_1.place(x = 0  ,y = 55)
        Var_2.place(x = 180,y = 55)
        Var_3.place(x = 350,y = 55)
        Var_4.place(x = 530,y = 55)
        title_bar.bind('<Button-1>', SaveLastClickPos)
        title_bar.bind('<B1-Motion>', Dragging)
    def var(self): #driver code window attributes
        self.uname = StringVar()
        self.passw = StringVar()
        self.canv = Canvas(height= 500,width = 700, bg="light blue")
        self.canv.place(x =0,y = 85)
        header = Label(self.canv, text = "ADMIN LOGIN", font = ('algerian', 20), bg="light blue")
        header.place(x = 200,y = 100)
        uname_lab = Label(self.canv, text = "User Name:", bg="light blue")
        uname_lab.place(x = 100,y = 150)
        uname_entry = Entry(self.canv,textvariable =self.uname)
        uname_entry.place(x = 200,y = 150)
        pass_lab = Label(self.canv, text = "Password:", bg="light blue")
        pass_lab.place(x = 100,y = 200)
        pass_entry = Entry(self.canv,show="*",textvariable =self.passw)
        pass_entry.place(x = 200,y = 200)
        login = Button(self.canv,text = "LOGIN",height=2,padx = 7,activebackground="#2C84EF",command = self.login)
        login.place(x = 200,y = 250)
    def links(self):# others
        canv1 = Canvas(height= 500,width = 700, bg="light blue")
        canv1.place(x =0,y = 85)
        B = Button(canv1, text= "Calculator",padx = 50,font = 30,command = self.calc).place(x = 100,y = 200) 
        B1 = Button(canv1, text= "Trending",padx = 50,font = 30,command = self.ext).place(x = 100,y = 100) 
    def calc(self): #calculator
        calc.app()
    def graph(self):# graphical analysis inputs
        self.canvx = Canvas(height =500,width = 700, bg="light blue")
        self.canvx.place(x=0,y=85)
        self.inpcode = StringVar()
        self.outcode = StringVar()
        self.date = StringVar()
        inpl = Label(self.canvx,text = "Input Currency Code:",bg = "light blue").place(x = 100,y = 100)
        inpb = Entry(self.canvx,textvariable = self.inpcode ).place(x = 300,y = 100)
        outb = Entry(self.canvx,textvariable = self.outcode  ).place(x = 300,y = 150)
        outl = Label(self.canvx,text = "Output Currency Code:",bg = "light blue").place(x = 100,y = 150)
        plot = Button(self.canvx,height = 1, width = 10,text = "Plot",command = self.graph_core).place(x = 200,y =250)
        x = ttk.Combobox(self.canvx, textvariable = self.date, state = 'readonly', font = ('arial', 10),width = 20)
        x['values'] = (2021,2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009)
        x.place(x = 300 , y = 200)      
        Label(self.canvx,text = "Choose Year:",bg= "light blue").place(x = 100,y = 200)
    def graph_core(self):# graphical analysis using matplotlib
        strinpcode = str(self.inpcode.get())
        stroutcode = str(self.outcode.get())
        strdate    = str(self.date.get())
        x,y  = [],[]
        z = ['6','12']
        fyear = int(strdate)
        tyear, tmonth , tday = map(int, str(date.today()).split("-"))
        if abs(fyear-tyear) > 5:
            for i in range(fyear,tyear+1):
                response = requests.get("https://api.ratesapi.io/api/{}-06-01?base={}&symbols={}".format(i,strinpcode,stroutcode))
                data = response.json()
                rate = data['rates'][stroutcode]
                y.append(rate)
                x.append(i)
        elif abs(fyear-tyear) <=5 and abs(fyear-tyear)>1:
            for i in range(fyear,tyear):
                for j in 6,12:
                    response = requests.get("https://api.ratesapi.io/api/{}-{}-01?base={}&symbols={}".format(i,j,strinpcode,stroutcode))
                    data = response.json()
                    rate = data['rates'][stroutcode]
                    y.append(rate)
                    x.append("{}/{}".format(i,j))
        elif fyear == 2021:
            for i in range(1,tmonth+1):
                response = requests.get("https://api.ratesapi.io/api/2021-{}-01?base={}&symbols={}".format(i,strinpcode,stroutcode))
                data = response.json()
                rate = data['rates'][stroutcode]
                y.append(rate)
                x.append("{}/{}".format(2021,i))
        else :
            for i in range(fyear,tyear):
                for j in range(1,13):
                    response = requests.get("https://api.ratesapi.io/api/{}-{}-01?base={}&symbols={}".format(i,j,strinpcode,stroutcode))
                    data = response.json()
                    rate = data['rates'][stroutcode]
                    y.append(rate)
                    x.append("{}/{}".format(i,j))
        hell = Tk()
        hell.attributes('-topmost', True)
        hell.title("{} vs {} comparision".format(strinpcode,stroutcode))
        hell.geometry("500x500")
        def ploti(x,y): 
            fig = Figure(figsize = (10, 10),dpi = 100) 
            plot1 = fig.add_subplot(111) 
            plot1.plot(x,y) 
            canvas = FigureCanvasTkAgg(fig, master = hell)   
            canvas.draw()  
            canvas.get_tk_widget().pack()  
            toolbar = NavigationToolbar2Tk(canvas,hell) 
            toolbar.update() 
            canvas.get_tk_widget().pack() 
        ploti(x,y)
        hell.mainloop()  
    def main(self): # currency conversion
        self.canv2 = Canvas(height= 500,width = 700, bg="light blue")
        self.canv2.place(x =0,y = 85)
        self.value_out = StringVar()
        self.value_in = StringVar()
        self.amount = StringVar()
        inp = Label(self.canv2,text="INPUT CURRENCY",font = ('algerian', 15), bg="light blue")
        inp.place(x = 75,y = 100)
        out = Label(self.canv2,text="OUTPUT CURRENCY",font = ('algerian', 15), bg="light blue")
        out.place(x = 400,y = 100)
        Optionout = ttk.Combobox(self.canv2, textvariable = self.value_out, state = 'readonly', font = ('arial', 15), width = 20)
        Optionout['values'] = ('GBP-Pound sterling','HKD-Hong Kong Dollar','IDR-Indonesian Rupiah','ILS-Israeli New Shekel','DKK-Danish Krone','INR-Indian rupee','CHF-Swiss Franc','MXN-Mexican peso','CZK-Czech koruna koruna česká','SGD-Singapore Dollar','THB-Thai baht','HRK-Croatian Kuna','EUR-Euro','MYR-Malaysian Ringgit','NOK-Norwegian Krone','CNY-Chinese yuan renminbi','BGN-Bulgarian Lev','PHP-Philippine peso','PLN-Polish zloty','ZAR-South African Rand','CAD-Canadian Dollar','ISK-Icelandic Króna','BRL-Brazilian real','RON-Romanian leu','NZD-New Zealand Dollar','TRY-Turkish lira','JPY-Japanese yen','RUB-Russian Ruble','KRW-South Korean won','USD-United States dollar','AUD-Australian Dollar','HUF-Hungarian Forint','SEK-Swedish Krona')
        Optionout.place(x = 400 , y = 150)
        Optionin = ttk.Combobox(self.canv2, textvariable = self.value_in, state = 'readonly', font = ('arial', 15), width = 20)
        Optionin['values'] = ('GBP-Pound sterling','HKD-Hong Kong Dollar','IDR-Indonesian Rupiah','ILS-Israeli New Shekel','DKK-Danish Krone','INR-Indian rupee','CHF-Swiss Franc','MXN-Mexican peso','CZK-Czech koruna koruna česká','SGD-Singapore Dollar','THB-Thai baht','HRK-Croatian Kuna','EUR-Euro','MYR-Malaysian Ringgit','NOK-Norwegian Krone','CNY-Chinese yuan renminbi','BGN-Bulgarian Lev','PHP-Philippine peso','PLN-Polish zloty','ZAR-South African Rand','CAD-Canadian Dollar','ISK-Icelandic Króna','BRL-Brazilian real','RON-Romanian leu','NZD-New Zealand Dollar','TRY-Turkish lira','JPY-Japanese yen','RUB-Russian Ruble','KRW-South Korean won','USD-United States dollar','AUD-Australian Dollar','HUF-Hungarian Forint','SEK-Swedish Krona')
        Optionin.place(x = 75 , y = 150)
        in_field = Entry(self.canv2,bd = 1, justify =CENTER, width = 22,font =20, textvariable = self.amount)
        in_field.place(x = 75 ,y = 200)
        self.out_field = Label(self.canv2,bd = 1, justify =CENTER, width = 22,font =20,bg = "white")  #add text output value
        self.out_field.place(x = 400 ,y = 200)
        convertb = Button(self.canv2,text = "CONVERT",height=2,padx = 7,activebackground="#2C84EF",command = self.convertbact)
        convertb.place(x = 300, y =250)
        history = Button(self.canv2,text = "RECENT",  height=2,padx = 11,command = self.history)
        history.place(x = 300, y =300)
        caution_red = Label(self.canv2,text= "*Enter only numbers",font =('Baskerville Old Face',8),fg = "red", bg="light blue")
        caution_red.place(x = 130 ,y = 230)
    def convertbact(self):# storing history 
        inp_curr = self.value_in.get()
        out_curr = self.value_out.get()
        input_amount = self.amount.get()
        RealTimeCurrencyConverter.convert(self,inp_curr,out_curr,input_amount)
        self.out_field['text'] = self.output_amount
        self.f = open('history.txt','a') 
        self.f.write("Input Currency Code:  %s\nOutput Currency Code:  %s\nInput Amount:  %s\nOutput Amount:  %s     Time :%s\n\n" % (self.inp_code,self.out_code,float(input_amount),round(float(self.output_amount),5),datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        self.f.close()
    def history(self):# displaying recent conversions
        self.canv3 = Canvas(height= 500,width = 700)
        self.canv3.place(x =0,y = 85)
        scrollbar = Scrollbar(self.canv3)
        scrollbar.place(x= 750,y = 0)
        mylist = Listbox(self.canv3 , yscrollcommand = scrollbar.set ,height = 20,width= 90)
        f = open("history.txt",'r')
        k = f.readlines()
        for i in range(len(k)):
            mylist.insert(END,k[i])
        mylist.place(x = 30,y = 30)
        scrollbar.config( command = mylist.yview )
        header = Label(self.canv3,text = "YOUR RECENT TRANSACTIONS : ")
        header.place(x=30,y=10)
        Button(self.canv3,text = "CLEAR RECENT",command = self.clearh).place(x = 500,y = 360)
    def clearh(self):   # deleting stored history
        f = open("history.txt",'w')
        f.close()
    def login(self):    # admin login
        e_unmae = self.uname.get().encode(encoding='UTF-8',errors='strict')
        e_passw = self.passw.get().encode(encoding='UTF-8',errors='strict')
        if base64.b64encode(e_unmae) == b'U1VSWUE=' and base64.b64encode(e_passw) == b'UEFTU1dPUkQ=':
            self.canv4  = Canvas(height= 500,width = 700)
            self.canv4.place(x =0,y = 85)
            show = Label(self.canv4,bd = 1, justify =CENTER,font =20,text="YOU HAVE SUCESSFULLY LOGGED IN!!!!")
            show.place(x = 200 ,y = 200)
        else:
            show = Label(self.canv,bd = 1, justify =CENTER,font =('Baskerville Old Face',8),fg = "red",text="Incorrect Username Or password,Try Again", bg="light blue")
            show.place(x = 120,y = 230)
    def ext(self):   # external resources
        x = []
        for i in ['USD','EUR','GBP']:
            response_url = "https://api.ratesapi.io/api/latest?base={}&symbols={}".format('INR', i)
            response = requests.get(response_url)
            data = response.json()
            rates = data['rates'][i]
            x.append("100 Indian Rupees = {} {}".format(rates*100,i))
        self.canvz = Canvas(height= 500,width = 700, bg="light blue")
        self.canvz.place(x =0,y = 85)
        Label(self.canvz,text= 'Current Trends', font = ("algerian",15),bg="light blue").place(x=50,y  = 20)
        l = str(date.today())
        stri = 'As on '+l+' \n'
        for i in x :
            stri = stri + i +"\n"
        Label(self.canvz,text = stri ,font = ("bradley hand itc",15,'bold')).place(x=50,y = 50)
        import webbrowser
        def openweb1():
            webbrowser.open("https://github.com/",new=1)
        def openweb2():
            webbrowser.open('https://www.airasia.co.in/content/air-asia/en/home',new=1)
        def openweb3():
            webbrowser.open("https://www.air.irctc.co.in/",new=1)
        def openweb4():
            webbrowser.open("https://www.goindigo.in/",new=1)
        Label(self.canvz,text = "Visit Some Trusted Travel Websites in India" ,font = ("bradley hand itc",15,'bold'),bg="light blue").place(x=50,y = 200)
        Button(self.canvz,text = "Check For Updates\nCurrent Version 1.1",command=openweb1).place(x=550,y=360)
        Button(self.canvz,text = "1.IRCTC Air",font = ("bradley hand itc",11,'bold'),width=20, command=openweb3).place(x=100,y=250)
        Button(self.canvz,text = "2.Air Asia", font =("bradley hand itc",11,'bold'),width=20,command=openweb2).place(x=100,y=300)
        Button(self.canvz,text = "3.IndiGo.",font =("bradley hand itc",11,'bold'),width=20,command=openweb4).place(x=100,y=350)

###_________driver code________

if __name__ == '__main__':
    App()
    root.mainloop()
