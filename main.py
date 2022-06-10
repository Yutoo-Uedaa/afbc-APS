import os
import time
import datetime
import pandas as pd
import streamlit as st
import numpy as np
import pickle


kyouji = """本実験は、エントレインメント抑制機能の性能評価として、通常のNLMS、周波数シフトを用いたNLMS、提案手法の音声を聴き比べ評価するものです。
                    \n提示された基準音と評価音の二つを聴き比べ、基準音にどちらが近い音かを評価してください。
                    \n６つの音源を聞き比べる
                    \n　　・クラシック
                    \n　　・鐘の音
                    \n　　・救急車のサイレン音
                    \n　　・ドアベル
                    \n　　・電話のコール音
                    \n　　・英語の音声
                    \n・音声の自然さ 　 　・・・音声が自然にきこえるか、滑らかであるか、聞きやすいか
                    \n音は何度聞き返してもかまいません。評価がおわりましたら「次の試験音へ」のボタンを押してください
                    \n 
                    \n  """#教示文

def inc_count():
    st.session_state.count += 1
    # print(st.session_state.count)
    # ページの更新
    st.experimental_rerun()

st.title('APS評価実験')
explainBef = st.empty()
with explainBef.expander("実験の説明", True):
    st.write(kyouji)

sizi = st.empty()
sizi.subheader('実験前のお願い')

explain = st.empty()
sizi2 = st.empty()
sizi2.write('本実験はヘッドホンでの参加をお願い致します。''こちらの音が聞きやすい大きさでPCの音量を調節し実験中はいじらないでください')

with explain.form("my_form"):
    sub_name = st.text_input("名前を入力してください   　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　""　　　　　 　　　　  　　　　　 ""例：リオン太郎さんの場合 >>>　t_rion")
    sub_age = st.selectbox('年代を選択してください', ('20代', '30代', '40代', '50代', '60代', '非公表',))
    submitted = st.form_submit_button("次へ")

if submitted and sub_name != "":
    st.session_state.key = str(deyTimeCheck(str(sub_name), str(sub_age)))
    explainBef.empty()
    explain.empty()
    sizi.empty()
    sizi2.empty()
    sizi3.empty()
  
elif submitted:
    st.warning('名前を入力して下さい')
    
    
sizi = st.empty()
sizi.subheader('提示音サンプル')
sizi2 = st.empty()
sizi2.write('評価対象音源のサンプルをお聞きください．')
sizi3 = st.empty()
sizi3.write('※まだ実験は始まっていません'
    
st.header('クラシック')
st.write('音源1')

st.write('音源2')
  
st.radio('音源選択',('音源1','音源2'))

"""
##　鐘の音
"""

