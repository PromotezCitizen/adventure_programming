from codec import HuffmanCodec
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog

# https://appia.tistory.com/111
# 파일 다이얼로그

# https://076923.github.io/posts/Python-tkinter-10/
# tkinter 사용법

# https://scribblinganything.tistory.com/294
# pack으로 조정해보자!

# https://runestone.academy/ns/books/published/thinkcspy/GUIandEventDrivenProgramming/02_standard_dialog_boxes.html
# python standard dialog

class GUI():
    def __init__(self):
        self._codec = HuffmanCodec()
        self._window = Tk()
        self._window_width = 600
        self._window_height = 400
        self._window_pos_x = (self._window.winfo_screenwidth() - self._window_width) // 2
        self._window_pos_y = (self._window.winfo_screenheight() - self._window_height) // 2
        self._margin = 30

    def run(self):
        self._makeMainWindow()

        self._makeMenubar()
        self._makeMainFrame()
        self._configureMainFrame()

        self._window.mainloop()

    def _makeMainWindow(self):
        self._window.title('Huffman 부호화')
        self._window.geometry("{0}x{1}+{2}+{3}".format(self._window_width, self._window_height, self._window_pos_x, self._window_pos_y))
        self._window.resizable(False, False)

    # https://simplecodingschool.tistory.com/entry/Python-Tkinter-%EB%A9%94%EB%89%B4menu-%EB%A7%8C%EB%93%A4%EA%B8%B0
    # 메뉴바 생성
    def _makeMenubar(self):
        menubar = Menu(self._window)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=self._createAboutDialog)

        menubar.add_cascade(label="Help", menu=helpmenu)

        self._window.config(menu=menubar)

    # https://memories.tistory.com/68
    # 다이얼로그 modal으로 생성
    def _createAboutDialog(self):
        sub = tkinter.Toplevel(self._window)

        sub.resizable(False, False)
        sub.title('About')
        sub.attributes('-topmost', 'true')

        label_use_data = [
            '사용법', 
            '1. load를 눌러 파일 불러오기', 
            '\tsave 버튼이 활성화되어있다면 save 버튼 비활성화', 
            '\t1.1 파일을 불러온 경우 convert 버튼 활성화', 
            '\t1.2 파일을 불러오지 못한 경우 convert 버튼 비활성화 유지', 
            '2. 1.1이 성공한 경우 convert 버튼 클릭', 
            '\t이 경우 다시 변환하는 과정을 거치지 않도록 convert 버튼 비활성화', 
            '\tsave 버튼 활성화', 
            '3. save 버튼이 활성화되면 save 버튼 클릭', 
            '\t3.1 저장이 된 경우 다시 저장하지 않도록 save 버튼 비활성화', 
            '\t3.2 취소 버튼을 눌러서 저장을 하지 않은 경우에는 save 버튼 활성화 유지', 
            '\n', 
            'load 버튼은 언제든 누를 수 있다', 
            '부호화된 파일인지 부호화되지 않은 파일인지 자동으로 확인', 
            '\n',
        ]
        for data in label_use_data:
            label_use = Label(sub)
            label_use.configure(text=data, anchor=W)
            label_use.pack(side="top", fill=X)

        label_footer_data = [
            '해당 창은 MODAL 방식으로 되어있습니다', 
            'by PromotezCitizen'
        ]
        for data in list(reversed(label_footer_data)):
            label_footer = Label(sub)
            label_footer.configure(text=data)
            label_footer.pack(side="bottom", fill=None)
        
        win_width = self._window_pos_x + (sub.winfo_screenmmwidth() - self._window_width)
        win_height = self._window_pos_y
        sub.geometry("+{0}+{1}".format(win_width, win_height))
        sub.grab_set()

    def _makeMainFrame(self):
        top_frame = Frame(
            self._window,
            relief='solid',
            bd=2,
            width=self._window_width,
            height=self._margin
        )
        top_frame.pack(side='top')

        bottom_frame = Frame(
            self._window,
            relief='solid',
            bd=2,
            width=self._window_width,
            height=self._margin
        )
        bottom_frame.pack(side='bottom')

        left_frame = Frame(
            self._window,
            relief='solid',
            bd=2,
            width=self._margin,
            height=self._window_height-self._margin*2
        )
        left_frame.pack(side='left')

        right_frame = Frame(
            self._window,
            relief='solid',
            bd=2,
            width=self._margin,
            height=self._window_height-self._margin*2
        )
        right_frame.pack(side='right')

        self._main_frame = Frame(
            self._window,
            relief='solid',
            bd=5,
            width=self._window_width-self._margin*2,
            height=self._window_height-self._margin*2
        )
        self._main_frame.pack()

    def _configureMainFrame(self):
        before_label = Label(self._main_frame, text="before")
        before_label.grid(column=0, row=0, sticky='wn', ipadx=5, pady=5)

        after_label = Label(self._main_frame, text="after")
        after_label.grid(column=0, row=1, sticky='w', ipadx=5, pady=5)

        # https://www.geeksforgeeks.org/tkinter-read-only-entry-widget/
        # readonly entry
        # before_filename = Entry(self._main_frame, width=30, state=DISABLED)
        self._before_filename = Label(self._main_frame, width=50)
        self._before_filename.grid(column=1, row=0, padx=10, pady=5, sticky='n')

        # after_filename = Entry(self._main_frame, width=30, state=DISABLED)
        self._after_filename = Label(self._main_frame, width=50)
        self._after_filename.grid(column=1, row=1, padx=10, pady=5, sticky='')

        self._load_btn = Button(self._main_frame, text="load", command=self._loadFile)
        self._load_btn.grid(column=2, row=0, padx=10, pady=5, sticky='en')

        self._save_btn = Button(self._main_frame, text="save", state=DISABLED, command=self._saveConvertedFile)
        self._save_btn.grid(column=2, row=1, padx=10, pady=5, sticky='e')

        self._convert_btn = Button(self._main_frame, text="convert", state=DISABLED, command=self._convertFile)
        self._convert_btn.grid(column=2, row=2, padx=10, pady=5, sticky='es')

        self._status = Label(self._main_frame, width=60)
        self._status.grid(column=0, row=2, columnspan=2, sticky='s')

        self._before_filename.configure(text="origin_file_name")
        self._after_filename.configure(text="converted_file_name")
        self._status.configure(text="None")

    def _loadFile(self):
        self._filename = filedialog.askopenfilename(initialdir="", title="Select file",
                                                filetypes=(("all files", "*.*"),))
                                # filetypes는 단 하나만 쓰더라도 ,(콤마) 필수
        if self._filename != '':
            self._before_filename.configure(text=self._filename)
            self._after_filename.configure(text="None")
            self._status.configure(text=("Encoded File" if self._codec.isEncoded(self._filename) else "Not Encoded File"))
            self._convert_btn.configure(state=NORMAL)
            self._save_btn.configure(state=DISABLED)

    def _convertFile(self):
        self._save_btn.configure(state=NORMAL)
        self._convert_btn.configure(state=DISABLED)
        self._codec.run(self._filename)

    def _saveConvertedFile(self):
        self._filename = simpledialog.askstring("Input", "저장할 파일의 이름을 적어주세요.\n확장자는 자동으로 생성됩니다.",
                        parent=self._window)

        if self._filename != '' and self._filename != None:
            self._filename += '.huf' if self._codec is self._codec.isEncoder() else ""
            self._filename = self._codec.save(self._filename)
            self._after_filename.configure(text=self._filename+"(save end)")
            self._save_btn.configure(state=DISABLED)

            self._status.configure(text=("{0} file saved".format('encoded' if self._codec.isEncoder() else 'decoded')))