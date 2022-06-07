import pygame as pg
import sys
import random


class Screen:   # 画面の作成
    def __init__(self, wh, title):   # 初期化メゾット
        pg.display.set_caption(title)
        self.width, self.height = wh                                 # (400,500)
        self.disp = pg.display.set_mode((self.width, self.height))   # 画面用Surface
        self.rect = self.disp.get_rect()                             # 画面用Rect


class Line:   # ブロックの3段目上に表示される黄色い線の作成
    def __init__(self, color, wh):   # 初期化メゾット
        self.image = pg.Surface(wh)                    # 線Surface
        pg.draw.rect(self.image,color,(0,195,400,5))   # 縦5、横400の四角形を作成
        self.rect = self.image.get_rect()              # 線Rect


class Block():
    ITIX_LIST = [50,150,250,350]       # 画像用Rectのx座標
    ITIY_LIST = [50,150,250,350,450]   # 画像用Rectのy座標
    y = [[0,0,0,0],     
         [0,0,0,0],
         [0,0,0,0],
         [0,0,0,0],
         [0,0,0,0]]
    # それぞれのマスにブロックがないときは0,あるときは入っているブロックの番号

    def __init__(self, n, r, xy):   # 初期化メゾット
        # n:ブロックの番号，r:拡大率，xy:初期配置座標
        self.n = n  
        self.i = 0                                                  # インデクス番号を0に初期化
        self.image = pg.image.load(f"kadai06/block/{self.n}.PNG")   # ブロック用Surface
        self.image.set_colorkey((0,0,0))                            # 黒色部分を透過する
        self.image = pg.transform.rotozoom(self.image, 0, r)        # 画像の拡大
        self.rect = self.image.get_rect()                           # ブロック用Rect
        self.rect.center = xy                                       # ブロック用Rectの中心を初期配置座標に設定

    def move_x(self, event):     # 横移動
        # 既にあるブロックをすり抜けないため移動先にブロックがあるかどうかを確認する
        # gはリストyのインデクス番号であり、ブロック用Rectの中央の場所で確認するリストyの要素を指定するために使う
        g = 0     
        if 50 < self.rect.centery <= 150:    # もし中央のy座標が50よりも大きく、150以下だったら
            g = 1
        if 150 < self.rect.centery <= 250:   # もし中央のy座標が150よりも大きく、250以下だったら
            g = 2
        if 250 < self.rect.centery <= 350:   # もし中央のy座標が250よりも大きく、350以下だったら
            g = 3
        if 350 < self.rect.centery <= 450:   # もし中央のy座標が350よりも大きく、450以下だったら
            g = 4
        if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:       # →が押されたら(右移動)
            self.i = Block.ITIX_LIST.index(self.rect.centerx)          # 今のインデクス番号を取得
            if self.i <= 2 and Block.y[g][self.i+1] == 0:              # インデクス番号が2以下かつ移動先にブロックがなかったら
                self.i += 1                                            # インデクス番号を1大きくする
            self.rect.centerx = Block.ITIX_LIST[self.i]                # 画像用Rectのx座標を変更する
        if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:        # ←が押されたら(左移動)
            self.i = Block.ITIX_LIST.index(self.rect.centerx)          # 今のインデクス番号を取得
            if self.i >= 1 and Block.y[g][self.i-1] == 0:              # インデクス番号が1以上かつ移動先にブロックがなかったら
                self.i -= 1                                            # インデクス番号を1小さくする
            self.rect.centerx = Block.ITIX_LIST[self.i]                # 画像用Rectのx座標を変更する

    def move_y(self):  # 縦移動。ブロックが積まれたところのインデクス番号を返す。
        for g in range(4):
            if Block.y[g+1][self.i] != 0 and self.rect.centery == Block.ITIY_LIST[g]:   
            # 落ちてくるブロックの真下に既にブロックがあったら、その上に落ちてきたものを表示
                Block.y[g][self.i] = self.n   # ブロックの位置のリストの要素を画像の番号に変更
                return  g, self.i
        if Block.y[4][self.i] == 0 and self.rect.centery >= 450:
           # 落ちてくるブロックの下にブロックがなく、ブロックが画面の一番下についたら
            Block.y[4][self.i] = self.n   # ブロックの位置のリストの要素を画像の番号に変更。一番下の段用。
            return  4, self.i
        else:
            return 9, 9

    def add_1(self, gy, ry):    # g:行、r:列      落ちてくるブロックについての計算
        if gy == 9 and ry == 9:   # ブロック落下中
            return
        number = Block.y[gy][ry]  # ブロックの番号
        while True:
            # 左右と下のブロックを確認し、番号が同じだったら番号同士を加算する
            # 加算されたブロックは落ちてきたブロックの場所に表示され、その他のブロックは消える
            original_n = number   # 元の番号
            if ry >= 1:
                if Block.y[gy][ry-1] != 0 and Block.y[gy][ry-1] == original_n:   # 左のブロックを確認
                    Block.y[gy][ry-1] = 0
                    number += original_n
                    Block.y[gy][ry] = number
            if ry <= 2:
                if Block.y[gy][ry+1] != 0 and Block.y[gy][ry+1] == original_n:   # 右のブロックを確認
                    Block.y[gy][ry+1] = 0
                    number += original_n
                    Block.y[gy][ry] = number
            if gy != 4:
                if Block.y[gy+1][ry] != 0 and Block.y[gy+1][ry] == original_n:   # 下のブロックを確認
                    Block.y[gy][ry] = 0 
                    number += original_n
                    Block.y[gy+1][ry] = number
                    gy += 1    # 加算後にさらに同じブロックがあった場合のために縦一列を確認
            if number == original_n:   # すべての計算が終わったら
                break

    def add_2(self):      # 既に存在するブロックの計算
        # リストyのすべての要素を調べ、左右または下に同じブロックがあったら加算。計算方法はadd_1関数を同様。
        while True:
            a = 1
            for g in range(5):
                for r in range(4):
                    if Block.y[g][r] != 0:
                        original_number = Block.y[g][r]
                        number = original_number
                        if r >= 1:
                            if Block.y[g][r-1] != 0 and Block.y[g][r-1] == original_number:   # 左のブロックを確認
                                Block.y[g][r-1] = 0
                                number += original_number
                                a += 1
                                Block.y[g][r] = number
                        if r <= 2:
                            if Block.y[g][r+1] != 0 and Block.y[g][r+1] == original_number:   # 右のブロックを確認
                                Block.y[g][r+1] = 0
                                number += original_number
                                a += 1
                                Block.y[g][r] = number
                        if g != 4:
                            if Block.y[g+1][r] != 0 and Block.y[g+1][r] == original_number:   # 下のブロックを確認
                                Block.y[g][r] = 0
                                number += original_number
                                a += 1
                                Block.y[g+1][r] = number
                        if original_number == number:   # 加算処理がなかったら、次の繰り返しに移る
                            continue
            if a == 1:   # 一度も加算処理がされなかったら
                break

    def block_stack(self, screen):   # 積まれたブロックの描写
        for g in range(5):    # 行
            for r in range(4):   # 列
                if g <= 3:   # 2段目以上のブロックに行う
                    if Block.y[g][r] != 0 and Block.y[g+1][r] == 0:    # 下のブロックがなくなったら、下に詰める
                        Block.y[g+1][r] = Block.y[g][r]
                        Block.y[g][r] = 0
                if Block.y[g][r] != 0:   # リストyの要素がブロックの数字だったら
                    self.stack_image = pg.image.load(f"kadai06/block/{Block.y[g][r]}.PNG")
                    self.stack_image = pg.transform.rotozoom(self.stack_image, 0, 0.7)
                    self.stack_rect = self.stack_image.get_rect()
                    self.stack_rect.center = (Block.ITIX_LIST[r],Block.ITIY_LIST[g])   # 描写する場所はインデクス番号で指定
                    screen.disp.blit(self.stack_image, self.stack_rect)

    def game_clear(self):   # ゲームクリア処理
        # ゲームクリアしたら画面中央に「GAME CLEAR」の文字を表示
        image = 0
        image_rect = 0
        for g in range(5):
            for r in range(4):
                flag = False
                # txt = 0
                # txt_rect = 0
                if Block.y[g][r] >= 100:   # 加算後に100以上の数字ができたら
                    flag = True
                    image = pg.image.load(f"kadai06/block/StageClear.PNG")
                    image_rect = image.get_rect()
                    image_rect.center = 200, 250
                    # font = pg.font.Font(None,80)
                    # txt = font.render("GAME CLEAR", True, (255,255,255))
                    # txt_rect = txt.get_rect()
                    # txt_rect.center = 200, 250
                    return flag, image, image_rect
                    #  return flag, txt, txt_rect
        return flag, image, image_rect
        # return flag, txt, txt_rect


def main():   # メインプログラム
    clock = pg.time.Clock()

    #BGM   #C0B21042
    pg.mixer.init()
    pg.mixer.music.load('kadai06/BGM/たぬきちの冒険.mp3')
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(0.1)

    screen = Screen((400, 500), "100以上をつくろう!!")
    line = Line((255,255,0), (400,500))
    n = random.randrange(10,31,10)     # 10～30のブロック画像をランダムに指定
    block = Block(n, 0.7, (50,50))

    while True:
        screen.disp.fill((0,0,0))                    # 画面を黒で塗りつぶす
        screen.disp.blit(screen.disp, (0,0))         # 画面の表示
        screen.disp.blit(line.image, (0,0))          # 線の表示
        block.block_stack(screen)                    # 積まれたブロックの表示
        screen.disp.blit(block.image, block.rect)    # 上からの落ちてくるブロックの表示
        block.rect.move_ip(0, 1)                     # ブロックの落下
        gy, ry = block.move_y()                      # y軸の移動
        for g in range(5):
            for r in range(4):
                if (block.y[g][r] != 0 
                        and block.rect.centerx == block.ITIX_LIST[r] 
                        and block.rect.centery == block.ITIY_LIST[g]):    
                # 次のブロックを出す。Blockクラス内にあるリストyの要素が0でない、
                # かつ、ブロック用Rectの座標が積んだブロックの中央にきたとき
                    n = random.randrange(10,31,10)   # 10～30のブロック画像をランダムに指定
                    block = Block(n, 0.7, (50,50))
          
        block.add_1(gy, ry)                          # 落下ブロックの加算
        block.add_2()                                # 既にあるブロックの加算
        flag, image, image_rect = block.game_clear()     # ゲームクリアの判定
        if flag:   # ゲームクリアしたら
            #BGMを初期化し、GAMECLEAR効果音を鳴らす  #C0B21042
            pg.mixer.init()
            pg.mixer.music.load('kadai06/BGM/GAMECLEAR.mp3')
            pg.mixer.music.play()
            pg.mixer.music.set_volume(0.2)
            screen.disp.fill((0,0,0))
            screen.disp.blit(image, image_rect)
            pg.display.update()
            clock.tick(0.5)
            return
        for event in pg.event.get():
            block.move_x(event)   # x軸の移動
            if event.type == pg.QUIT: return   # ✕ボタンでmain関数から戻る
        for r in range(4):
            if Block.y[1][r] != 0:   # 下から4段目にブロックが積まれたらGAMEOVER
                #BGMを初期化し、GAMEOVER効果音を鳴らす  #C0B21042
                pg.mixer.init()
                pg.mixer.music.load('kadai06/BGM/GAMEOVER.mp3')
                pg.mixer.music.play()
                pg.mixer.music.set_volume(0.3)
                screen.disp.fill((0,0,0))
                font = pg.font.Font(None,80)
                txt = font.render("GAME OVER", True, (255,255,255))
                txt_rect = txt.get_rect()
                txt_rect.center = 200, 250
                screen.disp.blit(txt, txt_rect)
                pg.display.update()
                clock.tick(0.5)
                return

        pg.display.update()  # 画面の更新
        clock.tick(100)


if __name__ == "__main__":
    pg.init() 
    main()
    pg.quit()
    sys.exit()