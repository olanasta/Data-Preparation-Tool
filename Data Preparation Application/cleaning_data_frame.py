from DataAnalysisFramework.data_frame_handler import DataFrameHandler
from tkinter import ttk
import tkinter as tk


class CleaningDataFrame(ttk.Frame):
    def __init__(self, container, data, btn_clicked, duplicates=0):
        super().__init__(container)

        self.data = data
        self.btn = btn_clicked
        self.duplicates = duplicates

        self.__create_widgets()

    def __create_widgets(self):
        s = ttk.Style()
        s.configure('.', font=('Arial', 14))  # Corrected font name from 'aerial' to 'Arial'

        columns_list = self.data.get_columns().to_list()
        self.selected_column = tk.StringVar()

        if self.btn == 'Remove Duplicates':
            self.data.remove_duplicates()
            label_text = f'In the process, {self.duplicates} duplicate entries \n' \
                         f'were identified and subsequently removed from the DataFrame'
            duplicates_info_lbl = ttk.Label(self, text=label_text)
            duplicates_info_lbl.grid(column=0, row=0, sticky=tk.W, padx=25, pady=5)
        elif self.btn == 'Remove Columns':
            label_text = 'Identify and exclude unnecessary columns from the DataFrame, effectively \n' \
                         'refining the dataset by removing the columns that are not essential for \n' \
                         'the analysis or task at hand.'
            prompt_lbl = ttk.Label(self, text=label_text)
            prompt_lbl.grid(columnspan=2, row=0, sticky=tk.W, padx=25, pady=5)

            self.dropdown = ttk.Combobox(self, textvariable=self.selected_column, values=columns_list)
            self.dropdown.grid(row=1, column=0, padx=10, pady=10)

            self.dropdown.set("Select a column")

            self.dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_select)

            self.remove_column_btn = ttk.Button(self, text='Remove column', command=self.on_remove_column_click,
                                                state='disabled',  # Setting initial state to disabled
                                                width=30)
            self.remove_column_btn.grid(column=1, row=1, pady=15, padx=15)

    def update_columns_list(self):
        columns_list = self.data.get_columns().to_list()
        self.dropdown['values'] = columns_list
        self.dropdown.set("Select a column")

    def on_dropdown_select(self, event):
        self.remove_column_btn['state'] = 'enabled'

    def on_remove_column_click(self):
        selected_value = self.selected_column.get()
        self.data.drop_column(selected_value)
        self.update_columns_list()

