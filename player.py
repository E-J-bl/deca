import time
from deck import card,deck
import random

class player:
    type_n="player"
    def __init__(self,name):
        self.name=name
        self.hand:list[card]=[]
        self.last_move="n"

    @property
    def points(self):
        if self.hand==[]:
            return 0
        suits_in_hand=set(card.suit for card in self.hand)
        suit_val={suit:0 for suit in suits_in_hand}
        for suit in suits_in_hand:
            val=0
            for card_s in self.hand:
                if card_s.suit==suit:
                    val+=card_s.value
                else:
                    val-=1

            suit_val[suit]=val
        return max(suit_val.values())

    
    def sort_hand(self):
        to_ret=[]
        suit_set={suit:[] for suit in set(card.suit for card in self.hand)}
        for card in self.hand:
            suit_set[card.suit].append(card)
        for suit in suit_set:
            suit_set[suit].sort(key=lambda x:x.value)
            to_ret+=suit_set[suit]
        return to_ret

    def display(self):
        return [f"{self.name:8}"
                ,f"[{'*'*(6*(len(self.hand)>6)+len(self.hand)*(len(self.hand)<6))}{' '*((6-len(self.hand))*(len(self.hand)<6))}]"
                ,f"{self.last_move:8}"]
        
    def __str__(self):
        return f"{self.name} \nHand:{list(map(lambda x:x.__str__(),self.hand))} \nScore:{self.points}"



class computer_player (player):
    type_n="computer_player"
    def __init__(self, name):
        super().__init__(name)
        

    def points_union(self,*,unison=[]):
        if isinstance(unison,card):
            unison=[unison]
            
        if self.hand+unison==[]:
            return 0
            
        suits_in_hand=set(card.suit for card in self.hand+unison)
        suit_val={suit:0 for suit in suits_in_hand}
        for suit in suits_in_hand:
            val=0
            for card_s in self.hand+unison:
                if card_s.suit==suit:
                    val+=card_s.value
                else:
                    val-=1

            suit_val[suit]=val
        
        return max(suit_val.values())

    
    def prob_draw(self,val,game_deck):
        tot,suf=(len(game_deck),sum(x.value>=val for x in game_deck))
        return suf/tot
        
    
    def eval_push_stack(self,stack,game_deck)-> float:
        if sum(x.value for x in stack)<8:
            return 0
        else:
            return self.prob_draw(12-sum(x.value for x in stack),game_deck) *(self.points_union(unison=stack)-self.points)

    
    def eval_take_stack(self,stack)-> float:
        if stack==[]:
            return 0
        return self.points_union(unison=stack[0])-self.points

    
    def eval(self,stack:list[card],game_deck:deck):
        push_stack=self.eval_push_stack(stack,game_deck)
        draw_stack=self.eval_take_stack(stack)
        if push_stack<draw_stack:
            return "t"
        else:
            return "s"


    def test(self,stack,game_deck):
        print(self.hand,self.points)
        print(stack,self.points_union(unison=stack))
        print(self.eval_push_stack(stack,game_deck))
        print(self.eval_take_stack(stack))
        print(self.eval(stack,game_deck))


def test():
    self=computer_player("a")
    game_deck=deck()
    stack=random.sample(game_deck.deck,3)
    print("stack",*stack)
    print("self",self.hand,self.points)
    print("self,hand",self.points_union(unison=stack))
    print("push",self.eval_push_stack(stack,game_deck))
    print("take",self.eval_take_stack(stack))
    print("final",self.eval(stack,game_deck))
