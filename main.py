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
                    \n音声の自然さ・・・音声が自然にきこえるか、滑らかであるか、聞きやすいか
                    \n音は何度聞き返してもかまいません。評価がおわりましたら「次の試験音へ」のボタンを押してください
                    \n 
                    \n  """#教示文

def inc_count():
    st.session_state.count += 1
    # print(st.session_state.count)
    # ページの更新
    st.experimental_rerun()

# 一度だけ実行
@st.cache
def deyTimeCheck(alpha, beta):
    dt_now = str(datetime.date.today())
    return str(alpha + beta + dt_now)
    
# スライドバーから、数値を返す
def format_func1(option):
    return CHOICES1[option]

def format_func2(option):
    return CHOICES2[option]

def format_func3(option):
    return CHOICES3[option]

if 'count' not in st.session_state: #ページ番号をつかさどっている
    st.session_state.count = -2
if 'group' not in st.session_state:
    st.session_state.group = -1
if 'key' not in st.session_state:
    st.session_state.key = 'value'
if 'time' not in st.session_state:
    st.session_state.time = 0
if 'time2' not in st.session_state:
    st.session_state.time2 = 0    

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
    st.session_state.count = -1
    csv_file = os.listdir(conf.exp_folder_path + '/result_each_subject')
  
elif submitted:
    st.warning('名前を入力して下さい')
    
    
if st.session_state.count == -2:
    sizi = st.empty()
    sizi.subheader('提示音サンプル')
    sizi2 = st.empty()
    sizi2.write('評価対象音源のサンプルをお聞きください．')
    sizi3 = st.empty()
    sizi3.write('※まだ実験は始まっていません')
    
    st.header('クラシック')
    st.write('リファレンス音源\n')
    audio_file=open('Test1_reference_60_classics.wav','rb')
    st.write('１．')
    st.write(' 音源1')
    audio_file1=open('Test1_AFC_60_classics.wav','rb')
    st.audio(audio_file1.read())
    st.write(' 音源2')
  　audio_file2=open('Test1_AFC_60_classics.wav','rb')
    st.audio(audio_file2.read())
    st.radio('よりリファレンス音源に近い音源を選択してください。',('音源1','音源2'))
    
    st.write('2．')
    st.write(' 音源1')
    audio_file3=open('Test1_AFC_60_classics.wav','rb')
    st.audio(audio_file3.read())
    st.write(' 音源2')
  　audio_file4=open('Test1_B_PEM_AFC_60_classics.wav','rb')
    st.audio(audio_file4.read())
    st.radio('よりリファレンス音源に近い音源を選択してください。',('音源1','音源2'))



