from tkinter import ttk
import tkinter as tk
from DataAnalysisFramework.data_frame_handler import DataFrameHandler


class TransformingDataFrame(ttk.Frame):
    def __init__(self, container, data, btn_clicked):
        super().__init__(container)

        self.data = data
        self.btn = btn_clicked
        self.columns = self.data.get_columns().to_list()
        self.data_types = ["int64", "float64", "object", "datetime64", "bool"]
        self.selected_column = tk.StringVar()
        self.columns_list = self.data.get_columns().to_list()

        # Create Combobox for column selection
        self.columns_cbox = ttk.Combobox(self, textvariable=self.selected_column, values=self.columns_list, width=30)
        self.columns_cbox.bind("<<ComboboxSelected>>", self.on_columns_cbox_select)

        self.__create_widgets()

    def __create_grid(self):
        # Create treeview
        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("Type", "Sample Data")

        # Add columns
        self.tree.heading("#0", text="Column")
        self.tree.column("#0", anchor="w", width=200)
        self.tree.heading("Type", text="Type")
        self.tree.column("Type", anchor="w", width=200)
        self.tree.heading("Sample Data", text="Sample Data")
        self.tree.column("Sample Data", anchor="w", width=300)

        # Populate treeview with DataFrame information
        for column in self.columns:
            column_type = self.data.get_column_type(column)
            sample_data = self.data.get_column_sample_data(column)
            self.tree.insert("", "end", text=column, values=(column_type, sample_data))

        self.tree.grid(columnspan=3, row=1, sticky=tk.W, padx=25, pady=5)

    def __create_widgets(self):
        s = ttk.Style()
        s.configure('.', font=('Arial', 14))

        if self.btn == 'Convert Column Type':
            self.update_column_type_frame(self.columns_list)
        elif self.btn == 'Replace Missing Values':
            self.update_filling_frame(self.columns_list)
        elif self.btn == 'Text Adjustments':
            self.update_text_adj_frame(self.columns_list)
        elif self.btn == 'Remove Rows':
            self.update_rows_with_null_frame(self.columns_list)
        elif self.btn == 'Remove Columns':
            self.update_columns_with_null_frame(self.columns_list)
        elif self.btn == 'Conditional Replace':
            self.update_conditional_replace_frame()

    def update_rows_with_null_frame(self, columns_list):
        total_null_count = self.data.sum_of_null_values()
        if total_null_count != 0:
            label_text = 'Select the column with null values and then filter the DataFrame ' \
                         'to exclude all rows where that \nspecific column has null values'
            prompt_lbl = ttk.Label(self, text=label_text)
            prompt_lbl.grid(row=0, columnspan=3, padx=25, pady=5)

            self.columns_cbox.grid(row=1, column=0, padx=25, pady=10)

            # Set a default value
            self.columns_cbox.set("Select a column")

            self.remove_rows_btn = ttk.Button(self, text='Remove Rows with Null Values',
                                              command=self.on_remove_rows_click,
                                              state='disabled',
                                              width=40)
            self.remove_rows_btn.grid(row=1, column=1, pady=15, padx=25)
        else:
            label_text = 'There are 0 null values in dataframe.'
            info_lbl = ttk.Label(self, text=label_text)
            info_lbl.grid(row=0, column=0, padx=25, pady=10)

    def update_columns_with_null_frame(self, columns_list):
        # Create Treeview with 2 columns
        self.tree = ttk.Treeview(self, columns=('Column', 'Number of Nulls', '% of Nulls'), show='headings')
        self.tree.heading('Column', text='Column')
        self.tree.heading('Number of Nulls', text='Number of Nulls')
        self.tree.heading('% of Nulls', text='% of Nulls')

        total_null_count = self.data.sum_of_null_values()
        if total_null_count != 0:
            # Insert data into the treeview
            for col in columns_list:
                null_count = self.data.sum_of_null_values_by_column(col)
                records_count = self.data.get_num_of_entries_columns()[0]
                if null_count != 0:
                    perc = float((null_count * 100) / records_count)
                    perc_str = "{:.2f} %".format(perc)
                    self.tree.insert('', 'end', values=(col, null_count, perc_str))
                    self.tree.grid(row=0, column=0)
        else:
            label_text = 'There are 0 null values in dataframe.'
            info_lbl = ttk.Label(self, text=label_text)
            info_lbl.grid(row=0, column=0, padx=25, pady=10)

    def update_conditional_replace_frame(self):
        label_text = 'Implement a feature for conditional text replacement to rectify inaccuracies,\n ' \
                     'incorrect entries, and inconsistencies within the dataset. This functionality \n' \
                     'enables targeted modifications based on predefined conditions, allowing for \n' \
                     'precise adjustments to ensure data accuracy and consistency.'
        prompt_lbl = ttk.Label(self, text=label_text)
        prompt_lbl.grid(row=0, columnspan=3, padx=25, pady=5)

        column_select_lbl = ttk.Label(self, text='Select a column')
        column_select_lbl.grid(row=2, column=0, padx=25, pady=5, sticky=tk.W)

        self.columns_cbox.grid(row=2, column=1, padx=10, pady=10)
        # Set a default value
        self.columns_cbox.set("Select a column")

    def update_columns_list(self):
        columns_list = self.data.get_columns().to_list()
        self.columns_cbox['values'] = self.columns_list
        self.columns_cbox.set("Select a column")

    def on_columns_cbox_select(self, event):
        selected_value = self.selected_column.get()
        if self.btn == 'Remove Columns':
            self.remove_column_btn['state'] = 'enabled'
        elif self.btn == 'Remove Rows':
            null_sum_by_column = self.data.sum_of_null_values_by_column(selected_value)
            if null_sum_by_column != 0:
                self.remove_rows_btn['state'] = 'enabled'
            else:
                label_text = 'There are 0 null values in the selected column.'
                info_lbl = ttk.Label(self, text=label_text)
                info_lbl.grid(row=2, columnspan=2, padx=25, pady=10, sticky=tk.NSEW)
        elif self.btn == 'Conditional Replace':
            selected_value = self.selected_column.get()
            unique_values = self.data.get_unique_values_per_column(selected_value)

            # Create a Label to prompt for unique values check
            un_values_lbl = ttk.Label(self, text='Check unique values below')
            un_values_lbl.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

            # Create a list box with multiple selection mode
            self.listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
            self.listbox.grid(row=2, rowspan=4, column=2)
            # Populate the list box with unique values
            for item in unique_values:
                self.listbox.insert(tk.END, item)
            # Bind select and deselect events
            self.listbox.bind("<<ListboxSelect>>", self.on_value_select)
            self.listbox.bind("<<ListboxUnselect>>", self.on_value_deselect)

            # Create a Label to prompt for input text to replace
            text_to_replace_lbl = ttk.Label(self, text='Enter text to replace')
            text_to_replace_lbl.grid(row=3, column=0, padx=25, pady=5, sticky=tk.W)
            # Create a Textbox to display selected unique values or input text to replace
            self.to_replace_txt = tk.Text(self, height=1, width=30)
            self.to_replace_txt.grid(row=3, column=1, padx=5, pady=5)

            # Create a Label to prompt for input replacement text
            replacement_text_lbl = ttk.Label(self, text='Enter replacement text')
            replacement_text_lbl.grid(row=4, column=0, padx=25, pady=5, sticky=tk.W)
            # Create a Textbox to input replacement text
            self.replacement_txt = tk.Text(self, height=1, width=30)
            self.replacement_txt.grid(row=4, column=1, padx=5, pady=5)

            replace_text_btn = ttk.Button(self, text='Replace Text', command=self.on_replace_text_click)
            replace_text_btn.grid(row=5, column=1)

    def on_replace_text_click(self):
        to_replace = self.to_replace_txt.get(1.0, tk.END).strip()
        # Split the text into a list based on commas
        values_to_replace = to_replace.split(",")
        values_to_replace = [word.strip() for word in values_to_replace]
        new_value = self.replacement_txt.get(1.0, tk.END)
        column = self.columns_cbox.get()
        self.data.replace_values_by_column(values_to_replace, new_value, column)
        info_lbl = ttk.Label(self, text='Text replacement process completed successfully.')
        info_lbl.grid(row=6, columnspan=3, padx=25, pady=5, sticky=tk.W)

    def on_value_select(self, event):
        # Get selected items
        selected_items = [self.listbox.get(idx) for idx in self.listbox.curselection()]
        # Update textbox with selected items
        self.to_replace_txt.delete(1.0, tk.END)
        for item in selected_items:
            self.to_replace_txt.insert(tk.END, item + ", ")

    def on_value_deselect(self, event):
        # Get deselected items
        deselected_item = self.listbox.get(event)
        # Remove deselected item from textbox
        self.to_replace_txt.delete("1.0", tk.END)
        # Get remaining selected items
        selected_items = [self.listbox.get(idx) for idx in self.listbox.curselection()]
        # Update textbox with remaining selected items
        for item in selected_items:
            self.to_replace_txt.insert(tk.END, item + ", ")

    def on_remove_column_click(self):
        selected_value = self.selected_column.get()
        self.data.drop_column(selected_value)
        self.update_columns_list()

    def on_remove_rows_click(self):
        selected_value = self.selected_column.get()
        rows_removed = self.data.remove_rows_with_null_values_by_column(selected_value)
        label_text = f"From the current process, {rows_removed} records were removed."
        info_lbl = ttk.Label(self, text=label_text)
        info_lbl.grid(row=2, columnspan=2, padx=25, pady=5)

    def on_update_type_click(self):
        column = self.columns_cbox.get()
        dtype = self.types_cbox.get()
        if dtype == 'datetime64':
            self.data.set_column_to_datetime(column)
        else:
            self.data.update_column_type(column, dtype)
        self.columns_list = self.data.get_columns().to_list()
        self.update_column_type_frame(self.columns_list)

    def on_methods_cbox_select(self, event):
        selected_method = self.methods_cbox.get()
        self.replace_values_btn['state'] = 'enabled'
        if 'specific value' in selected_method:
            # Create a text box to input the value
            self.new_value_txt = tk.Text(self, height=1, width=10)
            self.new_value_txt.grid(row=1, column=2, padx=10, pady=10)

    def on_replace_null_values_click(self):
        selected_column = self.columns_cbox.get()
        selected_method = self.methods_cbox.get()
        params = ''
        null_count_by_column = self.data.sum_of_null_values_by_column(selected_column)
        if 'specific value' in selected_method:
            # Get value from the text
            new_value = self.new_value_txt.get('1.0', 'end')
            self.data.replace_null_values_with_value(selected_column=selected_column, selected_value=new_value)
        elif 'previous value' in selected_method:
            # Set method to 'ffill'
            method = 'ffill'
            self.data.replace_null_values_by_method(selected_column=selected_column, selected_method=method)
        elif 'next value' in selected_method:
            # Set method to 'bfill'
            method = 'bfill'
            self.data.replace_null_values_by_method(selected_column=selected_column, selected_method=method)
        elif 'mean' in selected_method:
            # Set value to column mean
            new_value = self.data.get_column_mean(selected_column)
            self.data.replace_null_values_with_value(selected_column=selected_column, selected_value=new_value)
        elif 'median' in selected_method:
            # Set value to column median
            new_value = self.data.get_column_median(selected_column)
            self.data.replace_null_values_with_value(selected_column=selected_column, selected_value=new_value)
        elif 'mode' in selected_method:
            # Set value to column mode
            new_value = self.data.get_column_mode(selected_column)
            self.data.replace_null_values_with_value(selected_column=selected_column, selected_value=new_value)
        elif 'min' in selected_method:
            # Set value to column min
            new_value = self.data.get_column_min(selected_column)
            self.data.replace_null_values_with_value(selected_column=selected_column, selected_value=new_value)
        elif 'max' in selected_method:
            # Set value to column max
            new_value = self.data.get_column_max(selected_column)
            self.data.replace_null_values_with_value(selected_column=selected_column, selected_value=new_value)

        label_text = f"From the current process, {null_count_by_column} values were replaced."
        info_lbl = ttk.Label(self, text=label_text)
        info_lbl.grid(row=2, columnspan=2, padx=25, pady=5)

    def update_column_type_frame(self, columns_list):
        label_text = 'Verify the current data type of each column and, ' \
                     'if necessary, update it accordingly.'
        prompt_lbl = ttk.Label(self, text=label_text)
        prompt_lbl.grid(row=0, columnspan=3, sticky=tk.W, padx=25, pady=5)
        self.__create_grid()

        # Create a Combobox and set its values-columns' labels
        self.columns_cbox.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        # Set a default value
        self.columns_cbox.set("Select a column")

        # Create a Combobox and set its values-data types
        self.types_cbox = ttk.Combobox(self, values=self.data_types)
        self.types_cbox.grid(row=2, column=1, padx=10, pady=10, sticky=tk.NSEW)

        # Set a default value
        self.types_cbox.set("Select data type")

        # Create a Button to update data type for the selected column
        self.update_type_btn = ttk.Button(self, text='Update Data Type', command=self.on_update_type_click)
        self.update_type_btn.grid(row=2, column=2, padx=10, pady=10)

    def update_filling_frame(self, columns_list):
        methods_list = ['Fill with specific value',
                        'Fill with previous value in column',
                        'Fill with next value in column',
                        'Fill with column\'s mean',
                        'Fill with column\'s median',
                        'Fill with column\'s mode',
                        'Fill with column\'s max',
                        'Fill with column\'s min']

        total_null_count = self.data.sum_of_null_values()
        if total_null_count != 0:
            label_text = 'Identify the column(s) containing missing values in the DataFrame,' \
                         'implement an appropriate method to address and replace these missing values.'
            prompt_lbl = ttk.Label(self, text=label_text)
            prompt_lbl.grid(row=0, columnspan=4, padx=10, pady=5)

            self.columns_cbox.grid(row=1, column=0, padx=10, sticky=tk.NSEW)

            # Set a default value
            self.columns_cbox.set("Select a column")

            # Create a Combobox and set its values-filling methods
            self.methods_cbox = ttk.Combobox(self, values=methods_list, width=25)
            self.methods_cbox.grid(row=1, column=1, padx=10, sticky=tk.NSEW)

            # Set a default value
            self.methods_cbox.set("Select filling method")

            # Bind an event to handle selection changes
            self.methods_cbox.bind("<<ComboboxSelected>>", self.on_methods_cbox_select)

            self.replace_values_btn = ttk.Button(self, text='Replace',
                                                 command=self.on_replace_null_values_click,
                                                 state='disabled',
                                                 width=20)
            self.replace_values_btn.grid(row=1, column=3, padx=10, sticky=tk.NSEW)
        else:
            label_text = 'There are 0 null values in dataframe.'
            info_lbl = ttk.Label(self, text=label_text)
            info_lbl.grid(row=0, column=0, padx=25, pady=10, sticky=tk.NSEW)

    def update_text_adj_frame(self, columns_list):
        explanation_text = 'Use the options below to modify the text according to your preferences. \n' \
                           'Choose from operations like collapsing spaces, trimming spaces, or changing \n' \
                           'letter case. Select the appropriate buttons and customize your text effortlessly. '
        explanation_lbl = ttk.Label(self, text=explanation_text)
        explanation_lbl.grid(row=0, columnspan=2, padx=5, pady=15, sticky=tk.NSEW)

        column_selection_text = 'Select the column that requires text adjustments.'
        column_selection_lbl = ttk.Label(self, text=column_selection_text)
        column_selection_lbl.grid(row=1, column=0, padx=5, pady=5)
        self.columns_cbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

        # Set a default value
        self.columns_cbox.set("Select a column")

        collapse_selection_text = 'Click to reduce multiple spaces to a single space.'
        collapse_selection_lbl = ttk.Label(self, text=collapse_selection_text)
        collapse_selection_lbl.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        # Create a Button for 'Collapse Spaces'
        collapse_spaces_btn = ttk.Button(self, text='Collapse Spaces', command=self.on_collapse_spaces_click, width=20)
        collapse_spaces_btn.grid(row=2, column=1, pady=5, padx=5, sticky='nsew')

        trim_selection_text = 'Click to remove leading and trailing spaces.'
        trim_selection_lbl = ttk.Label(self, text=trim_selection_text)
        trim_selection_lbl.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
        # Create a Button for 'Trim Spaces'
        trim_spaces_btn = ttk.Button(self, text='Trim Spaces', command=self.on_trim_spaces_click, width=20)
        trim_spaces_btn.grid(row=3, column=1, pady=5, padx=5, sticky='nsew')

        lowercase_selection_text = 'Click to convert text to lowercase.'
        lowercase_selection_lbl = ttk.Label(self, text=lowercase_selection_text)
        lowercase_selection_lbl.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
        # Create a Button for 'Lowercase'
        lowercase_btn = ttk.Button(self, text='Lowercase', command=self.on_lowercase_click, width=20)
        lowercase_btn.grid(row=4, column=1, pady=5, padx=5, sticky='nsew')

        uppercase_selection_text = 'Click to convert text to uppercase.'
        uppercase_selection_lbl = ttk.Label(self, text=uppercase_selection_text)
        uppercase_selection_lbl.grid(row=5, column=0, padx=5, pady=5, sticky='nsew')
        # Create a Button for 'Uppercase'
        uppercase_btn = ttk.Button(self, text='Uppercase', command=self.on_uppercase_click, width=20)
        uppercase_btn.grid(row=5, column=1, pady=5, padx=5, sticky='nsew')

        capitalized_selection_text = 'Click to capitalize the first letter of each word.'
        capitalized_selection_lbl = ttk.Label(self, text=capitalized_selection_text)
        capitalized_selection_lbl.grid(row=6, column=0, padx=5, pady=5, sticky='nsew')
        # Create a Button for 'Capitalized'
        capitalized_btn = ttk.Button(self, text='Capitalized', command=self.on_capitalized_click, width=20)
        capitalized_btn.grid(row=6, column=1, pady=5, padx=5, sticky='nsew')

    def on_collapse_spaces_click(self):
        selected_column = self.columns_cbox.get()
        self.data.collapse_spaces_by_column(selected_column)

    def on_trim_spaces_click(self):
        selected_column = self.columns_cbox.get()
        self.data.trim_spaces_by_column(selected_column)

    def on_lowercase_click(self):
        selected_column = self.columns_cbox.get()
        self.data.set_column_to_lowercase(selected_column)

    def on_uppercase_click(self):
        selected_column = self.columns_cbox.get()
        self.data.set_column_to_uppercase(selected_column)

    def on_capitalized_click(self):
        selected_column = self.columns_cbox.get()
        self.data.set_column_to_capitalized(selected_column)
