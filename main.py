import os
import time
import datetime
import pandas as pd
import streamlit as st
import numpy as np
import pickle
import csv


kyouji = """本実験は、エントレインメント抑制機能の性能評価として、通常のNLMS、周波数シフトを用いたNLMS、提案手法の音声を聴き比べ評価するものです。
                    \n提示された基準音と評価音の二つを聴き比べ、基準音にどちらが近い音かを評価してください。
                    \n６つの音源によって調査を行う。
                    \n　　・クラシック
                    \n　　・鐘の音
                    \n　　・救急車のサイレン音
                    \n　　・ドアベル
                    \n　　・電話のコール音
                    \n　　・英語の音声
                    \n音源の到来方向が右側からになっています
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
    st.session_state.count = -21
if 'group' not in st.session_state:
    st.session_state.group = -1
if 'key' not in st.session_state:
    st.session_state.key = 'value'
    st.select1_1='value'
    st.select1_2='value'
    st.select1_3='value'
    st.select2_1='value'
    st.select2_2='value'
    st.select2_3='value'
    st.select3_1='value'
    st.select3_2='value'
    st.select3_3='value'
    st.select4_1='value'
    st.select4_2='value'
    st.select4_3='value'
    st.select5_1='value'
    st.select5_2='value'
    st.select5_3='value'
    st.select6_1='value'
    st.select6_2='value'
    st.select6_3='value'
if 'time' not in st.session_state:
    st.session_state.time = 0
if 'time2' not in st.session_state:
    st.session_state.time2 = 0    
    

if st.session_state.count == -21:
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
        st.session_state.count = -20
    elif submitted:
        st.warning('名前を入力して下さい')
    
    
if st.session_state.count == -20:
    sizi = st.empty()
    sizi.subheader('提示音サンプル')
    sizi2 = st.empty()
    sizi2.write('評価対象音源のサンプルを聞き音量を調整してください．')
    sizi3 = st.empty()
    sizi3.write('※まだ実験は始まっていません')
    
    start = st.empty()
    with start.form("my_form2"):
        start_button= st.form_submit_button("実験を始める")
    if start_button:
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        start.empty()
        st.session_state.count = -19
        
# クラシック AFC/FS
if st.session_state.count == -19:
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*1))
    sizi = st.empty()
    sizi.header('１ー１．クラシック')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源（リファレンス音源は何回聞いても問題ありません）')
    sizi3=st.empty()
    audio_file=open('Test1_reference_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5=st.empty()
    audio_file=open('Test1_AFC_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7=st.empty()
    audio_file=open('Test1_FS_AFC_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select1=sel1.radio('1-1.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select1_1=select1 
      
    nex=st.empty()
    next1_button=nex.button('次の音源へ(2/18)')
    if next1_button:
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -18
    
#  classic AFC/B-PEM-AFC    
if st.session_state.count == -18: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*2))
    sizi = st.empty()
    sizi.header('１ー２．クラシック')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源（リファレンス音源は何回聞いても問題ありません）')
    sizi3=st.empty()
    audio_file=open('Test1_reference_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test1_AFC_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test1_B_PEM_AFC_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select2=sel1.radio('1-2.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select1_2=select2 
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(3/18)')
    if next1_button:
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -17
        
#  FS-AFC/B-PEM-AFC
if st.session_state.count == -17: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*3))
    sizi = st.empty()
    sizi.header('１ー３．クラシック')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源（リファレンス音源は何回聞いても問題ありません）')
    sizi3=st.empty()
    audio_file=open('Test1_reference_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test1_FS_AFC_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test1_B_PEM_AFC_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select3=sel1.radio('1-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select1_3=select3 
    df = pd.DataFrame({'1': [st.session_state.key], '2': ['クラシック'], '3': [st.select1_1], '4': [st.select1_2], '5': [st.select1_3]})
    st.dataframe(df)
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(4/18)')
    if next1_button:
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -16
    

# bell AFC/FS
if st.session_state.count == -16:
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*4))
    sizi = st.empty()
    sizi.header('２ー１．鐘の音')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源（リファレンス音源は何回聞いても問題ありません）')
    sizi3=st.empty()
    audio_file=open('Test2_reference_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5=st.empty()
    audio_file=open('Test2_AFC_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7=st.empty()
    audio_file=open('Test2_FS_AFC_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select1=sel1.radio('2-1.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select2_1=select1       
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(5/18)')
    if next1_button:
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -15
    
#  鐘の音 AFC/B-PEM-AFC    
if st.session_state.count == -15: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*5))
    sizi = st.empty()
    sizi.header('２ー２．鐘の音')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源（リファレンス音源は何回聞いても問題ありません）')
    sizi3=st.empty()
    audio_file=open('Test2_reference_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test2_AFC_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test2_B_PEM_AFC_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select2=sel1.radio('2-2.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select2_2=select2  
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(6/18)')
    if next1_button:
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -14
        
#   鐘の音　FS-AFC/B-PEM-AFC
if st.session_state.count == -14: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*6))
    sizi = st.empty()
    sizi.header('２ー３．クラシック')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源（リファレンス音源は何回聞いても問題ありません）')
    sizi3=st.empty()
    audio_file=open('Test2_reference_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test2_FS_AFC_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test2_B_PEM_AFC_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select3=sel1.radio('2-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select2_3=select3  
    df = pd.DataFrame({'1': [st.session_state.key,st.session_state.key], '2': ['クラシック','鐘の音'], '3': [st.select1_1,st.select2_1], '4': [st.select1_2,st.select2_2], '5': [st.select1_3,st.select2_3]})
    st.dataframe(df)
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(7/18)')
    if next1_button:
        
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -13

# siren AFC/FS
if st.session_state.count == -13:
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*7))
    sizi = st.empty()
    sizi.header('３ー１．救急車のサイレン')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源（リファレンス音源は何回聞いても問題ありません）')
    sizi3=st.empty()
    audio_file=open('Test3_reference_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5=st.empty()
    audio_file=open('Test3_AFC_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7=st.empty()
    audio_file=open('Test3_FS_AFC_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select1=sel1.radio('3-1.リファレンス音源に近い音源を選択してください。',('1','2'))
      
    nex=st.empty()
    next1_button=nex.button('次の音源へ(8/18)')
    if next1_button:
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -12
    
#  siren AFC/B-PEM-AFC    
if st.session_state.count == -12: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*8))
    sizi = st.empty()
    sizi.header('３ー２．救急車のサイレン')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源（リファレンス音源は何回聞いても問題ありません）')
    sizi3=st.empty()
    audio_file=open('Test3_reference_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test3_AFC_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test3_B_PEM_AFC_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select2=sel1.radio('3-2.リファレンス音源に近い音源を選択してください。',('1','2'))

    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(9/18)')
    if next1_button:
        # df.to_csv('data/outresult_sample3.csv', mode='a',header=False, index=False, encoding='utf_8_sig')
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -11
        
#   救急車のサイレン　FS-AFC/B-PEM-AFC
if st.session_state.count == -11: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*9))
    sizi = st.empty()
    sizi.header('３ー３．救急車のサイレン')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源（リファレンス音源は何回聞いても問題ありません）')
    sizi3=st.empty()
    audio_file=open('Test3_reference_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test3_FS_AFC_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test3_B_PEM_AFC_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select3=sel1.radio('3-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    # df = pd.DataFrame({'1': [st.session_state.key], '2': ['クラシック'], '3': [select1], '4': [select2], '5': [select3]})
    #st.dataframe(df)
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(10/18)')
    if next1_button:
        #df.to_csv('data/outresult_sample3.csv', mode='a',header=False, index=False, encoding='utf_8_sig')
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -5
 
if st.session_state.count == -5:
    my_bar = st.progress(0)
    my_bar.progress(int(100/6*6))
    st.write('結果')
    wine = pd.read_csv("data/outresult_sample3.csv")
    st.dataframe(wine)
        
    st.title('実験は終了です。ご協力ありがとうございました。ブラウザを閉じてください')
        
        
    st.balloons()
    st.stop()




