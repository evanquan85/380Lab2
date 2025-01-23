import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('data/B01 Sam NCV.xlsx', sheet_name='Sam Wrist (B01)')
df2 = pd.read_excel('data/B01 Sam NCV.xlsx', sheet_name='Sam Elbow (B01)')
print(df.shape)
print(df2
