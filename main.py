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
                    \n音は何度聞き返してもかまいません。評価がおわりましたら「次の試験音へ」のボタンを押してください""" #教示文

def inc_count():
    st.session_state.count += 1
    # print(st.session_state.count)
    # ページの更新
    st.experimental_rerun()


st.title('APS評価実験')
st.write(kyouji)


if st.button('click here!'):
  st.write('音源１')
  
if st.checkbox('Show image'):
  img = Image.open('anaconda.png')
  st.image(img, caption='Anaconda Image', use_column_width=True)


