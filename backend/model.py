# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd 
# ダミー変数作成
from sklearn.preprocessing import LabelEncoder
import pickle
from optuna.integration import lightgbm as lgb
import os

""" 予測 """
def serving(test):
    # 推論モデルの読み込み
    model = pickle.load(open('trained_model.pkl', 'rb'))
    """ データ整形 """
    # データがすべて同じのカラムを抜き出す
    discard_data = ['勤務地\u3000最寄駅3（駅名）', '勤務地固定', '応募先\u3000名称', 
                    '勤務地\u3000最寄駅3（沿線名）', '（派遣先）勤務先写真コメント', 
                    '勤務地\u3000最寄駅3（分）', '無期雇用派遣', '未使用.14', '（派遣以外）応募後の流れ', 
                    '（派遣先）概要\u3000従業員数', '電話応対なし', '週払い', '週1日からOK',
                    '固定残業制 残業代 下限', 'ミドル（40〜）活躍中', 'ルーティンワークがメイン', 
                    '未使用.11', 'フリー項目\u3000内容', '先輩からのメッセージ', '対象者設定\u3000年齢下限', 
                    '未使用.10', '動画コメント', '未使用.8', '経験必須', '固定残業制 残業代に充当する労働時間数 下限',
                    '給与/交通費\u3000給与支払区分', 'ブロックコード2', '未使用.4', 'CAD関連のスキルを活かす',
                    '未使用.7', 'メモ', 'ブロックコード3', '固定残業制', 'WEB面接OK', '公開区分', '17時以降出社OK', 
                    '寮・社宅あり', '20代活躍中', '検索対象エリア', '就業形態区分', 'ネットワーク関連のスキルを活かす', 
                    'Wワーク・副業可能', '固定残業制 残業代に充当する労働時間数 上限', 'プログラム関連のスキルを活かす', 
                    '未使用.15', '30代活躍中', '未使用.12', 'エルダー（50〜）活躍中', '（派遣）応募後の流れ', '人材紹介', 
                    '主婦(ママ)・主夫歓迎', '雇用形態', 'Dip JobsリスティングS', 'ブロックコード1', 'フリー項目\u3000タイトル', 
                    '資格取得支援制度あり', '未使用.1', 'ブランクOK', '対象者設定\u3000年齢上限', '未使用.20', '社会保険制度あり', 
                    '募集形態', '勤務地\u3000最寄駅3（駅からの交通手段）', '応募先\u3000最寄駅（沿線名）', '仕事写真（下）\u3000写真1\u3000ファイル名', 
                    '未使用.16', '仕事写真（下）\u3000写真3\u3000ファイル名', 'オープニングスタッフ', 
                    '応募先\u3000所在地\u3000ブロックコード', '応募先\u3000所在地\u3000都道府県', 
                    '動画タイトル', '応募先\u3000最寄駅（駅名）', '残業月10時間未満', '外国人活躍中・留学生歓迎', 
                    '履歴書不要', '未使用.17', '未使用.9', '研修制度あり', '日払い', '未使用', '未使用.18', '未使用.22', 
                    '未使用.5', '勤務地\u3000周辺情報', '仕事写真（下）\u3000写真2\u3000ファイル名', 'バイク・自転車通勤OK', 
                    '仕事写真（下）\u3000写真2\u3000コメント', 'DTP関連のスキルを活かす', '未使用.3', '未使用.2', 
                    'WEB関連のスキルを活かす', '未使用.6', '給与\u3000経験者給与下限', '学生歓迎', '固定残業制 残業代 上限', 
                    '未使用.19', '給与\u3000経験者給与上限', '未使用.21', '待遇・福利厚生', 'シニア（60〜）歓迎', 'ベンチャー企業', 
                    '少人数の職場', '仕事写真（下）\u3000写真3\u3000コメント', '新卒・第二新卒歓迎', '産休育休取得事例あり', 
                    '動画ファイル名', '対象者設定\u3000性別', 'WEB登録OK', '応募先\u3000備考', '応募先\u3000所在地\u3000市区町村', 
                    '仕事写真（下）\u3000写真1\u3000コメント', '未使用.13', '応募拠点', 'これまでの採用者例', '（派遣先）概要\u3000勤務先名（フリガナ）']
            # 先程のカラムを削除
    test = test.drop(discard_data, axis=1)

    discard_data = []
    """### 雇用形態・会社情報のカラム"""
    discard_data.extend(['（派遣先）概要　事業内容', '（派遣先）勤務先写真ファイル名'])

    """### 給与に関するカラム"""
    def make_income(data):
        data['賞与'] = data['（紹介予定）年収・給与例'].str.extract('(賞与)', expand=False)
        data['賞与'] = data['賞与'].apply(lambda x: 1 if x == '賞与' else 0)
        # 賞与を作成した
        data['年収'] = data['（紹介予定）年収・給与例'].str.extract('((?<=年収).*?(?=万円))', expand=False)
        data['年収'] = data['年収'].apply(lambda x: x.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})) if type(x) != float else x)
        # 上限と下限を作成
        data['年収下限'] = data['年収'].str.replace('〜.*', '').str.replace('約', '').str.replace(":", "")
        data['年収上限'] = data['年収'].str.replace(".*?〜", '').str.replace('約', '').str.replace(":", "")
        # ''という空要素ができているので削除
        data['年収上限'] = data['年収上限'].apply(lambda x:np.nan if type(x) == str and len(x) == 0 else x)
        # float型に変換
        data['年収下限'] = data['年収下限'].astype(float)
        data['年収上限'] = data['年収上限'].astype(float)
        # 万単位なので数字に直す
        data['年収上限']
        data['年収上限'] = data['年収上限'].apply(lambda x: x * 10000 if not np.isnan(x) else x)
        data['年収下限'] = data['年収下限'].apply(lambda x: x * 10000 if not np.isnan(x) else x)
    make_income(test)
    discard_data.extend(['（紹介予定）年収・給与例', '年収'])

    # 名前を分かりやすくする
    def change_income(data):
        data['時給上限'] = data['給与/交通費\u3000給与上限']
        data['時給下限'] = data['給与/交通費\u3000給与下限']
        data['交通費'] = data['給与/交通費\u3000交通費']
    change_income(test)
    discard_data.extend(['給与/交通費\u3000給与上限', '給与/交通費\u3000給与下限', '給与/交通費\u3000備考'])

    """### 勤務地に関係するカラム"""
    # 数字を排除
    test['拠点番号'] = test['拠点番号'].str.extract('(\D+)', expand=False)
    test['勤務地　市区町村名'] = test['勤務地　備考'].str.extract('((?<=[都道府県]).*)', expand=False)

    """### 休日に関するカラム"""
    def make_date(data):
        data['休日休暇'] = data['（紹介予定）休日休暇'].str.extract('([0-9０-９]+)', expand=False)
        data['休日休暇'] = data['休日休暇'].apply(lambda x: x.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})) if type(x) != float else x)
        data['休日休暇'] = data['休日休暇'].astype(float)
        # 入社時期
        data['入社時期'] = data['（紹介予定）入社時期'].str.extract('([0-9]+)', expand=False).astype(float)
    make_date(test)
    discard_data.extend(['（紹介予定）休日休暇', '（紹介予定）入社時期'])

    """### 労働時間に関係するカラム"""
    discard_data.append("期間・時間　勤務開始日")
    test['勤務時間'] = test['期間・時間　勤務時間'].str.extract('(.*:.*〜.*:.[0-9])', expand=False)
    test['勤務開始時間'] = test['勤務時間'].str.extract('(.*(?=〜))', expand=False)
    test['勤務終了時間'] = test['勤務時間'].str.extract('((?<=〜).*)' , expand=False)
    discard_data.append('期間･時間\u3000備考')

    """### 応募方法・プロセスに関するカラム"""
    discard_data.extend(['掲載期間　開始日', '掲載期間　終了日'])

    """### カラム削除    """
    test = test.drop(discard_data, axis=1)

    """### ラベルエンコーディング"""
    for col in test:
        if test[col].dtypes == object:
            test[col] = test[col].fillna(test[col].mode().iloc[0])

    le = LabelEncoder()
    for col in test:
        if test[col].dtypes == object:
            d = test[col]
            le = le.fit(d)
            test[col] = le.transform(d)

    # 推論
    pred = model.predict(test)
    # 提出用
    submit = pd.DataFrame({"お仕事No.":test["お仕事No."], "応募数 合計":pred})
    return submit

