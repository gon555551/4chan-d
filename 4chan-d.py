import tkinter as tk
from tkinter import filedialog
import threading
import os
import bs4, requests


class App:
    def __init__(self):
        # Basic initialization

        self.root = tk.Tk()
        self.root.wm_resizable(width=False, height=False)
        self.root.title("4chan-d")
        self.root.iconphoto(
            True, tk.PhotoImage(file="4chan.png")
        )

        self.counter = 0
        self.item_number = 0
        self.threads = []

        self.thread_link = tk.StringVar()
        self.output_path = tk.StringVar()
        self.downloading = tk.StringVar()
        self.downloading.set("Enter a thread link")

        self.mainframe = tk.Frame(self.root)
        self.mainframe.grid(column=0, row=0)

        self.setup_widgets()

        self.root.mainloop()

    def setup_widgets(self):
        # Setup the widgets
        tk.Label(
            self.mainframe, text="Thread", padx=5, pady=5, height=1, font="Consolas"
        ).grid(column=0, row=0, sticky="nesw")
        tk.Button(
            self.mainframe,
            text="Output 📂",
            height=1,
            command=self.get_output,
            font="Consolas",
        ).grid(column=0, row=1, sticky="nesw")
        tk.Label(
            self.mainframe,
            textvariable=self.downloading,
            padx=5,
            pady=5,
            font="Consolas",
            height=1,
        ).grid(column=1, row=2, sticky="nesw")

        thread_entry = tk.Entry(
            self.mainframe, textvariable=self.thread_link, width=50, font="Consolas"
        )
        thread_entry.grid(column=1, row=0, sticky="nesw")
        thread_entry.focus()
        tk.Entry(
            self.mainframe, textvariable=self.output_path, width=50, font="Consolas"
        ).grid(column=1, row=1, sticky="nesw")

        tk.Button(
            self.mainframe,
            text="Download",
            height=1,
            command=self.download,
            font="Consolas",
        ).grid(column=0, row=2, sticky="nesw")

    def get_output(self):
        # Set the output path using filedialog
        self.output_path.set(filedialog.askdirectory(title="Select Output Directory"))

    def treat_output(self, output: str) -> str:
        # Treat the output string
        if output == "":
            output = os.path.join(os.path.expanduser("~"), "4chan-d")

        if not os.path.isdir(output):
            os.makedirs(output)

        if output[-1] != "\\":
            output += "\\"

        return output

    def get_links(self, thread: str) -> list[str]:
        # Get the links from the HTML
        links = bs4.BeautifulSoup(requests.get(thread).content, "html.parser").find_all(
            "div", {"class": "fileText"}
        )
        for i in range(links.__len__()):
            links[i] = f"https:{links[i].a['href']}"

        return links

    def download_worker(self, link: str, output: str):
        # The file worker thread
        with open(output + link.split("/")[-1], "wb") as result:
            result.write(requests.get(link).content)

        self.counter += 1

    def write_to_gui(self):
        # Download progress update function
        while sum([t.is_alive() for t in self.threads]):
            ten_ratio = round((self.counter) * 10 / self.item_number)
            self.downloading.set(
                f"Downloading: {'#' * ten_ratio}{'-' * (10 - ten_ratio)} ({self.counter}/{self.item_number})"
            )
        self.downloading.set(f"Completed!! ({self.counter}/{self.item_number})")
        self.threads = []
        self.counter = 0
        self.item_number = 0

    def download(self):
        # Download media
        thread = self.thread_link.get()
        output = self.treat_output(self.output_path.get())

        links = self.get_links(thread)

        self.item_number = links.__len__()

        for link in links:
            self.threads.append(
                threading.Thread(target=self.download_worker, args=(link, output))
            )

        for worker in self.threads:
            worker.start()

        threading.Thread(target=self.write_to_gui).start()


app = App()
