#GPTの最新の箇所参照してタイプミスを修正

import random
import time
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image,ImageTk
#カードのデッキを作成
#スート
suits = ["heart","club","diamond","spade"]
#数字
ranks = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

#山札を作成（全てのスートと数字の組み合わせを生成）
deck = []
for suit in suits:
    for rank in ranks:
        card = f"{suit} : {rank}" #例：ハートのA
        deck.append(card)

#画像のパス設定
CARD_IMAGE_DIR = r"C:/Users/8Java8/Desktop/workshop/ITWorkshop/public/image/"
 #画像フォルダのパス

#カード画像格納のディクショナリ
card_images = {}

#手札を保存するリスト
hand = []

#画像読み込みの関数
def load_card_images():
    global card_images
    for suit in suits:
        for rank in ranks:
            filename = f"{CARD_IMAGE_DIR}{suit}_{rank}.png" #例："cards\heart_2.png
            try:
                #Pillowを使って画像を開く
                image =Image.open(filename)
                #リサイズ（幅と高さを指定）
                image = image.resize((100,150))
                #Tkinter用に変換
                card_images[f"{suit}_{rank}"]= ImageTk.PhotoImage(image)
            except Exception as e:
                print(f"画像の読み込み失敗：{filename},{e}")

# suit_colors = {
#     "♥":"red",
#     "♦":"green",
#     "♣":"purple",
#     "♠":"blue"
# }
selected_cards = []
#手札表示用関数
def draw_cards():
    global hand,selected_cards

    #手札リセットしてランダムに5枚引く
    hand = random.sample(deck,5)    #デッキからランダムに5枚引く
    selected_cards.clear()

    #表示フレームのリセット
    for widget in hand_frame.winfo_children():
        widget.destroy()

    #カード画像を表示
    for index,card in enumerate(hand):
        suit,rank = card.split(" : ")
        card_key = f"{suit}_{rank}"
        card_image = card_images.get(card_key)

        if card_image: #画像が存在する場合のみ表示
            img_label = tk.Label(hand_frame,image=card_image,bg="dark green",bd=2,relief="flat")

            #カードクリック時の動作を設定
            img_label.bind("<Button-1>",lambda e,idx = index: toggle_card_selection(idx, e.widget))
            img_label.pack(side="left",padx=5)

    #チェンジボタンを再度有効化
    change_button.config(state="normal")

def toggle_card_selection(index,widget):
    if index in selected_cards:
        selected_cards.remove(index)
        widget.config(bd=2,relief="flat") #解除（枠線なし）
    else:
        if len(selected_cards) < 5:
            selected_cards.append(index)
            widget.config(bd=2,relief="solid")  #選択（枠線あり）

#役の判定関数
def evaluate_hand():
    global hand

    hand_suits = [card.split(" : ")[0] for card in hand]#スートだけ抽出
    hand_ranks = [card.split(" : ")[1] for card in hand]#数字だけ抽出

    #各数字を数値化してソート（ストレート判定用）
    rank_order = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
    hand_ranks_numeric = sorted([rank_order[rank]for rank in hand_ranks])# 数値化＆ソート

    #各数字の出現回数を数える
    rank_counts = {}
    for rank in hand_ranks:
        if rank in rank_counts:
            rank_counts[rank] += 1
        else:
            rank_counts[rank] = 1

    #各スートの出現回数を数える
    suit_counts={}
    for rank in hand_suits:
        if rank in suit_counts:
            suit_counts[rank] += 1
        else:
            suit_counts[rank] = 1

    #役の判定
    result = ""
    if 5 in suit_counts.values() and hand_ranks_numeric == [10,11,12,13,14]: #ロイヤルストレートフラッシュ
        result = "ロイヤルストレートフラッシュ！ \n-同じスートかつ10・J・Q・K・Aの組み合わせ-"

    elif 5 in suit_counts.values() and all(hand_ranks_numeric[i] + 1 == hand_ranks_numeric[i+1]for i in range(4)):  #ストレートフラッシュ
        result = "ストレートフラッシュ！\n-同じスートかつ連続した数字-"

    elif all(hand_ranks_numeric[i] + 1 == hand_ranks_numeric[i+1]for i in range(4)):    #ストレート
        result = "ストレート\n-数字が連続-"

    elif 5 in suit_counts.values(): #フラッシュ
        result = "フラッシュ\n-全て同じスート-"

    elif 4 in rank_counts.values() and 2 in rank_counts.values():
        result = "フルハウス\n-スリーカード+ワンペア-"

    elif 3 in rank_counts.values(): #スリーカード
        result = "スリーカード\n-3つの同じ数字-"

    elif list(rank_counts.values()).count(2) == 2:  #ツーペア
        result = "ツーペア\n-2組の同じ数字のペア-"

    elif 2 in rank_counts.values(): #ワンペア
        result = "ワンペア\n-2つの同じ数字-"

    else: #ブタ
        result = "ブタ\n-役なし-"

    #結果をウィンドウ内のラベルに表示
    result_label.config(text = f"この役は…:\n{result}")

#チェンジボタン
def change_cards():
    global hand , selected_cards

    #選ばれたカードを交換
    for idx in selected_cards:
        new_card = random.choice([card for card in deck if card not in hand])
        hand[idx] = new_card

    selected_cards.clear()  #選択状態リセット
    draw_cards()
    change_button.config(state="disabled")  #チェンジボタン無効化

#メインウィンドウ作成
root = tk.Tk()
root.title("ぼっちdeポーカー")
root.config(background="dark green")

# ウィンドウの背景色を設定
root.configure(background="dark green")

#UI部品作成
welcome_label = tk.Label(root,text="カードを引いて、5枚の手札で役を完成させよう",font=("Arial",14,"bold"),bg = "dark green",fg="white")
welcome_label.pack(pady=20)

#画像読み込み
load_card_images()

#手札表示用フレーム
hand_frame = tk.Frame(root,bg="dark green")
hand_frame.pack(pady=10)

draw_button = tk.Button(root,text="カードを引く",font=("Arial",12,"bold"),bg = "light green",fg = "black",command=draw_cards) 
draw_button.pack(pady=10)

hand_label = tk.Label(root, text="手札：まだ引いていません",font = ("Arial",12,"bold"),bg = "darkgreen", fg="white")
hand_label.pack(pady=10)

result_label = tk.Label(root,text="役判定結果がここに表示",font = ("Arial",12,"bold"),bg = "dark green",fg="white")
result_label.pack(pady=20)

change_button = tk.Button(root, text = "カードをチェンジ", font= ("Arial",12,"bold"),bg="orange",command=change_cards)
change_button.pack(pady=10)

eval_button = tk.Button(root,text="役を判定",font=("Arial",12,"bold"), bg="light green",fg="black",command = evaluate_hand)
eval_button.pack(pady=10)

exit_button = tk.Button(root,text = "終了", font=("Arial",12,"bold"), bg="light green",fg = "black",command=root.quit)
exit_button.pack(pady=20)

#メインループ実行
root.mainloop()
# -------------------------

# #デバッグ用
# print("山札補充完了")
# print(deck)

# #５枚組のデッキを作る（プレイヤーが一枚ずつカードを引く）
# hand = [] #手札(プレイヤーの手札を保存するリスト)

# print("\nカードを１枚ずつ引いて、５枚で役を完成させよう")

# #カードを引く
# for i in range(5):
#     input(F"Enterで{i+1}枚目のカードを引く")
#     card = random.choice(deck) #山札からランダムにカードを選ぶ
#     deck.remove(card) #引いたカードを山札から削除
#     hand.append(card) #引いたカードを手札に加える
#     print(f"{i+1}枚目のカードは「{card}」です")
# time.sleep(0.5)
# print(f"あなたの手札：{hand}\n")

# #役チェック機能
# input("役を判定するぞ")
# #手札のスートと数字に分けて考える
# hand_suits = [card.split("の")[0]for card in hand] #スートだけ抽出
# hand_ranks = [card.split("の")[1]for card in hand] #数字だけ抽出

# #各数字を数値化してソート（ストレート判定用）
# rank_order = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":11,"Q":12,"K":13,"A":14}
# hand_ranks_numeric = sorted([rank_order[rank]for rank in hand_ranks]) #数値化＆ソート

# #各数字の出現回数を数える
# rank_counts = {}
# for rank in hand_ranks:
#     if rank in rank_counts:
#         rank_counts[rank] += 1
#     else:
#         rank_counts[rank] = 1

# #各スートの出現回数を数える
# suit_counts = {}
# for rank in hand_suits:
#     if rank in suit_counts:
#         suit_counts[suit] += 1
#     else:
#         suit_counts[suit] = 1

# #役の判定
# if 5 in suit_counts.values() and hand_ranks_numeric == [10,11,12,13,14]:#同じスートかつ10､J,Q,K,Aの並び
#     print("ロイヤルストレートフラッシュ！")
#     time.sleep(2)
#     print("…あんた何者…？")
#     print("-同じスートかつ１０・Ｊ・Ｑ・Ｋ・Ａの組み合わせ-")

# elif 5 in suit_counts.values() and all(hand_ranks_numeric[i]+1 == hand_ranks_numeric[i+1]for i in range(4)):#スート同じ&連続した数字
#     print("ストレートフラッシュ！")
#     print("-同じスート且つ連続した数字-")

# elif 5 in suit_counts.values(): #全て同じスート
#     print("フラッシュ！")
#     print("-全て同じスート-")

# elif all(hand_ranks_numeric[i]+1 ==hand_ranks_numeric[i+1]for i in range(4)):
#     print("ストレート！")
#     print("-連続した数字-")
    
# elif 4 in rank_counts.values(): #4枚が同じ数字
#     print("フォーカード")
#     print("-４つの同じ数字-")

# elif 3 in rank_counts.values() and 2 in rank_counts.values(): #3枚と2枚
#     print("フルハウス")
#     print("-スリーカード＋ワンペア-")

# elif 3 in rank_counts.values(): #3枚が同じ数字
#     print("スリーカード")
#     print("-３つの同じ数字-")

# elif list(rank_counts.values()).count(2) == 2: #2枚ペアが2つ
#     print("ツーペア")
#     print("-２組の同じ数字のペア-")

# elif 2 in rank_counts.values(): #2枚が同じ数字
#     print("ワンペア")
#     print("-２つの同じ数字-")

# else:
#     print("ブタ")
#     print("-役なし-")

# print("ゲームオーバー")
# print("また遊んでね！")

# -------------------------