import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
DELTA={pg.K_UP:(0,-5),
       pg.K_DOWN:(0,+5),
       pg.K_LEFT:(-5,0),
       pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect:pg.Rect) -> tuple[bool,bool]:
    yoko,tate = True,True
    if rect.left<0 or WIDTH < rect.right:
        yoko = False
    if rect.top<0 or HEIGHT < rect.bottom:
        tate = False
    return yoko,tate


def gameover(screen: pg.Surface) -> None:
    black_img =pg.Surface((WIDTH, HEIGHT))
    black_img.set_alpha(180)
   
    fonto = pg.font.Font(None,80)
    txt = fonto.render("Game Over",True, (255,255,255))
    black_img.blit(txt,[WIDTH/2-130,HEIGHT/2])


    cry_img = pg.image.load("fig/8.png") 
    black_img.blit(cry_img,[WIDTH/2-200, HEIGHT/2])
    black_img.blit(cry_img,[WIDTH/2+200, HEIGHT/2])

    screen.blit(black_img,[0,0])

    pg.display.update()
    time.sleep(5)
  
    


# def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
#     for r in range(1,11):
#         bb_img = pg.Surface((20*r,20*r))
#         pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
#         bb_imgs.append(bb_img)
#         bb_accs = [a for a in range(1,11)]
#         return bb_imgs,bb_accs

    


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img =pg.Surface((20,20))#空のsurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習2：赤い爆弾
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  # 横座標用の乱数
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦座標用の乱数
    vx,vy=+5,+5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct): #kkとｂｂのレクとが重なったら
            gameover(screen)
            print("game over")
            return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k,tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0]+=tpl[0] #横方向移動
                sum_mv[1]+=tpl[1] #縦移動方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct)!=(True,True):#どこかしらはみ出てる
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])#先ほどの操作をキャンセル
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)#爆弾動く
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *=-1
        if not tate:
            vy *=-1
        
        screen.blit(bb_img,bb_rct) #爆弾表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
