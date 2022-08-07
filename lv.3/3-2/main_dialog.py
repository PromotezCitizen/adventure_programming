from codec import HuffmanCodec
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
        self._window_width = 600
        self._window_height = 400
        self._margin = 30
        self._main_frame = None
        self._filename = None
        None

    def run(self):
        self._makeMainWindow()
        self._makeMainFrame()
        self._configureMainFrame()

        self._window.mainloop()

    def _makeMainWindow(self):
        self._window = Tk()
        self._window.title('Huffman 부호화')
        self._window.geometry("{0}x{1}+1000+300".format(self._window_width, self._window_height))
        self._window.resizable(False, False)

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