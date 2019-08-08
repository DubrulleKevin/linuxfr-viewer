from tkinter import *
from tkinter import messagebox
import api


class NewsWindow(Toplevel):
    def __init__(self, master, news):
        Toplevel.__init__(self, master)
        self.title(news['name'])
        article_text = Text(self)
        article_text.config(foreground='white', background='black')
        article_text.config(font=("Consolas", 14))
        article_text.insert(END, news['article'])
        article_text.insert(END, '\n\n')
        for comment in news['comments']:
            article_text.insert(END, '\n\n========================================\n')
            article_text.insert(END, 'Title: {}\n'.format(comment['title']))
            article_text.insert(END, 'Author: {}\n'.format(comment['author']))
            article_text.insert(END, 'Note: {}\n\n'.format(comment['note']))
            article_text.insert(END, comment['content'])
        article_text.config(state=DISABLED)
        article_text.bind('<Escape>', lambda x: self.destroy())
        article_text.pack(side=LEFT, fill=BOTH, expand=TRUE)
        article_text.focus_set()
        scroll = Scrollbar(self)
        scroll.pack(side=RIGHT, fill=Y)
        scroll.config(command=article_text.yview)
        article_text.config(yscrollcommand=scroll.set)
        

class ClientTk(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('LinuxFR viewer')
        self._news_list = Listbox(self, width=120, height=30)
        self._news_list.config(foreground='white', background='black')
        self._news_list.config(font=("Consolas", 14))
        self._news_list.bind('<Double-1>', lambda x: self._open_news(self._news_list.selection_get()))
        self._news_list.bind('<Return>', lambda x: self._open_news(self._news_list.selection_get()))
        self._news_list.bind('<Left>', lambda x: self._prev_page())
        self._news_list.bind('<Right>', lambda x: self._next_page())
        self._news_list.pack(side=TOP, fill=BOTH, expand=TRUE)
        self._news_list.focus_set()
        self._current_page = 1
        self._fill_news_list_from_page()
        self._prev_btn = Button(text='Previous', command=self._prev_page)
        self._prev_btn.pack(side=LEFT, padx=5, pady=5)
        self._next_btn = Button(text='Next', command=self._next_page)
        self._next_btn.pack(side=RIGHT, padx=5, pady=5)
        self._page_number_label_text = StringVar()
        self._page_number_label_text.set('Page: {}'.format(self._current_page))
        self._page_number_label = Label(textvariable=self._page_number_label_text)
        self._page_number_label.pack(side=BOTTOM)

    def _open_news(self, news_title):
        news_number = -1
        i = 0
        for news in api.get_news_on_page(self._current_page):
            if news['title'] == news_title:
                news_number = i
            i = i + 1
        try:
            NewsWindow(self, api.get_news_content(self._current_page, news_number))
        except Exception as e:
            messagebox.showerror('Error', 'A error occured while getting news content:\n\n{}'.format(e))

    def _prev_page(self):
        if self._current_page > 1:
            self._current_page = self._current_page - 1
            self._page_number_label_text.set('Page: {}'.format(self._current_page))
            self._fill_news_list_from_page()

    def _next_page(self):
        self._current_page = self._current_page + 1
        self._page_number_label_text.set('Page: {}'.format(self._current_page))
        self._fill_news_list_from_page()

    def _fill_news_list_from_page(self):
        self._news_list.delete(0, END)
        for news in api.get_news_on_page(self._current_page):
            self._news_list.insert(END, news['title'])
