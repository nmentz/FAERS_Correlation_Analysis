"""
    Nathan Mentze
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from enum import Enum

class FAERDataFiles (Enum):
    """
        These are the keys for the files provided in 
        a FDA FAER quarterly report. This python script 
        is intended to handle these reports.
    """
    DEMO = 0
    DRUG = 1
    INDI = 2
    OUTC = 3
    REAC = 4
    RPSR = 5
    THER = 6

class DataAnalysis:

    """
        This class handles FDA FAER quarters. 

        The entire goal of this program is to show some data
        for the advertising budgets of certain drugs and 
        the amount of Food and Drug Administration 
        Adverse Event Reporting System. This class counts 
        the amount of adverse events reported per quarter. 
    """

    def __get_txt_files (self, dirpath) -> tuple:
        """
            Return a list of files ending with a .txt inside dirpath.
        """
        txt_files = []
        for file in os.listdir(dirpath): # Exception is automatically raised
            if file.endswith('.txt'):    # if dirpath doesn't exist.
                txt_files.append(os.path.join(dirpath, file))
        if not txt_files:
            raise Exception (f"No data files found in {dirpath}.")
        return tuple(txt_files)
    
    def __check_filenames (self, files):
        """
            This program is specifically intended to analyze quarterly 
            FDA FAER ASCII (not XML) reports. Which can be downloaded here
                https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html

            The program treats these txt files like they are dynamic;
            They aren't, to make anything resembling a meaningful 
            analysis on the data, I want to ensure I have all of the
            data files that a quarterly FAER report provides.

            This function forces the user to provide sufficient data by 
            ensuring the following files are in the user-provided directory:
                DEMOxxQx.txt
                DRUGxxQx.txt
                INDIxxQx.txt
                OUTCxxQx.txt
                REACxxQx.txt
                RPSRxxQx.txt
                THERxxQx.txt
        """
        files = ''.join(files)
        required_files = FAERDataFiles.__members__.keys()
        for i in required_files:
            if i not in files:
                raise Exception (f"Missing file {i}xxQx.txt")

    @property
    def faer_files (self):
        return self._faer_files

    @faer_files.setter
    def faer_files (self, path):
        f = self.__get_txt_files (path)
        self.__check_filenames (f)
        self._faer_files = f

    def __load_dataframes (self) -> tuple:
        """
            Load the data frame files dynamically into a list, return tuple.
        """
        dataframes = []
        files = FAERDataFiles.__members__.keys()
        for i in files:
            path = self.faer_files[FAERDataFiles[i].value]
            dataframes.append(
                pd.read_csv(
                    path, sep="$", low_memory=False
                )
            )
        return tuple(dataframes) if dataframes else None

    def __merge_dataframes (self, dataframes):
        """
            Merge all of the dataframes into one massive dataframe.

            Up until this point, the program has loaded all of the text
            files into a tuple of pandas DataFrame objects. But for what 
            I'm doing, I just want the DRUGS and REAC data.

            If someone were to take this program and do their own FDA FAER 
            data manipulation, this function is where to begin playing around.

            Here's some psuedo code

            merged = dataframes[0]
            for df in dataframes[1:]:
                merged = merged.merge (
                    df, on="primaryid", how="left"
                )
        """

        # Combine DRUG and REAC dataframes
        merged = dataframes[FAERDataFiles.DRUG.value]
        merged = merged.merge(dataframes[FAERDataFiles.REAC.value])

        return merged

    def __init__ (self, pathTo_faer_files, drug_reports):

        # self.faer_files is a tuple of the txt files
        # that are provided in a FDA FAER quarterly download
        self.faer_files = pathTo_faer_files

        # dataframes = a tuple of dataframes created from self.faer_files
        if not (dataframes := self.__load_dataframes ()):
            raise Exception ("No dataframes were loaded!")
        
        merged_dataframes = self.__merge_dataframes (dataframes)

        # This dataframe or 'df' object is what I want, no more boilerplate nonsense!
        df = merged_dataframes[['primaryid', 'caseid', 'drugname', 'drug_rec_act']]

        # Here, values are appended to drug reports for the respective quarter
        for key in drug_reports.keys():
            drug_reports[key][0] += df[df['drugname'] == key].shape[0]

def build_df (drug_map, dirpath):
    """
        A nice little function that builds pandas dataframes.
    """
    for q in dirpath:
        # Using q instead of i because it's qt... 
        # We are iterating through FAERS quarters.
        DataAnalysis(q, drug_map)

    highest_budget = []
    for drug, (reports, budget) in drug_map.items():
        highest_budget.append([drug, reports, budget])

    return pd.DataFrame(highest_budget, columns=['Drug Name', 'Reports', 'Advertising Budget'])


def main():
    try:

        faer_quarters = (
            "faers_ascii_2024Q1/ASCII",
            "faers_ascii_2024Q2/ASCII",
            "faers_ascii_2024Q3/ASCII",
            "faers_ascii_2024Q4/ASCII"
        )

        """
            Drugs with the highest advertising budget
            https://www.fiercepharma.com/marketing/abbvie-pulls-hat-trick-3rd-straight-year-top-tv-drug-ad-spender-buoyed-skyrizi-and-rinvoq
        """
        highest_budget_drugs_of_2024 = {
            # "DRUG NAME": FAER FDA Reports, advertising budget

            # brand name
            "SKYRIZI":  [0, 376.7],
            "RINVOQ":   [0, 337.8],
            "DUPIXENT": [0, 276.0],
            "WEGOVY":   [0, 261.1],
            "REXULTI":  [0, 223.6],
            "TREMFYA":  [0, 160.8],
            "JARDIANCE":[0, 131.7],
            "OZEMPIC":  [0, 124.4],
            "VRAYLAR":  [0, 117.7],
        }

        df_highest_budget = build_df (highest_budget_drugs_of_2024, faer_quarters)

        generic_counterparts = {
            # "DRUG NAME": FAER FDA Reports, advertising budget

            # generics are given the same price as their brand-name counterparts
            # because it mains consistency in categorization
            "RISANKIZUMAB-RZAA":[0, 376.7],
            "UPADACITINIB":     [0, 337.8],
            "DUPILUMAB":        [0, 276.0],
            "SEMAGLUTIDE":      [0, 261.1],
            "BREXPIPRAZOLE":    [0, 223.6],
            "GUSELKUMAB":       [0, 160.8],
            "EMPAGLIFLOZIN":    [0, 131.7],
            "SEMAGLUTIDE":      [0, 124.4],
            "CARIPRAZINE":      [0, 117.7],
        }

        df_generics = build_df (generic_counterparts, faer_quarters)





        plt.figure(figsize=(12, 8))

        sns.scatterplot(
            x='Reports',
            y='Advertising Budget',
            data=df_highest_budget,
            label="Brand-name Drugs",
            color='blue'
        )

        sns.scatterplot(
            x='Reports',
            y='Advertising Budget',
            data=df_generics,
            label="Generic Drugs",
            color='red',
            marker='X',
            s=100      
        )

        for i in range(df_highest_budget.shape[0]):
            plt.text(
                df_highest_budget['Reports'][i] + 0.5,
                df_highest_budget['Advertising Budget'][i] + 0.5,
                df_highest_budget['Drug Name'][i],
                fontsize=9,
                ha='left',
                va='bottom',
                color='black'
            )

        for i in range(df_generics.shape[0]):
            plt.text(
                df_generics['Reports'][i] - 0.5,
                df_generics['Advertising Budget'][i] + 0.5,
                df_generics['Drug Name'][i],
                fontsize=9,
                ha='right',
                va='bottom',
                color='darkred'
            )

        plt.title("Reports vs. Advertising Budget")
        plt.xlabel("Reports")
        plt.ylabel("Advertising Budget")
        plt.legend()
        plt.show()

    except Exception as e:
        print (f"Exception caught!\n\t{e}")
    return

if __name__ == "__main__":
    main()