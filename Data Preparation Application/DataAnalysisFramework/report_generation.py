import re
from yattag import Doc


class ReportGeneration:

    def __init__(self, doc, tag, text):
        self.doc = doc
        self.tag = tag
        self.text = text

    def print_describe_as_html_table(self, data):
        df_descr = data.get_describe()
        columns = data.get_numeric_columns()

        with self.tag('table'):
            # Create table header (column names)
            with self.tag('tr'):
                col_lst = list(columns)
                col_lst.insert(0, 'Statistics')
                for column in col_lst:
                    with self.tag('th'):
                        self.text(column)

            # Create table rows (data)
            for index, row in df_descr.iterrows():
                with self.tag('tr'):
                    with self.tag('td'):
                        self.text(index)  # Print the index column
                    for value in row:
                        with self.tag('td'):
                            self.text(str(value))

    def print_first_and_last_rows_as_html_table(self, data):
        df_head = data.get_first_and_last_rows()
        with self.tag('table'):
            # Create table header (column names)
            with self.tag('tr'):
                for column in df_head.columns:
                    with self.tag('th'):
                        self.text(column)

            # Create table rows (data)
            for _, row in df_head.iterrows():
                with self.tag('tr'):
                    for value in row:
                        with self.tag('td'):
                            self.text(str(value))

    def print_number_of_entries_columns(self, data):
        df_num_of_entries = data.get_num_of_entries_columns()[0]
        df_num_of_columns = data.get_num_of_entries_columns()[1]

        with self.tag('h3'):
            self.text('The dataframe consists of ' + str(df_num_of_entries) + ' entries and ' + str(df_num_of_columns) + ' columns')

    def print_columns_as_html_table(self, data):
        columns = data.get_columns()
        splitted_columns = [columns[i:i + 8] for i in range(0, len(columns), 8)]
        with self.tag('table'):
            for row in splitted_columns:
                with self.tag('tr'):
                    for cell in row:
                        with self.tag('td'):
                            self.text(cell)

    def format_info_data(self, data):
        info = data.get_formatted_info()
        remove_to = info.find('>')
        info = info[remove_to + 1:]
        info = info.split('\n')
        info = info[1:]
        info = info[:-3]

        info = info[3:]
        formatted_data = []
        # Strings to be removed
        strings_to_remove = ['[', ', ', ']']

        # Remove specified strings using list comprehension
        filtered_array = [word for word in info if
                          word not in strings_to_remove]

        for line in filtered_array[1:]:
            line = line.strip()
            numbers = re.findall(r'\d+', line)
            line_length = len(line)
            numbers_length = len(numbers)
            index = numbers[0]
            last_number_index = line.find(numbers[numbers_length - 1])
            # According to the number of numbers in each line we check which number will be used
            if numbers_length == 2:
                end_of_column_name_index = line.find(numbers[1])
            elif numbers_length == 3:
                if last_number_index >= line_length - len(numbers[2]):
                    end_of_column_name_index = line.find(numbers[1])
                else:
                    end_of_column_name_index = line.find(numbers[2])
            else:
                end_of_column_name_index = line.find(numbers[2])

            column_name = line[2:end_of_column_name_index].strip()
            # Find the index of the last space
            last_space_index = line.rfind(' ')
            # Find the index of the second last space by slicing the string up to the last space
            second_last_space_index = line.rfind(' ', 0, last_space_index)
            non_null_count = line[end_of_column_name_index:second_last_space_index].strip()
            # get the total count of records
            total_rec = data.get_num_of_entries_columns()[0]
            total_rec = re.findall(r'\d+', str(total_rec))
            # append total records in non_null_count column
            non_null_count = non_null_count + ' of ' + total_rec[0]
            dtype = line[second_last_space_index:].strip()

            formatted_data.append([index, column_name, non_null_count, dtype])

        return formatted_data

    def print_info(self, data):
        with self.tag('div'):
            self.text(data.get_formatted_info())

    def print_info_as_html_table(self, data):
        formatted_info_data = self.format_info_data(data)
        titles = ['', 'Column', 'Non-null values', 'Type']
        with self.tag('table'):
            with self.tag('tr'):
                for title in titles:
                    with self.tag('th'):
                        self.text(title)
            for data_row in formatted_info_data:
                with self.tag('tr'):
                    for data_column in data_row:
                        if ' non-null' in data_column:
                            non_null_count = re.findall(r'\d+', data_column)
                            if non_null_count[0] != non_null_count[1]:
                                with self.tag('td', klass='red'):
                                    self.text(data_column)
                            else:
                                with self.tag('td'):
                                    self.text(data_column)
                        else:
                            with self.tag('td'):
                                self.text(data_column)

    def print_dtypes_as_html_table(self, data):
        types = data.get_data_types()
        columns = data.get_columns()

        with self.tag('table'):
            for column in columns:
                with self.tag('tr'):
                    with self.tag('td'):
                        self.text(str(column))
                    with self.tag('td'):
                        self.text(str(types[column]))

    def print_num_of_duplicates(self, data):
        n = data.num_of_duplicates()
        with self.tag('div'):
            self.text('The dataframe contains ' + str(n) + ' duplicates')

    def print_sum_of_null_values_as_html_table(self, data):
        n = data.sum_of_null_values()
        columns = df.get_columns()

        with self.tag('table'):
            for column in columns:
                with self.tag('tr'):
                    with self.tag('td'):
                        self.text(str(column))
                    with self.tag('td'):
                        self.text(str(n[column]))

    def print_correlation_matrix(self, data):
        img_path = data.save_correlation_matrix_as_img()
        with self.tag('div'):
            with self.tag('img', src=img_path, alt='Correlation Matrix'):
                pass

    def print_unique_values_per_column(self, data, column):
        un_values = data.get_unique_values_per_column(column)
        splitted_values = [un_values[i:i + 8] for i in range(0, len(un_values), 8)]
        with self.tag('div'):
            with self.tag('h4'):
                self.text(column)
            with self.tag('div'):
                with self.tag('table'):
                    for row in splitted_values:
                        with self.tag('tr'):
                            for cell in row:
                                with self.tag('td'):
                                    self.text(str(cell))

