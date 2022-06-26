#
#  Copyright (c) 2022 Jesper Olsen
#  License: MIT, see License.txt
#

import sys
from pprint import pprint
import time
import collections


pval={}
pval['P']=(
    100, 100, 101, 102, 104, 106, 108, 900,
    100, 100, 102, 104, 106, 109, 112, 900,
    100, 100, 104, 108, 112, 115, 118, 900,
    100, 100, 107, 114, 121, 128, 135, 900,
    100, 100, 106, 112, 118, 124, 132, 900,
    100, 100, 104, 108, 112, 116, 120, 900,
    100, 100, 102, 104, 106, 108, 112, 900,
    100, 100, 101, 102, 104, 106, 108, 900)
pval['p']=(
    -900, -108, -106, -104, -102, -101, -100, -100,
    -900, -112, -109, -106, -103, -102, -100, -100,
    -900, -118, -115, -112, -109, -104, -100, -100,
    -900, -135, -128, -121, -114, -107, -100, -100,
    -900, -132, -124, -118, -112, -106, -100, -100,
    -900, -120, -116, -112, -108, -104, -100, -100,
    -900, -112, -108, -106, -104, -102, -100, -100,
    -900, -108, -106, -104, -102, -101, -100, -100)

pval['R']=(
    500, 500, 500, 500, 500, 500, 522, 500,
    500, 500, 500, 500, 500, 500, 522, 500,
    500, 500, 500, 500, 500, 500, 522, 500,
    500, 500, 500, 500, 500, 500, 522, 500,
    500, 500, 500, 500, 500, 500, 522, 500,
    500, 500, 500, 500, 500, 500, 522, 500,
    500, 500, 500, 500, 500, 500, 522, 500,
    500, 500, 500, 500, 500, 500, 522, 500)
pval['r']=(
    -500, -522, -500, -500, -500, -500, -500, -500,
    -500, -522, -500, -500, -500, -500, -500, -500,
    -500, -522, -500, -500, -500, -500, -500, -500,
    -500, -522, -500, -500, -500, -500, -500, -500,
    -500, -522, -500, -500, -500, -500, -500, -500,
    -500, -522, -500, -500, -500, -500, -500, -500,
    -500, -522, -500, -500, -500, -500, -500, -500,
    -500, -522, -500, -500, -500, -500, -500, -500)
pval['N']=(
    315, 315, 315, 315, 315, 315, 315, 315,
    315, 320, 320, 320, 320, 320, 320, 315,
    315, 320, 325, 325, 330, 330, 320, 315,
    315, 320, 325, 325, 330, 330, 320, 315,
    315, 320, 325, 325, 330, 330, 320, 315,
    315, 320, 325, 325, 330, 330, 320, 315,
    315, 320, 320, 320, 320, 320, 320, 315,
    315, 315, 315, 315, 315, 315, 315, 315)
pval['n']=( 
    -315, -315, -315, -315, -315, -315, -315, -315,
    -315, -320, -320, -320, -320, -320, -320, -315,
    -315, -320, -330, -330, -325, -325, -320, -315,
    -315, -320, -330, -330, -325, -325, -320, -315,
    -315, -320, -330, -330, -325, -325, -320, -315,
    -315, -320, -330, -330, -325, -325, -320, -315,
    -315, -320, -320, -320, -320, -320, -320, -315,
    -315, -315, -315, -315, -315, -315, -315, -315)
pval['B']=( 
    339, 350, 350, 350, 350, 350, 350, 350,
    339, 350, 350, 350, 350, 350, 350, 350,
    339, 350, 350, 350, 350, 350, 350, 350,
    339, 350, 350, 350, 350, 350, 350, 350,
    339, 350, 350, 350, 350, 350, 350, 350,
    339, 350, 350, 350, 350, 350, 350, 350,
    339, 350, 350, 350, 350, 350, 350, 350,
    339, 350, 350, 350, 350, 350, 350, 350)
pval['b']=( 
    -350, -350, -350, -350, -350, -350, -350, -339,
    -350, -350, -350, -350, -350, -350, -350, -339,
    -350, -350, -350, -350, -350, -350, -350, -339,
    -350, -350, -350, -350, -350, -350, -350, -339,
    -350, -350, -350, -350, -350, -350, -350, -339,
    -350, -350, -350, -350, -350, -350, -350, -339,
    -350, -350, -350, -350, -350, -350, -350, -339,
    -350, -350, -350, -350, -350, -350, -350, -339)
pval['Q']=( 
    900, 900, 900, 900, 900, 900, 900, 900, 
    900, 900, 900, 900, 900, 900, 900, 900, 
    900, 900, 900, 900, 900, 900, 900, 900, 
    900, 900, 900, 900, 900, 900, 900, 900, 
    900, 900, 900, 900, 900, 900, 900, 900, 
    900, 900, 900, 900, 900, 900, 900, 900, 
    900, 900, 900, 900, 900, 900, 900, 900, 
    900, 900, 900, 900, 900, 900, 900, 900)
pval['q']=( 
    -900, -900, -900, -900, -900, -900, -900, -900, 
    -900, -900, -900, -900, -900, -900, -900, -900, 
    -900, -900, -900, -900, -900, -900, -900, -900, 
    -900, -900, -900, -900, -900, -900, -900, -900, 
    -900, -900, -900, -900, -900, -900, -900, -900, 
    -900, -900, -900, -900, -900, -900, -900, -900, 
    -900, -900, -900, -900, -900, -900, -900, -900, 
    -900, -900, -900, -900, -900, -900, -900, -900)

pval['K']=(
    24,  24,  12,  6,  6,  12,  24,  24, 
    24,  12,  6,   0,  0,  6,   12,  24, 
    12,  6,   0,  -6, -6,  0,   6,  12, 
    6,   0,  -6, -12, -12, -6,  0,  6, 
    6,   0,  -6, -12, -12, -6,  0,  6, 
    12,  6,   0,  -6, -6,  0,   6,  12, 
    24,  12,  6,   0,  0,  6,   12,  24, 
    24,  24,  12,  6,  6,  12,  24,  24)
pval['k']=(
      -24, -18, -12, -6, -6, -12, -24, -24, 
      -24, -12, -6,  -0, -0, -6,  -12, -24, 
      -12, -6,  -0,   6,  6, -0,  -6,  -12, 
      -6,  -0,   6,  12,  12,  6, -0,  -6, 
      -6,  -0,   6,  12,  12,  6, -0,  -6, 
      -12, -6,  -0,   6,  6, -0,  -6,  -12, 
      -24, -12, -6,  -0, -0, -6,  -12, -24, 
      -24, -24, -12, -6, -6, -12, -24, -24)

def eval_material(board):
    return sum([pval[p][i] for i,p in enumerate(board) if p!='.'])

def abs_eval_material(board):
    return sum([abs(pval[p][i]) for i,p in enumerate(board) if board[i]!='.'])

def eval_pawn_structure(board):
    return sum(score_pawn_structure(board))

def score_pawn_structure(board):
    dl={}
    isolated_penalty={'p': 20, 'P': -20}
    double_penalty={'p': 4, 'P': -4}
    for c in ['P','p']:
        l=sorted([i//8 for i in range(64) if board[i]==c])
        dl[c]=list(dict.fromkeys(l)) # remove duplicates, preserve order
        n=len(l)-len(dl[c])
        #print(f"Double pawns {c}: {n}")
        yield double_penalty[c]*n

        l=[100]+dl[c]+[100] 
        n=sum([1 for i,c in enumerate(l[:-1]) if i>0 and l[i-1]+1!=l[i] and l[i]+1!=l[i+1]])
        #print(f"Isolated pawns {c}: {n}")
        yield isolated_penalty[c]*n

    def freeP(i):
        lr=[range(i+1,i//8*8+7)]
        if i//8<7: lr+=[range(i+9,(i//8+1)*8+7)]
        if i//8>0: lr+=[range(i-7,(i//8-1)*8+7)]
        for r in lr:
            for q in r:
                if board[q]=='p': return False
        return True

    def freep(i):
        lr=[range(i-1,i//8*8,-1)]
        if i//8<7: lr+=[range(i+7,(i//8+1)*8,-1)]
        if i//8>0: lr+=[range(i-9,(i//8-1)*8,-1)]
        for r in lr:
            for q in r:
                if board[q]=='P': 
                    return False
        return True

    #passed pawns
    passed=sum([2*q%8*q%8 for q in [i for i,c in enumerate(board) if c=='P'] if freeP(q)])  
    yield passed
    #print("Passed P",passed)
    passed=sum([-2*(7-q%8)*(7-q%8) for q in [i for i,c in enumerate(board) if c=='p'] if freep(q)])  
    #print("Passed p",passed)
    yield passed



pieces="RNBKQP"
WHITE=1
BLACK=0
INFINITE=10000
p2colour={p:WHITE for p in pieces} | {p.lower():BLACK for p in pieces} | {'.':2}

def i2str(i):
    """Translate integer coordinates to chess square"""
    x=7-i//8
    y=i%8 +1
    return "ABCDEFGH"[x]+str(y)

def m2str(d): 
    return f"{i2str(d['from'])}{'x' if 'kill' in d else ' '}{i2str(d['to'])}"



# h1 is 0, a8 is 63
# 63  55  47  39  31  23  15   7
# 62  54  46  38  30  22  14   6
# 61  53  45  37  29  21  13   5
# 60  52  44  36  28  20  12   4
# 59  51  43  35  27  19  11   3
# 58  50  42  34  26  18  10   2
# 57  49  41  33  25  17   9   1
# 56  48  40  32  24  16   8   0

#
#  +9 +1 -7                +1,+1  0,+1  -1,+1          
#  +8    -8                +1,0         -1,0
#  +7 -1 -9                +1,-1  0,-1  -1,-1
#
#    +10 x -6               +1,+2  x  -1,+2
# +17  x x  x -15        +2,+1     x        -2,+1
#      x X  x                      X        
# +15  x x  x -17        +2,-1     x        -2,-1
#     +6 x  -10              +1,-2 x  -1,-2


#Build a 'ray-map' - squares that rook,bishop,queen can glide to on an empty board
#+ map for king, Knight

def print_board(board):
    print()
    for y in range(7,-1,-1):
        print(f"{y+1} ", end="")
        for x in range(8):
            print(board[(7-x)*8+y],end="")
        print()
    print("  ABCDEFGH")


r={}
for k in ["w","e","n","s","nw","ne","sw","se","k","knight"]:
    r[k]={}
for i in range(64):
    r['w'][i]=range(i+8,7*8+1+i%8,8)
    r['e'][i]=range(i-8,i%8-1,-8)
    r['n'][i]=range(i+1,(i//8)*8+8)
    r['s'][i]=range(i-1,(i//8)*8-1,-1)
    r['nw'][i]=range(i+9,min(64,i+(8-i%8)*9),9)
    r['ne'][i]=range(i-7,max(-1,i-(7-i%8)*7-1),-7)
    r['sw'][i]=range(i+7,min(64,i+i%8*7+1),7)
    r['se'][i]=range(i-9,max(-1,i-(i%8)*9-1),-9)

    x=i//8 #col
    y=i%8  #row

    #Knight
    l=[(-1,2),(-2,1),(-2,-1), (-1,-2), (1,-2), (2,-1), (2,1), (1,2)]
    l=[(a,b) for (a,b) in map(lambda t: (t[0]+x,t[1]+y),l) if a>=0 and a<8 and b>=0 and b<8]
    r['knight'][i]=map(lambda t: t[0]*8+t[1], l)

    #King
    l=[(1,1),(0,1),(-1,1),(1,0),(-1,0),(1,-1),(0,-1),(-1,-1)]
    l=[(a,b) for (a,b) in map(lambda t: (t[0]+x,t[1]+y),l) if a>=0 and a<8 and b>=0 and b<8]
    r['k'][i]=map(lambda t: t[0]*8+t[1], l)

for x in r:
    for i in r[x]:
        r[x][i]=list(r[x][i])

def to_string(self):
    board=list("."*64)
    for (tp,i,is_white) in self.get_pieces():
        if is_white==1:
            board[i]=tp.upper()
        else:
            board[i]=tp.lower()
    return "".join(board)

def ray_moves(rays, game, frm):
    board=game.board
    def extract(board, frm, rto):
        for to in rto:
            if board[to]=='.': 
                yield {'from': frm, 'to': to, 'val': pval[board[frm]][to]-pval[board[frm]][frm]}
            elif p2colour[board[to]]!=p2colour[board[frm]]:  #capture - end here
                yield {'from':frm, 'to': to, 'kill':(board[to],to), 'val': pval[board[frm]][to]-pval[board[frm]][frm]-pval[board[to]][to]}
                return 
            else: return

    for k in rays:
        yield from extract(board, frm, r[k][frm])

def king_moves(game, frm):
    board=game.board
    for to in r['k'][frm]:
        if board[to]=='.':
            #yield {'from':frm, 'to':to} 
            yield {'from':frm, 'to':to, 
                   'val': pval[board[frm]][to]-pval[board[frm]][frm]} 
        elif p2colour[board[to]]!=p2colour[board[frm]]:
            #yield {'from':frm, 'to':to, 'kill':(board[to],to)} 
            yield {'from':frm, 'to':to, 'kill':(board[to],to), 
                   'val': pval[board[frm]][to]-pval[board[frm]][frm]-pval[board[to]][to]} 


    colour=p2colour[board[frm]]
    cc=game.can_castle[-1][colour]
    if cc['short'] or cc['long']:
        if p2colour[board[frm]]==WHITE:
            if frm==24:
                if board[0]=='R' and board[8]=='.' and board[16]=='.': 
                    yield {'from':frm, 'to': 8, 'castle':True,
                           'val': pval['K'][8]-pval['K'][frm] + pval['R'][frm-8]-pval['R'][frm-24]} 
                if board[56]=='R' and board[32]=='.' and board[40]=='.' and board[48]=='.': 
                    yield {'from':frm, 'to':48, 'castle':True,
                           'val': pval['K'][48]-pval['K'][frm] + pval['R'][frm+8]-pval['R'][frm+32]} 

        else:
            if frm==31:
                if board[7]=='r' and board[15]=='.' and board[23]=='.': 
                    yield {'from':frm, 'to': 15, 'castle':True,
                           'val': pval['k'][15]-pval['k'][frm] + pval['r'][frm-8]-pval['r'][frm-24]}
                if board[63]=='r' and board[55]=='.' and board[47]=='.' and board[39]=='.': 
                    yield {'from':frm, 'to': 55, 'castle':True,
                           'val': pval['k'][55]-pval['K'][frm] + pval['R'][frm+8]-pval['R'][frm+32]} 

def knight_moves(game, frm):
    board=game.board
    for to in r['knight'][frm]:
        if board[to]=='.':
            yield {'from':frm, 'to':to, 'val': pval[board[frm]][to]-pval[board[frm]][frm]} 
        elif p2colour[board[to]]!=p2colour[board[frm]]:
            yield {'from':frm, 'to':to, 'kill':(board[to],to), 'val': pval[board[frm]][to]-pval[board[frm]][frm]-pval[board[to]][to]} 

def pawn_moves(game, frm):
    board=game.board
    log=game.log
    last_move=None if log==[] else (board[log[-1]['to']],log[-1]['from'],log[-1]['to'])
    x=frm//8 #col
    y=frm%8  #row
    if p2colour[board[frm]]==WHITE:
        if y<7 and board[frm+1]=='.': 
            if y==6:
                yield {'from':frm, 'to':frm+1, 'val':pval['P'][frm+1]-pval['P'][frm], 'transform':('P','Q')}
            else:
                yield {'from':frm, 'to':frm+1, 'val':pval['P'][frm+1]-pval['P'][frm]}
        if y==1 and board[frm+1]=='.' and board[frm+2]=='.': 
            yield {'from':frm, 'to':frm+2, 'val':pval['P'][frm+2]-pval['P'][frm]}
        if x<7 and y<7:
            if p2colour[board[frm+9]]==BLACK: #capture
                yield {'from':frm, 'to':frm+9, 'kill':(board[frm+9],frm+9), 
                       'val':pval['P'][frm+9]-pval['P'][frm]-pval[board[frm+9]][frm+9]}
            elif (y==4 and board[frm+9]=='.' and last_move==('p',frm+8,frm+10)): #en passant capture
                yield {'from':frm, 'to':frm+9, 'kill':('p',frm+10),
                       'val':pval['P'][frm+9]-pval['P'][frm]-pval['p'][frm+10]}
        if x>0 and y<7:
            if p2colour[board[frm-7]]==BLACK: #capture
                yield {'from':frm, 'to':frm-7, 'kill':(board[frm-7],frm-7), 
                       'val':pval['P'][frm-7]-pval['P'][frm]-pval[board[frm-7]][frm-7]}
            elif (y==4 and board[frm-7]=='.' and last_move==('p',frm-6,frm-8)): #en passant capture
                yield {'from':frm, 'to':frm-7, 'kill':('p',frm-8), 
                       'val':pval['P'][frm-7]-pval['P'][frm]-pval['p'][frm-8]}
    else:
        if y>0 and board[frm-1]=='.': #1 forward
            if y==1:
                yield {'from':frm, 'to': frm-1, 'val':pval['p'][frm-1]-pval['p'][frm], 'transform':('p','q')}  
            else:
                yield {'from':frm, 'to': frm-1, 'val':pval['p'][frm-1]-pval['p'][frm]}  
        if y==6 and board[frm-1]=='.' and board[frm-2]=='.': #2 forward
            yield {'from':frm, 'to':frm-2, 'val': pval['p'][frm-2]-pval['p'][frm]} 
        if x<7 and y>0:
            if p2colour[board[frm+7]]==WHITE: #capture
                yield {'from': frm, 'to': frm+7, 'kill':(board[frm+7],frm+7), 'val':pval['p'][frm+7]-pval['p'][frm]-pval[board[frm+7]][frm+7]}
            elif (y==3 and board[frm+6]=='.' and last_move==('P',frm+6,frm+8)):  #en passant capture
                yield {'from':frm, 'to': frm+7, 'kill':('P',frm+8),
                       'val':pval['p'][frm+7]-pval['p'][frm]-pval['P'][frm+8]}
        if x>0 and y>0:
            if p2colour[board[frm-9]]==WHITE: #capture
                yield {'from':frm, 'to': frm-9, 'kill':(board[frm-9],frm-9), 'val':pval['p'][frm-9]-pval['p'][frm]-pval[board[frm-9]][frm-9]}
            elif (y==3 and board[frm-9]=='.' and last_move==('P',frm-10,frm-8)): #en passant capture
                yield {'from': frm, 'to': frm-9, 'kill':('P',frm-8),
                       'val':pval['p'][frm-9]-pval['p'][frm]-pval['P'][frm-8]}
    
rrays=['n','s','e','w']
brays=['ne','nw','se','sw']

import functools
p2moves={'r': functools.partial(ray_moves,rrays),
         'n': functools.partial(knight_moves),
         'b': functools.partial(ray_moves,brays),
         'k': functools.partial(king_moves),
         'q': functools.partial(ray_moves,rrays+brays),
         'p': functools.partial(pawn_moves)
         }


class Game:
    def __init__(self):
        self.log=[]
        self.board=list('R......rN.....pnB.....pbKP....pkQ.....pqBP....pbNP.....nRP.....r')
        self.board=list('R......rN......nB......bK......kQ......qB......bN......nR......r') # no pawns
        self.board=list('RP......NP......BP......KP.....kQP......BP......NP......RP......') # black only king
        self.board=list('R.......N.......B.......K......kQ.......B.......N.......R.......') # black only king, no pawns
        self.board=list('R.......................K......kQ.......................R.......') # black only king, white K,Q,R
        self.board=list('RP....prNP....pnBP....pbKP....pkQP....pqBP....pbNP....pnRP....pr') # root 

        #Test pos
        #board=list('.'*64)
        #board[23]='k'
        #board[6]='R'
        #board[56]='R'
        #board[32]='Q'
        #board[24]='K'

        self.can_castle=[{WHITE: {'short': True, 'long': True}, BLACK:{'short': True, 'long': True}}]
        self.MAX_DEPTH=50
        self.UPPER_BOUND=-1
        self.LOWER_BOUND=1
        self.material=sum([pval[p][i] for i,p in enumerate(self.board) if p!='.'])
        #self.mobility={WHITE: 0, BLACK: 0}
        self.rep={("".join(self.board),self.turn()): 1}
        self.ttable={} #transposition table
        self.ktable=[collections.Counter() for i in range(self.MAX_DEPTH)]

    def turn(self):
        if (len(self.log)+1)%2==WHITE: return WHITE
        return BLACK

    def moves(self, colour=None):
        if colour==None: colour=(len(self.log)+1)%2
        for i,p in ((i,p) for (i,p) in enumerate(self.board) if p2colour[p]==colour):
            yield from p2moves[p.lower()](self,i)    

    def legal_moves(self):
        def legal(game, m):
            self.update(m)
            flag=[d for d in self.moves() if 'kill' in d and d['kill'][0].lower()=='k']==[]
            self.backdate()
            return flag

        return sorted([m for m in self.moves() if legal(self,m)], key=lambda x: x['val'], reverse=self.turn()==WHITE)

    def update(self, d):
        self.log+=[d]
        if 'castle' in d:
            colour=p2colour[self.board[d['from']]]
            cc=self.can_castle[-1].copy()
            cc[colour]['short']=False
            cc[colour]['long']=False
            self.can_castle+=[cc]
            if d['to']<=15: #short
                self.board[d['from']-8]=self.board[d['from']-24]
                self.board[d['from']-24]='.'
            else: # long
                self.board[d['from']+8]=self.board[d['from']+32]
                self.board[d['from']+32]='.'
        if 'transform' in d:
            self.board[d['to']]=d['transform'][1]
        else:
            self.board[d['to']]=self.board[d['from']]
        self.board[d['from']]='.'
        self.material+=d['val']

    def backdate(self):
        if self.log==[]: return
        d=self.log.pop()
        if 'castle' in d:
            colour=p2colour[self.board[d['to']]]
            self.can_castle.pop()
            if d['to']<=15: #short
                self.board[d['from']-24]=self.board[d['from']-8]
                self.board[d['from']-8]='.'
            else: # long
                self.board[d['from']+32]=self.board[d['from']+8]
                self.board[d['from']+8]='.'
            
        if 'transform' in d:
            self.board[d['from']]=d['transform'][0]
        else:
            self.board[d['from']]=self.board[d['to']]
        self.board[d['to']]='.'
        if 'kill' in d: self.board[d['kill'][1]]=d['kill'][0] #kill stores coor because ireg en passant
        self.material-=d['val']

    def display(self):
        print_board(self.board)

    def retrieve(self,key):
        if key in self.ttable:
            return self.ttable[key]
        return None

    def store(self, depth,score,alpha,beta,move):
        key="".join(self.board),self.turn()
        if key not in self.ttable or self.ttable[key]['depth']<=depth:
            self.ttable[key]={'depth': depth, 'score': score, 'move': move, 'bound':'EXACT'}
            if score<=alpha:
                self.ttable[key]['bound']='UPPER'
            if score>=beta:
                self.ttable[key]['bound']='LOWER'
        self.ktable[depth][(move['from'],move['to'])]+=1

    def eval(self):
        v=self.material + eval_pawn_structure(self.board) #+ game.mobility[WHITE]-game.mobility[BLACK]
        return v if self.turn()==WHITE else -v

    def in_check(self, colour=None):
        if colour==None:
            colour=BLACK if self.turn()==WHITE else WHITE
        return [m for m in self.moves(colour) if 'kill' in m and m['kill'][0].lower()=='k']!=[]

def score_moves(game,depth=1):
   t0=time.time()
   moves=game.legal_moves()
   if moves==[]: return []
   for depth in range(1, depth+1):
       alpha=-INFINITE
       best =-INFINITE # remember 1st move regardless of value
       beta = INFINITE

       #search 1st move with full beam
       game.update(moves[0])
       scores=[-pvs(game, depth-1, 1, -beta, -max(alpha,best)) ]
       best=scores[0]
       game.backdate()

       for m in moves[1:]:
           if best>=beta: 
               print("Checkmate - shouldn't happen here")
               print(moves)
               print(scores)
               return None
           game.update(m)
           alpha=max(best,alpha)
           scores+=[-pvs(game, depth-1, 1, -alpha-1, -alpha)]
           if scores[-1]>best:
               if scores[-1]>alpha and scores[-1]<beta and depth>2:
                   scores[-1]=-pvs(game, depth-1, 1, -beta, -scores[-1])
               best=scores[-1]
           game.backdate()

       l=[(scores[i],m) for i,m in enumerate(moves)]
       l.sort(key=lambda x: x[0], reverse=True)
       #for i, (s,m) in enumerate(l):
       #    print(i, s,m, m2str(m))
       moves=[m for (s,m) in l]
   return moves

def quiescence_fab(game, depth, ply, alpha, beta):
    best=-INFINITE+ply
    moves=game.legal_moves()
    lt=game.log[-1]['to'] 
    if game.board[lt].lower()!='p' or (lt%8 != 6 or lt%8!=1): # quiescent
        moves=[m for m in moves if 'kill' in m]
        moves=[m for m in moves if m['to']==lt]
    if moves==[]: return game.eval()
    for m in moves:
        game.update(m)
        score=-quiescence_fab(game, depth-1, ply+1, -beta, -max(alpha,best))
        if score>best:
            best=score
            if best>=beta:
                game.backdate()
                return best
        game.backdate()
    return best
    
def pvs(game, depth, ply, alpha, beta):
    key="".join(game.board),game.turn()
    if game.rep.setdefault(key,0)>=2:
        return 0
    game.rep[key]+=1

    d=game.retrieve(key)
    if d!=None:
        if d['depth']>=depth:
            if d['bound']=='EXACT': return d['score']
            if d['bound']=='LOWER': alpha=max(alpha,d['score'])
            elif d['bound']=='UPPER': beta=min(beta,d['score'])
            if alpha>=beta: return d['score']

    bscore=-INFINITE+ply
    bmove=None
    moves=game.legal_moves()


    # move killer moves to head of list
    for i in [i for (k,v) in game.ktable[depth].most_common(1) for (i,m) in enumerate(moves) if i!=0 and (m['from'],m['to'])==k][::-1]:
        #print(f"Killer {i}->0")
        moves=[moves.pop(i)] + moves
    if d!=None:
        i=moves.index(d['move'])
        if i!=0: moves=[moves.pop(i)] + moves

    #moves=sorted([m for m in game.moves()], key=lambda x: x['val'], reverse=game.turn()==WHITE)
    if moves==[]:
        if game.in_check(): 
            game.rep[key]-=1
            return bscore
        return 0

    if depth<=0: 
        game.rep[key]-=1
        return quiescence_fab(game, depth, ply+1, alpha, beta)

    for i,m in enumerate(moves):
        game.update(m)
        if i==0: 
            bscore=-pvs(game,depth-1,ply+1,-beta,-max(bscore,alpha))
            bmove=m
        else:
            alpha=max(bscore,alpha)
            score=-pvs(game,depth-1,ply+1, -alpha-1,-alpha)
            if score>bscore:
                if score>alpha and score<beta and depth>2:
                    score=-pvs(game,depth-1,ply+1,-beta,-score)
                bscore=score
                bmove=m
        game.backdate()
        if bscore>=beta: 
            game.store(depth,bscore,alpha,beta,bmove) 
            game.rep[key]-=1
            return bscore

    game.rep[key]-=1
    game.store(depth,bscore,alpha,beta,bmove) 
    return bscore

def print_moves(moves):
    for i,m in enumerate(moves):
        print(i, m, m2str(m))

def autoplay():
    label={WHITE:"White", BLACK:"Black"}
    label2={True: "Check", False: ""}
    game=Game()
    t0=time.time()
    game_over=False
    game.display()
    while not game_over:
        game.ttable={} #transposition table
        game.ktable=[collections.Counter() for i in range(game.MAX_DEPTH)]
        game.rep={key:game.rep[key] for key in game.rep if game.rep[key]>0}
        key="".join(game.board),game.turn()
        game.rep.setdefault(key,0)
        if game.rep["".join(game.board),game.turn()]>=3:
            print("Draw by repetition")
            game_over=True
            sys.exit(1)
        moves=score_moves(game,2)
        if moves==[]:
            if game.in_check(): 
                print(f"{label[game.turn()]} is check mate")
            else: 
                print("Draw")
            game_over=True
        else:
            s=f"{label[game.turn()]}: {m2str(moves[0])}"
            game.update(moves[0])
            game.display()
            print(s+f" {label2[game.in_check()]}")
    print("Time:",time.time()-t0)

if __name__=="__main__":
    autoplay()
