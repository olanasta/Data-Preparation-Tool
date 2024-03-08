import tkinter as tk
import tkinter.ttk as ttk
from main_bar_btns_frame import MainBarButtonFrame
from import_data_frame import ImportDataFrame


class DataAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Data Preparation for Analysis')
        self.geometry()
        self.main_frame = None

        # Set up the layout on the root window
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

        # Create and configure widgets
        self.__create_widgets()

    def __create_widgets(self):
        # Configure the default style for all widgets
        default_style = ttk.Style()
        default_style.configure('.', font=('Arial', 14))

        # Create the button frame
        button_frame = MainBarButtonFrame(self, tk.RIDGE, self.update_main_frame)
        button_frame.grid(column=0, row=0, pady=40)

    def clear_frame(self, frame):
        # Remove all widgets from the frame
        for widget in frame.winfo_children():
            widget.destroy()
        frame.grid_forget()

    def update_main_frame(self, frame_class, *args):
        # Clear the existing main frame
        if self.main_frame:
            self.main_frame.grid_forget()
            self.clear_frame(self.main_frame)

        # Update the main frame content based on the button click
        self.main_frame = frame_class(self, *args)
        self.main_frame.grid(column=1, row=0, pady=40, sticky='nsew')
        self.geometry()

        # Center the window on the screen
        self.update_idletasks()
        x_position = (self.winfo_screenwidth() - self.winfo_reqwidth()) // 2
        y_position = (self.winfo_screenheight() - self.winfo_reqheight()) // 2
        self.geometry(f"+{x_position}+{y_position}")


if __name__ == '__main__':
    app = DataAnalysisApp()
    app.update_idletasks()
    x_position = (app.winfo_screenwidth() - app.winfo_reqwidth()) // 2
    y_position = (app.winfo_screenheight() - app.winfo_reqheight()) // 2
    app.geometry(f"+{x_position}+{y_position}")
    app.mainloop()
