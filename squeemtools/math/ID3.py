import pandas as pd
import numpy as np
from scipy.stats import entropy

def total_entropy(df : pd.DataFrame) -> float:
    '''Gets the entropy of the entire dataset'''
    label = df.keys()[-1]

    # Gets the total entropy of the dataframe
    ent = entropy(df[label].value_counts(),base=2)
    return ent

def attribute_entropy(df : pd.DataFrame,attribute : str) -> float:
    '''Gets the entropy of a specific attribute'''
    label = df.keys()[-1]
    variables = df[attribute].unique()

    # Gets the entropy of the attribute
    ent = np.array([-(len(df[df[attribute] == variable]) / len(df)) * entropy(df[df[attribute]==variable][label].value_counts(),base=2) for variable in variables]).sum()
    return abs(ent)

def create_tree(df : pd.DataFrame) -> dict:
    '''ID3 decision tree creating algorithm. Requires df to be a pd.DataFrame, and that the label of the data is the last column'''
    label = df.keys()[-1]
    #Get attribute with maximum information gain
    node = df.keys()[:-1][np.argmax([total_entropy(df)-attribute_entropy(df,key) for key in df.keys()[:-1]])]

    #Get distinct value of that attribute
    att_values = df[node].unique()
    # Create the tree
    tree={}
    tree[node] = {}

    for att_value in att_values:
        # Create table with specific attribute
        subtable = df[df[node] == att_value].reset_index(drop=True)
        # Get how many outcomes there are for the attribute
        table_values,counts = np.unique(subtable[label],return_counts=True)

        # If there is only one outcome
        if len(counts) == 1:
            tree[node][att_value] = table_values[0]
        # If there is more than one outcome, need to create another node
        else:
            tree[node][att_value] = create_tree(subtable)
    return tree

def is_number(s) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False

def go(dic : dict, last_key : None, current_level : None) -> None:
    '''Prints the tree, best used with the wrapper. ONLY WORKS ON TREES WITH NUMERIC ENTRIES'''
    for key, value in dic.items():
        if is_number(key):
            for i in range(current_level - 1):
                print("| ", end="")

            print(last_key, "= ", end="")
            print(key, ": ", end="")
        else:
            if current_level > 0:
                print("")

            current_level = current_level + 1

        if isinstance(value, dict):
            go(value, key, current_level)
        else:
            print(value)

def print_tree(tree : dict) -> None:
    '''Prints the tree created with ID3 algorithm
       ONLY PRINTS PROPERLY WITH TREES WITH NUMERIC NODE ENTRIES'''
    go(tree,None,0)

def classify_series(data : pd.Series,tree : dict):
    '''Given a series, returns the tree's classification of the series
       data is a pd.Series object, and tree is a dict created with the ID3 algorithm'''
    label = tree
    while isinstance(label,dict):
        key = list(label.keys())[0]
        value = data[key]
        label = label[key][value]
    return label
