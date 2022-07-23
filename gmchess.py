#
#  Copyright (c) 2022 Jesper Olsen
#  License: MIT, see License.txt
#
#  Golden Monkey Chess - pure python implementation in one file.
#  Run as main or call autoplay() for self play...
#
#  TODO - replace ttable, ktable, rep with more efficient maps
#       - add mobility to scoring

import sys
import time
import collections
import locale
import functools
import random

pieces="RNBKQP"
WHITE=1
BLACK=0
INFINITE=10000
p2colour={p:WHITE for p in pieces} | {p.lower():BLACK for p in pieces} | {'.':2}

# board layout - h1 is 0, a8 is 63
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

#positional piece values
k1val=( 24,  24,  12,  6,  6,  12,  24,  24, 
        24,  12,  6,   0,  0,  6,   12,  24, 
        12,  6,   0,  -6, -6,  0,   6,  12, 
         6,   0,  -6, -12, -12, -6,  0,  6, 
         6,   0,  -6, -12, -12, -6,  0,  6, 
        12,  6,   0,  -6, -6,  0,   6,  12, 
        24,  12,  6,   0,  0,  6,   12,  24, 
        24,  24,  12,  6,  6,  12,  24,  24)
k2val=tuple(-x for x in k1val)

nval=( 315, 315, 315, 315, 315, 315, 315, 315,
       315, 320, 320, 320, 320, 320, 320, 315,
       315, 320, 325, 325, 330, 330, 320, 315,
       315, 320, 325, 325, 330, 330, 320, 315,
       315, 320, 325, 325, 330, 330, 320, 315,
       315, 320, 325, 325, 330, 330, 320, 315,
       315, 320, 320, 320, 320, 320, 320, 315,
       315, 315, 315, 315, 315, 315, 315, 315)

pawnval=( 100, 100, 101, 102, 104, 106, 108, 900,
          100, 100, 102, 104, 106, 109, 112, 900,
          100, 100, 104, 108, 112, 115, 118, 900,
          100, 100, 107, 114, 121, 128, 135, 900,
          100, 100, 106, 112, 118, 124, 132, 900,
          100, 100, 104, 108, 112, 116, 120, 900,
          100, 100, 102, 104, 106, 108, 112, 900,
          100, 100, 101, 102, 104, 106, 108, 900)

pval={'P':pawnval,
      'p':tuple([-x for x in pawnval[::-1]]),
      'R':tuple(([500]*6+[522,500])*8),
      'r':tuple(([-500,-522]+[-500]*6)*8),
      'N':nval,
      'n':tuple([-x for x in nval[::-1]]),
      'B':tuple(([339]+[350]*7)*8),
      'b':tuple(([-350]*7+[-339])*8),
      'Q':tuple([900]*64),
      'q':tuple([-900]*64),
      'K':k1val,
      'k':k2val}

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
    passed=sum([-2*(7-q%8)*(7-q%8) for q in [i for i,c in enumerate(board) if c=='p'] if freep(q)])  
    yield passed

def i2str(i):
    """Translate integer coordinates to chess square"""
    x=7-i//8
    y=i%8 +1
    return "abcdefgh"[x]+str(y)

def m2str(d): 
    return f"{i2str(d['from'])}{'x' if 'kill' in d else ' '}{i2str(d['to'])}"


#Build a 'ray-map' - squares that rook,bishop,queen can glide to on an empty board
#+ map for king, Knight

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
                yield {'from':frm, 'to':frm+1, 'val':pval['Q'][frm+1]-pval['P'][frm], 'transform':('P','Q')}
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
                yield {'from':frm, 'to': frm-1, 'val':pval['Q'][frm-1]-pval['p'][frm], 'transform':('p','q')}  
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

#map - piece type to function that generate its moves
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
        self.board=list('R......rN......nB......bK......kQ......qB......bN......nR......r') # no pawns
        self.board=list('RP......NP......BP......KP.....kQP......BP......NP......RP......') # black only king
        self.board=list('R.......N.......B.......K......kQ.......B.......N.......R.......') # black only king, no pawns
        self.board=list('R.......................K......kQ.......................R.......') # black only king, white K,Q,R
        self.board=list('RP....prNP....pnBP....pbKP....pkQP....pqBP....pbNP....pnRP....pr') # root 

        self.can_castle=[{WHITE: {'short': True, 'long': True}, BLACK:{'short': True, 'long': True}}]
        self.MAX_DEPTH=50
        self.UPPER_BOUND=-1
        self.LOWER_BOUND=1
        self.material=sum([pval[p][i] for i,p in enumerate(self.board) if p!='.'])
        #self.mobility={WHITE: 0, BLACK: 0}
        self.rep={("".join(self.board),self.turn()): 1}
        self.ttable={} #transposition table
        self.ktable=[collections.Counter() for i in range(self.MAX_DEPTH)]
        self.n_searched=0
        self.max_searched=100000
        self.END_GAME_MATERIAL=0.3*abs_eval_material('RP....prNP....pnBP....pbKP....pkQP....pqBP....pbNP....pnRP....pr')

    def turn(self):
        return (len(self.log)+1)%2 

    def labeled_moves(self):
        """https://cheatography.com/davechild/cheat-sheets/chess-algebraic-notation/"""
        moves=self.legal_moves()
        moves.sort(key=lambda m: (self.board[m['from']],m['to']))
        for i,m in enumerate(moves):
            p=self.board[m['from']].upper()
            s=""
            if 'castle' in m:
                s='0-0' if m['to']<31 else '0-0-0'
            elif 'transform' in m:
                s="*"

            if p!='P':
                s+=p
            if i<len(moves)-1:
                m2=moves[i+1]
                if m2['to']==m['to'] and self.board[m['from']]==self.board[m2['from']]:
                    a=i2str(m['from'])
                    if p in "RNB":
                        l=[i2str(i) for i in range(64) if self.board[i]==self.board[m['from']]]
                        if len(l)==1 or l[0][0]!=l[1][0]:
                            s+=a[0]
                        else:
                            s+=a[1]

            if 'kill' in m: 
                if p=='P': s+=i2str(m['from'])[0]
                s+='x'
            s+=i2str(m['to'])
            m['label']=s
        return moves
            
    def moves(self, colour=None):
        if colour==None: colour=(len(self.log)+1)%2
        for i,p in ((i,p) for (i,p) in enumerate(self.board) if p2colour[p]==colour):
            self.n_searched+=1  
            yield from p2moves[p.lower()](self,i)    

    def legal_moves(self):
        def legal(game, m):
            self.update(m)
            flag=[d for d in self.moves() if 'kill' in d and d['kill'][0].lower()=='k']==[]
            self.backdate()
            return flag

        return sorted([m for m in self.moves() if legal(self,m)], key=lambda x: x['val'], reverse=self.turn()==WHITE)

    def make_move(self, m):
        # shift killer moves 1 level up
        #self.ktable=[collections.Counter() for i in range(self.MAX_DEPTH)]
        for i in range(self.MAX_DEPTH-1):
            self.ktable[i]=collections.Counter({k:2-j for j,(k,v) in enumerate(self.ktable[i+1].most_common(2))})
        self.ktable[self.MAX_DEPTH-1]=collections.Counter()

        key="".join(self.board),self.turn()
        if 'kill' in m or self.board[m['from']].upper()=='P':
            self.rep={("".join(self.board),self.turn()): 0} #ireversible move - clear rep table
        else:
            self.rep={key:self.rep[key] for key in self.rep if self.rep[key]>0} #py map remebers old keys

        self.update(m)

        key="".join(self.board),self.turn()
        self.rep.setdefault(key,0)
        self.rep[key]+=1

        #clear transposition table
        if key in self.ttable:
            self.ttable={key: self.ttable[key]}
        else:
            self.ttable={}


        #adjust king value in end game
        if abs_eval_material(self.board) < self.END_GAME_MATERIAL:
            if pval['K']==k1val:
                pval['K']=k2val
                pval['k']=k1val

        #update castling permissions
        colour=p2colour[self.board[m['to']]]
        if 'castle' in m or self.board[m['to']].lower()=='k':
            self.can_castle[-1][colour]={'long': False, 'short':False}
        else:
            if self.can_castle[-1][colour]['long'] and self.board[m['to']].lower()=='r' and m['from']//8==7:
                self.can_castle[-1][colour]['long']=False
            if self.can_castle[-1][colour]['short'] and self.board[m['to']].lower()=='r' and m['from']//8==0:
                self.can_castle[-1][colour]['short']=False

    def check_50_move_rule(self):
        if sum(self.rep.values())>=100:
            for key in self.rep:
                print(key, self.rep[key])
        return sum(self.rep.values())>=100
            
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
        print()
        for y in range(7,-1,-1):
            print(f"{y+1} ", end="")
            for x in range(8):
                print(self.board[(7-x)*8+y],end="")
            print()
        print("  ABCDEFGH")

    def retrieve(self,key):
        if key in self.ttable:
            return self.ttable[key]
        return None

    def store(self, depth,score,alpha,beta,move):
        key="".join(self.board),self.turn()

        if key not in self.ttable or self.ttable[key]['depth']<=depth: #update transposition table
            self.ttable[key]={'depth': depth, 'score': score, 'move': move, 'bound':'EXACT'}
            if score<=alpha:
                self.ttable[key]['bound']='UPPER'
            if score>=beta:
                self.ttable[key]['bound']='LOWER'

        self.ktable[depth][(move['from'],move['to'])]+=1 #update kill table

    def eval(self):
        v=self.material + eval_pawn_structure(self.board) #+ game.mobility[WHITE]-game.mobility[BLACK]
        return v if self.turn()==WHITE else -v

    def in_check(self, colour=None):
        if colour==None:
            colour=BLACK if self.turn()==WHITE else WHITE
        else:
            colour=WHITE if self.turn()==WHITE else BLACK
        return [m for m in self.moves(colour) if 'kill' in m and m['kill'][0].lower()=='k']!=[]

    def score_moves(self,moves,depth=1,max_searched=100000):
       t0=time.time()
       if moves==None:
           moves=self.labeled_moves()
       if moves==[]: return []

       # lookup best move from ttable - move to head
       key="".join(self.board),self.turn()
       d=self.retrieve(key)
       if d!=None:
           def find(q, moves):
               for i,m in enumerate(moves):
                   if q['from']==m['from'] and q['to']==m['to']:
                       return i
               return -1
           i=find(d['move'],moves)
           if i>0: moves=[moves.pop(i)] + moves

       self.n_searched=0
       for depth in range(1, depth+1):
           if depth>1 and self.n_searched>max_searched: break
           alpha=-INFINITE
           beta = INFINITE

           #search 1st move with full beam
           self.update(moves[0])
           best=-pvs(self, depth-1, 1, -beta, INFINITE) 
           moves[0]['depth']=depth
           moves[0]['score']=best
           self.backdate()

           for m in moves[1:]:
               if best>=beta: 
                   print("Checkmate - shouldn't happen here")
                   print(moves)
                   print(scores)
                   return None
               m['depth']=depth
               self.update(m)
               alpha=max(best,alpha)
               m['score']=-pvs(self, depth-1, 1, -alpha-1, -alpha)
               if m['score']>best:
                   if m['score']>alpha and m['score']<beta and depth>2:
                       m['score']=-pvs(self, depth-1, 1, -beta, -m['score'])
                   best=m['score']
               self.backdate()

           moves.sort(key=lambda x: x['score'], reverse=True)
       return moves

def reply_fab(game, depth, ply, alpha, beta):
    lt=game.log[-1]['to'] 
    #moves=game.legal_moves()
    moves=game.moves()
    moves=[m for m in moves if 'kill' in m] #captures
    #moves=[m for m in moves if m['to']==lt] #replies
    if moves==[]: return game.eval()

    best=-INFINITE+ply
    for m in moves:
        game.update(m)
        if not game.in_check('p'):
            score=-reply_fab(game, depth-1,ply+1,-beta, -max(alpha,best))
            if score>best:
                best=score
                if best>=beta:
                    game.backdate()
                    return best
        game.backdate()
    return best
    
def quiescence_fab(game, depth, ply, alpha, beta):
    #moves=game.legal_moves()
    moves=list(game.moves())
    lt=game.log[-1]['to'] 
    quiescent=game.board[lt].lower()!='p' or (lt%8 != 6 or lt%8!=1)
    if quiescent:
        moves=[m for m in moves if 'kill' in m]
    if moves==[]: return game.eval()

    best=-INFINITE+ply
    for m in moves:
        game.update(m)
        if not game.in_check('p'): #legal move
            if quiescent:
                score=-reply_fab(game, depth-1, ply+1, -beta, -max(alpha,best))
            else:
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

    if game.in_check(): depth+=1

    d=game.retrieve(key)
    if d!=None:
        if d['depth']>=depth:
            if d['bound']=='EXACT': 
                game.rep[key]-=1
                return d['score']
            if d['bound']=='LOWER': alpha=max(alpha,d['score'])
            elif d['bound']=='UPPER': beta=min(beta,d['score'])
            if alpha>=beta: 
                game.rep[key]-=1
                return d['score']

    if depth<=0: 
        game.rep[key]-=1
        return quiescence_fab(game, depth, ply+1, alpha, beta)

    bscore=-INFINITE+ply
    bmove=None
    #moves=game.legal_moves()
    moves=list(game.moves())

    for i in [i for (k,v) in game.ktable[depth].most_common(2) for (i,m) in enumerate(moves) if i!=0 and (m['from'],m['to'])==k][::-1]:
        #print(f"Killer {i}->0")
        moves=[moves.pop(i)] + moves
    if d!=None:
        i=moves.index(d['move'])
        if i!=0: moves=[moves.pop(i)] + moves

    for i,m in enumerate(moves):
        game.update(m)
        if not game.in_check('o'): #legal move
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
        if bmove!=None and bscore>=beta: 
            game.store(depth,bscore,alpha,beta,bmove) 
            game.rep[key]-=1
            return bscore

    game.rep[key]-=1
    if bmove!=None:
        game.store(depth,bscore,alpha,beta,bmove) 
    elif not game.in_check():
        return 0

    return bscore

def autoplay(verbose=False):
    game=Game()
    t0=time.time()
    tot=0 # statistics - total # of positions explored
    moves=game.labeled_moves()
    while True:
        if game.rep["".join(game.board),game.turn()]>=3:
            print("1/2-1/2 Draw by repetition")
            break
        if game.check_50_move_rule():
            print("1/2-1/2 Draw by the 50-move rule")
            break
        moves=game.score_moves(moves,25,100000)
        tot+=game.n_searched

        if moves==[]:
            s="1-0" if game.turn()==BLACK else "0-1"
            print(s) if game.in_check() else print("1/2-1/2 Draw")
            break

        #m=random.choice( [m for m in moves if m['score']==moves[0]['score']] ) #same score
        m=moves[0]

        s=f"{len(game.log)//2+1}. "
        s+=f"{m['label']}" if 'label' in m else f"{m2str(moves[0])}"
        game.make_move(m)
        game.display()
        moves=game.labeled_moves()
        if game.in_check():
            if moves==[]:
                s+="#"
            else:
                s+="+"
        if verbose: s+=f" ; Value: {m['score']}, Searched {game.n_searched:n}; {tot/(time.time()-t0):n} positions/sec; depth: {m['depth']}"
        print(s)
    print(f"Time: {time.time()-t0}, Search total: {tot:n}")

if __name__=="__main__":
    locale.setlocale(locale.LC_ALL, '')
    random.seed()

    autoplay(verbose=True)
