import tkinter as tk
from tkinter import filedialog
import os
import bs4, requests


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_resizable(width=False, height=False)
        self.root.title("4chan-d")
        self.root.iconphoto(True, tk.PhotoImage(file="C:\\Users\\gonve\\Code\\4chan-d\\4chan.png"))

        self.thread_link = tk.StringVar()
        self.output_path = tk.StringVar()
        self.downloading = tk.StringVar()

        self.mainframe = tk.Frame(self.root)
        self.mainframe.grid(column=0, row=0)

        self.setup_widgets()

        self.root.mainloop()

    def setup_widgets(self):
        tk.Label(self.mainframe, text="Thread", padx=5, pady=5, height=1).grid(column=0, row=0)
        tk.Button(self.mainframe, text="Output 📂", padx=5, pady=5, command=self.get_output).grid(column=0, row=1)
        tk.Label(self.mainframe, textvariable=self.downloading, padx=5, pady=5).grid(column=3, row=2)
        
        tk.Entry(self.mainframe, textvariable=self.thread_link, width=50).grid(column=1, row=0)
        tk.Entry(self.mainframe, textvariable=self.output_path, width=50).grid(column=1, row=1)

        tk.Button(self.mainframe, text="Download", padx=5, pady=5, command=self.download, anchor="e").grid(column=0, row=2)

    def get_output(self):
        self.output_path.set(filedialog.askdirectory(title="Select output directory"))

    def treat_output(self, output: str) -> str:
        if output == "":
            output = os.path.join(os.path.expanduser("~"), "4chan-d")

        if not os.path.isdir(output):
            os.makedirs(output)

        if output[-1] != "\\":
            output += "\\"

        return output
    
    def get_links(self, thread: str) -> list[str]:
        links = bs4.BeautifulSoup(requests.get(thread).content, "html.parser").find_all(
            "div", {"class": "fileText"}
        )
        for i in range(links.__len__()):
            links[i] = f"https:{links[i].a['href']}"

        return links

    def download(self):
        thread = self.thread_link.get()
        output = self.treat_output(self.output_path.get())

        links = self.get_links(thread)

        item_number = links.__len__()
        counter = 1

        for link in links:
            with open(output+link.split("/")[-1], "wb") as result:
                result.write(requests.get(link).content)
            counter += 1

        self.downloading.set("Completed")     

app = App()
