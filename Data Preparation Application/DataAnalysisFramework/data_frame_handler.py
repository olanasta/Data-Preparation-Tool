import io
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.impute import KNNImputer
from scipy.stats import zscore
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataFrameHandler:
    def __init__(self, data_file=''):

        np.random.seed(42)
        self.filetype = None

        if data_file.lower().endswith('.csv'):
            self.data = pd.read_csv(data_file)  # Read data from a CSV file
            self.filetype = 'csv'
        elif data_file.lower().endswith('.xlxs'):
            self.data = pd.read_excel(data_file)  # Read data from an EXCEL file
            self.filetype = 'xlxs'
        elif data_file.lower().endswith('.json'):
            self.data = pd.read_json(data_file)  # Read data from a JSON file
            self.filetype = 'json'

    def get_dataframe(self):
        return self.data

    def get_info(self):
        self.data.info()

    def get_formatted_info(self):
        buf = io.StringIO()
        self.data.info(buf=buf)
        info = buf.getvalue()
        return info

    def get_describe(self):
        return self.data.describe()

    def get_column_mean(self, column_name):
        return self.data[column_name].mean()

    def get_column_median(self, column_name):
        return self.data[column_name].median()

    def get_column_mode(self, column_name):
        # Mode can be a series, so take the first value
        return self.data[column_name].mode().iloc[0]

    def get_column_min(self, column_name):
        return self.data[column_name].min()

    def get_column_max(self, column_name):
        return self.data[column_name].max()

    def get_columns(self):
        return self.data.columns

    def get_numeric_columns(self):
        return self.data.select_dtypes(include='number')

    def get_all_data(self):
        return self.data

    def get_first_and_last_rows(self):
        head = self.data.head()
        tail = self.data.tail()
        merged_data = pd.merge(head, tail, how='outer')
        return merged_data
    
    def get_column_sample_data(self, column):
        return self.data[column].unique()[0:4]

    def get_num_of_entries_columns(self):
        return self.data.shape

    def num_of_duplicates(self):
        nod = self.data.duplicated().sum()
        return nod

    def get_index(self):
        return self.data.index

    def drop_row_by_index(self, index):
        self.data.drop(index, inplace=True)

    def drop_column(self, column):
        self.data.drop(column, axis=1, inplace=True)

    def remove_duplicates(self):
        self.data.drop_duplicates(inplace=True)

    def apply_changes(self, func):
        self.data = self.data.applymap(func)

    def get_data_types(self):
        return self.data.dtypes

    def convert_to_float_dot_separator(self, value):
        try:
            # Attempt to convert the value to float using comma as a decimal separator
            new_value = str(value).replace(',', '.')
            return float(new_value)
        except ValueError:
            # If the conversion fails, return the original value
            return float('nan')

    def update_column_type(self, column, dtype):
        # If dtype=float64, check column data for float with comma separator and update it with dot separator
        if 'float' in dtype:
            self.data[column] = pd.to_numeric(self.data[column].apply(self.convert_to_float_dot_separator), errors='coerce')
        self.data[column] = self.data[column].astype(dtype)

    def set_column_to_datetime(self, column):
        self.data[column] = pd.to_datetime(self.data[column])

    def get_column_type(self, column):
        return self.data[column].dtype

    def sum_of_null_values(self):
        return self.data.isna().sum().sum()

    def sum_of_null_values_by_column(self, column):
        return self.data[column].isnull().sum()

    def remove_rows_with_null_values_by_column(self, column):
        initial_len = len(self.data)
        self.data = self.data.dropna(subset=[column])
        final_len = len(self.data)
        rows_removed = initial_len - final_len
        return rows_removed

    def replace_values_by_column(self, values_to_replace, new_value, column):
        for val in values_to_replace:
            self.data[column].replace(val, new_value, inplace=True)

    def get_unique_values_per_column(self, column):
        return self.data[column].unique()

    def replace_null_values_with_value(self, selected_column, selected_value):
        # Replace null values with a specific value or statistic measure
        self.data[selected_column].fillna(value=selected_value, inplace=True)
        
    def replace_null_values_by_method(self, selected_column, selected_method):
        # Replace null values using a specified method
        if selected_method == 'bfill':
            self.data[selected_column] = self.data[selected_column].bfill()
        elif selected_method == 'ffill':
            self.data[selected_column] = self.data[selected_column].ffill()

    def collapse_spaces(self, text):
        return ' '.join(text.split())

    def collapse_spaces_by_column(self, column):
        self.data[column] = self.data[column].apply(self.collapse_spaces)

    def trim_spaces_by_column(self, column):
        self.data[column] = self.data[column].str.strip()

    def save_dataframe_to_file(self, filepath):
        # Check if the user provided a file path
        if filepath:
            # Determine the file type based on the selected file extension
            file_type = filepath.split('.')[-1].lower()

            # Save DataFrame to the specified file based on the file type
            if file_type == 'csv':
                self.data.to_csv(filepath, index=False)
            elif file_type == 'xlsx':
                self.data.to_excel(filepath, index=False)
            elif file_type == 'json':
                self.data.to_json(filepath, orient='records', lines=True)
            else:
                print(f"Unsupported file type: {file_type}")
                return

    def knn_imputation(self, column, neighbors):
        imputer = KNNImputer(n_neighbors=neighbors)
        # Reshape the column to a 2D array
        column_2d = self.data[column].values.reshape(-1, 1)

        # Perform KNN imputation
        imputed_values = imputer.fit_transform(column_2d).ravel()

        # Update the DataFrame with imputed values
        self.data[column] = imputed_values

    def update_column_value(self, column, old_value, new_value):
        self.data.loc[self.data[column] == old_value, column] = new_value
        print(self.data)

    def update_date_format_by_column(self, column, date_format):

        self.data[column] = pd.to_datetime(self.data[column])

        if date_format == 'MM/DD/YYYY':
            self.data[column] = self.data[column].dt.strftime("%m/%d/%Y")
        elif date_format == 'DD/MM/YYYY':
            self.data[column] = self.data[column].dt.strftime("%d/%m/%Y")
        elif date_format == 'YYYY/MM/DD':
            self.data[column] = self.data[column].dt.strftime("%Y/%m/%d ")
        elif date_format == 'Month DD, YYYY':
            self.data[column] = self.data[column].dt.strftime("%B %d, %Y")
        elif date_format == 'DD Month, YYYY':
            self.data[column] = self.data[column].dt.strftime("%d %B, %Y")
        elif date_format == 'YYYY, Month DD':
            self.data[column] = self.data[column].dt.strftime("%Y, %d %B")
        elif date_format == 'Mon DD, YYYY':
            self.data[column] = self.data[column].dt.strftime("%b %d, %Y")
        elif date_format == 'DD Mon, YYYY':
            self.data[column] = self.data[column].dt.strftime("%d %b, %Y")
        elif date_format == 'YYYY, Mon DD':
            self.data[column] = self.data[column].dt.strftime("%d %b, %Y")
        
    def set_column_to_upppercase(self, column):
        self.data[column] = self.data[column].str.upper()
        
    def set_column_to_lowercase(self, column):
        self.data[column] = self.data[column].str.lower()
        
    def set_column_to_capitalized(self, column):
        self.data[column] = self.data[column].str.capitalize()

    def remove_columns(self, columns_to_remove):
        for column in columns_to_remove:
            del self.data[column]

    def split_dataframe(self, column, filepath):
        grouped = self.data.groupby(column)
        
        if self.filetype == None:
            self.filetype = 'xlsx'

        # Iterate over groups and save each group to a separate file according to 
        # the initial filetype (if None set to excel)
        for name, group in grouped:
            file_name = f"{filepath}/{column}_{name}.{self.filetype}"
            if self.filetype == 'csv':
                group.to_csv(file_name, index=False)
            elif self.filetype == 'xlsx':
                group.to_excel(file_name, index=False)
            elif self.filetype == 'json':
                group.to_json(file_name, index=False)

    def identify_columns_with_outliers(self, threshold):
        outlier_columns = []
        for column in self.data.columns:
            if self.data[column].dtype in [np.float64, np.int64]:
                z_scores = np.abs((self.data[column] - self.data[column].mean()) / self.data[column].std())
                outliers = self.data[z_scores > threshold]
                if not outliers.empty:
                    outlier_columns.append(column)
        return outlier_columns

    def get_boxplot(self, column):
        # Create a seaborn boxplot for the specific column
        sns.set(style="whitegrid")
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        sns.boxplot(x=self.data[column], ax=ax)

        # Customize the boxplot
        ax.set_title(f'Boxplot for {column}')

        return fig

    def get_scatterplot(self, column):
        # Create a scatter plot for the specific column
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        ax.scatter(range(len(self.data)), self.data[column])

        # Customize the scatter plot
        ax.set_title(f'Scatter Plot for {column}')

        return fig

    def get_histogram(self, column):
        # Create a histogram for the specific column
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        sns.histplot(self.data[column], ax=ax, kde=False)

        # Customize the histogram
        ax.set_title(f'Histogram for {column}')

        return fig

    def get_distplot(self, column):
        # Create a distplot for the specific column
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        sns.histplot(self.data[column], ax=ax, kde=True)

        # Customize the distplot
        ax.set_title(f'Distplot for {column}')

        return fig

    def get_head_tail_of_sorted_column(self, column):
        sorted_dataframe = self.data[column].sort_values()
        sorted_column_head = sorted_dataframe.head(10).to_list()
        sorted_column_tail = sorted_dataframe.tail(10).to_list()
        sorted_data = sorted_column_head + sorted_column_tail
        return sorted_data

    def remove_row_with_outlier(self, column, outlier):
        self.data.drop(self.data.loc[self.data[column] == outlier].index, inplace=True)

    def identify_outliers_iqr(self, column):
        upper_limit = self.get_iqr_upper_limit(column)
        lower_limit = self.get_iqr_lower_limit(column)

        outliers = self.data.loc[(self.data[column] > upper_limit) | (self.data[column] < lower_limit)]
        return outliers[column].values.tolist()

    def identify_outliers_zscore(self, column):
        upper_limit = self.get_zscore_upper_limit(column)
        lower_limit = self.get_zscore_lower_limit(column)

        outliers = self.data.loc[(self.data[column] > upper_limit) | (self.data[column] < lower_limit)]
        return outliers[column].values.tolist()

    def get_zscore_upper_limit(self, column):
        upper_limit = self.data[column].mean() + 3 * self.data[column].std()

        return upper_limit

    def get_zscore_lower_limit(self, column):
        lower_limit = self.data[column].mean() - 3*self.data[column].std()

        return lower_limit

    def calculate_q1(self, column):
        return self.data[column].quantile(0.25)

    def calculate_q3(self, column):
        return self.data[column].quantile(0.75)

    def calculate_iqr(self, column):
        q1 = self.calculate_q1(column)
        q3 = self.calculate_q3(column)
        iqr = q3 - q1

        return iqr

    def get_iqr_upper_limit(self, column):
        q3 = self.calculate_q3(column)
        iqr = self.calculate_iqr(column)

        upper_limit = q3 + (1.5 * iqr)

        return upper_limit

    def get_iqr_lower_limit(self, column):
        q1 = self.calculate_q1(column)
        iqr = self.calculate_iqr(column)

        lower_limit = q1 - (1.5 * iqr)

        return lower_limit

    def replace_outlier_with_upper_limit(self, column, upper_limit):
        print(upper_limit)
        self.data.loc[self.data[column] > upper_limit, column] = upper_limit

    def replace_outlier_with_lower_limit(self, column, lower_limit):
        print(lower_limit)
        self.data.loc[self.data[column] < lower_limit, column] = lower_limit
