import csv

import pandas as pdf


def csv_to_list(path: str) -> list[str]:
    """
    Extracts the data from a csv file and returns it as a pandas dataframe
    """
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        data = []
        for row in reader:
            for i in range(len(row)):
                row[i] = row[i].replace('"', "") 
            data.append(row)
        ret= []
        for i in data:
            ret.append(i[0])
        return ret
    
    
    
if __name__ == "__main__":
    text = csv_to_list("C:/Users/aky547/Desktop/semap/71.csv")
    #remove linebreaks
    print(text)