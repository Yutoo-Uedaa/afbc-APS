import os
import time
import datetime
import streamlit as st
import numpy as np
import pandas as pd
# import matplotlib.pyploy as plt

import pickle
import csv


kyouji = """本実験は、エントレインメント抑制機能の性能評価として、通常のNLMS、周波数シフトを用いたNLMS、提案手法の出力音声を聴き比べ評価するものです。
                    \n提示されたリファレンス音源と評価音源の音源１、音源２を聴き比べ、リファレンス音源にどちらが近い音かを回答してください。
                    \n６つの音源によって調査を行います。
                    \n　　・クラシック
                    \n　　・鐘の音
                    \n　　・救急車のサイレン音
                    \n　　・ドアベル
                    \n　　・電話のコール音
                    \n　　・英語の音声
                    \n音源の到来方向が右側からになっています。右側イヤホンからの音が大きく聞こえます。
                    \n音は何度聞き返してもかまいません。評価がおわりましたら「次へ」のボタンを押してください
                    \n回答が終わりましたら終了ボタンを押して終了してください。
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
    st.session_state.count = -40
if 'group' not in st.session_state:
    st.session_state.group = -1
if 'key' not in st.session_state:
    st.session_state.key = 'value'
    st.select1_1='value' #AFC/FS
    st.select1_2='value' #AFC/swAFC
    st.select1_3='value' #AFC/Prop
    st.select1_4='value' #FS/swAFC
    st.select1_5='value' #FS/Prop
    st.select1_6='value' #swAFC/Prop
    st.select2_1='value' #AFC/FS
    st.select2_2='value' #AFC/swAFC
    st.select2_3='value' #AFC/Prop
    st.select2_4='value' #FS/swAFC
    st.select2_5='value' #FS/Prop
    st.select2_6='value' #swAFC/Prop
    st.select3_1='value' #AFC/FS
    st.select3_2='value' #AFC/swAFC
    st.select3_3='value' #AFC/Prop
    st.select3_4='value' #FS/swAFC
    st.select3_5='value' #FS/Prop
    st.select3_6='value' #swAFC/Prop
    st.select4_1='value' #AFC/FS
    st.select4_2='value' #AFC/swAFC
    st.select4_3='value' #AFC/Prop
    st.select4_4='value' #FS/swAFC
    st.select4_5='value' #FS/Prop
    st.select4_6='value' #swAFC/Prop    
    st.select5_1='value' #AFC/FS
    st.select5_2='value' #AFC/swAFC
    st.select5_3='value' #AFC/Prop
    st.select5_4='value' #FS/swAFC
    st.select5_5='value' #FS/Prop
    st.select5_6='value' #swAFC/Prop
    st.select6_1='value' #AFC/FS
    st.select6_2='value' #AFC/swAFC
    st.select6_3='value' #AFC/Prop
    st.select6_4='value' #FS/swAFC
    st.select6_5='value' #FS/Prop
    st.select6_6='value' #swAFC/Prop
    
if 'time' not in st.session_state:
    st.session_state.time = 0
if 'time2' not in st.session_state:
    st.session_state.time2 = 0    
    

if st.session_state.count == -40:
    st.title('APS評価実験') 
    explainBef = st.empty()
    with explainBef.expander("実験の説明", True):
        st.write(kyouji)

    sizi = st.empty()
    sizi.subheader('実験前のお願い')

    explain = st.empty()
    sizi2 = st.empty()
    sizi2.write('本実験はヘッドホンでの参加をお願い致します。''こちらの音が聞きやすい大きさでPCの音量を調節し実験中はいじらないでください')
    resu=st.empty()
    resu1_button=resu.button('結果一覧')
    
    with explain.form("my_form"):
        sub_name = st.text_input("名前を入力してください   　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　""　　　　　 　　　　  　　　　　 ""例：リオン太郎さんの場合 >>>　t_rion")
        sub_age = st.selectbox('年代を選択してください', ('10代', '20代', '30代', '40代', '50代', '60代', '非公表',))
        submitted = st.form_submit_button("次へ")

    if submitted and sub_name != "":
        st.session_state.key = str(deyTimeCheck(str(sub_name), str(sub_age)))
        explainBef.empty()
        explain.empty()
        sizi.empty()
        sizi2.empty()
        resu.empty()
        st.session_state.count = -39
    elif submitted:
        st.warning('名前を入力して下さい')
        
    
    if resu1_button:
        explainBef.empty()
        explain.empty()
        sizi.empty()
        sizi2.empty()
        st.session_state.count =0
    
if st.session_state.count == 0:    
    wine = pd.read_csv('data/outresult_TEST1.csv', names=('name','source','AFC(1)/FS-AFC(2)','AFC(1)/Prop(2)','FS-AFC(1)/Prop(2)'))
    st.dataframe(wine)
    wine1=wine[(wine['AFC(1)/FS-AFC(2)'] != "value") & (wine['AFC(1)/Prop(2)'] != "value") & (wine['FS-AFC(1)/Prop(2)'] != "value")]
    sum_all=((wine1['source']=='クラシック'))
    st.write('アンケート回答数 : '+ str(sum_all.sum()))
    data1=wine1.query('source == "クラシック"')
    s_bool1 = ((data1['source'] == 'クラシック') & ((data1['AFC(1)/FS-AFC(2)'] == '2') | (data1['AFC(1)/FS-AFC(2)'] == 2)))
    s_bool2 = ((data1['source'] == 'クラシック') & ((data1['AFC(1)/Prop(2)'] == '2') | (data1['AFC(1)/Prop(2)'] == 2)))
    s_bool3 = ((data1['source'] == 'クラシック') & ((data1['FS-AFC(1)/Prop(2)'] == '2') | (data1['FS-AFC(1)/Prop(2)'] == 2)))
    df1 = pd.DataFrame({'1': ['クラシック','AFC/FS-AFC','AFC/Prop','FS-AFC/Prop'], '2': ['AFC',str(sum_all.sum()-s_bool1.sum()),str(sum_all.sum()-s_bool2.sum()),'0'],
                       '3': ['FS',str(s_bool1.sum()),'0',str(sum_all.sum()-s_bool3.sum())], '4': ['Prop','0',str(s_bool2.sum()),str(s_bool3.sum())]})
  
    data1=wine1.query('source == "鐘の音"')
    s_bool1 = ((data1['source'] == '鐘の音') & ((data1['AFC(1)/FS-AFC(2)'] == '2') | (data1['AFC(1)/FS-AFC(2)'] == 2)))
    s_bool2 = ((data1['source'] == '鐘の音') & ((data1['AFC(1)/Prop(2)'] == '2') | (data1['AFC(1)/Prop(2)'] == 2)))
    s_bool3 = ((data1['source'] == '鐘の音') & ((data1['FS-AFC(1)/Prop(2)'] == '2') | (data1['FS-AFC(1)/Prop(2)'] == 2)))
    df2 = pd.DataFrame({'1': ['鐘の音','AFC/FS-AFC','AFC/Prop','FS-AFC/Prop'], '2': ['AFC',str(sum_all.sum()-s_bool1.sum()),str(sum_all.sum()-s_bool2.sum()),'0'],
                       '3': ['FS',str(s_bool1.sum()),'0',str(sum_all.sum()-s_bool3.sum())], '4': ['Prop','0',str(s_bool2.sum()),str(s_bool3.sum())]})
    #st.dataframe(df2)
    data1=wine1.query('source == "救急車のサイレン"')
    s_bool1 = ((data1['source'] == '救急車のサイレン') & ((data1['AFC(1)/FS-AFC(2)'] == '2') | (data1['AFC(1)/FS-AFC(2)'] == 2)))
    s_bool2 = ((data1['source'] == '救急車のサイレン') & ((data1['AFC(1)/Prop(2)'] == '2') | (data1['AFC(1)/Prop(2)'] == 2)))
    s_bool3 = ((data1['source'] == '救急車のサイレン') & ((data1['FS-AFC(1)/Prop(2)'] == '2') | (data1['FS-AFC(1)/Prop(2)'] == 2)))
    df3 = pd.DataFrame({'1': ['救急車のサイレン','AFC/FS-AFC','AFC/Prop','FS-AFC/Prop'], '2': ['AFC',str(sum_all.sum()-s_bool1.sum()),str(sum_all.sum()-s_bool2.sum()),'0'],
                       '3': ['FS',str(s_bool1.sum()),'0',str(sum_all.sum()-s_bool3.sum())], '4': ['Prop','0',str(s_bool2.sum()),str(s_bool3.sum())]})
    #st.dataframe(df3)
    data1=wine1.query('source == "ドアベル"')
    s_bool1 = ((data1['source'] == 'ドアベル') & ((data1['AFC(1)/FS-AFC(2)'] == '2') | (data1['AFC(1)/FS-AFC(2)'] == 2)))
    s_bool2 = ((data1['source'] == 'ドアベル') & ((data1['AFC(1)/Prop(2)'] == '2') | (data1['AFC(1)/Prop(2)'] == 2)))
    s_bool3 = ((data1['source'] == 'ドアベル') & ((data1['FS-AFC(1)/Prop(2)'] == '2') | (data1['FS-AFC(1)/Prop(2)'] == 2)))
    df4 = pd.DataFrame({'1': ['ドアベル','AFC/FS-AFC','AFC/Prop','FS-AFC/Prop'], '2': ['AFC',str(sum_all.sum()-s_bool1.sum()),str(sum_all.sum()-s_bool2.sum()),'0'],
                       '3': ['FS',str(s_bool1.sum()),'0',str(sum_all.sum()-s_bool3.sum())], '4': ['Prop','0',str(s_bool2.sum()),str(s_bool3.sum())]})
    #st.dataframe(df4)
    data1=wine1.query('source == "電話のコール音"')
    s_bool1 = ((data1['source'] == '電話のコール音') & ((data1['AFC(1)/FS-AFC(2)'] == '2') | (data1['AFC(1)/FS-AFC(2)'] == 2)))
    s_bool2 = ((data1['source'] == '電話のコール音') & ((data1['AFC(1)/Prop(2)'] == '2') | (data1['AFC(1)/Prop(2)'] == 2)))
    s_bool3 = ((data1['source'] == '電話のコール音') & ((data1['FS-AFC(1)/Prop(2)'] == '2') | (data1['FS-AFC(1)/Prop(2)'] == 2)))
    df5 = pd.DataFrame({'1': ['電話のコール音','AFC/FS-AFC','AFC/Prop','FS-AFC/Prop'], '2': ['AFC',str(sum_all.sum()-s_bool1.sum()),str(sum_all.sum()-s_bool2.sum()),'0'],
                       '3': ['FS',str(s_bool1.sum()),'0',str(sum_all.sum()-s_bool3.sum())], '4': ['Prop','0',str(s_bool2.sum()),str(s_bool3.sum())]})
    #st.dataframe(df5)
    data1=wine1.query('source == "英語の音声"')
    s_bool1 = ((data1['source'] == '英語の音声') & ((data1['AFC(1)/FS-AFC(2)'] == '2') | (data1['AFC(1)/FS-AFC(2)'] == 2)))
    s_bool2 = ((data1['source'] == '英語の音声') & ((data1['AFC(1)/Prop(2)'] == '2') | (data1['AFC(1)/Prop(2)'] == 2)))
    s_bool3 = ((data1['source'] == '英語の音声') & ((data1['FS-AFC(1)/Prop(2)'] == '2') | (data1['FS-AFC(1)/Prop(2)'] == 2)))
    df6 = pd.DataFrame({'1': ['英語の音声','AFC/FS-AFC','AFC/Prop','FS-AFC/Prop'], '2': ['AFC',str(sum_all.sum()-s_bool1.sum()),str(sum_all.sum()-s_bool2.sum()),'0'],
                       '3': ['FS',str(s_bool1.sum()),'0',str(sum_all.sum()-s_bool3.sum())], '4': ['Prop','0',str(s_bool2.sum()),str(s_bool3.sum())]})
    #st.dataframe(df6)
    
    DF=pd.concat([df1, df2, df3, df4,df5,df6],axis='index')
    st.write('全体の結果')
 
    
    #st.dataframe(DF)
    #st.write('クラシック (AFC/FS-AFC) でAFCを選んだ人数 : '+str(sum_all.sum()-s_bool1.sum())+'   FS-AFCを選んだ人数 : '+str(s_bool1.sum()))
    #st.write('クラシック (AFC/Prop) でAFCを選んだ人数 : '+str(sum_all.sum()-s_bool2.sum())+'   Propを選んだ人数 : '+str(s_bool2.sum()))
    #st.write('クラシック (FS-AFC/Prop) でFS-AFCを選んだ人数 : '+str(sum_all.sum()-s_bool3.sum())+'   Propを選んだ人数 : '+str(s_bool3.sum()))
    #st.dataframe(data1)
    #st.dataframe(wine1)
    
    coment=pd.read_csv('data/coment1.csv')
    st.dataframe(coment)
    csv_financde = DF.to_csv().encode('utf-8-sig').decode()
    st.download_button(
    label='CSVダウンロード',
    data=csv_financde,
    file_name='評価データ.csv',
    mime='text/csv'
)
    
if st.session_state.count == -39:
    sizi = st.empty()
    sizi.subheader('提示音サンプル')
    
    sizi2 = st.empty()
    sizi2.write('評価対象音源のサンプルを聞き音量を調整してください．')
    sizi3 = st.empty()
    sizi3.write('※まだ実験は始まっていません')
    sizi4=st.empty()
    audio_file=open('Test1_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi4.audio(audio_file_test_bytes, start_time=0)
    start = st.empty()
    with start.form("my_form2"):
        start_button= st.form_submit_button("実験を始める")
    if start_button:
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        start.empty()
        st.session_state.count = -38
######################################################################################
# 3 2 1 4 6 5
# クラシック1-3 AFC/Prop 
st.session_state.time = time.time()
if st.session_state.count == -38:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*1))
    sizi = st.empty()
    sizi.header('１ー１．クラシック')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test1_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test1_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test1_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select1_3=sel1.radio('1-1.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(2/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -37
# クラシック1-2 AFC/swAFC
st.session_state.time = time.time()
if st.session_state.count == -37:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*2))
    sizi = st.empty()
    sizi.header('１ー２．クラシック')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test1_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test1_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test1_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select1_2=sel1.radio('1-2.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(3/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -36
# クラシック1-1 AFC/FS
st.session_state.time = time.time()
if st.session_state.count == -36:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*3))
    sizi = st.empty()
    sizi.header('１ー３．クラシック')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test1_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test1_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test1_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select1_1=sel1.radio('1-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(4/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -35
# クラシック1-4 FS/swAFC 
st.session_state.time = time.time()
if st.session_state.count == -35:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*4))
    sizi = st.empty()
    sizi.header('１ー４．クラシック')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test1_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test1_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test1_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select1_4=sel1.radio('1-4.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(5/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -34
        st.session_state.time = time.time()
# クラシック1-6 sw/Prop　
if st.session_state.count == -34:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*5))
    sizi = st.empty()
    sizi.header('１ー５．クラシック')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test1_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test1_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test1_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select1_6=sel1.radio('1-5.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(6/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -33
# クラシック1-5 FS/Prop　
if st.session_state.count == -33:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*6))
    sizi = st.empty()
    sizi.header('１ー６．クラシック')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test1_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test1_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test1_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select1_5=sel1.radio('1-6.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(7/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -32
        st.session_state.time = time.time()  
    #if select1=='1':
    #    st.select1_1=str('2')
    #else:
    #    st.select1_1=str('1')   
#####################################################################################################
# 5 2 6 3 4 1 
# 鐘の音        
# 鐘の音2-5 FS/Prop　
if st.session_state.count == -32:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*7))
    sizi = st.empty()
    sizi.header('２ー１．鐘の音')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test2_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test2_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test2_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select2_5=sel1.radio('2-1.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(8/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -31
        st.session_state.time = time.time()

# 鐘の音2-2 AFC/swAFC
st.session_state.time = time.time()
if st.session_state.count == -31:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*8))
    sizi = st.empty()
    sizi.header('２ー２．鐘の音')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test2_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test2_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test2_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select2_2=sel1.radio('2-2.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(9/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -30
# 鐘の音2-6 sw/Prop　
if st.session_state.count == -30:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*9))
    sizi = st.empty()
    sizi.header('２ー３．鐘の音')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test2_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test2_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test2_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select2_6=sel1.radio('2-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(10/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -29
# 鐘の音2-3 AFC/Prop 
st.session_state.time = time.time()
if st.session_state.count == -29:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*10))
    sizi = st.empty()
    sizi.header('２ー４．鐘の音')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test2_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test2_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test2_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select2_3=sel1.radio('2-4.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(11/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -28
# 鐘の音2-4 FS/swAFC 
st.session_state.time = time.time()
if st.session_state.count == -28:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*11))
    sizi = st.empty()
    sizi.header('２ー５．鐘の音')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test2_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test2_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test2_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select2_4=sel1.radio('2-5.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(12/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -27
# 鐘の音2-1 AFC
st.session_state.time = time.time()
if st.session_state.count == -27:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*12))
    sizi = st.empty()
    sizi.header('２ー６．鐘の音')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test2_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test2_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test2_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select2_1=sel1.radio('2-6.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(13/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -26        
######################################################################################
# 5 3 1 6 4 2 
# サイレン3-5 FS/Prop　
if st.session_state.count == -26:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*13))
    sizi = st.empty()
    sizi.header('３ー１．サイレン')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test3_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test3_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test3_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select3_5=sel1.radio('3-1.リファレンス音源に近い音源を選択してください。',('1','2'))
   
    nex=st.empty()
    next1_button=nex.button('次の音源へ(14/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -25
# サイレン3-3 AFC/Prop 
st.session_state.time = time.time()
if st.session_state.count == -25:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*14))
    sizi = st.empty()
    sizi.header('３ー２．サイレン')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test3_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test3_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test3_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select3_3=sel1.radio('3-2.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(15/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -24
# サイレン3-1 AFC
st.session_state.time = time.time()
if st.session_state.count == -24:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*15))
    sizi = st.empty()
    sizi.header('３ー３．サイレン')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test3_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test3_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test3_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select3_1=sel1.radio('3-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(16/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -23
# サイレン3-6 sw/Prop　
if st.session_state.count == -23:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*16))
    sizi = st.empty()
    sizi.header('３ー４．サイレン')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test3_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test3_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test3_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select3_6=sel1.radio('3-4.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(17/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -22  
# サイレン3-4 FS/swAFC 
st.session_state.time = time.time()
if st.session_state.count == -22:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*17))
    sizi = st.empty()
    sizi.header('３ー５．サイレン')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test3_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test3_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test3_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select3_4=sel1.radio('3-5.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(18/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -21
        st.session_state.time = time.time()
# サイレン3-2 AFC/swAFC
st.session_state.time = time.time()
if st.session_state.count == -21:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*18))
    sizi = st.empty()
    sizi.header('３ー６．サイレン')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test3_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test3_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test3_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select3_2=sel1.radio('3-6.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(19/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -20
 ######################################################################################
# 1 5 3 6 4 2
# ドアベル4-1 AFC/FS
st.session_state.time = time.time()
if st.session_state.count == -20:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*19))
    sizi = st.empty()
    sizi.header('4ー１．ドアベル')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test4_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test4_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test4_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select4_1=sel1.radio('4-1.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(20/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -19
# ドアベル4-5 FS/Prop　
if st.session_state.count == -19:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*20))
    sizi = st.empty()
    sizi.header('４ー２．ドアベル')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test4_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test4_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test4_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select4_5=sel1.radio('4-2.リファレンス音源に近い音源を選択してください。',('1','2'))
   
    nex=st.empty()
    next1_button=nex.button('次の音源へ(21/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -18
        st.session_state.time = time.time()
# ドアベル4-3 AFC/Prop 
st.session_state.time = time.time()
if st.session_state.count == -18:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*21))
    sizi = st.empty()
    sizi.header('４ー３．ドアベル')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test4_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test4_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test4_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select4_3=sel1.radio('4-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(22/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -17
# ドアベル４-6 sw/Prop　
if st.session_state.count == -17:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*22))
    sizi = st.empty()
    sizi.header('４ー４．ドアベル')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test4_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test4_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test4_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select4_6=sel1.radio('4-4.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(23/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -16           
# ドアベル4-4 FS/swAFC 
st.session_state.time = time.time()
if st.session_state.count == -16:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*23))
    sizi = st.empty()
    sizi.header('４ー５．ドアベル')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test4_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test4_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test4_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select4_4=sel1.radio('4-5.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(24/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -15
        st.session_state.time = time.time()
# ドアベル4-2 AFC/swAFC
st.session_state.time = time.time()
if st.session_state.count == -15:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*24))
    sizi = st.empty()
    sizi.header('４ー６．ドアベル')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test4_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test4_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test4_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select4_2=sel1.radio('4-6.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(25/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -14
 ######################################################################################
# 6 4 3 5 2 1
# 電話のコール音5-6 sw/Prop　
if st.session_state.count == -14:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*25))
    sizi = st.empty()
    sizi.header('５ー１．電話のコール音')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test5_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test5_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test5_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select5_6=sel1.radio('5-1.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(26/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -13  
#電話のコール音5-4 FS/swAFC 
st.session_state.time = time.time()
if st.session_state.count == -13:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*26))
    sizi = st.empty()
    sizi.header('５ー２．電話のコール音')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test5_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test5_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test5_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select5_4=sel1.radio('5-2.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(27/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -12
        st.session_state.time = time.time()
# 電話のコール5-3 AFC/Prop 
st.session_state.time = time.time()
if st.session_state.count == -12:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*27))
    sizi = st.empty()
    sizi.header('５ー３．電話のコール音')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test5_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test5_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test5_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select5_3=sel1.radio('5-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(28/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -11
# 電話のコール音5-5 FS/Prop　
if st.session_state.count == -11:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*28))
    sizi = st.empty()
    sizi.header('５ー４．電話のコール音')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test5_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test5_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test5_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select5_5=sel1.radio('5-4.リファレンス音源に近い音源を選択してください。',('1','2'))
   
    nex=st.empty()
    next1_button=nex.button('次の音源へ(29/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -10
        st.session_state.time = time.time()
# 電話のコール音5-2 AFC/swAFC
st.session_state.time = time.time()
if st.session_state.count == -10:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*29))
    sizi = st.empty()
    sizi.header('５ー５．電話のコール音')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test5_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test5_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test5_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select5_2=sel1.radio('5-5.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(30/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -9
# 電話のコール音5-1 AFC/FS
if st.session_state.count == -9:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*30))
    sizi = st.empty()
    sizi.header('５ー６．電話のコール音')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test5_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test5_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test5_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select5_1=sel1.radio('5-6.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(31/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -8
 ######################################################################################
# 1 4 2 3 5 6
# 英語の音声6-1 AFC/FS
st.session_state.time = time.time()
if st.session_state.count == -8:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*31))
    sizi = st.empty()
    sizi.header('６ー１．英語の音声')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test6_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test6_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test6_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select6_1=sel1.radio('6-1.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(32/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -7
#英語の音声6-4 FS/swAFC 
st.session_state.time = time.time()
if st.session_state.count == -7:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*32))
    sizi = st.empty()
    sizi.header('６ー２．英語の音声')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test6_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test6_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test6_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select6_4=sel1.radio('6-2.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(33/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -6
        st.session_state.time = time.time()
# 英語の音声6-2 AFC/swAFC
st.session_state.time = time.time()
if st.session_state.count == -6:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*33))
    sizi = st.empty()
    sizi.header('６ー３．英語の音声')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test6_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test6_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test6_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select6_2=sel1.radio('6-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(34/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -5
# 英語の音声6-3 AFC/Prop 
st.session_state.time = time.time()
if st.session_state.count == -5:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*34))
    sizi = st.empty()
    sizi.header('６ー４．英語の音声')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test6_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test6_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test6_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select6_3=sel1.radio('6-4.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(35/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -4

# 英語の音声6-5 FS/Prop　
if st.session_state.count == -4:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*35))
    sizi = st.empty()
    sizi.header('６ー５．英語の音声')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test6_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test6_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test6_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select6_5=sel1.radio('6-5.リファレンス音源に近い音源を選択してください。',('1','2'))
   
    nex=st.empty()
    next1_button=nex.button('次の音源へ(36/36)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -3
        st.session_state.time = time.time()
# 英語の音声6-6 sw/Prop　
if st.session_state.count == -3:
    my_bar = st.progress(0)
    my_bar.progress(int(100/36*36))
    sizi = st.empty()
    sizi.header('６ー６．英語の音声')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test6_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5 = st.empty()
    audio_file=open('Test6_swPEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test6_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    st.select6_6=sel1.radio('6-6.リファレンス音源に近い音源を選択してください。',('1','2'))
    
    nex=st.empty()
    next1_button=nex.button('終了')
    if next1_button:
        sel1.empty()
        nex.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -1  

 

if st.session_state.count == -1:
    my_bar = st.progress(0)
    my_bar.progress(int(100/6*6))
    st.write('自分の結果')
    df = pd.DataFrame({'名前': [st.session_state.key,st.session_state.key,st.session_state.key,st.session_state.key,st.session_state.key,st.session_state.key], 
                       '音声': ['クラシック','鐘の音','救急車のサイレン','ドアベル','電話のコール音','英語の音声'], 
                       'AFC(1)/FS-AFC(2)　': [st.select1_1,st.select2_1,st.select3_1,st.select4_1,st.select5_1,st.select6_1],
                       'AFC(1)/swPEM-AFC(2)　': [st.select1_2,st.select2_2,st.select3_2,st.select4_2,st.select5_2,st.select6_2],
                       'AFC(1)/Prop(2)　': [st.select1_3,st.select2_3,st.select3_3,st.select4_3,st.select5_3,st.select6_3], 
                       'FS-AFC(1)/swPEM-AFC(2)　': [st.select1_4,st.select2_4,st.select3_4,st.select4_4,st.select5_4,st.select6_4],
                       'FS-AFC(1)/Prop(2)　': [st.select1_5,st.select2_5,st.select3_5,st.select4_5,st.select5_5,st.select6_5],
                       'swPEM-AFC(1)/Prop(2)　': [st.select1_6,st.select2_6,st.select3_6,st.select4_6,st.select5_6,st.select6_6],
                      })    
    st.dataframe(df)
    df.to_csv('data/outresult_TEST1.csv', mode='a',header=False, index=False,encoding='utf_8_sig')
    st.write('結果が"value"の場合はお手数ですがもう一度お願いします。')
    
      
    
        
    st.title('実験は終了です。ご協力ありがとうございました。ブラウザを閉じてください')    
    st.balloons()
    st.stop()




