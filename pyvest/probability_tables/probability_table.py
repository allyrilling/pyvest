import ipywidgets as widgets
import pandas as pd  # Import pandas
from IPython.display import display, clear_output

class ProbabilityTable:
    def __init__(self):
        # Initialize text fields for row and column input
        self.rows_input = widgets.IntText(
            value=2, description="Rows:", style={'description_width': 'initial'}
        )
        self.cols_input = widgets.IntText(
            value=2, description="Columns:", style={'description_width': 'initial'}
        )

        # Initialize the 'Create Table' button
        self.create_table_button = widgets.Button(description="Create Table")

        # Output area for displaying the table and messages
        self.output_area = widgets.Output()

        # Stored values for table inputs
        self.stored_values = []

        # Private property to hold the table as a DataFrame
        self.__table = pd.DataFrame()

        # Setup event handlers
        self.create_table_button.on_click(self.on_create_table_clicked)

        # Display initial UI elements
        display(self.rows_input, self.cols_input, self.create_table_button, self.output_area)

    def on_create_table_clicked(self, b):
        with self.output_area:
            clear_output(wait=True)
            self.display_table(self.rows_input.value, self.cols_input.value)

    def display_table(self, r, c):
        # Create text widgets for table inputs
        text_widgets = [
            widgets.Text(
                value=str(self.stored_values[i * c + j]) if i * c + j < len(self.stored_values) else "",
                placeholder=f"R{i+1}C{j+1}",
                description='',
                layout=widgets.Layout(width='70px')  # Smaller input fields
            )
            for i in range(r) for j in range(c)
        ]

        self.text_widgets = text_widgets  # Store reference to widgets for later use

        # Layout for the grid of text widgets
        grid = widgets.GridBox(
            text_widgets,
            layout=widgets.Layout(grid_template_columns=f"repeat({c}, auto)")
        )

        # Button to submit table values
        submit_values_button = widgets.Button(description="Submit Values")
        submit_values_button.on_click(lambda b: self.print_table_values(text_widgets, r, c))

        # Button to clear all values
        clear_values_button = widgets.Button(description="Clear All Values")
        clear_values_button.on_click(lambda b: self.clear_all_values(text_widgets))

        # Display the grid, submit button, and clear button
        display(grid, submit_values_button, clear_values_button)

    def print_table_values(self, widget_list, rows, cols):
        # Format and print the table values
        self.stored_values = [widget.value for widget in widget_list]
        formatted_values = [self.stored_values[i * cols: (i + 1) * cols] for i in range(rows)]
        self.__table = pd.DataFrame(formatted_values)  # Set the values into the DataFrame
        with self.output_area:
            clear_output(wait=True)
            print("Table Values:\n")
            print(self.__table.to_string(index=False, header=False))  # Print the DataFrame without column names

            # Display the 'Back to Table Input' button only after values are submitted
            back_button = widgets.Button(description="Back to Table Input")
            back_button.on_click(self.on_create_table_clicked)
            display(back_button)

    def clear_all_values(self, widget_list):
        # Clear all text fields
        for widget in widget_list:
            widget.value = ""
        # Clear stored values and the DataFrame
        self.stored_values = []
        self.__table = pd.DataFrame()

    # Method to safely access the __table property from outside the class
    @property
    def table(self):
        return self.__table.copy()  # Return a copy to prevent direct modification

    def fill_table(self, rows, cols, values):
        # Update the rows and cols input values
        self.rows_input.value = rows
        self.cols_input.value = cols

        # Update stored values with the provided list
        self.stored_values = values[:rows * cols]  # Ensure the list fits the table size

        # Re-display the table with the new values
        # self.display_table(rows, cols)

        text_widgets = [
            widgets.Text(
                value=str(self.stored_values[i * cols + j]) if i * cols + j < len(self.stored_values) else "",
                placeholder=f"R{i+1}C{j+1}",
                description='',
                layout=widgets.Layout(width='70px')  # Smaller input fields
            )
            for i in range(rows) for j in range(cols)
        ]
        self.print_table_values(text_widgets, rows, cols)