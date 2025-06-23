
import pandas as pd
import os

class CSVManager:
    """
    A class to manage a CSV file as a database-style object,
    allowing for querying, adding, updating, and saving changes.
    """
    def __init__(self, filepath, index_col=None):
        """
        Initializes the CSVManager.

        Args:
            filepath (str): The path to the CSV file.
            index_col (str, optional): The name of the column to use as the
                                       DataFrame index. If None, a default
                                       integer index is used.
        """
        self.filepath = filepath
        self.data = self._load_csv(index_col)
        print(f"CSV '{filepath}' loaded successfully. Shape: {self.data.shape}")

    def _load_csv(self, index_col):
        """Loads the CSV file into a pandas DataFrame."""
        if not os.path.exists(self.filepath):
            print(f"Warning: CSV file '{self.filepath}' not found. Creating an empty DataFrame.")
            return pd.DataFrame() # Return empty DataFrame if file doesn't exist
        try:
            # Try to infer index column or use specified one
            if index_col:
                df = pd.read_csv(self.filepath, index_col=index_col)
            else:
                df = pd.read_csv(self.filepath)
            return df
        except pd.errors.EmptyDataError:
            print(f"Warning: CSV file '{self.filepath}' is empty. Creating an empty DataFrame.")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return pd.DataFrame() # Return empty DataFrame on other errors

    def query(self, condition_func=None, columns=None):
        """
        Queries the data based on a condition function and/or selects specific columns.

        Args:
            condition_func (callable, optional): A function that takes a row (Series)
                                                 and returns True if the row matches
                                                 the query, False otherwise.
                                                 E.g., `lambda row: row['Age'] > 30`.
                                                 If None, all rows are returned.
            columns (list, optional): A list of column names to return.
                                      If None, all columns are returned.

        Returns:
            pd.DataFrame: A new DataFrame containing the queried data.
        """
        if self.data.empty:
            print("No data to query. DataFrame is empty.")
            return pd.DataFrame()

        queried_data = self.data.copy() # Work on a copy to avoid accidental modification

        if condition_func:
            # Apply the condition function to filter rows
            queried_data = queried_data[queried_data.apply(condition_func, axis=1)]

        if columns:
            # Select specific columns, ensuring they exist
            existing_columns = [col for col in columns if col in queried_data.columns]
            if len(existing_columns) < len(columns):
                missing = set(columns) - set(existing_columns)
                print(f"Warning: The following columns were not found and will be ignored: {missing}")
            queried_data = queried_data[existing_columns]

        return queried_data

    def add_row(self, row_data):
        """
        Adds a new row to the DataFrame.

        Args:
            row_data (dict): A dictionary where keys are column names and values
                             are the data for the new row.
                             Missing columns will be filled with NaN.
        """
        # Ensure the new row DataFrame has the same columns as the existing data
        # and fill missing columns with NaN to avoid pandas alignment issues.
        new_row_df = pd.DataFrame([row_data])
        # Reindex to match self.data columns, adding NaN for missing ones
        new_row_df = new_row_df.reindex(columns=self.data.columns, fill_value=None)

        self.data = pd.concat([self.data, new_row_df], ignore_index=True)
        print(f"Row added. New shape: {self.data.shape}")


    def update_data(self, condition_func, updates):
        """
        Updates cells in rows that match a given condition.

        Args:
            condition_func (callable): A function that takes a row (Series)
                                       and returns True if the row should be updated.
                                       E.g., `lambda row: row['Status'] == 'Pending'`.
            updates (dict): A dictionary where keys are column names to update
                            and values are the new values. Values can be static
                            or a callable function that takes a row (Series) and
                            returns the new value for that cell.
                            E.g., `{'Status': 'Completed', 'Age': lambda row: row['Age'] + 1}`.
        """
        if self.data.empty:
            print("No data to update. DataFrame is empty.")
            return

        # Find indices of rows to update
        # Using boolean indexing is often more efficient than apply for simple conditions
        # However, the prompt specified condition_func takes a row, so sticking to apply
        rows_to_update_mask = self.data.apply(condition_func, axis=1)
        rows_to_update_indices = self.data[rows_to_update_mask].index


        if rows_to_update_indices.empty:
            print("No rows matched the update condition.")
            return

        for col, value in updates.items():
            if col in self.data.columns:
                if callable(value):
                    # If the value is a function, apply it row-wise to the filtered rows
                    self.data.loc[rows_to_update_indices, col] = self.data.loc[rows_to_update_indices].apply(value, axis=1)
                else:
                    # Otherwise, set the static value for the filtered rows
                    self.data.loc[rows_to_update_indices, col] = value
            else:
                print(f"Warning: Column '{col}' not found for update. Skipping.")
        print(f"Updated {len(rows_to_update_indices)} rows.")

    def delete_rows(self, condition_func):
        """
        Deletes rows that match a given condition.

        Args:
            condition_func (callable): A function that takes a row (Series)
                                       and returns True if the row should be deleted.
                                       E.g., `lambda row: row['Status'] == 'Completed'`.
        """
        if self.data.empty:
            print("No data to delete. DataFrame is empty.")
            return

        original_shape = self.data.shape[0]
        # Create a boolean mask for rows to keep
        rows_to_keep_mask = ~self.data.apply(condition_func, axis=1)
        self.data = self.data[rows_to_keep_mask].reset_index(drop=True)
        deleted_count = original_shape - self.data.shape[0]
        print(f"Deleted {deleted_count} rows. New shape: {self.data.shape}")


    def save_changes(self, output_filepath=None, **kwargs):
        """
        Saves the current state of the DataFrame back to a CSV file.

        Args:
            output_filepath (str, optional): The path to save the updated CSV.
                                             If None, it overwrites the original file.
            **kwargs: Additional keyword arguments to pass to pandas.DataFrame.to_csv().
                      (e.g., `index=False` to prevent writing the DataFrame index).
        """
        path_to_save = output_filepath if output_filepath else self.filepath
        try:
            self.data.to_csv(path_to_save, **kwargs)
            print(f"Changes saved successfully to '{path_to_save}'.")
        except Exception as e:
            print(f"Error saving changes to CSV: {e}")

# Note: The example usage block (__main__) is removed
# as this file is intended to be part of a package, not a standalone script.
