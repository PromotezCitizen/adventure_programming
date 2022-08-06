from codec import HuffmanCodec
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
import multiprocessing as mp

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
        self._margin = 30
        self._filename = None
        None

    def run(self):
        self._window.title('Huffman 부호화')
        self._window.geometry("{0}x{1}+1000+300".format(self._window_width, self._window_height))
        self._window.resizable(False, False)
        self._makeMainFrame()

        main_frame = Frame(
            self._window,
            relief='solid',
            bd=5,
            width=self._window_width-self._margin*2,
            height=self._window_height-self._margin*2
        )
        main_frame.pack()

        self._configureMainFrame(main_frame)

        self._window.mainloop()

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

    def _configureMainFrame(self, window):
        before_label = Label(window, text="before")
        before_label.grid(column=0, row=0, sticky='wn', ipadx=5, pady=5)

        after_label = Label(window, text="after")
        after_label.grid(column=0, row=1, sticky='w', ipadx=5, pady=5)

        # https://www.geeksforgeeks.org/tkinter-read-only-entry-widget/
        # readonly entry
        # before_filename = Entry(window, width=30, state=DISABLED)
        self._before_filename = Label(window, width=50)
        self._before_filename.grid(column=1, row=0, padx=10, pady=5, sticky='n')

        # after_filename = Entry(window, width=30, state=DISABLED)
        self._after_filename = Label(window, width=50)
        self._after_filename.grid(column=1, row=1, padx=10, pady=5, sticky='')

        self._load_btn = Button(window, text="load", command=self._loadFile)
        self._load_btn.grid(column=2, row=0, padx=10, pady=5, sticky='en')

        self._save_btn = Button(window, text="save", state=DISABLED, command=self._saveConvertedFile)
        self._save_btn.grid(column=2, row=1, padx=10, pady=5, sticky='e')

        self._convert_btn = Button(window, text="convert", state=DISABLED, command=self._convertFile)
        self._convert_btn.grid(column=2, row=2, padx=10, pady=5, sticky='es')

        self._status = Label(window, width=60)
        self._status.grid(column=0, row=2, columnspan=2, sticky='s')

        self._before_filename.configure(text="origin_file_name")
        self._after_filename.configure(text="converted_file_name")
        self._status.configure(text="None")

    def _loadFile(self):
        self._filename = filedialog.askopenfilename(initialdir="", title="Select file",
                                                filetypes=(("all files", "*.*"),))
                                # filetypes는 단 하나만 쓰더라도 ,(콤마) 필수
        print(self._filename)
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

        print(self._filename)
        if self._filename != '' and self._filename != None:
            self._filename += '.huf' if self._codec is self._codec.isEncoder() else ""
            self._filename = self._codec.save(self._filename)
            self._after_filename.configure(text=self._filename+"(save end)")
            self._save_btn.configure(state=DISABLED)
            # self._convert_btn.configure(state=DISABLED)

# codec = HuffmanCodec()
# window = Tk()
# window_width = 600
# window_height = 400

# margin=30
# window.title('Huffman 부호화')
# window.geometry("{0}x{1}+1000+300".format(window_width, window_height))
# window.resizable(False, False)



# def makeMainFrame(window, width, height, margin):
#     top_frame = Frame(
#         window,
#         relief='solid',
#         bd=2,
#         width=width,
#         height=margin
#     )
#     top_frame.pack(side='top')

#     bottom_frame = Frame(
#         window,
#         relief='solid',
#         bd=2,
#         width=width,
#         height=margin
#     )
#     bottom_frame.pack(side='bottom')

#     left_frame = Frame(
#         window,
#         relief='solid',
#         bd=2,
#         width=margin,
#         height=height-margin*2
#     )
#     left_frame.pack(side='left')

#     right_frame = Frame(
#         window,
#         relief='solid',
#         bd=2,
#         width=margin,
#         height=height-margin*2
#     )
#     right_frame.pack(side='right')

# def configureMainFrame(window):
#     before_label = Label(window, text="before")
#     before_label.grid(column=0, row=0, sticky='wn', ipadx=5, pady=5)

#     after_label = Label(window, text="after")
#     after_label.grid(column=0, row=1, sticky='w', ipadx=5, pady=5)

#     # https://www.geeksforgeeks.org/tkinter-read-only-entry-widget/
#     # readonly entry
#     # before_filename = Entry(window, width=30, state=DISABLED)
#     before_filename = Label(window, width=30)
#     before_filename.grid(column=1, row=0, padx=10, pady=5, sticky='n')

#     # after_filename = Entry(window, width=30, state=DISABLED)
#     after_filename = Label(window, width=30)
#     after_filename.grid(column=1, row=1, padx=10, pady=5, sticky='')

#     load_btn = Button(window, text="load")
#     load_btn.grid(column=2, row=0, padx=10, pady=5, sticky='en')

#     save_btn = Button(window, text="save")
#     save_btn.grid(column=2, row=1, padx=10, pady=5, sticky='e')

#     isencoded = Label(window, width=60)
#     isencoded.grid(column=0, row=2, columnspan=3, sticky='s')


#     before_filename.configure(text="origin_file_name")
#     after_filename.configure(text="converted_file_name")
#     isencoded.configure(text="asdf")

# makeMainFrame(window, window_width, window_height, margin)

# main_frame = Frame(
#     window,
#     relief='solid',
#     bd=2,
#     width=window_width-margin*2,
#     height=window_height-margin*2
# )

# main_frame.pack()
# configureMainFrame(main_frame)

# before_label = Label(main_frame, text="before")
# before_label.grid(column=0, row=0, sticky='wn', ipadx=5, pady=5)

# after_label = Label(main_frame, text="after")
# after_label.grid(column=0, row=1, sticky='w', ipadx=5, pady=5)

# # https://www.geeksforgeeks.org/tkinter-read-only-entry-widget/
# # readonly entry
# # before_filename = Entry(main_frame, width=30, state=DISABLED)
# before_filename = Label(main_frame, width=30)
# before_filename.grid(column=1, row=0, padx=10, pady=5, sticky='n')

# # after_filename = Entry(main_frame, width=30, state=DISABLED)
# after_filename = Label(main_frame, width=30)
# after_filename.grid(column=1, row=1, padx=10, pady=5, sticky='')

# load_btn = Button(main_frame, text="load")
# load_btn.grid(column=2, row=0, padx=10, pady=5, sticky='en')

# save_btn = Button(main_frame, text="save")
# save_btn.grid(column=2, row=1, padx=10, pady=5, sticky='e')

# isencoded = Label(main_frame, width=60)
# isencoded.grid(column=0, row=2, columnspan=3, sticky='s')


# before_filename.configure(text="origin_file_name")
# after_filename.configure(text="converted_file_name")
# isencoded.configure(text="asdf")

# window.mainloop()

import os

print(mp.current_process().name, __name__)

if __name__ == "__main__":
    mp.freeze_support()
    # https://github.com/pyinstaller/pyinstaller/issues/3957#issuecomment-674579877
    # Pyinstaller multiprocessing name of process is always "MainProcess" 해결
    if 'main_started' not in os.environ:
        os.environ['main_started'] = ''
        GUI().run()
        os.system('pause')

# pyinstaller --onefile gui.py