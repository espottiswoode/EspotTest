# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu



# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

Python_output_df = ... # Compute a Pandas dataframe to write into Python_output


# Write recipe outputs
Python_output = dataiku.Dataset("Python_output")
Python_output.write_with_schema(Python_output_df)
