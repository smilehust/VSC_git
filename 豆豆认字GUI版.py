import tkinter as tk


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.show_label = tk.Label(self, font = ("黑体, 200"))
        self.show_label.pack()

        self.revious_button = tk.Button(self, height=5, width=30, text="<---", command=self.revious_fun)
        self.revious_button.pack(side="left")
    
        self.yihui_button = tk.Button(self, height=5, width=20, text="已会", command=self.yihui_fun)
        self.yihui_button.pack(side="left")

        self.next_button = tk.Button(self, height=5, width=30,  text="--->", command=self.next_fun)
        self.next_button.pack(side="left")

    def revious_fun(self):
        self.show_label['text'] = '后退一个字'

    def yihui_fun(self):
        self.show_label['text'] = '添加到已会文件'

    def next_fun(self):
        self.show_label['text'] = '前进一个字'


# 设置主窗口属性
root = tk.Tk()
root.title('豆豆认字')
root.geometry('1024x768')

# 实例化对象并把对象放进主窗口
app = App(master=root)
app.mainloop()


# tk = tkinter.Tk()     # 实例化一个窗体
# tk.title('豆豆认字')   # 给组件命名
# tk.geometry('1024x768')

# laber = tkinter.Label(master=tk, text='认字内容')
# laber.pack()          # 将label加到窗体中，要使用到pack方法才能显示在窗体中

# def button_1_fun():
#     print('button_1_press')

# button_1 = tkinter.Button(master=tk, text='下一个', command=button_1_fun)
# button_1.pack()

# tk.mainloop()         # 循环，没有这行，程序会立刻结束
