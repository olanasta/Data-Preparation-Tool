import os
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import filedialog as fd
from import_data_frame import ImportDataFrame
from basic_info_frame import BasicInfoFrame
from cleaning_data_frame import CleaningDataFrame
from transform_data_frame import TransformingDataFrame
from outliers_frame import HandleOutliersFrame

from DataAnalysisFramework.data_frame_handler import DataFrameHandler


class MainBarButtonFrame(ttk.Frame):
    def __init__(self, container, relief, update_main_frame):
        super().__init__(container, relief=relief)

        # initialize the dataframe to None until file selected
        self.data = None

        self.container = container
        self.update_main_frame = update_main_frame

        # setup the grid layout manager
        self.columnconfigure(0, weight=1)

        self.menus = []     # List to store menus and submenus

        self.__create_widgets()

    def __create_widgets(self):
        s = ttk.Style()
        s.configure('.', font=('aerial', 14))

        self.import_data_btn = ttk.Button(self, text='Import Data', command=self.on_import_data_click, width=40)
        self.import_data_btn.grid(column=0, row=0, ipady=10, padx=10)

        # Create a menu bar
        menu_bar = tk.Menu(self)
        self.menus.append(menu_bar)

        # Create a "File" menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import Data",
                              command=self.on_import_data_click)
        file_menu.add_command(label="Basic Information",
                              command=self.on_basic_info_click,
                              state='disabled')
        file_menu.add_command(label="Save Changes",
                              command=self.on_save_click,
                              state='disabled')
        file_menu.add_separator()
        file_menu.add_command(label="Close", command=self.on_close_click)
        self.menus.append(file_menu)

        # Add the "File" menu to the menu bar
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Create a "Clean Data" menu
        cleaning_data_menu = tk.Menu(menu_bar, tearoff=0)
        cleaning_data_menu.add_command(label='Remove Duplicates', command=self.on_remove_duplicates_click)
        cleaning_data_menu.add_command(label='Remove Unnecessary Columns', command=self.on_remove_columns_click)

        # Add the "Clean Data" menu to the menu bar
        menu_bar.add_cascade(label="Clean Data", menu=cleaning_data_menu, state='disabled')

        # Create a "Transform Data" menu
        transforming_data_menu = tk.Menu(menu_bar, tearoff=0)
        transforming_data_menu.add_command(label='Convert Column Data Type', command=self.on_convert_column_type_click)

        # Create a "Handle Missing Values" submenu
        missing_values_submenu = tk.Menu(transforming_data_menu, tearoff=0)
        missing_values_submenu.add_command(label='Remove Rows with Missing Values',
                                           command=self.on_remove_empty_rows_click)
        missing_values_submenu.add_command(label='Remove Columns with Missing Values',
                                   command=self.on_remove_empty_columns_click)
        missing_values_submenu.add_command(label='Replace Missing Values',
                                           command=self.on_replace_missing_values_click)

        # Add the "Handle Missing Values" submenu to the "Transform Data" menu
        transforming_data_menu.add_cascade(label='Handle Missing Values', menu=missing_values_submenu)

        # Create a "Text Transformation" submenu
        text_transformation_submenu = tk.Menu(transforming_data_menu, tearoff=0)
        text_transformation_submenu.add_command(label='Text Adjustments',
                                           command=self.on_text_adjustments_click)
        text_transformation_submenu.add_command(label='Conditional Replace',
                                                command=self.on_conditional_replace_click)

        # Add the "Text Transformation" submenu to the "Transform Data" menu
        transforming_data_menu.add_cascade(label='Text Transformation', menu=text_transformation_submenu)

        # Add the "Transform Data" menu to the menu bar
        menu_bar.add_cascade(label="Transform Data", menu=transforming_data_menu, state='disabled')

        # Create a "Handle Outliers" menu
        outliers_menu = tk.Menu(menu_bar, tearoff=0)
        outliers_menu = tk.Menu(outliers_menu, tearoff=0)
        outliers_menu.add_command(label='Visualize Data',
                                  command=self.on_visualize_click)
        outliers_menu.add_command(label='Sort Values Ascending',
                                  command=self.on_sort_values_click)
        outliers_menu.add_command(label='IQR',
                                  command=self.on_iqr_click)
        outliers_menu.add_command(label='Z-Score',
                                  command=self.on_zscore_click)

        # Add the "Handle Outliers" menu to the menu bar
        menu_bar.add_cascade(label="Handle Outliers", menu=outliers_menu, state='disabled')

        # Configure the root window to use the menu bar
        self.container.config(menu=menu_bar)

    def enable_menus(self):
        self.menus[0].entryconfigure('Transform Data', state='active')
        self.menus[0].entryconfigure('Clean Data', state='normal')
        self.menus[0].entryconfigure('Handle Outliers', state='normal')

        self.menus[1].entryconfigure('Basic Information', state='normal')
        self.menus[1].entryconfigure('Save Changes', state='normal')

    def on_import_data_click(self):
        filetypes = (
            ('csv files', '*.csv'),
            ('excel files', '*.xlsx'),
            ('json files', '*.json'),
            ('All files', '*.*')
        )
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Relative path to datasets directory
        relative_path = os.path.join(base_dir, "Datasets")
        file = fd.askopenfile(title='Open a file',
                              initialdir=relative_path,
                              filetypes=filetypes)

        # Clear frame
        self.grid_forget()

        # update the main frame content with the filename
        self.update_main_frame(ImportDataFrame, file.name)

        # initialize dataframe
        self.data = DataFrameHandler(file.name)
        self.enable_menus()

    def on_basic_info_click(self):
        self.update_main_frame(BasicInfoFrame, self.data)

    def on_remove_duplicates_click(self):
        d = self.data.num_of_duplicates()
        btn_clicked = 'Remove Duplicates'
        self.update_main_frame(CleaningDataFrame, self.data, btn_clicked, d)

    def on_remove_columns_click(self):
        btn_clicked = 'Remove Columns'
        self.update_main_frame(CleaningDataFrame, self.data, btn_clicked)

    def on_remove_empty_rows_click(self):
        btn_clicked = 'Remove Rows'
        self.update_main_frame(TransformingDataFrame, self.data, btn_clicked)

    def on_remove_empty_columns_click(self):
        btn_clicked = 'Remove Columns'
        self.update_main_frame(TransformingDataFrame, self.data, btn_clicked)

    def on_convert_column_type_click(self):
        btn_clicked = 'Convert Column Type'
        self.update_main_frame(TransformingDataFrame, self.data, btn_clicked)

    def on_replace_missing_values_click(self):
        btn_clicked = 'Replace Missing Values'
        self.update_main_frame(TransformingDataFrame, self.data, btn_clicked)

    def on_text_adjustments_click(self):
        btn_clicked = 'Text Adjustments'
        self.update_main_frame(TransformingDataFrame, self.data, btn_clicked)

    def on_conditional_replace_click(self):
        btn_clicked = 'Conditional Replace'
        self.update_main_frame(TransformingDataFrame, self.data, btn_clicked)

    def on_save_click(self):
        # Ask user for the file path using a save dialog
        filepath = fd.asksaveasfilename(defaultextension=".csv", filetypes=[
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ('JSON files', "*.json"),
            ("All files", "*.*")
        ])

        self.data.save_dataframe_to_file(filepath)

    def on_close_click(self):
        self.container.destroy()

    def on_sort_values_click(self):
        btn_clicked = 'sort'
        self.update_main_frame(HandleOutliersFrame, self.data, btn_clicked)

    def on_visualize_click(self):
        btn_clicked = 'visualize'
        self.update_main_frame(HandleOutliersFrame, self.data, btn_clicked)

    def on_iqr_click(self):
        btn_clicked = 'iqr'
        self.update_main_frame(HandleOutliersFrame, self.data, btn_clicked)

    def on_zscore_click(self):
        btn_clicked = 'zscore'
        self.update_main_frame(HandleOutliersFrame, self.data, btn_clicked)
