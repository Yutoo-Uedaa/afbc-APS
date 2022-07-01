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
    resu=st.empty()
    resu1_button=resu.button('結果一覧')
    
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
        resu.empty()
        st.session_state.count = -20
    elif submitted:
        st.warning('名前を入力して下さい')
        
    
    if resu1_button:
        explainBef.empty()
        explain.empty()
        sizi.empty()
        sizi2.empty()
        st.session_state.count =0
    
if st.session_state.count == 0:    
    wine = pd.read_csv('data/outresult_test2.csv', names=('name','source','AFC(1)/FS-AFC(2)','AFC(1)/Prop(2)','FS-AFC(1)/Prop(2)'))
    
    wine1=wine[wine['AFC(1)/FS-AFC(2)'] != "value"]
    sum_all=(wine1['source']=='クラシック')
    st.write('アンケート回答数 : '+ str(sum_all.sum()))
    data1=wine.query('source == "クラシック"')
    s_bool1 = ((data1['source'] == 'クラシック') & (data1['AFC(1)/FS-AFC(2)'] == 2))
    s_bool2 = ((data1['source'] == 'クラシック') & (data1['AFC(1)/Prop(2)'] == 2))
    s_bool3 = ((data1['source'] == 'クラシック') & (data1['FS-AFC(1)/Prop(2)'] == 2))
    df1 = pd.DataFrame({'1': ['クラシック','AFC/FS-AFC','AFC/Prop','FS-AFC/Prop'], '2': ['AFC',str(sum_all.sum()-s_bool1.sum()),str(sum_all.sum()-s_bool2.sum()),'0'],
                       '3': ['FS',str(s_bool1.sum()),'0',str(sum_all.sum()-s_bool3.sum())], '4': ['Prop','0',str(s_bool2.sum()),str(s_bool3.sum())]})
    #st.dataframe(df1)
    data1=wine.query('source == "鐘の音"')
    s_bool1 = ((data1['source'] == '鐘の音') & (data1['AFC(1)/FS-AFC(2)'] == 2))
    s_bool2 = ((data1['source'] == '鐘の音') & (data1['AFC(1)/Prop(2)'] == 2))
    s_bool3 = ((data1['source'] == '鐘の音') & (data1['FS-AFC(1)/Prop(2)'] == 2))
    df2 = pd.DataFrame({'1': ['鐘の音','AFC/FS-AFC','AFC/Prop','FS-AFC/Prop'], '2': ['AFC',str(sum_all.sum()-s_bool1.sum()),str(sum_all.sum()-s_bool2.sum()),'0'],
                       '3': ['FS',str(s_bool1.sum()),'0',str(sum_all.sum()-s_bool3.sum())], '4': ['Prop','0',str(s_bool2.sum()),str(s_bool3.sum())]})
    #st.dataframe(df2)
    data1=wine.query('source == "救急車のサイレン"')
    s_bool1 = ((data1['source'] == '救急車のサイレン') & (data1['AFC(1)/FS-AFC(2)'] == 2))
    s_bool2 = ((data1['source'] == '救急車のサイレン') & (data1['AFC(1)/Prop(2)'] == 2))
    s_bool3 = ((data1['source'] == '救急車のサイレン') & (data1['FS-AFC(1)/Prop(2)'] == 2))
    df3 = pd.DataFrame({'1': ['救急車のサイレン','AFC/FS-AFC','AFC/Prop','FS-AFC/Prop'], '2': ['AFC',str(sum_all.sum()-s_bool1.sum()),str(sum_all.sum()-s_bool2.sum()),'0'],
                       '3': ['FS',str(s_bool1.sum()),'0',str(sum_all.sum()-s_bool3.sum())], '4': ['Prop','0',str(s_bool2.sum()),str(s_bool3.sum())]})
    #st.dataframe(df3)
    data1=wine.query('source == "ドアベル"')
    s_bool1 = ((data1['source'] == 'ドアベル') & (data1['AFC(1)/FS-AFC(2)'] == 2))
    s_bool2 = ((data1['source'] == 'ドアベル') & (data1['AFC(1)/Prop(2)'] == 2))
    s_bool3 = ((data1['source'] == 'ドアベル') & (data1['FS-AFC(1)/Prop(2)'] == 2))
    df4 = pd.DataFrame({'1': ['ドアベル','AFC/FS-AFC','AFC/Prop','FS-AFC/Prop'], '2': ['AFC',str(sum_all.sum()-s_bool1.sum()),str(sum_all.sum()-s_bool2.sum()),'0'],
                       '3': ['FS',str(s_bool1.sum()),'0',str(sum_all.sum()-s_bool3.sum())], '4': ['Prop','0',str(s_bool2.sum()),str(s_bool3.sum())]})
    #st.dataframe(df4)
    data1=wine.query('source == "電話のコール音"')
    s_bool1 = ((data1['source'] == '電話のコール音') & (data1['AFC(1)/FS-AFC(2)'] == 2))
    s_bool2 = ((data1['source'] == '電話のコール音') & (data1['AFC(1)/Prop(2)'] == 2))
    s_bool3 = ((data1['source'] == '電話のコール音') & (data1['FS-AFC(1)/Prop(2)'] == 2))
    df5 = pd.DataFrame({'1': ['電話のコール音','AFC/FS-AFC','AFC/Prop','FS-AFC/Prop'], '2': ['AFC',str(sum_all.sum()-s_bool1.sum()),str(sum_all.sum()-s_bool2.sum()),'0'],
                       '3': ['FS',str(s_bool1.sum()),'0',str(sum_all.sum()-s_bool3.sum())], '4': ['Prop','0',str(s_bool2.sum()),str(s_bool3.sum())]})
    #st.dataframe(df5)
    data1=wine.query('source == "英語の音声"')
    s_bool1 = ((data1['source'] == '英語の音声') & (data1['AFC(1)/FS-AFC(2)'] == 2))
    s_bool2 = ((data1['source'] == '英語の音声') & (data1['AFC(1)/Prop(2)'] == 2))
    s_bool3 = ((data1['source'] == '英語の音声') & (data1['FS-AFC(1)/Prop(2)'] == 2))
    df6 = pd.DataFrame({'1': ['英語の音声','AFC/FS-AFC','AFC/Prop','FS-AFC/Prop'], '2': ['AFC',str(sum_all.sum()-s_bool1.sum()),str(sum_all.sum()-s_bool2.sum()),'0'],
                       '3': ['FS',str(s_bool1.sum()),'0',str(sum_all.sum()-s_bool3.sum())], '4': ['Prop','0',str(s_bool2.sum()),str(s_bool3.sum())]})
    #st.dataframe(df6)
    
    DF=pd.concat([df1, df2, df3, df4,df5,df6],axis='index')
    st.write('全体の結果')
 
    
    st.dataframe(DF)
    #st.write('クラシック (AFC/FS-AFC) でAFCを選んだ人数 : '+str(sum_all.sum()-s_bool1.sum())+'   FS-AFCを選んだ人数 : '+str(s_bool1.sum()))
    #st.write('クラシック (AFC/Prop) でAFCを選んだ人数 : '+str(sum_all.sum()-s_bool2.sum())+'   Propを選んだ人数 : '+str(s_bool2.sum()))
    #st.write('クラシック (FS-AFC/Prop) でFS-AFCを選んだ人数 : '+str(sum_all.sum()-s_bool3.sum())+'   Propを選んだ人数 : '+str(s_bool3.sum()))
    #st.dataframe(data1)
    st.dataframe(wine)
    
    csv_financde = DF.to_csv().encode('utf-8-sig').decode()
    st.download_button(
    label='CSVダウンロード',
    data=csv_financde,
    file_name='評価データ.csv',
    mime='text/csv'
)
    
if st.session_state.count == -20:
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
        st.session_state.count = -19
# 3 1 2        
# クラシック FS/B-PEM-AFC
st.session_state.time = time.time()
if st.session_state.count == -19:
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*1))
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
    select3=sel1.radio('1-1.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select1_3=select3 
    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(2/18)')
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

#  classic FS-AFC/AFC    
if st.session_state.count == -18:
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*2))
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
    sizi5=st.empty()
    audio_file=open('Test1_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7=st.empty()
    audio_file=open('Test1_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select1=sel1.radio('1-2.リファレンス音源に近い音源を選択してください。',('1','2'))
    if select1=='1':
        st.select1_1=str('2')
    else:
        st.select1_1=str('1')   
    nex=st.empty()
    next1_button=nex.button('次の音源へ(3/18)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sel1.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -17
        
#  classics B-PEM-AFC/AFC
if st.session_state.count == -17: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*3))
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
    audio_file=open('Test1_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test1_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select2=sel1.radio('1-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    if select2=='1':
        st.select1_2=str('2')  
    else:
        st.select1_2=str('1')  
    nex=st.empty()
    next1_button=nex.button('次の音源へ(4/18)')
    if next1_button:
        sel1.empty()
        nex.empty()
        sel1.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        sizi4.empty()
        sizi5.empty()
        sizi6.empty()
        sizi7.empty()
        my_bar.empty()
        st.session_state.count = -16
    
# 1 3 2
# bell FS-AFC/AFC
if st.session_state.count == -16:
    nex=st.empty()
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*4))
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
    sizi5=st.empty()
    audio_file=open('Test2_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7=st.empty()
    audio_file=open('Test2_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select1=sel1.radio('2-1.リファレンス音源に近い音源を選択してください。',('1','2'))
    if select1=='1':
        st.select2_1=str('2')  
    else:
        st.select2_1=str('1')  
    nex=st.empty()
    next1_button=nex.button('次の音源へ(5/18)')
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
        sel1.empty()
        my_bar.empty()
        st.session_state.count = -15
    
#  鐘の音 FS-AFC/B-PEM-AFC    
if st.session_state.count == -15: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*5))
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
    select3=sel1.radio('2-2.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select2_3=select3  
    nex=st.empty()
    next1_button=nex.button('次の音源へ(6/18)')
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
        sel1.empty()
        my_bar.empty()
        st.session_state.count = -14
        
#   鐘の音　AFC/B-PEM-AFC
if st.session_state.count == -14: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*6))
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
    select2=sel1.radio('2-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select2_2=select2  
    nex=st.empty()
    next1_button=nex.button('次の音源へ(7/18)')
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

# 1 3 2         
# siren AFC/FS
if st.session_state.count == -13:
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*7))
    sizi = st.empty()
    sizi.header('３ー１．救急車のサイレン')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test3_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5=st.empty()
    audio_file=open('Test3_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7=st.empty()
    audio_file=open('Test3_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select1=sel1.radio('3-1.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select3_1=select1    
    nex=st.empty()
    next1_button=nex.button('次の音源へ(8/18)')
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
    
#  siren AFC/B-PEM-AFC    
if st.session_state.count == -12: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*8))
    sizi = st.empty()
    sizi.header('３ー２．救急車のサイレン')
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
    select3=sel1.radio('3-2.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select3_3=select3   
    nex=st.empty()
    next1_button=nex.button('次の音源へ(9/18)')
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
        
#   救急車のサイレン　B-PEM-AFC/AFC
if st.session_state.count == -11: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*9))
    sizi = st.empty()
    sel1 = st.empty()
    sizi.header('３ー３．救急車のサイレン')
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
    audio_file=open('Test3_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test3_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select2=sel1.radio('3-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    if select2=='1':
        st.select3_2=str('2')  
    else:
        st.select3_2=str('1')  
    nex=st.empty()
    next1_button=nex.button('次の音源へ(10/18)')
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
 
# 1 2 3
# doorbell AFC/FS
if st.session_state.count == -10:
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*10))
    sizi = st.empty()
    sel1 = st.empty()
    sizi.header('４ー１．ドアベル')
    # リファレンス音源
    sizi2 = st.empty()
    sizi2.write('・リファレンス音源')
    sizi3=st.empty()
    audio_file=open('Test4_reference_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi3.audio(audio_file_test_bytes, start_time=0)
    sizi4 = st.empty()
    sizi4.write('・音源1')
    sizi5=st.empty()
    audio_file=open('Test4_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7=st.empty()
    audio_file=open('Test4_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select1=sel1.radio('4-1.リファレンス音源に近い音源を選択してください。',('1','2'))
    if select1=='1':
        st.select4_1=str('2')
    else:
        st.select4_1=str('1')
    nex=st.empty()
    next1_button=nex.button('次の音源へ(11/18)')
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
 

#  doorbell AFC/B-PEM-AFC    
if st.session_state.count == -9: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*11))
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
    select2=sel1.radio('4-2.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select4_2=select2
    nex=st.empty()
    next1_button=nex.button('次の音源へ(12/18)')
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
        
#   ドアベル　FS-AFC/B-PEM-AFC
if st.session_state.count == -8: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*12))
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
    audio_file=open('Test4_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test4_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select3=sel1.radio('4-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    if select3=='1':
        st.select4_3=str('2')
    else:
        st.select4_3=str('1')
    nex=st.empty()
    next1_button=nex.button('次の音源へ(13/18)')
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
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -7
# 2 1 3 
# 電話のコール音 AFC/B-PEM-AFC
if st.session_state.count == -7:
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*13))
    sizi = st.empty()
    sel1 = st.empty()
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
    audio_file=open('Test5_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test5_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select2=sel1.radio('5-1.リファレンス音源に近い音源を選択してください。',('1','2'))
    if select2=='1':
        st.select5_2=str('2')
    else:
        st.select5_2=str('1')
      
    nex=st.empty()
    next1_button=nex.button('次の音源へ(14/18)')
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
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -6
    
#  電話のコール音 AFC/FS-AFC    
if st.session_state.count == -6: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*14))
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
    sizi5=st.empty()
    audio_file=open('Test5_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7=st.empty()
    audio_file=open('Test5_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select1=sel1.radio('5-2.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select5_1=select1
    nex=st.empty()
    next1_button=nex.button('次の音源へ(15/18)')
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
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -5
        
#   電話のコール音　FS-AFC/B-PEM-AFC
if st.session_state.count == -5: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*15))
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
    select3=sel1.radio('5-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select5_3=select3   
    nex=st.empty()
    next1_button=nex.button('次の音源へ(16/18)')
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
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -4

 # 3 2 1       
# 英語の音声 FS-AFC/B-PEM-AFC
if st.session_state.count == -4:
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*16))
    sizi = st.empty()
    sel1 = st.empty()
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
    select3=sel1.radio('6-1.リファレンス音源に近い音源を選択してください。',('1','2'))
    st.select6_3=select3  
       
    nex=st.empty()
    next1_button=nex.button('次の音源へ(17/18)')
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
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -3
    
#  英語の音声 AFC/B-PEM-AFC    
if st.session_state.count == -3: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*17))
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
    audio_file=open('Test6_B_PEM_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7 = st.empty()
    audio_file=open('Test6_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select2=sel1.radio('6-2.リファレンス音源に近い音源を選択してください。',('1','2'))
    if select2=='1':
        st.select6_2=str('2')
    else:
        st.select6_2=str('1')
    nex=st.empty()
    next1_button=nex.button('次の音源へ(18/18)')
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
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -2
        
#   英語の音声　AFC/FS-AFC
if st.session_state.count == -2: 
    my_bar = st.progress(0)
    my_bar.progress(int(100/18*18))
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
    sizi5=st.empty()
    audio_file=open('Test6_FS_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi5.audio(audio_file_test_bytes, start_time=0)
    sizi6 = st.empty()
    sizi6.write('・音源2')
    sizi7=st.empty()
    audio_file=open('Test6_AFC_60.wav','rb')
    audio_file_test_bytes = audio_file.read()
    sizi7.audio(audio_file_test_bytes, start_time=0)
    sel1 = st.empty()
    select1=sel1.radio('6-3.リファレンス音源に近い音源を選択してください。',('1','2'))
    if select1=='1':
        st.select6_1=str('2')  
    else:
        st.select6_1=str('1')
    sizi8=st.empty()    
    sizi8.write('今回のアンケートで気づいたことなどありましたらコメントお願いします。')
    sizi9=st.empty()
    text = sizi9.text_input(label='記入欄', value='')
    dff=pd.DataFrame({'名前':[st.session_state.key],
                      'コメント':[text]
                    })
    dff.to_csv('data/coment1.csv', mode='a',header=False, index=False,encoding='utf_8_sig')
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
        sizi8.empty()
        sizi9.empty()
        sel1.empty()
        nex.empty()
        my_bar.empty()
        st.session_state.count = -1
        
if st.session_state.count == -1:
    my_bar = st.progress(0)
    my_bar.progress(int(100/6*6))
    st.write('自分の結果')
    df = pd.DataFrame({'名前': [st.session_state.key,st.session_state.key,st.session_state.key,st.session_state.key,st.session_state.key,st.session_state.key], 
                       '音声': ['クラシック','鐘の音','救急車のサイレン','ドアベル','電話のコール音','英語の音声'], 
                       'AFC(1)/FS-AFC(2)': [st.select1_1,st.select2_1,st.select3_1,st.select4_1,st.select5_1,st.select6_1],
                       'AFC(1)/Prop(2)': [st.select1_2,st.select2_2,st.select3_2,st.select4_2,st.select5_2,st.select6_2], 
                       'FS-AFC(1)/Prop(2)': [st.select1_3,st.select2_3,st.select3_3,st.select4_3,st.select5_3,st.select6_3]
                      })    
    st.dataframe(df)
    df.to_csv('data/outresult_test2.csv', mode='a',header=False, index=False,encoding='utf_8_sig')
    
    
      
    
        
    st.title('実験は終了です。ご協力ありがとうございました。ブラウザを閉じてください')    
    st.balloons()
    st.stop()




