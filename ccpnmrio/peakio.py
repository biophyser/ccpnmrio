
import pandas as pd
import re


def read_ccp(filepath):
    """
    Reads in a peak list exported from the Peak:Peak Lists:Peak Table window of
    the ccpnmr analysis program and adds the residue number(s) and single-letter
    amino acid names in separate columns.

    Parameters
    ----------

    """
    df = pd.read_csv(filepath, sep='\t', index_col=0)
    _addResNumCols(df)
    return df

def _pullName(entry):
    try:
        name = re.findall(r'[A-Z][a-z]{2}', entry)[0]
    except:
        name = 'X'
    return name

def _pullNum(entry):
    return str(re.findall(r'\d+', entry)[0])


def _nameAndNum(assignSeries):
    """
    Pulls the residue name(s) and number(s) from a ccpnmr assignment string that is usually
    of the form 109LeuN or (25Lys/45Leu)N for multiple assignments.

    Output:
    A string of each residue name separated by '-', for example:
    Leu and 109 or Lys-Leu and 25-45
    """

    nameList, numList = list(), list()

    for n, assignment in enumerate(assignSeries):
        intList = assignment.split('/')
        if len(intList) == 1:
            resName = _pullName(intList[0])
            resNum  = _pullNum(intList[0])
        else:
            tempName = []
            tempNum = []
            for item in intList:
                tempName.append(_pullName(item))
                tempNum.append(_pullNum(item))
            resName = '-'.join(tempName)
            resNum = '-'.join(tempNum)
        nameList.append(resName)
        numList.append(resNum)
    return nameList, numList



def _addResNumCols(df):
    """
    Add columns to a pandas dataframe that contain just the residue name and
    number separately. Adding columns for each
    """

    cols = ['Assign F1', 'Assign F2']
    for n, col in enumerate(cols):
        resn, index = _nameAndNum(df[col])
        df['resname{}'.format(n+1)] = resn
        df['resnum{}'.format(n+1)]  = index

def _cull_assign(df):
    _addResNumCols(df)
    return df[df.resname1 != 'X']

def _reset_index(df):
    return _cull_assign(df).set_index('resnum1').sort_index()
