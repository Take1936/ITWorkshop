import random
import time
#カードのデッキを作成
#スート
suits = ["ハート","クラブ","ダイヤ","スペード"]
#数字
ranks = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

#山札を作成（全てのスートと数字の組み合わせを生成）
deck = []
for suit in suits:
    for rank in ranks:
        card = f"{suit}の{rank}" #例：ハートのA
        deck.append(card)

#デバッグ用
print("山札補充完了")
print(deck)

#５枚組のデッキを作る（プレイヤーが一枚ずつカードを引く）
hand = [] #手札(プレイヤーの手札を保存するリスト)

print("\nカードを１枚ずつ引いて、５枚で役を完成させよう")

#カードを引く
for i in range(5):
    input(F"Enterで{i+1}枚目のカードを引く")
    card = random.choice(deck) #山札からランダムにカードを選ぶ
    deck.remove(card) #引いたカードを山札から削除
    hand.append(card) #引いたカードを手札に加える
    print(f"{i+1}枚目のカードは「{card}」です")
time.sleep(0.5)
print(f"あなたの手札：{hand}\n")

#役チェック機能
input("役を判定するぞ")
#手札のスートと数字に分けて考える
hand_suits = [card.split("の")[0]for card in hand] #スートだけ抽出
hand_ranks = [card.split("の")[1]for card in hand] #数字だけ抽出

#各数字を数値化してソート（ストレート判定用）
rank_order = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":11,"Q":12,"K":13,"A":14}
hand_ranks_numeric = sorted([rank_order[rank]for rank in hand_ranks]) #数値化＆ソート

#各数字の出現回数を数える
rank_counts = {}
for rank in hand_ranks:
    if rank in rank_counts:
        rank_counts[rank] += 1
    else:
        rank_counts[rank] = 1

#各スートの出現回数を数える
suit_counts = {}
for rank in hand_suits:
    if rank in suit_counts:
        suit_counts[suit] += 1
    else:
        suit_counts[suit] = 1

#役の判定
if 5 in suit_counts.values() and hand_ranks_numeric == [10,11,12,13,14]:
    print("ロイヤルストレートフラッシュ！")
    time.sleep(2)
    print("…あんた何者…？")
    print("-同じスートかつ１０・Ｊ・Ｑ・Ｋ・Ａの組み合わせ-")
elif 5 in suit_counts.values() and all(hand_ranks_numeric[i]+1 == hand_ranks_numeric[i+1]for i in range(4)):
    ##作業ここまで　
elif 5 in suit_counts.values(): #全て同じスート
    print("フラッシュ！")
    print("-全て同じスート-")
elif 4 in rank_counts.values(): #4枚が同じ数字
    print("フォーカード")
    print("-４つの同じ数字-")
elif 3 in rank_counts.values() and 2 in rank_counts.values(): #3枚と2枚
    print("フルハウス")
    print("-スリーカード＋ワンペア-")
elif 3 in rank_counts.values(): #3枚が同じ数字
    print("スリーカード")
    print("-３つの同じ数字-")
elif list(rank_counts.values()).count(2) == 2: #2枚ペアが2つ
    print("ツーペア")
    print("-２枚の同じ数字のペア-")
elif 2 in rank_counts.values(): #2枚が同じ数字
    print("ワンペア")
    print("-２つの同じ数字-")
else:
    print("ブタ")
    print("役なし")
print("ゲームオーバー")
print("また遊んでね！")