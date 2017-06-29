#!/usr/bin/env python
# -*- coding: utf-8 -*-


### writen by josmiley ###


from pygame import *
font.init()
from math import cos,radians
import GUI_GetEvent

def menu(menu,pos='center',font1=None,font2=None,color1=(128,128,128),color2=None,interline=5,justify=True,light=5,speed=300,lag=30,neon=True,commfont=None,commtime=2000):
    """
    menu(menu,pos,font1=None,font2=None,color1=(128,128,128),color2=None,interline=5,justify=True,light=5)
    
    menu: [str,str,...]
    pos: (int,int)|'topleft'|'topright'|'bottomleft'|'bottomright'|'midtop'|'midleft'|'midright'|'midbottom'|'center': position of menu
    font1: font object (None ==> pygame font): unhighlighted item font
    font2: font object (None ==> font1): highlighted item font
    color1: (int,int,int)|color object: unhighlighted item color
    color2: (int,int,int)|color object: highlighted item color (None => calculated from the light arg)
    interline: int
    justify: boolean: items spacing
    light: 0<=int<=10: use if not color2
    speed: int (0 =>no sliding): anim speed
    lag: int (0<=int<=90)
    neon: boolean: set neon effect
    commfont: font object (None ==> pygame font)
    commtime: int
    
    return: (str,int)|(None,None) if hit escape
    """
    class Item(Rect,object):
        def __init__(self,rect,label,comm):
            Rect.__init__(self,rect)
            self.label = label
            self.comm = comm
                
    def show():
        i = Rect((0,0),font2.size(menu[idx].label))
        if justify: i.center = menu[idx].center 
        else: i.midleft = menu[idx].midleft
        display.update((scr.blit(bg,menu[idx],menu[idx]),
                        scr.blit(font2.render(menu[idx].label,1,(0,0,0)),i.move(3,3)),
                        scr.blit(font2.render(menu[idx].label,1,(255,255,255)),i)))
        time.wait(50)
        scr.blit(bg,r2,r2)
        for item in menu:
            if item!=menu[idx]:
                shadow = font1.render(item.label,1,(0,0,0))
                surfarray.pixels_alpha(shadow)[:] /= 4
                scr.blit(shadow,item.move(3,3))
        [scr.blit(font1.render(item.label,1,color1),item) for item in menu if item!=menu[idx]]
        
        if neon:
            for x,y in ((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)):
                scr.blit(font2.render(menu[idx].label,1,color2),i.move(x,y))
            r = scr.blit(font2.render(menu[idx].label,1,color1),i)
        else:
            r = scr.blit(font2.render(menu[idx].label,1,color2),i)
        
        display.update(r2)
        return r
    
    def anim():
        clk = time.Clock()
        a = [menu[0]] if lag else menu[:]
        c = 0
        while a:
            for i in a:
                g = i.__copy__()
                i.x = i.animx.pop(0)
                r = scr.blit(font1.render(i.label,1,color1),i)
                display.update((g,r))
                scr.blit(bg,r,r)
            c +=1
            if not a[0].animx:
                a.pop(0)
                if not lag: break
            if lag:
                foo,bar = divmod(c,lag)
                if not bar and foo < len(menu):
                    a.append(menu[foo])
            clk.tick(speed)
        
    mouse_bottonright = mouse.get_cursor()[0]
    events = event.get()
    scr = display.get_surface()
    scrrect = scr.get_rect()
    bg = scr.copy()
    if not font1: font1 = font.Font(None,scrrect.h//len(menu)//3)
    if not font2: font2 = font1
    if not color1: color1 = (128,128,128)
    if not color2: color2 = list(map(lambda x:x+(255-x)*light//10,color1))
    if not commfont: commfont = font.Font(None,int(font1.size('')[1]//1.5))
    menu,comm = zip(*[i.partition('::')[0::2]for i in menu])
    m = max(menu,key=font1.size)
    r1 = Rect((0,0),font1.size(m))
    ih = r1.size[1]
    r2 = Rect((0,0),font2.size(m))
    r2.union_ip(r1)
    w,h = r2.w-r1.w,r2.h-r1.h
    r1.h = (r1.h+interline)*len(menu)-interline
    r2 = r1.inflate(w,h).inflate(6,6)
    
    try: setattr(r2,pos,getattr(scrrect,pos))
    except: r2.topleft = pos
    if justify: r1.center = r2.center
    else : r1.midleft = r2.midleft

    menu = [Item(((r1.x,r1.y+e*(ih+interline)),font1.size(i)),i,comm[e]) for e,i in enumerate(menu)if i]
    if justify:
         for i in menu: i.centerx = r1.centerx
         
    if speed:
        for i in menu:
            z = r1.w-i.x+r1.x
            i.animx = [cos(radians(x))*(i.x+z)-z for x in list(range(90,-1,-1))]
            i.x = i.animx.pop(0)
        anim()
        for i in menu:
            z = scrrect.w+i.x-r1.x
            i.animx = [cos(radians(x))*(-z+i.x)+z for x in list(range(0,-91,-1))]
            i.x = i.animx.pop(0)
        
    
    mpos = Rect(mouse.get_pos(),(0,0))
    event.post(event.Event(MOUSEMOTION,{'pos': mpos.topleft if mpos.collidelistall(menu) else menu[0].center}))
    idx = -1
    comm_seen = 0
    while True:
        ev = GUI_GetEvent.poll()
        if ev.type == NOEVENT and ev.inactiv >= commtime:
            if not comm_seen and menu[idx].comm and r.collidepoint(mouse.get_pos()):
                commsurf = commfont.render(menu[idx].comm,1,(0,0,0))
                rcom = commsurf.get_rect(topleft=mouse.get_pos()).inflate(4,4).move(mouse_bottonright).clamp(scrrect)
                combg = scr.subsurface(rcom).copy()
                scr.fill((255,255,255),rcom)
                scr.blit(commsurf,rcom.move(2,2))
                draw.rect(scr,(0,0,0),rcom,1)
                display.update(rcom)
                comm_seen = 1            
        if ev.type == MOUSEMOTION:
            idx_ = Rect(ev.pos,(0,0)).collidelist(menu)
            if idx_ != idx:
                if comm_seen and not r.collidepoint(mouse.get_pos()):
                    display.update(scr.blit(combg,rcom))
                    comm_seen = 0
                if idx_ > -1:
                    idx = idx_
                    r = show()
        elif ev.type == MOUSEBUTTONUP and r.collidepoint(ev.pos):
            ret = menu[idx].label,idx
            break
        elif ev.type == KEYDOWN:
            try:
                idx = (idx + {K_UP:-1,K_DOWN:1}[ev.key])%len(menu)
                r = show()
            except:
                if ev.key in (K_RETURN,K_KP_ENTER):
                    ret = menu[idx].label,idx
                    break
                elif ev.key == K_ESCAPE:
                    ret = None,None
                    break
    if comm_seen:
        display.update(scr.blit(combg,rcom))
    scr.blit(bg,r2,r2)
    
    if speed:
        [scr.blit(font1.render(i.label,1,color1),i) for i in menu]
        display.update(r2)
        time.wait(50)
        scr.blit(bg,r2,r2)
        anim()
    else: display.update(r2)
    
    for ev in events: event.post(ev)
    return ret

def slidemenu(content):
    """
        content example :
        ['one player',
            'two players',
            '',
            'options',
            're-show::click here to show again',
            'quit::good bye']
    """
                     
    from os.path import dirname,join
    here = dirname(__file__)
    scr = display.set_mode((600,560))
    f1 = font.Font('font/321impact.ttf',65)
    f2 = font.Font('font/321impact.ttf',25)
    scr.blit(image.load('img/bg_slidemenu.png'),(0,0))
    mainmenu = f1.render('Main Menu',1,(200,200,200))
    scr.blit(mainmenu,mainmenu.get_rect(midtop=(300,120)))
    display.flip()
    
    while True:
        resp = menu(content,
                     font2=f2,pos='center',color1=(250,100,50),light=10,speed=200,lag=10,commtime=250)
        if resp[0] != "re-show": break

    return resp
