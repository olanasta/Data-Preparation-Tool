from tkinter import ttk
import tkinter as tk
from DataAnalysisFramework.basic_information_report import basic_info_report_generation


class BasicInfoFrame(ttk.Frame):
    def __init__(self, container, data):
        super().__init__(container)
        self.data = data
        self.options_checkbox_list = []
        self.columns_unique_list = []

        self.__create_widgets()

    def __create_widgets(self):
        s = ttk.Style()
        s.configure('.', font=('aerial', 14))

        # select the desired information about dataframe 
        prompt_lbl = ttk.Label(self, text='Select the desired information about dataframe:')
        prompt_lbl.grid(column=0, row=0, columnspan=2, sticky=tk.W)

        # Dimensionality checkbox
        dimension = tk.StringVar()
        dimension_check = ttk.Checkbutton(
            master=self,
            variable=dimension,
            onvalue='dim',
            offvalue='',
            text='Dimensionality of DataFrame')
        dimension_check.grid(column=0, row=1, sticky=tk.W)
        self.options_checkbox_list.append(dimension)

        # Columns' labels checkbox
        columns = tk.StringVar()
        columns_check = ttk.Checkbutton(
            master=self,
            variable=columns,
            onvalue='col',
            offvalue='',
            text='Columns\' Labels of DataFrame')
        columns_check.grid(column=0, row=2, sticky=tk.W)
        self.options_checkbox_list.append(columns)

        # First and Last Rows checkbox
        head_tail = tk.StringVar()
        head_tail_check = ttk.Checkbutton(
            master=self,
            variable=head_tail,
            onvalue='hd',
            offvalue='',
            text='First and Last Rows of DataFrame')
        head_tail_check.grid(column=0, row=3, sticky=tk.W)
        self.options_checkbox_list.append(head_tail)

        # Concise summary checkbox
        con_summary = tk.StringVar()
        con_summary_check = ttk.Checkbutton(
            master=self,
            text='Concise Summary of DataFrame',
            variable=con_summary,
            onvalue='info',
            offvalue='')
        con_summary_check.grid(column=0, row=4, sticky=tk.W)
        self.options_checkbox_list.append(con_summary)

        # Descriptive statistics checkbox
        desc_statistics = tk.StringVar()
        desc_statistics_check = ttk.Checkbutton(
            master=self,
            variable=desc_statistics,
            onvalue='descr',
            offvalue='',
            text='Descriptive Statistics of DataFrame')
        desc_statistics_check.grid(column=0, row=5, sticky=tk.W)
        self.options_checkbox_list.append(desc_statistics)

        # Unique values per column checkbox
        self.unique = tk.StringVar()
        unique_check = ttk.Checkbutton(
            master=self,
            variable=self.unique,
            onvalue='uniq',
            offvalue='',
            text='Unique values per column',
            command=self.on_unique_check)
        unique_check.grid(column=0, row=6, sticky=tk.W)
        self.options_checkbox_list.append(self.unique)

        # Report generation button
        report_btn = ttk.Button(
            master=self,
            text='Generate Report',
            command=self.on_report_generate_click)
        report_btn.grid(column=0, row=7, sticky=tk.W)

        for widget in self.winfo_children():
            widget.grid(padx=25, pady=5)

    def on_report_generate_click(self):
        options_selection = []
        for check in self.options_checkbox_list:
            if check.get():
                options_selection.append(check.get())

        basic_info_report_generation(options_selection, self.columns_unique_list, self.data)

    def on_unique_check(self):
        if self.unique.get():
            columns = self.data.get_columns()
            clen = len(columns)

        self.columns_lstbx = tk.Listbox(self, selectmode=tk.MULTIPLE, width=20, height=10)
        self.columns_lstbx.grid(row=1, column=2, rowspan=6, padx=20)

        # Get the column names from the DataFrame
        column_names = self.data.get_columns().tolist()

        # Insert the column names into the listbox
        for col in column_names:
            self.columns_lstbx.insert(tk.END, col)

        # Bind the event for selection changes
        self.columns_lstbx.bind("<<ListboxSelect>>", self.on_un_columns_select)

    def on_un_columns_select(self, event):
        # Clear the previous selection
        self.columns_unique_list.clear()

        # Get the selected indices
        selected_indices = self.columns_lstbx.curselection()

        # Get the selected column names
        for index in selected_indices:
            self.columns_unique_list.append(self.columns_lstbx.get(index))
