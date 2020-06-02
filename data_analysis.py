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

    def scatter_plot(self, fig, label_var1, label_var2, background_color='white'):
        X = self.df[label_var1]
        y = self.df[label_var2]

        axes = fig.add_subplot(1, 1, 1)
        axes.scatter(X, y, s=50, alpha=0.5)
        axes.set_title(f'{label_var2} vs {label_var1}')
        axes.set_xlabel(f'{label_var1}')
        axes.set_ylabel(f'{label_var2}')
        fig.set_edgecolor(background_color)
        fig.set_facecolor(background_color)
        axes.set_facecolor(background_color)

        return axes

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
