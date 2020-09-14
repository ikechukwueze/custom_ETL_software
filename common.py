

import easygui
import pandas as pd
import numpy as np
from tkinter import filedialog


def browseFile(title="Select a file"):

	excel_filetypes = ("Excel files", "*.xlsx; *.xls; *.csv")
	all_filetypes = ("all files", "*.*")
	#title = "Select a file"

	filename = filedialog.askopenfilename(title = title, filetypes = (excel_filetypes, all_filetypes))
	if filename:
		return filename
