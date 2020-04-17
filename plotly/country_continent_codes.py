# -*- coding: utf-8 -*-

# Copyright (c) ALT-F1 SPRL, Abdelkrim Boujraf. All rights reserved.
# Licensed under the EUPL License, Version 1.2. See LICENSE in the project root for license information.

import pandas as pd
import numpy as np

class CountryContinentCodes:

    def __init__(self):
        self.df = pd.read_csv(
            'https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv',
            sep=',',
            usecols=['alpha-3', 'region'],
            #dtype={"region": str, "alpha-3": str},
            # dtype=str
            index_col='alpha-3'
        )

    def data(self):
        return self.df

    """
        clease the data : 
        - drop the NaN from the DataFrame
    """
    def cleanse(self):
        df = self.df.dropna()
        return df

    """
        create a dictionnary including alpha3:region (continent)
        Useful to create a column with the region/continents based on a alpha-3 code
    """
    def map(self):
        return self.df['region'].to_dict()