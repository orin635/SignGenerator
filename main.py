import imp
from multiprocessing.connection import wait
import sys
import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import filedialog
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
from time import *
from bs4 import BeautifulSoup


#####Globals
username = os.getlogin()
global filelocation
filelocation = "C:/users/"+username+"/desktop"




class Sign:
    def __init__(self, price = 0, rrp = 0, sku = "", name = "", sold_as_seen = False, sign_position = 1, next_sign = 0):
        self.price = price
        self.rrp = rrp
        self.sku = sku
        self.name = name
        self.sold_as_seen = sold_as_seen
        self.sign_postion = sign_position
        self.next_sign = next_sign


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



def generateImage(sign = Sign()):
    yAdustment = 700
    #Price location values
    priceX = 200
    if(sign.sign_position == 2 or sign.sign_position == 4):
        priceX = 700
    priceY = 446
    if(sign.sign_position == 3 or sign.sign_position == 4):
        priceY = priceY + yAdustment
    priceYadjustments = 0

    #SKU Location Values
    skuX = 200
    if(sign.sign_position == 2 or sign.sign_position == 4):
        skuX = 700
    skuY = 500
    if(sign.sign_position == 3 or sign.sign_position == 4):
        skuY = skuY + yAdustment
    skuYadjustments = 0

    #RRP Location Values
    rrpX = 200
    if(sign.sign_position == 2 or sign.sign_position == 4):
        rrpX = 700
    rrpY = 390
    if(sign.sign_position == 3 or sign.sign_position == 4):
        rrpY = rrpY + yAdustment
    rrpYadjustments = 0

    #RRP Location Values
    nameX = 200
    if(sign.sign_position == 2 or sign.sign_position == 4):
        nameX = 700
    nameY = 265
    if(sign.sign_position == 3 or sign.sign_position == 4):
        nameY = nameY + yAdustment
    nameYadjustments = 0
    
    #Sold as Seen Location Values
    sasX = 200
    if(sign.sign_position == 2 or sign.sign_position == 4):
        sasX = 700
    sasY = 240
    if(sign.sign_position == 3 or sign.sign_position == 4):
        sasY = sasY + yAdustment
    sasYadjustments = 0


    #Adjust for Sold As Seen
    if(sign.sold_as_seen == True):
        priceYadjustments = 16
        skuYadjustments = 7
        rrpYadjustments = 20
        nameYadjustments = 15

    #Generate todays date & time
    dt = strftime("%Y-%m-%d--%H-%M-%S", gmtime())
    dt = str(dt)

    global filelocation
    if(filelocation == ""):
        filelocation = "C:/users/"+username+"/desktop"


    #What image to open
    if(sign.sign_position == 1):
        img = Image.open(resource_path("data/blank_sign.png"))
    elif(sign.sign_position == 2):
        img = Image.open("C:/Users/"+username+"/gen_sign/sign1_final.png")
    elif(sign.sign_position == 3):
        img = Image.open("C:/Users/"+username+"/gen_sign/sign2_final.png")
    elif(sign.sign_position == 4):
        img = Image.open("C:/Users/"+username+"/gen_sign/sign3_final.png")
    else:
        img = Image.open(resource_path("data/blank_sign.png"))



    img1 = ImageDraw.Draw(img)

    #Add the price
    price_font = ImageFont.truetype(resource_path('data/Lato-Black.ttf'), 57)
    img1.text((priceX, priceY + priceYadjustments),
                    text = "Now "+sign.price,
                    font = price_font,
                    fill=(255,0,0),
                    anchor="mm"
                    )

    #Add SKU
    sku_font = ImageFont.truetype(resource_path('data/Lato-Regular.ttf'), 22)
    img1.text((skuX,skuY+skuYadjustments),
                text=sign.sku,
                font=sku_font,
                fill=(0,0,0),
                anchor="mm"
                )


    #Adding the RRP
    rrp = str(sign.rrp)
    rrp_text = ""
    if(float(rrp.replace("€", "").replace(",", "")) > 0):
        rrp_text = "RRP "+rrp
    rrp_font = ImageFont.truetype(resource_path('data/Lato-Regular.ttf'), 27)
    img1.text((rrpX,rrpY+rrpYadjustments),
                text=rrp_text,
                font=rrp_font,
                fill=(0,0,0),
                anchor="mm"
                )




    #Add The Name
    name_font_size = 38
    name_parts = []
    name_parts2 = []
    add_second_name = 0
    add_third_name = 0
    nameYadjustments = 40
    #If name is longer than 24 characters split in 2 lines
    name = sign.name
    if(len(name)> 24):
        name_font_size = 34
        if(len(name) == 24):
            name_font_size = 30
        nameYadjustments = 20

        name1 = name[0:24]
        name2 = name[24:]
        name1 = name1[24::-1]
        name1 = name1.replace(" ", "\n", 1)
        name1 = name1[24::-1]
        name = name1 + name2

        name_parts = name.split("\n")
        name = name_parts[0]

        add_second_name = 1

        #If second line is longer than 2 charcters split in 2 lines again
        if(len(name_parts[1])>24):
            name3 = name_parts[1]
            name4 = name3[24:]
            name3 = name3[0:24]
            name3 = name3[24:: -1]
            name3 = name3.replace(" ", "\n", 1)
            name3 = name3[24:: -1]
            name3 = name3 + name4
            name_parts2 = name3.split("\n")
            name_parts[1] = name_parts2[0]

            add_third_name = 1

    #Adjust Font for name length
    if(len(name)>48):
        name_font_size = 28
        nameYadjustments = 0

    #Adding Line 1
    name_font = ImageFont.truetype(resource_path('data/Lato-Black.ttf'), name_font_size)
    img1.text((nameX,nameY+nameYadjustments),
                text=name,
                font=name_font,
                fill=(0,0,0),
                anchor="mm"
                )
    #If you dont need to add another name line or sold as seen save
    if(add_second_name == 0 and sign.sold_as_seen == False):
        if(sign.next_sign == 1):
            img.save("C:/Users/"+username+"/gen_sign/sign1_final.png")
        elif(sign.next_sign == 2):
            img.save("C:/Users/"+username+"/gen_sign/sign2_final.png")
        elif(sign.next_sign == 3):
            img.save("C:/Users/"+username+"/gen_sign/sign3_final.png")
        else:
            file_name = "/Sign_"+dt+".png"
            img.save(filelocation+file_name)  
    
    #Add the second line name
    if(add_second_name == 1):
        img1.text((nameX,nameY+nameYadjustments+35),
                    text=name_parts[1],
                    font=name_font,
                    fill=(0,0,0),
                    anchor="mm"
                    )
        if(add_third_name == 0 and sign.sold_as_seen == False):
            if(sign.next_sign == 1):
                img.save("C:/Users/"+username+"/gen_sign/sign1_final.png")
            elif(sign.next_sign == 2):
                img.save("C:/Users/"+username+"/gen_sign/sign2_final.png")
            elif(sign.next_sign == 3):
                img.save("C:/Users/"+username+"/gen_sign/sign3_final.png")
            else:
                file_name = "/Sign_"+dt+".png"
                img.save(filelocation+file_name)
        
    #Adding Line 3
    if(add_third_name == 1):
        img1.text((nameX,nameY+nameYadjustments+70),
                    text=name_parts2[1],
                    font=name_font,
                    fill=(0,0,0),
                    anchor="mm"
                    )
        if(sign.sold_as_seen == False):
            if(sign.next_sign == 1):
                img.save("C:/Users/"+username+"/gen_sign/sign1_final.png")
            elif(sign.next_sign == 2):
                img.save("C:/Users/"+username+"/gen_sign/sign2_final.png")
            elif(sign.next_sign == 3):
                img.save("C:/Users/"+username+"/gen_sign/sign3_final.png")
            else:
                file_name = "/Sign_"+dt+".png"
                img.save(filelocation+file_name)





    #Adding Sold as Seen
    if(sign.sold_as_seen == 1):
        sold_as_seen_font = ImageFont.truetype(resource_path('data/Lato-Black.ttf'), 35)
        img1.text((sasX, sasY + sasYadjustments),
                        text = "Sold as Seen",
                        font = sold_as_seen_font,
                        fill=(255,0,0),
                        anchor="mm"
                        )
        
        if(sign.next_sign == 1):
            img.save("C:/Users/"+username+"/gen_sign/sign1_final.png")
        elif(sign.next_sign == 2):
            img.save("C:/Users/"+username+"/gen_sign/sign2_final.png")
        elif(sign.next_sign == 3):
            img.save("C:/Users/"+username+"/gen_sign/sign3_final.png")
        else:
            file_name = "/Sign_"+dt+".png"
            img.save(filelocation+file_name)





def generateImageData(link, tickbox,sign_number, custom_price, another_sign):
    sign = Sign()

    URL = link
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id = "maincontent")
    price_elements = results.find_all("span", class_="price")
    sku_elements = results.find_all("div", class_="product attribute sku")
    name_elements = results.find_all("span", class_="base")


    #Get Price
    sign.price = price_elements[0].text.strip()

    try:#Try get RRP if it exists
        sign.rrp = price_elements[1].text.strip()
    except:#Else default to 0
        sign.rrp= 0

    if(sign.rrp == sign.price):
        sign.rrp = 0

    #Get SKU
    sign.sku = sku_elements[0].text.strip().replace("SKU", "").strip()
    #Get Name
    sign.name = name_elements[0].text.strip()

    sign.sign_position = sign_number

    #mark if sold as seen
    if(tickbox == 1):
        sign.sold_as_seen = True
    else:
        sign.sold_as_seen = False

    sign.next_sign = another_sign


    if(custom_price != ""):
        sign.price = "\u20AC" + str(custom_price)

    generateImage(sign)



def loadUI():
    ##Initial
    window = tk.Tk()
    window.geometry("1600x1000")
    window.title("Sign Generator")
    default_font = font.Font(family= "Helvetica", size= 17)
    window.iconbitmap(resource_path("data/signGenerator.ico"))



 
    ############SIGN 1
    sign1_bg = "#f6e74c"
    sign1_canvas = tk.Canvas(width=600, height= 250, bg= sign1_bg)
    sign1_canvas.place(x=25, y = 25)
    #Label for sign 1 input
    sign1_label = tk.Label(text="Enter sign 1", font= default_font, bg= sign1_bg)
    sign1_label.place(x = 50, y = 50)
    #sign 1 entry Field
    sign1_entry = tk.Entry(bg="#b3b8bd", width=50)
    sign1_entry.place(x=50, y = 90)
    #sign 1 CheckBox
    sign1_checkbox_value = tk.IntVar()
    sign1_checkbox = tk.Checkbutton(text = "Sold As Seen", variable= sign1_checkbox_value, onvalue= 1, offvalue= 0, font= default_font, bg= sign1_bg)
    sign1_checkbox.place(x=50, y = 120)
    #Label for sign 1 customer price
    sign1_label = tk.Label(text="Enter a Customer price if required", font= default_font, bg= sign1_bg)
    sign1_label.place(x = 50, y = 160)
    #sign 1 Custom Price
    sign1_custom_price = tk.Entry(bg="#b3b8bd", width=30)
    sign1_custom_price.place(x=50, y = 195)


    ############SIGN 2
    sign2_bg = "#9bf64c"
    sign2_canvas = tk.Canvas(width=600, height= 250, bg= sign2_bg)
    sign2_canvas.place(x=975, y = 25)
    #Label for sign 1 input
    sign2_label = tk.Label(text="Enter sign 2", font= default_font, bg= sign2_bg)
    sign2_label.place(x = 1000, y = 50)
    #sign 1 entry Field
    sign2_entry = tk.Entry(bg="#b3b8bd", width=50)
    sign2_entry.place(x=1000, y = 90)
    #sign 1 CheckBox
    sign2_checkbox_value = tk.IntVar()
    sign2_checkbox = tk.Checkbutton(text = "Sold As Seen", variable= sign2_checkbox_value, onvalue= 1, offvalue= 0, font= default_font, bg= sign2_bg)
    sign2_checkbox.place(x=1000, y = 120)
    #Label for sign 1 customer price
    sign2_label = tk.Label(text="Enter a Customer price if required", font= default_font, bg= sign2_bg)
    sign2_label.place(x = 1000, y = 160)
    #sign 1 Custom Price
    sign2_custom_price = tk.Entry(bg="#b3b8bd", width=30)
    sign2_custom_price.place(x=1000, y = 195)
    
    
    ############SIGN 3
    sign3_bg = "#c72323"
    sign3_canvas = tk.Canvas(width=600, height= 250, bg= sign3_bg)
    sign3_canvas.place(x=25, y = 425)
    #Label for sign 1 input
    sign3_label = tk.Label(text="Enter sign 3", font= default_font, bg= sign3_bg)
    sign3_label.place(x = 50, y = 450)
    #sign 1 entry Field
    sign3_entry = tk.Entry(bg="#b3b8bd", width=50)
    sign3_entry.place(x=50, y = 490)
    #sign 1 CheckBox
    sign3_checkbox_value = tk.IntVar()
    sign3_checkbox = tk.Checkbutton(text = "Sold As Seen", variable= sign3_checkbox_value, onvalue= 1, offvalue= 0, font= default_font, bg= sign3_bg)
    sign3_checkbox.place(x=50, y = 520)
    #Label for sign 1 customer price
    sign3_label = tk.Label(text="Enter a Customer price if required", font= default_font, bg= sign3_bg)
    sign3_label.place(x = 50, y = 560)
    #sign 1 Custom Price
    sign3_custom_price = tk.Entry(bg="#b3b8bd", width=30)
    sign3_custom_price.place(x=50, y = 595)
    

    ############SIGN 4
    sign4_bg = "#5e94f7"
    sign4_canvas = tk.Canvas(width=600, height= 250, bg= sign4_bg)
    sign4_canvas.place(x=975, y = 425)
    #Label for sign 1 input
    sign4_label = tk.Label(text="Enter sign 4", font= default_font, bg= sign4_bg)
    sign4_label.place(x = 1000, y = 450)
    #sign 1 entry Field
    sign4_entry = tk.Entry(bg="#b3b8bd", width=50)
    sign4_entry.place(x=1000, y = 490)
    #sign 1 CheckBox
    sign4_checkbox_value = tk.IntVar()
    sign4_checkbox = tk.Checkbutton(text = "Sold As Seen", variable= sign4_checkbox_value, onvalue= 1, offvalue= 0, font= default_font, bg= sign4_bg)
    sign4_checkbox.place(x=1000, y = 520)
    #Label for sign 1 customer price
    sign4_label = tk.Label(text="Enter a Customer price if required", font= default_font, bg= sign4_bg)
    sign4_label.place(x = 1000, y = 560)
    #sign 1 Custom Price
    sign4_custom_price = tk.Entry(bg="#b3b8bd", width=30)
    sign4_custom_price.place(x=1000, y = 595)





    def selectFileLocation():
        global filelocation
        default_filelocation = "C:/users/"+username+"/desktop"
        filelocation = filedialog.askdirectory(title='Select Folder to save to(default is desktop)', initialdir=default_filelocation)

    #save location
    location_select = tk.Button(text="Select Save Location",width=25,height=2,bg = "#759cff",fg = "#020303",font = default_font,command= selectFileLocation)
    location_select.place(x = 160,y = 900)



    def load_signs():
        try:
            os.mkdir("C:/Users/"+username+"/gen_sign")
        except:
            pass
        
        def load_sign1():
            sign1 = sign1_entry.get()
            sign2 = sign2_entry.get()
            if(sign1 != ""):        
                checkbox = sign1_checkbox_value.get()
                custom_price = sign1_custom_price.get()
                sign_number = 1
                another_sign = 0
                if(sign2 != ""):
                    another_sign = 1
                generateImageData(sign1, checkbox,sign_number,custom_price, another_sign)
        
        def load_sign2():
            sign2 = sign2_entry.get()
            sign3 = sign3_entry.get()
            if(sign2 != ""):
                checkbox = sign2_checkbox_value.get()
                custom_price = sign2_custom_price.get()
                sign_number = 2
                another_sign = 0
                if(sign3 != ""):
                    another_sign = 2        
                generateImageData(sign2, checkbox,sign_number,custom_price, another_sign)
        
        def load_sign3():
            sign3 = sign3_entry.get()
            sign4 = sign4_entry.get()
            if(sign3 != ""):
                checkbox = sign3_checkbox_value.get()
                custom_price = sign3_custom_price.get()
                sign_number = 3
                another_sign = 0 
                if(sign4 != ""):
                    another_sign = 3           
                generateImageData(sign3, checkbox,sign_number,custom_price, another_sign)
        
        def load_sign4():
            sign4 = sign4_entry.get()
            if(sign4 != ""):
                checkbox = sign4_checkbox_value.get()
                custom_price = sign4_custom_price.get()
                sign_number = 4
                another_sign = 0            
                generateImageData(sign4, checkbox,sign_number,custom_price, another_sign)

        load_sign1()
        load_sign2()
        load_sign3()
        load_sign4()



    #submitButton
    submit = tk.Button(text="Generate Sign",width=15,height=2,bg = "#759cff",fg = "#020303",font = default_font,command= load_signs)
    submit.place(x = 700,y = 900)


    window.mainloop()




def main():
    loadUI()



if __name__ == "__main__":
    main()