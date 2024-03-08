import os
import yattag
from yattag import Doc
import webbrowser
from DataAnalysisFramework.report_generation import ReportGeneration


def basic_info_report_generation(options, un_columns_selection, data):
    selected_labels_text = ', '.join(options)
    doc, tag, text = Doc().tagtext()
    step1_report = ReportGeneration(doc, tag, text)

    with tag('html'):
        with tag('head'):
            doc.stag('link', rel='stylesheet', href='style.css')
        with tag('body'):
            with tag('h1'):
                text('Data Analysis Report - Step 1')

            if 'dim' in selected_labels_text:
                doc.stag('hr')  # Horizontal line for separation
                with tag('div'):
                    step1_report.print_number_of_entries_columns(data)
            if 'col' in selected_labels_text:
                doc.stag('hr')  # Horizontal line for separation
                with tag('h3'):
                    text('Columns\' labels of dataframe are listed below : ')
                with tag('div'):
                    step1_report.print_columns_as_html_table(data)
            if 'hd' in selected_labels_text:
                doc.stag('hr')  # Horizontal line for separation
                with tag('h3'):
                    text('First and last rows of the  dataframe : ')
                with tag('div'):
                    step1_report.print_first_and_last_rows_as_html_table(data)
            if 'info' in selected_labels_text:
                doc.stag('hr')  # Horizontal line for separation
                with tag('h3'):
                    text('Concise Summary of dataframe : ')
                with tag('div'):
                    step1_report.print_info_as_html_table(data)
            if 'descr' in selected_labels_text:
                doc.stag('hr')  # Horizontal line for separation
                with tag('h3'):
                    text('Descriptive Statistics of dataframe : ')
                with tag('div'):
                    step1_report.print_describe_as_html_table(data)
            if 'uniq' in selected_labels_text:
                doc.stag('hr')  # Horizontal line for separation
                with tag('h3'):
                    text('Unique values per column')
                with tag('div'):
                    for column in un_columns_selection:
                        step1_report.print_unique_values_per_column(data, column)
    html_document = doc.getvalue()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Relative path to reports directory
    relative_path = os.path.join(base_dir, "../reports", "basic_information_report.html")
    with open(relative_path, 'w') as f:
        f.write(html_document)

    webbrowser.open_new_tab("file://" + os.path.abspath(relative_path))