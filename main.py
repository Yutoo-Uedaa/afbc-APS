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


st.title('APS評価実験')

if st.session_state.count == -2:
    
    explainBef = st.empty()
    with explainBef.expander("実験の説明", True):
        st.write(kyouji)

    sizi = st.empty()
    sizi.subheader('実験前のお願い')
    
    sizi2 = st.empty()
    sizi2.write('本実験はヘッドホンでの参加をお願い致します。'
                'こちらの音が聞きやすい大きさでPCの音量を調節し実験中はいじらないでください')
    
    testSound = st.empty()
    testSound.write('ボリューム調整用のサンプル音')
    audio_file_test = open(conf.csv_path + 'VOICEACTRESS100_007.wav', 'rb')
    audio_file_test_bytes = audio_file_test.read()
    testSound.audio(audio_file_test_bytes, start_time=0)

    # 名前と年代の入力
    sizi3 = st.empty()
    sizi3.write('名前と年代を入力してください')
    explain = st.empty()
    with explain.form("my_form"):

        sub_name = st.text_input("名前を入力してください   　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　"
                          "　　　　　 　　　　  　　　　　 "
                          "例：リオン太郎さんの場合 >>>　t_rion")
        sub_age = st.selectbox('年代を選択してください', ('20代', '30代', '40代', '50代', '60代', '非公表',))
        # Every form must have a submit button.
        submitted = st.form_submit_button("次へ")
    # 名前が入力され、開始ボタンが押された時
    if submitted and sub_name != "":
        # 画面 2ページ目
        # csvのname
        st.session_state.key = str(deyTimeCheck(str(sub_name), str(sub_age)))
        explainBef.empty()
        explain.empty()
        sizi.empty()
        sizi2.empty()
        sizi3.empty()
        testSound.empty()
        st.session_state.count = -1
        # result_csv内のcsvを数える
        csv_file = os.listdir(conf.exp_folder_path + '/result_each_subject')
        # csvの数を総実験パターン数で割り、出た余りを実験パターンに設定する
        st.session_state.group = len(csv_file) % conf.sub_num
        df = pd.DataFrame({'1': ["group" + str(st.session_state.group)], '2': ["main"], '3': ["compare"],
                           '4': ["main_num"], '5': ["compare_num"], '6': ["音量"], '7': ["自然"], '8': ["雑音"],
                           '9': ["wav_num"]})

        df.to_csv(conf.exp_folder_path + '/result_each_subject/'+str(st.session_state.group)+ '_' + st.session_state.key + '.csv', mode='a',
                  header=False, index=False,
                  encoding='utf_8_sig')

    elif submitted:
        st.warning('名前を入力して下さい')
