import numpy as np
import pandas as pd


class DataAnalysis:
    """
    class that will handle all the calculation of data
    """

    def _load_data(self, file_path):
        """
        load the excel file and store it into a DataFrame
        Args:
         file_path [str]: path to the excel file
        Return:
            None
        """
        self.df = pd.read_excel(file_path, sheet_name=0)

    def get_statistics(self):
        """
        get statistics from the data
        Args:
            None
        Return:
            None
        """
        self.stats = self.df.describe()

    @staticmethod
    def create_object(file_path):
        """
        create a DataAnalysis object and loan onto it the data from an excel
        Args:
            file_path [str]: path to the excel file
        Return:
            DataAnalysis object
        """
        da = DataAnalysis()
        da._load_data(file_path)

        return da
