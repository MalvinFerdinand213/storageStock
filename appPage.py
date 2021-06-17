import tkinter as tk
import time as tm
from tkinter import *
from tkinter import messagebox as msg
from PIL import Image, ImageTk

class AppPage(tk.Frame):

    def __init__(self, parent, App):
        self.app = App
        self.settings = App.settings
        self.current_barangs = self.settings.barang[0]
        self.last_current_barangs_index = 0
        self.update_mode = False
        self.barang_index = []

        super().__init__(parent) #parent = window.container
        self.grid(row=0, column=0, sticky="nsew")

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.create_left_frame()
        self.create_right_frame()
        self.config_left_and_right_frame()      

    def create_left_frame(self):
        self.left_frame = tk.Frame(self, bg="pink")
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.create_left_header()
        self.create_left_content()

    def create_right_frame(self):
        self.right_frame = tk.Frame(self, bg="white", width=2*self.settings.width//3)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.create_right_header()
        self.create_right_content()
        self.create_right_footer()

    def config_left_and_right_frame(self):
        self.grid_columnconfigure(0, weight=1) # 1/3
        self.grid_columnconfigure(1, weight=2) # 2/3
        self.grid_rowconfigure(0, weight=1)

    def create_left_header(self):
        frame_w = self.settings.width//3
        frame_h = self.settings.height//5
        self.left_header = tk.Frame(self.left_frame, width=frame_w, height=frame_h)
        self.left_header.pack()

        image = Image.open(self.settings.logo)
        i_w, i_h = image.size
        ratio = i_w/frame_w
        new_size = (int(i_w/ratio), int(i_h/ratio)) # (x,y)
        image = image.resize(new_size)
        self.logo = ImageTk.PhotoImage(image)

        self.label_logo = tk.Label(self.left_header, image=self.logo)
        self.label_logo.pack()

        self.search_box_frame = tk.Frame(self.left_frame, bg="white", width=frame_w, height=frame_h//4)
        self.search_box_frame.pack(fill="x")

        self.entry_search_var = tk.StringVar()
        self.entry_search = tk.Entry(self.search_box_frame, bg="white", fg="black", font=("Arial", 12), textvariable=self.entry_search_var)
        self.entry_search.grid(row=0, column=0)

        self.button_search = tk.Button(self.search_box_frame, bg="white", fg="black", text="Find", font=("Arial", 12), command=self.clicked_search_btn)
        self.button_search.grid(row=0, column=1)

        self.search_box_frame.grid_columnconfigure(0, weight=3)
        self.search_box_frame.grid_columnconfigure(1, weight=1)

    def update_contact_index_list(self):
        barang = self.settings.barang
        self.barang_index = []
        index_counter = 0
        for barangs in barang:
            self.barang_index.append(index_counter)
            index_counter += 1

    def show_list_barang_in_listbox(self):
        barangs = self.settings.barang
        self.update_contact_index_list()
        print(self.barang_index)
        for index in self.barang_index:
            barang = barangs[index]
            for phone, info in barang.items():
                full_barang = f"{info['f_barang']} {info['l_barang']}"
                self.barang_list_box.insert("end", full_barang)

    def show_all_barangs_in_listbox(self):
        self.barang_list_box.delete(0, 'end')
        barang = self.settings.barang
        self.barang_index = []
        counter = 0
        for barangs in barang:
            self.barang_index.append(counter)
            counter += 1
        self.show_list_barang_in_listbox()

    def create_left_content(self):
        frame_w = self.settings.width//3
        frame_h = 4*self.settings.height//5
        self.left_content = tk.Frame(self.left_frame, width=frame_w, height=frame_h, bg="white")
        self.left_content.pack(fill="x")

        self.barang_list_box = tk.Listbox(self.left_content, bg="white", fg="black", font=("Arial", 12), height=frame_h)
        self.barang_list_box.pack(side="left", fill="both", expand=True)

        self.barang_scroll = tk.Scrollbar(self.left_content)
        self.barang_scroll.pack(side="right", fill="y")

        self.show_all_barangs_in_listbox()

        self.barang_list_box.configure(yscrollcommand=self.barang_scroll.set) # set di Scroll
        self.barang_scroll.configure(command=self.barang_list_box.yview) # yview di Listbox

        self.barang_list_box.bind("<<ListboxSelect>>", self.clicked_item_inListBox)


    def clicked_item_inListBox(self, event):
        if not self.update_mode:
            selection = event.widget.curselection()
            try :
                clicked_item_index = selection[0]
            except IndexError:
                clicked_item_index = self.last_current_barangs_index
            index = self.barang_index[clicked_item_index]
            self.last_current_barangs_index = index
            self.current_barangs = self.settings.barang[index]
            print(clicked_item_index,"=>",index)
            for totalBarang, info in self.current_barangs.items():
                barang = totalBarang
                full_barang = info['f_barang']+" "+info['l_barang']
                address = info['address']

            self.full_barang_label.configure(text=full_barang)
            self.table_info[0][1].configure(text=barang)
            self.table_info[1][1].configure(text=address)


    def create_right_header(self):
        frame_w = 2*self.settings.width//3
        frame_h = self.settings.height//5

        self.right_header = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="bisque")
        self.right_header.pack()
        self.create_detail_right_header()

    def create_detail_right_header(self):
        frame_w = 2*self.settings.width//3
        frame_h = self.settings.height//5

        self.detail_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="green")
        self.detail_header.grid(row=0, column=0, sticky="nsew")

        data_dictionary = list(self.current_barangs.values())[0]
        full_barang = f"{data_dictionary['f_barang']} {data_dictionary['l_barang']}"
        self.virt_img = tk.PhotoImage(width=1, height=1)
        self.full_barang_label = tk.Label(self.detail_header, text=full_barang, font=("Arial", 30), width=frame_w, height=frame_h, image=self.virt_img, compound='c', bg="white")
        self.full_barang_label.pack()

        self.right_header.grid_rowconfigure(0, weight=1)
        self.right_header.grid_columnconfigure(0, weight=1)

    def clock(self):
        frame_w = 2*self.settings.width//3
        frame_h = self.settings.height//5

        hour = self.time.strftime("%H")
        minute = self.time.strftime("%M")
        second = self.time.strftime("%S")

        my_label.config(text=hour + ":" + minute + ":" + second)
        mylabel.after(1000, clock)

        my_label = Label(root, text="", font=("Helvetica", 48), fg="green", bg="black")
        my_label.pack(pady=20)

        clock()    

    def create_right_content(self):
        frame_w = 2*self.settings.width//3
        frame_h = 3*(4*self.settings.height//5)//4

        self.right_content = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
        self.right_content.pack(expand=True, pady=90)
        self.create_detail_right_content()

    def create_detail_right_content(self):
        frame_w = 2*self.settings.width//3
        frame_h = 3*(4*self.settings.height//5)//4

        self.detail_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
        self.detail_content.grid(row=0, column=0, sticky="nsew")

        for totalBarang, info in self.current_barangs.items():
            info = [
                ['Jumlah Barang :', totalBarang],
                ['Lokasi saat ini :', info['address']]
            ]
        self.table_info = []
        rows, columns = len(info), len(info[0]) # 3, 2
        for row in range(rows):
            aRow = []
            for column in range(columns):
                label = tk.Label(self.detail_content, text=info[row][column], font=("Arial", 12), bg="white")
                aRow.append(label)
                if column == 0:
                    sticky = "e"
                else:
                    sticky = "w"
                label.grid(row=row, column=column, sticky=sticky)
            self.table_info.append(aRow)


        self.right_content.grid_rowconfigure(0, weight=1)
        self.right_content.grid_columnconfigure(0, weight=1)


    def create_right_footer(self):
        frame_w = 2*self.settings.width//3
        frame_h = (4*self.settings.height//5)//4

        self.right_footer = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
        self.right_footer.pack(expand=True)

        self.create_detail_right_footer()


    def create_detail_right_footer(self):
        frame_w = 2*self.settings.width//3
        frame_h = (4*self.settings.height//5)//4

        self.detail_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
        self.detail_footer.grid(row=0, column=0, sticky="nsew")

        features = ['Update', 'Delete', 'Add New']
        commands = [self.clicked_update_btn, self.clicked_delete_btn, self.clicked_add_new_btn]
        self.buttons_features = []
        for feature in features:
            button = tk.Button(self.detail_footer, text=feature, bg="white", fg="black", bd=0, font=("Arial", 12, "bold"), command=commands[features.index(feature)])
            button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20)
            self.buttons_features.append(button)

        self.right_footer.grid_rowconfigure(0, weight=1)
        self.right_footer.grid_columnconfigure(0, weight=1)

    def recreate_right_frame(self):
        self.detail_header.destroy()
        self.detail_update_content.destroy()
        self.detail_update_footer.destroy()

        #RECREATE HEADER
        self.create_detail_right_header()

        #RECREATE CONTENT
        self.create_detail_right_content()

        #RECREATE FOOTER
        self.create_detail_right_footer()

    def recreate_right_frame_after_delete(self):
        self.detail_header.destroy()
        self.detail_content.destroy()
        self.detail_footer.destroy()

        #RECREATE HEADER
        self.create_detail_right_header()

        #RECREATE CONTENT
        self.create_detail_right_content()

        #RECREATE FOOTER
        self.create_detail_right_footer()

    def recreate_right_frame_after_add_new(self):
        self.detail_add_contact_header.destroy()
        self.detail_add_contact_content.destroy()
        self.detail_add_contact_footer.destroy()

         #RECREATE HEADER
        self.create_detail_right_header()

        #RECREATE CONTENT
        self.create_detail_right_content()

        #RECREATE FOOTER
        self.create_detail_right_footer()


    def clicked_update_btn(self):
        self.update_mode = True
        frame_w = 2*self.settings.width//3
        frame_h = self.settings.height//5

        self.detail_content.destroy()
        self.detail_footer.destroy()

        self.detail_update_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
        self.detail_update_content.grid(row=0, column=0, sticky="nsew")

        for totalBarang, info in self.current_barangs.items():
            info = [
                ['Nama Depan Barang :', info['f_barang']],
                ['Nama Belakang Barang :', info['l_barang']],
                ['Jumlah Barang :', totalBarang],
                ['Alamat :', info['address']],
            ]
        self.table_info = []
        self.entry_update_barangs_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        rows, columns = len(info), len(info[0]) # 3, 2
        for row in range(rows):
            aRow = []
            for column in range(columns):
                if column == 0:
                    label = tk.Label(self.detail_update_content, text=info[row][column], font=("Arial", 12), bg="white")
                    sticky = "e"
                    aRow.append(label)
                    label.grid(row=row, column=column, sticky=sticky)
                else:
                    entry = tk.Entry(self.detail_update_content, font=("Arial", 12), bg="white", textvariable=self.entry_update_barangs_vars[row])
                    entry.insert(0, info[row][column])
                    sticky = "w"
                    aRow.append(entry)
                    entry.grid(row=row, column=column, sticky=sticky)
            self.table_info.append(aRow)

        self.right_content.grid_rowconfigure(0, weight=1)
        self.right_content.grid_columnconfigure(0, weight=1)

        frame_w = 2*self.settings.width//3
        frame_h = (4*self.settings.height//5)//4

        self.detail_update_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
        self.detail_update_footer.grid(row=0, column=0, sticky="nsew")

        features = ['Save', 'Cancel']
        commands = [self.clicked_save_barangs_btn, self.clicked_cancel_barangs_btn]
        self.buttons_features = []
        for feature in features:
            button = tk.Button(self.detail_update_footer, text=feature, bg="white", fg="black", bd=0, font=("Arial", 12, "bold"), command=commands[features.index(feature)])
            button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20)
            self.buttons_features.append(button)

        self.right_footer.grid_rowconfigure(0, weight=1)
        self.right_footer.grid_columnconfigure(0, weight=1)


    def clicked_delete_btn(self):
        confirm = msg.askyesnocancel('barangsapp Save Confirmation', 'Kamu yakin ingin menghapus semua informasi barang ini ?')

        if confirm:
            #print(self.current_barangs, self.last_current_barangs_index)
            self.settings.barang.pop(self.last_current_barangs_index)
            barang = self.settings.barang
            self.barang_index = []
            index_counter = 0
            for barangs in barang:
                self.barang_index.append(index_counter)
                index_counter += 1
            self.update_contact_index_list()
            self.settings.save_data_to_json()

            self.recreate_right_frame_after_delete()
            self.barang_list_box.delete(0, 'end')
            self.show_list_barang_in_listbox()


    def clicked_add_new_btn(self):
        self.update_mode = True
        frame_w = 2*self.settings.width//3
        frame_h = self.settings.height//5

        self.detail_header.destroy()
        self.detail_content.destroy()
        self.detail_footer.destroy()

        self.detail_add_contact_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="green")
        self.detail_add_contact_header.grid(row=0, column=0, sticky="nsew")

        self.virt_img = tk.PhotoImage(width=1, height=1)
        self.add_barang_label = tk.Label(self.detail_add_contact_header, text="Tambah Barang Baru", font=("Arial", 30), width=frame_h, image=self.virt_img, compound="c", bg="white")
        self.add_barang_label.pack()

        frame_w = 2*self.settings.width//3
        frame_h = self.settings.height//5

        self.detail_add_contact_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
        self.detail_add_contact_content.grid(row=0, column=0, sticky="nsew")

        info = [
                ['Nama Depan Barang :', None],
                ['Nama Belakang Barang :', None],
                ['Jumlah Barang :', None],
                ['Alamat :', None],
            ]

        rows, columns = len(info), len(info[0])
        self.entry_update_barangs_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        for row in range(rows):
            aRow = []
            for column in range(columns):
                if column == 0:
                    label = tk.Label(self.detail_add_contact_content, text=info[row][column], font=("Arial", 12), bg="white")
                    sticky = "e"
                    aRow.append(label)
                    label.grid(row=row, column=column, sticky=sticky)
                else:
                    entry = tk.Entry(self.detail_add_contact_content, font=("Arial", 12), bg="white", textvariable=self.entry_update_barangs_vars[row])
                    sticky = "w"
                    aRow.append(entry)
                    entry.grid(row=row, column=column, sticky=sticky)
            self.table_info.append(aRow)

        self.right_content.grid_rowconfigure(0, weight=1)
        self.right_content.grid_columnconfigure(0, weight=1)

        frame_w = 2*self.settings.width//3
        frame_h = (4*self.settings.height//5)//4

        self.detail_add_contact_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
        self.detail_add_contact_footer.grid(row=0, column=0, sticky="nsew")

        features = ['Save', 'Cancel']
        commands = [self.clicked_save_new_contact_btn, self.clicked_cancel_barangs_btn]
        self.buttons_features = []
        for feature in features:
            button = tk.Button(self.detail_add_contact_footer, text=feature, bg="white", fg="black", bd=0, font=("Arial", 12, "bold"), command=commands[features.index(feature)])
            button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20)
            self.buttons_features.append(button)

        self.right_footer.grid_rowconfigure(0, weight=1)
        self.right_footer.grid_columnconfigure(0, weight=1)




    def clicked_save_barangs_btn(self):
        self.update_mode = False

        confirm = msg.askyesnocancel('barangsapp Save Confirmation', 'Kamu yakin ingin mengupdate informasi barang ini ?')
        
        index = self.last_current_barangs_index
        if confirm:
            f_barang = self.entry_update_barangs_vars[0].get()
            l_barang = self.entry_update_barangs_vars[1].get()
            phone = self.entry_update_barangs_vars[2].get()
            address = self.entry_update_barangs_vars[3].get()
            self.settings.barang[index] = {
                phone : {
                    "f_barang" : f_barang,
                    "l_barang" :l_barang,
                    "address" : address
                }
            }
            self.settings.save_data_to_json()
        self.current_barangs = self.settings.barang[index]

        self.recreate_right_frame()

        self.barang_list_box.delete(0, 'end')
        self.show_list_barang_in_listbox()


    def clicked_cancel_barangs_btn(self):
        self.update_mode = False

        self.recreate_right_frame()


    def clicked_search_btn(self):

        item_search = self.entry_search_var.get()
        if item_search:
            barang = self.settings.barang
            self.barang_index = []
            index_counter = 0
            for barangs in barang:
                for totalBarang, info in barangs.items():
                    if item_search in totalBarang:
                        print(totalBarang)
                        self.barang_index.append(index_counter)
                    elif item_search in info['f_barang']:
                        print(info['f_barang'])
                        self.barang_index.append(index_counter)
                    elif item_search in info['l_barang']:
                        print(info['l_barang'])
                        self.barang_index.append(index_counter)
                index_counter += 1
            print(self.barang_index)
            self.barang_list_box.delete(0, 'end')
            self.show_list_barang_in_listbox()
        else:
            self.show_all_barangs_in_listbox()

    def clicked_save_new_contact_btn(self):
        self.update_mode = False

        confirm = msg.askyesnocancel('barangsapp Save Confirmation', 'Kamu yakin ingin menambahkan informasi barang ini ?')
        
        index = self.last_current_barangs_index
        if confirm:
            f_barang = self.entry_update_barangs_vars[0].get()
            l_barang = self.entry_update_barangs_vars[1].get()
            phone = self.entry_update_barangs_vars[2].get()
            address = self.entry_update_barangs_vars[3].get()
            product = {
                phone : {
                    "f_barang" : f_barang,
                    "l_barang" :l_barang,
                    "address" : address
                }
            }
            self.settings.barang.append(product)
            self.last_current_barangs_index = len(self.settings.barang)-1
            self.settings.save_data_to_json()
            self.current_barangs = self.settings.barang[index]

        self.recreate_right_frame_after_add_new()
        self.barang_list_box.delete(0, 'end')
        self.show_list_barang_in_listbox()


    def clicked_cancel_new_contact_btn(self):
        self.update_mode = False

        self.recreate_right_frame_after_add_new()











