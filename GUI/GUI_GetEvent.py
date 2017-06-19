from pygame import time,event,MOUSEBUTTONDOWN,MOUSEBUTTONUP,NOEVENT


### writen by josmiley ####

_Clic = [0,0,0,0,0,0]
_Ticks = [time.Clock(),time.Clock(),time.Clock(),time.Clock(),time.Clock(),time.Clock()]
LAPS = 200
_NoEvent_Clock = time.Clock()
_Inactiv = 0

def wait():
    ev=event.wait()
    _foo(ev)
    return ev

def poll():
    ev=event.poll()
    _foo(ev)
    return ev

def get(evs=range(50)):
    ev=event.get(evs)
    for e in ev: _foo(e)
    return ev

def _foo(e):
    global _Clic,_Ticks,_Inactiv
    if e.type==NOEVENT:
        _Inactiv+=_NoEvent_Clock.tick()
        e.dict.update({'inactiv':_Inactiv})
    else:
        _Inactiv = 0
        if e.type==MOUSEBUTTONDOWN:
            if e.button!=_Clic[0] or _Ticks[e.button].tick()>LAPS: _Clic=[e.button,0,0,0,0,0]
        elif e.type==MOUSEBUTTONUP:
            if _Ticks[e.button].tick()>LAPS: _Clic=[e.button,0,0,0,0,0]
            else:
                _Clic[e.button]+=1
            e.dict.update({'click':_Clic})
        
