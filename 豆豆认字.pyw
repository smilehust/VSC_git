import codecs
import win32com.client  # 文字转语音
import tkinter as tk
from pypinyin import pinyin, lazy_pinyin  # 这个支持多音字

NUM         = 50      # 每次学习的字词数
root_width  = 1024    # 设置主窗口尺寸，最好是1024x768
root_height = 768
dangqian = set()
yihui    = set()
total    = set()

# 全部学会“A正在学字库.txt”后清空这个文件，就能自动调入新的50个了
with codecs.open('字库文件\A正在学字库.txt', 'r+', 'utf-8') as f_d,\
     codecs.open('字库文件\C总字库.txt', 'r', 'utf-8') as f_t,\
     codecs.open('字库文件\B已会字库.txt', 'r', 'utf-8') as f_y:  
    for line in f_d:
        a = line.strip('\n').strip('\r')
        dangqian.add(a)
    for line in f_t:
        a = line.strip('\n').strip('\r')
        total.add(a)
    for line in f_y:
        a = line.strip('\n').strip('\r')
        yihui.add(a)
    study = total - yihui
    study.discard('')   # 删除集合中空元素，如果不存在，忽略
    if not dangqian:    # 如果A正在学字库是空的，则全新写入NUM个进去，此处用r+和a+一样效果
        dangqian = set(list(study)[:NUM])
        for line in dangqian:
            f_d.write(line + '\n')
        study = dangqian
    else:
        study = dangqian - yihui
    study = list(study)      # 生成按顺序学习的列表

class Mysdudy():
    index = 0    
  
pinyin('预加载')  # 提前加载一次库，提高用户体验
####################### 以下为 GUI 界面，不要更改设置顺序 ######################
# 设置主窗口
root = tk.Tk()
root.title('豆豆认字')
# 设置主窗口居中
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
sw = int((sw-root_width)/2)
sh = int((sh-root_height)/2)
root.geometry('{}x{}+{}+{}'.format(root_width, root_height, sw, sh))  
root.iconbitmap('字库文件\豆豆.ico')  # 窗口图标
root.resizable(0,0)                 # 禁止主窗口调整大小

# 定义控制函数
def revious_fun():
    try:
        Mysdudy.index -= 1
        _renzi = study[Mysdudy.index]
        hanzi_label['text']  = _renzi
        pinyin_label['text'] = ' '.join(''.join(i) for i in pinyin(_renzi))
    except IndexError:
        Mysdudy.index += 1
        hanzi_label['text']  = '|<---'
        pinyin_label['text'] = ''    

def yihui_fun():
    with codecs.open('字库文件\B已会字库.txt', 'a', 'utf-8') as f:
        try:
            f.write('\n' + study[Mysdudy.index])
            del study[Mysdudy.index]
            hanzi_label['text']  = study[Mysdudy.index]
            pinyin_label['text'] = ' '.join(''.join(i) for i in pinyin(study[Mysdudy.index]))
        except IndexError:
            pass
    
def next_fun():
    try:
        Mysdudy.index += 1
        _renzi = study[Mysdudy.index]        
        hanzi_label['text']  = _renzi
        pinyin_label['text'] = ' '.join(''.join(i) for i in pinyin(_renzi))        
    except IndexError:
        Mysdudy.index -= 1
        hanzi_label['text']  = '--->|'
        pinyin_label['text'] = ''

def pinyin_fun():
    hanzi_label['text']  = shuru_entry.get()
    pinyin_label['text'] = ' '.join(''.join(i) for i in pinyin(shuru_entry.get()))

def add_fun():
    with codecs.open('字库文件\A正在学字库.txt', 'a', 'utf-8') as f_d,\
        codecs.open('字库文件\C总字库.txt', 'a', 'utf-8') as f_t:
        f_d.write('\n' + shuru_entry.get())
        f_t.write('\n' + shuru_entry.get())
        
def shuru_entry_return(event):
    pinyin_fun()

def root_left(event):
    revious_fun()

def root_right(event):
    next_fun()

def speech_fun():
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(study[Mysdudy.index])
    # speech.say(study[Mysdudy.index])

# 放置控件，设置属性，绑定控制函数。注意：运行中需要更改属性的就不要在创建时偷懒同时pack()
pinyin_label = tk.Label(root, fg='blue', font = ('黑体, 80'))
pinyin_label.pack()  
hanzi_label = tk.Label(root, text='点击开始',font = ('黑体, 195'))
hanzi_label.pack()

shuru_entry = tk.Entry(root, font = ('黑体', 60))
shuru_entry.pack(side='bottom')
shuru_entry.bind('<Return>', shuru_entry_return)  # 绑定回车键
pinyin_button = tk.Button(root, height=2, width=20, text='显示拼音', command=pinyin_fun)
pinyin_button.pack(padx=120, side='bottom')  
add_button = tk.Button(root, height=2, width=20, text='加入字库', command=add_fun)
add_button.pack(padx=120, side='bottom')  
speech_button = tk.Button(root, height=2, width=20, text='语音播放(beta)', command=speech_fun)
speech_button.pack(padx=120, side='bottom')  

revious_button = tk.Button(root, height=5, width=30, text='<---后退', command=revious_fun)
revious_button.pack(padx=108, side='left')    
yihui_button = tk.Button(root, height=5, width=20, text='已会', bg='light blue', command=yihui_fun)
yihui_button.pack(side='left')
next_button = tk.Button(root, height=5, width=30,  text='前进--->', command=next_fun)
next_button.pack(padx=108, side='left')

root.bind('<Left>', root_left)
root.bind('<Right>', root_right)

# 主窗口循环
tk.mainloop()
####################### 以上为 GUI 界面，不要更改设置顺序 ######################

