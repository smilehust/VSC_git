import codecs
import tkinter as tk
from pypinyin import pinyin, lazy_pinyin  # 这个支持多音字

NUM = 50             # 每次学习的字词数
root_width = 1024    # 设置主窗口尺寸，最好是1024x768
root_height = 768

dangqian = set()
yihui = set()
total = set()
study_total = ()

# 全部学会“当前学字库.txt”后清空这个文件，就能自动调入新的50个了
with codecs.open('当前学字库.txt', 'r+', 'utf-8') as f_d,\
        codecs.open('已会字库.txt', 'r', 'utf-8') as f_y,\
        codecs.open('总字库.txt', 'r', 'utf-8') as f_t:
    for line in f_d:
        a = line.strip('\n').strip('\r')
        dangqian.add(a)
    for line in f_y:
        a = line.strip('\n').strip('\r')
        yihui.add(a)
    for line in f_t:
        a = line.strip('\n').strip('\r')
        total.add(a)
    study_total = total - yihui
    if not dangqian:    # 如果当前学字库是空的，则全新写入NUM个进去，此处用r+和a+一样效果
        dangqian = set(list(study_total)[:NUM])
        for line in dangqian:
            f_d.write(line + '\n')
        study = dangqian
    else:    
        study = dangqian - yihui
        if not study:  # 如果当前字库都已学会，则新生成NUM个并覆盖写入当前字库文件
            study = set(list(study_total)[:NUM])
            for line in study:
                f_d.write(line + '\n')
study.discard('')        # 删除集合中空元素，如果不存在，忽略
study = list(study)[:NUM]      # 生成按顺序学习的列表


# 全局变量，函数内部会修改这些变量
NOW_NUM = len(study)      # 本次学习的总字数，可能小于NUM数
index = 0                # 当前学的字的列表索引
leftKey_flag = 1         # 左方向键开关
rightKey_flag = 1        # 右方向键开关
upkey_flag = 1           # 向上键，加入已会字库


pinyin('预加载')  # 提前加载一次库，提高用户体验
####################### 以下为 GUI 界面，不要更改设置顺序 ######################
# 设置主窗口
root = tk.Tk()
root.title('豆豆认字 V20180924')
# 设置主窗口居中
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
sw = int((sw-root_width)/2)
sh = int((sh-root_height)/2)
root.geometry('{}x{}+{}+{}'.format(root_width, root_height, sw, sh))
root.iconbitmap('豆豆.ico')    # 窗口图标
root.resizable(0, 0)    # 禁止主窗口调整大小


# 定义控制函数
def revious_fun():
    global NOW_NUM, index, leftKey_flag, rightKey_flag 
    next_button['state'] = "normal"
    rightKey_flag = 1
    index -= 1
    if 0 <= index <= NOW_NUM - 1:
        hanzi_label['text'] = study[index]
        pinyin_label['text'] = ' '.join(''.join(i) for i in pinyin(study[index]))
        index_label['text'] = '{}/{}'.format(index+1, NOW_NUM)
        if index == 0:
            revious_button['state'] = "disabled"
            leftKey_flag = 0


def yihui_fun():
    global NOW_NUM, index, leftKey_flag, rightKey_flag, upkey_flag
    with codecs.open('已会字库.txt', 'a', 'utf-8') as f:
        f.write('\n' + study[index])
    study.remove(study[index])
    NOW_NUM -= 1
    if NOW_NUM == 0:  # 当前待学习的列表为空，都加入已会后，就锁住界面
        yihui_button['state'] = "disabled"
        upkey_flag = 0
        revious_button['state'] = "disabled"
        next_button['state'] = "disabled"
        leftKey_flag = 0
        rightKey_flag = 0
        hanzi_label['text'] = ''
        pinyin_label['text'] = ''
    elif NOW_NUM > 0:
        if index == NOW_NUM:  # 处理列表最后一个元素的显示问题
            index -= 1
            next_button['state'] = "disabled"
        hanzi_label['text'] = study[index]
        pinyin_label['text'] = ' '.join(''.join(i) for i in pinyin(study[index]))
        index_label['text'] = '{}/{}'.format(index+1, NOW_NUM)

def next_fun():
    global NOW_NUM, index, leftKey_flag, rightKey_flag
    revious_button['state'] = "normal"
    leftKey_flag = 1
    index += 1
    if 0 <= index <= NOW_NUM - 1:
        hanzi_label['text'] = study[index]
        pinyin_label['text'] = ' '.join(''.join(i) for i in pinyin(study[index]))
        index_label['text'] = '{}/{}'.format(index+1, NOW_NUM)
        if index == NOW_NUM - 1:
            next_button['state'] = "disabled"
            rightKey_flag = 0

def add_fun():
    with codecs.open('当前学字库.txt', 'a', 'utf-8') as f_d, codecs.open('总字库.txt', 'a', 'utf-8') as f_t:
        f_d.write('\n' + shuru_entry.get())
        f_t.write('\n' + shuru_entry.get())
    e_shuru_entry.set('')    # 清空输入栏

def shuru_entry_return(event):
    hanzi_label['text'] = shuru_entry.get()
    pinyin_label['text'] = ' '.join(''.join(i) for i in pinyin(shuru_entry.get()))

def root_left(event):
    if leftKey_flag:
        revious_fun()

def root_right(event):
    if rightKey_flag:
        next_fun()

def root_up(event):
    if upkey_flag:
        yihui_fun()

def root_down(event):
    add_fun()

def pinyin_switch_fun():  # 响应拼音开关复选框事件
    if not e.get():
        pinyin_label['fg'] = "#D4D0C8"   # 底色和主窗口相同，隐藏拼音
    if e.get():
        pinyin_label['fg'] = 'blue'      # 显示出蓝色的拼音


# 放置控件，设置属性，绑定控制函数。注意：运行中需要更改属性的就不要在创建时偷懒同时pack()
pinyin_label = tk.Label(root, fg='blue', text=' '.join(''.join(i) for i in pinyin(study[0])), font=('黑体, 80'))
pinyin_label.pack()
hanzi_label = tk.Label(root, text=study[0], font=('黑体, 195'))
hanzi_label.pack()
index_label = tk.Label(root, text='{}/{}'.format(index+1, NOW_NUM))
index_label.pack()

e = tk.IntVar()  # 检测拼音开关变量
pinyin_switch = tk.Checkbutton(root, variable = e, onvalue = 1, offvalue = 0, text='拼音开关', command=pinyin_switch_fun)
pinyin_switch.pack()
pinyin_switch.select()

e_shuru_entry = tk.StringVar()
shuru_entry = tk.Entry(root, textvariable=e_shuru_entry, font=('黑体', 60))
shuru_entry.pack(side='bottom')
shuru_entry.bind('<Return>', shuru_entry_return)  # 绑定回车键

add_button = tk.Button(root, height=2, width=20, text='不会（加入字库） ∨', command=add_fun)
add_button.pack(padx=120, side='bottom')
revious_button = tk.Button(root, height=5, width=30, text='< 后退', state='disabled', command=revious_fun)
revious_button.pack(padx=108, side='left')
yihui_button = tk.Button(root, height=5, width=20, text='已会（移出字库） ^', command=yihui_fun)
yihui_button.pack(side='left')
next_button = tk.Button(root, height=5, width=30, text='前进 >', command=next_fun)
next_button.pack(padx=108, side='left')

root.bind('<Left>', root_left)
root.bind('<Right>', root_right)
root.bind('<Up>', root_up)
root.bind('<Down>', root_down)


# 主窗口循环
tk.mainloop()
####################### 以上为 GUI 界面，不要更改设置顺序 ######################
