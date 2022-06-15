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
    st.session_state.count = -10
if 'group' not in st.session_state:
    st.session_state.group = -1
if 'key' not in st.session_state:
    st.session_state.key = 'value'
if 'key' not in st.session_state: #結果
    st.result1.data = 'value'
if 'time' not in st.session_state:
    st.session_state.time = 0
if 'time2' not in st.session_state:
    st.session_state.time2 = 0    
    
if st.session_state.count == -10:  
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
        st.session_state.count = -9
        # csv_file = os.listdir(conf.exp_folder_path + '/result_each_subject')
  
    elif submitted:
        st.warning('名前を入力して下さい')
    
    
if st.session_state.count == -9:
    sizi = st.empty()
    sizi.subheader('提示音サンプル')
    sizi2 = st.empty()
    sizi2.write('評価対象音源のサンプルをお聞きください．')
    sizi3 = st.empty()
    sizi3.write('※まだ実験は始まっていません')
    
    start = st.empty()
    with start.form("my_form2"):
        start_button= st.form_submit_button("実験を始める")
    if start_button:
        df = pd.DataFrame({'1': ['名前'], '2': ['音源'], '3': ['テスト１(AFC/FS)'], '4': ['テスト２(AFC/B)'], '5': ['テスト３(FS/B)']})
        df.to_csv('data/outresult_sample2.csv', mode='a',header=False, index=False, encoding='utf_8_sig')
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        start.empty()
        st.session_state.count = -8
        
# クラシック  
if st.session_state.count == -8:
    my_bar = st.progress(0)
    my_bar.progress(int(100/6*1))
    sizi = st.empty()
    sizi.header('１．クラシック')
    sizi2 = st.empty()
    sizi2.write('リファレンス音源は何回聞いても問題ありません')
    audio_file=open('Test1_reference_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi2.audio(audio_file_test_bytes, start_time=0)
    # AFC/FS
    sel1 = st.empty()
    select1=sel1.radio('１－１．よりリファレンス音源に近い音源を選択してください。',('1','2'))
    sizi3 = st.empty()
    sizi3.write(' 音源1')
    audio_file=open('Test1_AFC_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write(' 音源2')
    audio_file=open('Test1_FS_AFC_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi4.audio(audio_file_test_bytes, start_time=0)
    # AFC/B-PEM-AFC
    sel2 = st.empty()
    select2=sel2.radio('１ー２．リファレンス音源に近い音源を選択してください。',('1','2'))
    sizi5 = st.empty()
    sizi5.write(' 音源1')
    audio_file=open('Test1_AFC_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write(' 音源2')
    audio_file=open('Test1_B_PEM_AFC_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi6.audio(audio_file_test_bytes, start_time=0)
    # FS-AFC/B-PEM-AFC
    sel3 = st.empty()
    select3=sel3.radio('１ー３．リファレンス音源に近い音源を選択してください。',('1','2'))
    sizi7 = st.empty()
    sizi7.write(' 音源1')
    audio_file=open('Test1_FS_AFC_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sizi8 = st.empty()
    sizi8.write(' 音源2')
    audio_file=open('Test1_B_PEM_AFC_60_classics.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi8.audio(audio_file_test_bytes, start_time=0)
    df = pd.DataFrame({'1': [st.session_state.key], '2': ['クラシック'], '3': [select1], '4': [select2], '5': [select3]})
    #st.dataframe(df)
    
    nex=st.empty()
    next2_button=nex.button('次の音源(鐘の音)へ')
    if next2_button:
        df.to_csv('data/outresult_sample2.csv', mode='a',header=False, index=False, encoding='utf_8_sig')
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        sizi8.empty()
        sel1.empty()
        sel2.empty()
        sel3.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -7
    

# 鐘の音
if st.session_state.count == -7:
    my_bar = st.progress(0)
    my_bar.progress(int(100/6*2))
    sizi = st.empty()
    sizi.header('２．鐘の音')
    sizi2 = st.empty()
    sizi2.write('リファレンス音源は何回聞いても問題ありません')
    audio_file=open('Test2_reference_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi2.audio(audio_file_test_bytes, start_time=0)
    # AFC/FS
    sel1 = st.empty()
    select1=sel1.radio('２－１．よりリファレンス音源に近い音源を選択してください。',('1','2'))
    sizi3 = st.empty()
    sizi3.write(' 音源1')
    audio_file=open('Test2_AFC_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write(' 音源2')
    audio_file=open('Test2_FS_AFC_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi4.audio(audio_file_test_bytes, start_time=0)
    # AFC/B-PEM-AFC
    sel2 = st.empty()
    select2=sel2.radio('２ー２．リファレンス音源に近い音源を選択してください。',('1','2'))
    sizi5 = st.empty()
    sizi5.write(' 音源1')
    audio_file=open('Test2_AFC_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write(' 音源2')
    audio_file=open('Test2_B_PEM_AFC_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi6.audio(audio_file_test_bytes, start_time=0)
    # FS-AFC/B-PEM-AFC
    sel3 = st.empty()
    select3=sel3.radio('２ー３．リファレンス音源に近い音源を選択してください。',('1','2'))
    sizi7 = st.empty()
    sizi7.write(' 音源1')
    audio_file=open('Test2_FS_AFC_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sizi8 = st.empty()
    sizi8.write(' 音源2')
    audio_file=open('Test2_B_PEM_AFC_60_bell.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi8.audio(audio_file_test_bytes, start_time=0)
    df = pd.DataFrame({'1': [st.session_state.key], '2': ['鐘の音'], '3': [select1], '4': [select2], '5': [select3]})
    # st.dataframe(df)
    
    nex=st.empty()
    next3_button=nex.button('次の音源(救急車のサイレン)へ')
    if next3_button:
        df.to_csv('data/outresult_sample2.csv', mode='a',header=False, index=False, encoding='utf_8_sig')
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        sizi8.empty()
        sel1.empty()
        sel2.empty()
        sel3.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -6

#　救急車のさいれん
if st.session_state.count == -6:
    my_bar = st.progress(0)
    my_bar.progress(int(100/6*3))
    sizi = st.empty()
    sizi.header('３．救急車のサイレン')
    sizi2 = st.empty()
    sizi2.write('リファレンス音源は何回聞いても問題ありません')
    audio_file=open('Test3_reference_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi2.audio(audio_file_test_bytes, start_time=0)
    # AFC/FS
    sel1 = st.empty()
    select1=sel1.radio('３－１．リファレンス音源に近い音源を選択してください。',('1','2'))
    sizi3 = st.empty()
    sizi3.write(' 音源1')
    audio_file=open('Test3_AFC_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write(' 音源2')
    audio_file=open('Test3_FS_AFC_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi4.audio(audio_file_test_bytes, start_time=0)
    # AFC/B-PEM-AFC
    sel2 = st.empty()
    select2=sel2.radio('３ー２．リファレンス音源に近い音源を選択してください。',('1','2'))
    sizi5 = st.empty()
    sizi5.write(' 音源1')
    audio_file=open('Test3_AFC_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write(' 音源2')
    audio_file=open('Test3_B_PEM_AFC_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi6.audio(audio_file_test_bytes, start_time=0)
    # FS-AFC/B-PEM-AFC
    sel3 = st.empty()
    select3=sel3.radio('３ー３．リファレンス音源に近い音源を選択してください。',('1','2'))
    sizi7 = st.empty()
    sizi7.write(' 音源1')
    audio_file=open('Test3_FS_AFC_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sizi8 = st.empty()
    sizi8.write(' 音源2')
    audio_file=open('Test3_B_PEM_AFC_60_ambulance_siren.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi8.audio(audio_file_test_bytes, start_time=0)
    df = pd.DataFrame({'1': [st.session_state.key], '2': ['救急車のサイレン'], '3': [select1], '4': [select2], '5': [select3]})
    #st.dataframe(df)
   
    nex=st.empty()
    if nex.button("終了"):
        df.to_csv('data/outresult_sample2.csv', mode='a',header=False, index=False, encoding='utf_8_sig')
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        sizi8.empty()
        sel1.empty()
        sel2.empty()
        sel3.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -5
 
if st.session_state.count == -5:
    my_bar = st.progress(0)
    my_bar.progress(int(100/6*6))
    st.write('結果')
    wine = pd.read_csv("data/outresult_sample2.csv")
    st.dataframe(wine)
        
    st.title('実験は終了です。ご協力ありがとうございました。ブラウザを閉じてください')
        
        
    st.balloons()
    st.stop()




