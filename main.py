import os
import time
import datetime
import pandas as pd
import streamlit as st
import numpy as np
import pickle

kyouji = """本実験は、雑音抑制機能の性能評価として、雑音の「大きさ」、音声の「大きさ」、「自然さ」を評価するものです。
                    \n提示された基準音と評価音を聴いて、相対的評価を以下の3つの観点から7段階で評価してください。
                    \n・雑音の大きさ 　　 ・・・雑音が大きいか、うるさいか
                    \n・音声の大きさ 　　 ・・・音声部分の音量感があるか（SNRでなく音声のみで評価）
                    \n・音声の自然さ 　 　・・・音声が自然にきこえるか、滑らかであるか
                    \n本実験では雑音の評価をおこなった後、雑音下音声の評価をしていただきます。
                    \n音は何度聞き返してもかまいません。評価がおわりましたら「次の試験音へ」のボタンを押してください""" #教示文

def inc_count():
    st.session_state.count += 1
    # print(st.session_state.count)
    # ページの更新
    st.experimental_rerun()


st.title('APS評価実験')

