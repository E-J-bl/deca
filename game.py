import random
import time
from deck import deck
from player import player,computer_player

class game:
    def __init__(self,*players):
        self.game_deck=deck()
        self.play_stack=[]
        self.players:list[player]=list(players)
        self.last_human=None


    @property
    def stack_count(self):
        return sum(x.value for x in self.play_stack)

    def stack_setup(self):

        three_chosen=random.sample(list(self.game_deck),3)
        while sum(x.value for x in three_chosen)==12:
            three_chosen=random.sample(list(self.game_deck),3)
        for i in three_chosen:
            self.game_deck.remove(i)
            self.play_stack.append(i)

    def winner(self):
        return max(self.players,key= lambda x:x.points).name

    def player_stack(self,player_ind):
        if self.game_deck:
                card_rand=random.choice(self.game_deck)
                self.game_deck.remove(card_rand)
                self.play_stack.append(card_rand)

        else:
                print("\rdeck is empty please try again")
                
                time.sleep(1)
                

                print("\033[H\033[J")

    def player_take(self,player_r,player_ind):
        if self.play_stack:
            player_r.hand.append(self.play_stack[0])
            self.play_stack.pop(0)

        else:
                print("\rstack is empty please try again")
                time.sleep(1)

                print("\033[H\033[J")


    def update_screen(self,player_r):
        other_players=(x.display() for x in self.players if x!=player_r)
        other_players=list(zip(*other_players))
        player_names="| ".join(other_players[0])
        hand_d="| ".join(other_players[1])
        last_move="| ".join(other_players[2])

        print("\033[H\033[J")
        print(player_names)
        print(hand_d)
        print(last_move,"\n")
        print(f"\r[Deck] \nStack: {list(map(lambda x:x.__str__(),self.play_stack))} {self.stack_count} \n\n\n{player_r} \nDo you want to take the top card (t) or add a new card to the stack (s)")



        
    def real_turn(self,player_r):
        self.update_screen(player_r)

        choice=input()
        while choice.lower() not in ["s","t"]:
            print("\rinvalid input try again please")
            time.sleep(1)

            print("\033[H\033[J")
            print(f"\r[Deck] \nStack: {list(map(lambda x:x.__str__(),self.play_stack))} {self.stack_count} \n\n\n{player_r} \nDo you want to take the top card (t) or add a new card to the stack (s)")

            choice=input()
        return choice

    def ai_turn(self,player_r):
        
        return player_r.eval(self.play_stack,self.game_deck)

    def player_turn(self,player_ind):
        player_r=self.players[player_ind]
        choice="s"
        
        if player_r.type_n=="player":
            choice=self.real_turn(player_r)
            self.last_human=player_r
            

        elif player_r.type_n=='computer_player':
            choice=self.ai_turn(player_r)
            time.sleep(1)
        
            
        if choice.lower()=="s":
            self.player_stack(player_ind)

        if choice.lower()=="t":
            self.player_take(player_r,player_ind)

        if self.stack_count>=12:
            player_r.hand+=self.play_stack
            self.play_stack.clear()

        if len(self.play_stack)==0:
            self.stack_setup()

        player_r.last_move=choice

        player_r.sort_hand()
        
    def end_screen(self):
        #print("\033[H\033[J")
        print(f"\r[Deck] \nStack: {list(map(lambda x:x.__str__(),self.play_stack))} {self.stack_count}")
        print(*list(map(lambda x: "\n"+x.__str__()   ,(x for x in self.players))))


    def game_loop(self):
        self.stack_setup()
        counter=0
        while self.game_deck  or self.play_stack:
          
            self.player_turn(counter%len(self.players))
            counter+=1
            self.update_screen(self.last_human)
        self.end_screen()
        return self.winner()



def setup():
    print("\033[H\033[J")
    print("Welcome to the game of decathlon")
    num_pl=int(input("How many player will be joining us: "))
    num_bt=int(input("How many bots?"))
    players=[] 
    for i in range(num_pl):

        players.append(player(input(f"player {i+1} enter your name (it can not contain numbers): ")))
        
    for i in range(num_bt):
        players.append(computer_player(f"bot {i+1}"))
        
    ga=game(*players)
    
    return ga
