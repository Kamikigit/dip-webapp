# -*- coding: utf-8 -*-
from time import sleep
import pandas as pd
import pickle
import lightgbm
import os

""" 予測 """
class PredictAPI:
    def __init__(self):
        # 推論モデルの読み込み
        self.model = pickle.load(open('trained_model.pkl', 'rb'))
  
    def predict(self, test):
        # データ整形
        test_col =[]
        for column in test.columns:
            if test[column].isnull().sum() == False and (test[column].dtypes == int or test[column].dtypes == float ):
                test_col.append(column)
        test = test[test_col]

        # 推論
        pred = self.model.predict(test)
        # 提出用
        submit = pd.DataFrame({"お仕事No.":test["お仕事No."], "応募数 合計":pred})
        return submit

