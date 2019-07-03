import pygame
import os
import random
from copy import *

def print_list(List):
    N = len(str(len(List)))
	
    # 横坐标
    Lx = len(List[0])
    L_Lx = len(str(Lx-1))
    for m in range(L_Lx-1,-1,-1):
        print(" "*N,end = '')
        for n in range(0,Lx):
            print('   ',str(n//(10**m))[-1],end = '')
        print()

    # 纵坐标
    for x in range (len(List)):
        x_out = deepcopy("0"*(N-len(str(x)))+str(x))
        print(x_out,List[x],sep = '  ')
    print()

def rgbcolor(color):
    rgb = 0
    if color == 1:
        rgb =(243,255,89) # 黄色
    if color == 2:
        rgb =(255,93,79) # 红色
    if color == 3:
        rgb =(66,72,255) # 蓝色
    if color == 4:
        rgb =(15,255,40) # 绿色
    if color == 5:
        rgb =(255,0,255) # 紫色
    if color == 6:
        rgb =(0,236,255) # 青色
    return rgb

def conadr(width, height, size, thi):
    global playx, playy, playwid, playhei, xsi, ysi
    wisi = width // size -2
    hesi = height // size -2
    xsi = wisi
    ysi = hesi
    x = (width -wisi*size)//2
    y = (height -hesi*size)//2
    playx = x
    playy = y
    playwid = wisi*size
    playhei = hesi*size
    adress = [(x -thi,y -thi),(x +wisi*size +thi,y -thi),(x +wisi*size +thi,y +hesi*size +thi),(x -thi,y +hesi*size +thi)]
    # print("playx, playy, playwid, playhei =",playx, playy, playwid, playhei)
    return adress

def changeblock(color):
    blockback = pygame.Surface((size,size))
    blockback.fill(rgbcolor(color))
    block.set_alpha(100)
    blockback.blit(block,(0,0))
    return blockback

def changesur(list,surface,dy = 5,rgb = (220,220,220),xy = 0):
    if xy ==0 :
        surface = pygame.Surface((playwid,playhei))
    surface.fill(rgb)
    surface.set_colorkey((220,220,220))
    for iy in range(len(list)):
        for ix in range(len(list[0])):
            if list[iy][ix] != 0 and iy >= dy:
                surface.blit(changeblock(list[iy][ix]),(ix*size,(iy-dy)*size))
    return surface

def turnleft(adress):
    return [adress[1],-adress[0]]

def addblock(block, list_stay):
    global jug
    list = deepcopy(list_stay)
    OTL = pain[block[0]]
    OTL_turn = deepcopy(OTL)
    if block[1] != 0 :
        for i in range(block[1]):
            for n in range (len(OTL)):
                OTL_turn[n] = turnleft(OTL_turn[n])
    # print("block =",block)
    # print("OTL, OTL_turn =", OTL, OTL_turn)
    jug = True
    for m in range (len(OTL)):
        if 0 <= block[3][1]+OTL_turn[m][1] < ysi+5 and 0 <= block[3][0]+OTL_turn[m][0] < xsi:
            pass
        else:
            jug = False
            break
        # print("jug",jug,len(list),block[3][1]+OTL_turn[m][1],ysi+4)
        if list[block[3][1]+OTL_turn[m][1]][block[3][0]+OTL_turn[m][0]] != 0 and jug:
            jug = False
            break
    if jug:
        for m in range (len(OTL)):
            # print("坐标",block[3][1]+OTL_turn[m][1],block[3][0]+OTL_turn[m][0])
            # print(len(list[0]),len(list),xsi,ysi)
            list[block[3][1]+OTL_turn[m][1]][block[3][0]+OTL_turn[m][0]] = block[2]
    # print("list =")
    # print_list(list)
    return list

def timemove(block):
    block[3] = [block[3][0],block[3][1]+1] 
    return block

def bomb(bas_stay):
    global score
    bas = deepcopy(bas_stay)
    for i in range(len(bas)):
        i_b = ""
        if 0 in bas[i]:
            pass
        else:
            score += 20
            i_b = deepcopy(i)
            for n in range(len(bas[i])):
                bas[i][n] = 0
            break
    if i_b != "":
        print("delet")
        for n in range(0,i):
            n = i-n
            bas[n] = deepcopy(bas[n-1])
    return bas

def write(msg, size=24, color=(0,0,0)):
    myfont = pygame.font.SysFont("None", size)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext

pygame.init()

scw = 640
sch = 540
size = 20
playx = 0
playy = 0
playwid = 0
playhei = 0
playtime = 0
dtime = 0
FPS =60
xsi = 0
ysi = 0
score = 0
falljug = False
Timejug = False
deadjug = False
endjug = True
jug = True
continuejug = False
stopjug = False
playtimejug = False
baslist = [
    []
]
realist = [
    []
]
realist_b = [
    []
]
juglist = [
    []
]
moveblock = [0,0,0,0] # 图形, 朝向, color, 坐标
nextblock = [0,0,0,0] # 图形, 朝向, color, 坐标

# 基本图形
pain = [
    [[0,0],[1,0],[0,1],[1,1]],
    [[0,0],[-1,-1],[0,-1],[0,1]],
    [[0,0],[0,-1],[0,1],[0,2]],
    [[0,0],[0,-1],[1,-1],[0,1]],
    [[0,0],[0,-1],[1,0],[1,1]],
    [[0,0],[0,-1],[-1,0],[1,0]]
]


screen = pygame.display.set_mode((scw, sch))
background = pygame.Surface(screen.get_size())
background.fill((200,200,200)) 
background = background.convert()

blockjpg = pygame.image.load(os.path.join("data","block.jpg")).convert()
block = pygame.Surface((size,size)) 
pygame.transform.scale(blockjpg, (size, size), block)

clock = pygame.time.Clock()

adr = conadr(2*scw//3, sch, size, 1) # 最后一项不是粗细,是直线扩张的粗细, 比如粗细为 3 时 thi 为 1
baslist = []
for i in range(ysi+5):
    baslist.append(deepcopy([0]*xsi))
realist = deepcopy(baslist)

pygame.draw.line(background, (100,100,100), adr[0], adr[1], 3)
pygame.draw.line(background, (100,100,100), adr[1], adr[2], 3)
pygame.draw.line(background, (100,100,100), adr[2], adr[3], 3)
pygame.draw.line(background, (100,100,100), adr[3], adr[0], 3)

pygame.draw.line(background, (100,100,100), (2*scw//3+20, sch//11), (2*scw//3+20 + 140, sch//11), 5)
pygame.draw.line(background, (100,100,100), (2*scw//3+20 + 140, sch//11), (2*scw//3+20 + 140, sch//11 +140), 5)
pygame.draw.line(background, (100,100,100), (2*scw//3+20 + 140, sch//11 +140), (2*scw//3+20, sch//11 + 140), 5)
pygame.draw.line(background, (100,100,100), (2*scw//3+20, sch//11 + 140), (2*scw//3+20, sch//11), 5)

playsurface = pygame.Surface((playwid,playhei))
playsurface.fill((220,220,220))
playsurface.set_colorkey((220,220,220))
playback = pygame.Surface((playwid,playhei))
playback.fill((220,220,220))
playsurface_next = pygame.Surface((140,140))
playsurface_next.fill((220,220,220))

baslist_next = []
for i in range (7):
    baslist_next.append(deepcopy([0]*7))

mainloop = True
firstmade = True
while mainloop:

    moveblock_b = deepcopy(moveblock)
    realist_b = deepcopy(realist)

    milliseconds = clock.tick(FPS) # do not go faster than this framerate
    playtime += milliseconds / 1000.0
    dtime += milliseconds /1000.0
    if firstmade:
        moveblock = [random.randint(0,5),random.randint(0,3),random.randint(1,6),[xsi//2,3]]
        nextblock = [random.randint(0,5),random.randint(0,3),random.randint(1,6),[xsi//2,3]]
        # print(moveblock)
        firstmade = False

    pygame.display.set_caption("Tetris V 0.2.2 by Yang H. Xu Y.C. Wang Z.Y.  Frame rate %.2f frames per second." % (clock.get_fps()))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False # pygame window closed by user
            print("Your score is",score)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False # user pressed ESC
                print("Your score is",score)
            if event.key == pygame.K_UP:
                if moveblock[0] != 0:
                    moveblock[1] = (moveblock[1] +1) %4
                    continuejug = True
                pass
            if event.key == pygame.K_DOWN:
                if moveblock[0] != 0:
                    moveblock[1] = (moveblock[1] +3) %4
                    continuejug = True
                pass
            if event.key == pygame.K_RIGHT:
                moveblock[3] = [moveblock[3][0]+1,moveblock[3][1]]
                continuejug = True
                pass
            if event.key == pygame.K_LEFT:
                moveblock[3] = [moveblock[3][0]-1,moveblock[3][1]]
                continuejug = True
                pass
            if event.key == pygame.K_SPACE:
                falljug = True
                pass
            if event.key == pygame.K_DELETE:
                stopjug = True
                pass
    
    if playtimejug:
        playtime = deepcopy(playtime_b) 
        dtime = deepcopy(dtime_b)
        playtimejug = False   

    while stopjug:
        playtime_b = deepcopy(playtime)
        dtime_b = deepcopy(dtime)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
                print("Your score is",score)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC
                    print("Your score is",score)

                if event.key == pygame.K_DELETE:
                    stopjug = False
                    playtimejug = True
                    pass
        pass

    realist = addblock(moveblock,baslist)
    # print(nextblock,baslist_next)

    if jug:
        pass
    else:
        realist = deepcopy(realist_b)
        moveblock = deepcopy(moveblock_b)

    if continuejug:
        continuejug = False
        continue
    
    speed = 5 + 0.5 *(score //50)
    speedtime = 1 / speed

    if dtime >= speedtime or falljug or Timejug:
        if Timejug or falljug:
            Timejug = False
        # print("Frame rate %.2f frames per second.Playtime: %.2f seconds" % (clock.get_fps(),playtime))
        else:
            dtime -= speedtime
        # print("time's up")
        moveblock = timemove(moveblock)
        realist = addblock(moveblock,baslist)
        if jug:
            pass
        else:
            falljug = False
            baslist = deepcopy(realist_b)
            # print(baslist,jug,realist)
            moveblock = nextblock
            nextblock = [random.randint(0,5),random.randint(0,3),random.randint(1,6),[xsi//2,3]]
            Timejug = True
        pass

    realist_next = addblock([nextblock[0],nextblock[1],nextblock[2],(3,3)],baslist_next)

    baslist = bomb(baslist)
    playsurface = changesur(realist, playsurface)
    playsurface_next = changesur(realist_next, playsurface_next, 0 ,(230,230,230), 1)
    # print(realist_next, playsurface_next)

    screen.blit(background,(0,0))
    screen.blit(playback,(playx, playy))
    screen.blit(playsurface,(playx, playy))
    screen.blit(playsurface_next,(2*scw//3+20,sch//11))

    # print(2*scw//3+20,sch//9,2*scw//3+20,11*sch//27,2*scw//3+20,17*sch//27)
    screen.blit(write("SCORE: " + str(score)),(2*scw//3+20,11*sch//27))
    screen.blit(write("TIME: %.2f"%(playtime)),(2*scw//3+20,17*sch//27))

    for k in range(6):
        for kb in range(len(baslist[k])):
            if baslist[k][kb] != 0:
                print("Your score is",score)
                deadjug = True # pygame window closed by user
    while deadjug:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
                print("Your score is",score)
                deadjug = False
                endjug = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # pygame window closed by user
                    print("Your score is",score)
                    deadjug = False
                    endjug = False
            
    if endjug:
        pygame.display.flip() 
    pass