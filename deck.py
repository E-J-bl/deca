
class card:
    def __init__(self,suit,value):
        self.suit=suit
        self.value=value

    def __str__(self):
        return f"{self.value}{self.suit}"


class deck:
    defult_dist={0:2,1:4,2:3,3:3,4:1}
    defult_symbols=["*","§","=","_","%"]

    def __init__(self):
        self.drawn=[]
        self.ind=0
        self.deck=[card(suit,num) for suit in self.defult_symbols for kl in ([i]*k for i,k in self.defult_dist.items()) for num in kl]

    def __iter__(self):
        self.ind=0
        return self

    def __next__(self):
        if self.ind<len(self.deck):
            self.ind+=1

            return self.deck[self.ind-1]
        else:
            raise StopIteration

    def __getitem__(self,ind):
        return self.deck[ind]

    def remove(self,value):
        self.drawn.append(value)
        self.deck.remove(value)

    def __len__(self):
        return len(self.deck)

    def __list__(self):
        return self.deck

    def __str__(self):
        return f"{list(map(lambda x:x.__str__(),self.deck))}"
