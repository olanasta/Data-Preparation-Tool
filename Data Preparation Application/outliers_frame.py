from DataAnalysisFramework.data_frame_handler import DataFrameHandler
from tkinter import ttk
import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class HandleOutliersFrame(ttk.Frame):
    def __init__(self, container, data, btn_clicked):
        super().__init__(container)

        self.data = data
        self.btn = btn_clicked
        self.selected_column = tk.StringVar()
        self.columns_list = self.data.get_columns().to_list()

        # Create Combobox for column selection
        self.columns_cbox = ttk.Combobox(self, textvariable=self.selected_column, values=self.columns_list, width=30)
        self.columns_cbox.bind("<<ComboboxSelected>>", self.on_columns_cbox_select)

        # Create a ListBox for outliers
        self.outliers_lst = tk.Listbox(self,
                                       listvariable=None,
                                       height=10,
                                       selectmode=tk.SINGLE)
        self.outliers_lst.bind("<<ListboxSelect>>", self.on_outlier_select)

        # Create Buttons to replace outliers
        self.replace_upper_outlier_btn = ttk.Button(self, text='Replace Outlier with Upper Limit',
                                                    command=self.on_replace_upper_outlier_click,
                                                    state='disabled')
        self.replace_lower_outlier_btn = ttk.Button(self, text='Replace Outlier with Lower Limit',
                                                    command=self.on_replace_lower_outlier_click,
                                                    state='disabled')

        # Create a Label for general prompt
        self.prompt_lbl = ttk.Label(self, text='')

        self.__create_widgets()

    def __create_widgets(self):
        s = ttk.Style()
        s.configure('.', font=('Arial', 14))  # Corrected font name from 'aerial' to 'Arial'

        if self.btn == 'visualize':
            self.__create_visualization_frame()
        elif self.btn == 'sort':
            self.__create_ascending_sort_frame()
        elif self.btn == 'iqr':
            self.__create_iqr_frame()
        elif self.btn == 'zscore':
            self.__create_zscore_frame()

    def __create_iqr_frame(self):
        # Add prompt label for selecting column to compute iqr to frame
        self.prompt_lbl['text'] = 'Select the desired column to identify outliers using IQR method. \n' \
                                  'Consider removing or replacing outliers for more accurate analysis.'
        self.prompt_lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Add columns ComboBox to frame
        self.columns_cbox.grid(row=1, column=0, padx=10, pady=10)
        self.columns_cbox.set("Select a column")  # Set default value

    def __create_zscore_frame(self):
        # Create a label for selecting column to compute z-score
        self.prompt_lbl['text'] = 'Select the desired column to identify outliers using Z-Score method. \n' \
                                  'Consider removing or replacing outliers for more accurate analysis.'
        self.prompt_lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Add columns ComboBox to frame
        self.columns_cbox.grid(row=1, column=0, padx=10, pady=10)
        self.columns_cbox.set("Select a column")  # Set default value

    def __create_visualization_frame(self):
        # Add a label for selecting column and plot
        self.prompt_lbl ['text'] = 'Select the desired column and plot for identifying outliers.'
        self.prompt_lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Add columns ComboBox to frame
        self.columns_cbox.grid(row=1, column=0, padx=10, pady=10)
        self.columns_cbox.set("Select a column")    # Set default value

        # Create a Combobox for plot choices
        self.plot_cbox = ttk.Combobox(self, values=["Box Plot", "Scatter Plot", "Histogram", "Dist Plot"])
        self.plot_cbox.grid(row=1, column=1, pady=(0, 10))
        self.plot_cbox.set("Select a plot")   # Set default selection
        self.plot_cbox.bind("<<ComboboxSelected>>", self.on_plot_cbox_select)

    def __create_ascending_sort_frame(self):
        # Add a label for selecting column
        self.prompt_lbl['text'] = 'Select the desired column to sort ascending for identifying outliers. \n' \
                                  'Consider removing outliers for more accurate analysis.'
        self.prompt_lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Add columns ComboBox to frame
        self.columns_cbox.grid(row=1, column=0, padx=10, pady=10)
        self.columns_cbox.set("Select a column")    # Set default value

    def on_plot_cbox_select(self, event):
        selected_column = self.columns_cbox.get()
        selected_plot = self.plot_cbox.get()

        if selected_plot == 'Box Plot':
            plot = self.data.get_boxplot(selected_column)
        elif selected_plot == 'Scatter Plot':
            plot = self.data.get_scatterplot(selected_column)
        elif selected_plot == 'Dist Plot':
            plot = self.data.get_distplot(selected_column)
        elif selected_plot == 'Histogram':
            plot = self.data.get_histogram(selected_column)

        # Create a canvas to display the plot
        canvas = FigureCanvasTkAgg(plot, master=self)
        canvas.draw()

        # Place the canvas in the tkinter frame
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def __create_sorted_values_frame(self, column):

        self.prompt_lbl['text'] = 'View the first and last values to identify potential outliers. \n' \
                                  'Consider removing outliers for more accurate analysis.'
        # Get the data from the specified column and sort in ascending order
        sorted_data = self.data.get_head_tail_of_sorted_column(self.column)
        var = tk.Variable(value=sorted_data)
        # Add a ListBox widget with outliers
        self.outliers_lst['listvariable'] = var
        self.outliers_lst.grid(row=1, column=0, padx=10, pady=10)

    def __create_zscore_values_frame(self, column):
        outliers = self.data.identify_outliers_zscore(column)
        sorted_outliers = sorted(outliers)

        if outliers:
            self.columns_cbox.grid_forget()
            var = tk.Variable(value=sorted_outliers)
            # Add a ListBox widget with outliers
            self.outliers_lst['listvariable'] = var
            self.outliers_lst.grid(row=1, column=0, rowspan=3, padx=10, pady=10)

            self.replace_upper_outlier_btn.grid(row=1, column=1, padx=10, pady=10)
            self.replace_lower_outlier_btn.grid(row=2, column=1, padx=10, pady=10)

        else:
            self.prompt_lbl['text'] = f'There are no outliers in column {column}'

    def __create_iqr_values_frame(self, column):
        outliers = self.data.identify_outliers_zscore(column)
        sorted_outliers = sorted(outliers)

        if outliers:
            self.columns_cbox.grid_forget()
            var = tk.Variable(value=sorted_outliers)
            # Add a ListBox widget with outliers
            self.outliers_lst['listvariable'] = var
            self.outliers_lst.grid(row=1, column=0, rowspan=3, padx=10, pady=10)

            self.replace_upper_outlier_btn.grid(row=1, column=1, padx=10, pady=10)
            self.replace_lower_outlier_btn.grid(row=2, column=1, padx=10, pady=10)
        else:
            self.prompt_lbl['text'] = f'There are no outliers in column {column}'

    def on_columns_cbox_select(self, event):
        self.column = self.selected_column.get()

        if 'sort ascending' in self.prompt_lbl['text']:
            self.__create_sorted_values_frame(self.column)
        elif 'Z-Score method' in self.prompt_lbl['text']:
            self.__create_zscore_values_frame(self.column)
        elif 'IQR method' in self.prompt_lbl['text']:
            self.__create_iqr_values_frame(self.column)

        self.remove_outlier_btn = ttk.Button(self, text='Remove Outlier',
                                             command=self.on_remove_outlier_click,
                                             state='disabled',
                                             width=20)
        self.remove_outlier_btn.grid(row=3, column=1, padx=10, pady=10)
        self.columns_cbox.grid_forget()

    def on_outlier_select(self, event):
        # Enable Button
        self.remove_outlier_btn['state'] = 'enabled'
        # Check if the replace buttons are placed in the frame
        replace_buttons_placed = False
        for child in self.winfo_children():
            if child == self.replace_upper_outlier_btn or child == self.replace_lower_outlier_btn:
                replace_buttons_placed = True
                break

        if replace_buttons_placed:
            self.replace_lower_outlier_btn['state'] = 'enabled'
            self.replace_upper_outlier_btn['state'] = 'enabled'
        # Get the selected item
        selected_item = self.outliers_lst.curselection()
        # Get the text of the selected item
        self.selected_text = self.outliers_lst.get(selected_item)

    def on_remove_outlier_click(self):
        self.data.remove_row_with_outlier(self.column, self.selected_text)
        self.on_columns_cbox_select("<<ComboboxSelected>>")

    def on_replace_upper_outlier_click(self):
        if 'Z-Score method' in self.prompt_lbl['text']:
            upper_limit = self.data.get_zscore_upper_limit(self.column)
            self.data.replace_outlier_with_upper_limit(self.column, upper_limit)
        elif 'IQR method' in self.prompt_lbl['text']:
            upper_limit = self.data.get_iqr_upper_limit(self.column)
            self.data.replace_outlier_with_upper_limit(self.column, upper_limit)
        self.on_columns_cbox_select("<<ComboboxSelected>>")

    def on_replace_lower_outlier_click(self):
        if 'Z-Score method' in self.prompt_lbl['text']:
            lower_limit = self.data.get_zscore_upper_limit(self.column)
            self.data.replace_outlier_with_lower_limit(self.column, lower_limit)
        elif 'IQR method' in self.prompt_lbl['text']:
            lower_limit = self.data.get_iqr_lower_limit(self.column)
            self.data.replace_outlier_with_lower_limit(self.column, lower_limit)
        self.on_columns_cbox_select("<<ComboboxSelected>>")
