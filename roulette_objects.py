import random
import matplotlib.pyplot as plt

class RouletteWheel:
    def __init__(self, zeroes=2):
        self.style = 'European'
        if zeroes == 2:
            self.style = 'American'
    
    def spin(self):
        start = 0
        if self.style == 'American':
            start = -1
        result = random.randint(start, 36)
        return result
    

class Bettor:
    def __init__(self, pocket=0, wheel=RouletteWheel()):
        self.money = pocket
        self.wheel = wheel
    
    def single_bet(self, amount, num=1):
        #Operates on a 35 to 1

        self.money = self.money - amount
        
        if num == self.wheel.spin():
            self.money = self.money + (amount * 35) + amount
            outcome = (True, ((amount * 35) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome

    def two_bet(self, amount, nums=(1,2)):
        #Operates on a 17 to 1
        self.money = self.money - amount
        
        if  self.wheel.spin() in nums:
            self.money = self.money + (amount * 17) + amount
            outcome = (True, ((amount * 17) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome
    
    def three_bet(self, amount, nums=(1,2,3)):
        #Operates on an 11 to 1
        self.money = self.money - amount
        
        if  self.wheel.spin() in nums:
            self.money = self.money + (amount * 11) + amount
            outcome = (True, ((amount * 11) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome
    
    def four_bet(self, amount, nums=(1,2,4,5)):
        #Operates on an 8 to 1
        self.money = self.money - amount
        
        if  self.wheel.spin() in nums:
            self.money = self.money + (amount * 8) + amount
            outcome = (True, ((amount * 8) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome
    
    def five_bet(self, amount, nums=(-1,0,1,2,3)):
        if(self.wheel.style == 'European'):
            return 'No five bet for Europe'
        
        #Operates on a 6 to 1 (according to online resources)
        self.money = self.money - amount
        
        if  self.wheel.spin() in nums:
            self.money = self.money + (amount * 6) + amount
            outcome = (True, ((amount * 6) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome
    
    def six_bet(self, amount, nums=(1,2,3,4,5,6)):     
        #Operates on a 5 to 1 
        self.money = self.money - amount
        
        if  self.wheel.spin() in nums:
            self.money = self.money + (amount * 5) + amount
            outcome = (True, ((amount * 5) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome
    
    def twelve_bet(self, amount, nums=(1,2,3,4,5,6,7,8,9,10,11,12)):     
        #Operates on a 2 to 1 
        self.money = self.money - amount
        
        if  self.wheel.spin() in nums:
            self.money = self.money + (amount * 2) + amount
            outcome = (True, ((amount * 2) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome
    
    def half_bet(self, amount, nums=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18)):     
        #Operates on a 1 to 1 
        self.money = self.money - amount
        
        if  self.wheel.spin() in nums:
            self.money = self.money + (amount * 1) + amount
            outcome = (True, ((amount * 1) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome
    
class Table:
    def __init__(self, num_b=10, wealth=0, bet_limit='stagger', round_limit=30, wheel=RouletteWheel()):
        
        self.bettors = []
        for i in range(num_b):
            self.bettors.append(Bettor(wealth, wheel))
        
        self.limit = 10000
        if bet_limit == 'stagger':
            self.limit = (2500, 5000, 7500, 10000, 12500, 15000, 25000, 50000)
        else:
            self.limit = (bet_limit, bet_limit, bet_limit, bet_limit, bet_limit, bet_limit, bet_limit, bet_limit)
        self.rounds = round_limit
    
    def run_table(self, amount_ratio=1, bet=0.5):
        
        data = []

        for i in range(self.rounds):
            data.append([])
            for gambler in self.bettors:

                out = None
            
                match bet:
                    case 1:
                        out = gambler.single_bet(amount_ratio * self.limit[0])
                    case 2:
                        out = gambler.two_bet(amount_ratio * self.limit[1])
                    case 3:
                        out = gambler.three_bet(amount_ratio * self.limit[2])
                    case 4:
                        out = gambler.four_bet(amount_ratio * self.limit[3])
                    case 5:
                        out = gambler.five_bet(amount_ratio * self.limit[4])
                    case 6:
                        out = gambler.six_bet(amount_ratio * self.limit[5])
                    case 12:
                        out = gambler.twelve_bet(amount_ratio * self.limit[6])
                    case 0.5:
                        out = gambler.half_bet(amount_ratio * self.limit[7])
                    case _:
                        out = None

                
                round_result = (out, gambler.money)
                data[i].append(round_result)
        
        return data
    
    def run_martingale(self, bet=0.5, lim=False, min_bet=1, broke_on=True):
        
        data = []

        for i in range(self.rounds):
            data.append([])
            j = 0
            for gambler in self.bettors:
                amt = min_bet
                if (i == 0):
                    amt = min_bet
                elif(data[i-1][j][0][0] == False):
                    amt = -2 * data[i-1][j][0][1]
                else:
                    amt = min_bet
                
                out = None
                choice = bet
                if(broke_on and gambler.money < 1):
                    choice = "broke" 
            
                match choice:
                    case 1:
                        if(lim and amt > self.limit[0]):
                            amt = self.limit[0]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.single_bet(amt)
                    case 2:
                        if(lim and amt > self.limit[1]):
                            amt = self.limit[1]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.two_bet(amt)
                    case 3:
                        if(lim and amt > self.limit[2]):
                            amt = self.limit[2]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.three_bet(amt)
                    case 4:
                        if(lim and amt > self.limit[3]):
                            amt = self.limit[3]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.four_bet(amt)
                    case 5:
                        if(lim and amt > self.limit[4]):
                            amt = self.limit[4]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.five_bet(amt)
                    case 6:
                        if(lim and amt > self.limit[5]):
                            amt = self.limit[5]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.six_bet(amt)
                    case 12:
                        if(lim and amt > self.limit[6]):
                            amt = self.limit[6]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.twelve_bet(amt)
                    case 0.5:
                        if(lim and amt > self.limit[7]):
                            amt = self.limit[7]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.half_bet(amt)
                    case "broke":
                        out = "BROKE"
                    case _:
                        out = None

                
                round_result = (out, gambler.money)
                data[i].append(round_result)
                j += 1
        
        return data
    
    def run_fibonacci(self, bet=0.5, lim=False, min_bet=1, broke_on=True):
        
        data = []
        bet_tracker = {}
        temp = 0
        for gambler in self.bettors:
            bet_tracker[gambler] = [0, 1]

        for i in range(self.rounds):
            data.append([])
            j = 0
            for gambler in self.bettors:
                amt = min_bet
                if (i == 0):
                    amt = min_bet
                elif(data[i-1][j][0][0] == False):
                    temp = bet_tracker[gambler][0] + bet_tracker[gambler][1]
                    bet_tracker[gambler][0] = bet_tracker[gambler][1]
                    bet_tracker[gambler][1] = temp
                    amt = bet_tracker[gambler][0] + bet_tracker[gambler][1]  
                else:
                    if((bet_tracker[gambler][0] == 1 and bet_tracker[gambler][1] == 1) or bet_tracker[gambler][0] == 0):
                        bet_tracker[gambler][1] = 1
                        bet_tracker[gambler][0] = 0
                    else:
                        bet_tracker[gambler][1] = bet_tracker[gambler][1] - bet_tracker[gambler][0]
                        bet_tracker[gambler][0] = bet_tracker[gambler][0] - bet_tracker[gambler][1]
                    amt = bet_tracker[gambler][0] + bet_tracker[gambler][1]
                
                out = None
                choice = bet
                if(broke_on and gambler.money < 1):
                    choice = "broke" 
            
                match choice:
                    case 1:
                        if(lim and amt > self.limit[0]):
                            amt = self.limit[0]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.single_bet(amt)
                    case 2:
                        if(lim and amt > self.limit[1]):
                            amt = self.limit[1]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.two_bet(amt)
                    case 3:
                        if(lim and amt > self.limit[2]):
                            amt = self.limit[2]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.three_bet(amt)
                    case 4:
                        if(lim and amt > self.limit[3]):
                            amt = self.limit[3]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.four_bet(amt)
                    case 5:
                        if(lim and amt > self.limit[4]):
                            amt = self.limit[4]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.five_bet(amt)
                    case 6:
                        if(lim and amt > self.limit[5]):
                            amt = self.limit[5]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.six_bet(amt)
                    case 12:
                        if(lim and amt > self.limit[6]):
                            amt = self.limit[6]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.twelve_bet(amt)
                    case 0.5:
                        if(lim and amt > self.limit[7]):
                            amt = self.limit[7]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.half_bet(amt)
                    case "broke":
                        out = "BROKE"
                    case _:
                        out = None

                
                round_result = (out, gambler.money)
                data[i].append(round_result)
                j += 1
        
        return data
    
    def run_dAlembert(self, unit_ratio=0.01, bet=0.5, lim=False, min_bet=1, broke_on=True):
        
        data = []

        unit = self.bettors[0].money * unit_ratio
        bet_tracker = {}
        for gambler in self.bettors:
            bet_tracker[gambler] = unit
        min_bet = unit

        for i in range(self.rounds):
            data.append([])
            j = 0
            for gambler in self.bettors:
                amt = min_bet
                if (i == 0):
                    amt = min_bet
                elif(data[i-1][j][0][0] == False):
                    bet_tracker[gambler] = bet_tracker[gambler] + unit
                    amt = bet_tracker[gambler]
                else:
                    if(bet_tracker[gambler] != min_bet):
                        bet_tracker[gambler] = bet_tracker[gambler] - unit
                    amt = bet_tracker[gambler]
                
                out = None
                choice = bet
                if(broke_on and gambler.money < 1):
                    choice = "broke" 
            
                match choice:
                    case 1:
                        if(lim and amt > self.limit[0]):
                            amt = self.limit[0]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.single_bet(amt)
                    case 2:
                        if(lim and amt > self.limit[1]):
                            amt = self.limit[1]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.two_bet(amt)
                    case 3:
                        if(lim and amt > self.limit[2]):
                            amt = self.limit[2]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.three_bet(amt)
                    case 4:
                        if(lim and amt > self.limit[3]):
                            amt = self.limit[3]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.four_bet(amt)
                    case 5:
                        if(lim and amt > self.limit[4]):
                            amt = self.limit[4]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.five_bet(amt)
                    case 6:
                        if(lim and amt > self.limit[5]):
                            amt = self.limit[5]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.six_bet(amt)
                    case 12:
                        if(lim and amt > self.limit[6]):
                            amt = self.limit[6]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.twelve_bet(amt)
                    case 0.5:
                        if(lim and amt > self.limit[7]):
                            amt = self.limit[7]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.half_bet(amt)
                    case "broke":
                        out = "BROKE"
                    case _:
                        out = None

                
                round_result = (out, gambler.money)
                data[i].append(round_result)
                j += 1
        
        return data
    
    def run_parlay(self, bet=0.5, lim=False, min_bet=1, broke_on=True):
        
        data = []
        bet_tracker = {}
        for gambler in self.bettors:
            bet_tracker[gambler] = min_bet

        for i in range(self.rounds):
            data.append([])
            j = 0
            for gambler in self.bettors:
                amt = min_bet
                if (i == 0):
                    amt = min_bet
                elif(data[i-1][j][0][0] == False):
                    bet_tracker[gambler] = min_bet
                    amt = bet_tracker[gambler]
                else:
                    bet_tracker[gambler] = bet_tracker[gambler] * 2
                    amt = bet_tracker[gambler]
                
                out = None
                choice = bet
                if(broke_on and gambler.money < 1):
                    choice = "broke" 
            
                match choice:
                    case 1:
                        if(lim and amt > self.limit[0]):
                            amt = self.limit[0]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.single_bet(amt)
                    case 2:
                        if(lim and amt > self.limit[1]):
                            amt = self.limit[1]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.two_bet(amt)
                    case 3:
                        if(lim and amt > self.limit[2]):
                            amt = self.limit[2]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.three_bet(amt)
                    case 4:
                        if(lim and amt > self.limit[3]):
                            amt = self.limit[3]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.four_bet(amt)
                    case 5:
                        if(lim and amt > self.limit[4]):
                            amt = self.limit[4]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.five_bet(amt)
                    case 6:
                        if(lim and amt > self.limit[5]):
                            amt = self.limit[5]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.six_bet(amt)
                    case 12:
                        if(lim and amt > self.limit[6]):
                            amt = self.limit[6]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.twelve_bet(amt)
                    case 0.5:
                        if(lim and amt > self.limit[7]):
                            amt = self.limit[7]
                        if(broke_on and amt > gambler.money):
                            amt = gambler.money
                        out = gambler.half_bet(amt)
                    case "broke":
                        out = "BROKE"
                    case _:
                        out = None

                
                round_result = (out, gambler.money)
                data[i].append(round_result)
                j += 1
        
        return data
                    
                    



        
#Functions for testing


#Roulette table test
def bet_chances_test(num_r=10000):
    bots = []
    bets = [[], [], [], [], [], [], [], []]
    for i in range(num_r):
        bots.append(Bettor())

    for bot in bots:
        bets[0].append(bot.single_bet(1))
        bets[1].append(bot.two_bet(1))
        bets[2].append(bot.three_bet(1))
        bets[3].append(bot.four_bet(1))
        bets[4].append(bot.five_bet(1))
        bets[5].append(bot.six_bet(1))
        bets[6].append(bot.twelve_bet(1))
        bets[7].append(bot.half_bet(1))

    wins = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(8):
        for bet in bets[i]:
            if(bet[0]):
                wins[i] = wins[i] + 1
            
    print("single: " + str(1/38) + " | " + str(wins[0]/num_r))
    print("two: " + str(2/38) + " | " + str(wins[1]/num_r))
    print("three: " + str(3/38) + " | " + str(wins[2]/num_r))
    print("four: " + str(4/38) + " | " + str(wins[3]/num_r))
    print("five: " + str(5/38) + " | " + str(wins[4]/num_r))
    print("six: " + str(6/38) + " | " + str(wins[5]/num_r))
    print("twelve: " + str(12/38) + " | " + str(wins[6]/num_r))
    print("half: " + str(18/38) + " | " + str(wins[7]/num_r))


def martin_test1(num_r=10):
    test1 = Table(num_r, 55000, 10000, 30, RouletteWheel())
    results1 = test1.run_martingale()

    #Writing Results to a file
    i = 0
    with open("exploring_math_data1.txt", "w") as fp:
        for roun in results1:
            fp.write("Round " + str(i) + ": " + str(roun) + "\n")
            i += 1
        fp.write("--------------------------------------------------------------------------------------------------------------\n")
        for j in range(len(results1[0])):
            robot = []
            for roun in results1:
                robot.append(roun[j])
            fp.write("Bettor " + str(j) + ": " + str(robot) + "\n")


def martin_test2(num_r=100):
    test2 = Table(num_r, 10000, 1000, 100, RouletteWheel())
    #100 Bettors, $10000 start, $1000 limit on bets, 100 rounds
    results2 = test2.run_martingale()

    count_winners = 0
    start_end_diff = 0
    went_broke = 0
    for robot in results2[-1]:

        if robot[1] >= 10000:
            count_winners += 1   
        elif robot[0] == "BROKE":
            went_broke += 1
        
        start_end_diff += robot[1] - 10000

    print("start vs. end: " + str(start_end_diff))
    print("avg diff: " + str(start_end_diff/num_r))
        
    print("winners: " + str(count_winners) + " | losers: " + str(num_r - count_winners))
    print("broke: " + str(went_broke))

    #Writing Results to a file
    i = 0
    with open("exploring_math_data2.txt", "w") as fp:
        for roun in results2:
            fp.write("Round " + str(i) + ": " + str(roun) + "\n")
            i += 1
        fp.write("--------------------------------------------------------------------------------------------------------------\n")
        contestant = "winner"
        for j in range(len(results2[0])):
            robot = []
            for roun in results2:
                robot.append(roun[j])
            if(robot[-1][1] >= 10000):
                contestant = "winner"
            else:
                contestant = "loser"
            fp.write("Bettor " + str(j) + ": " + str(robot) + " | " + contestant + "\n")
        
        fp.write("--------------------------------------------------------------------------------------------------------------\n")
        fp.write("start vs. end: " + str(start_end_diff) + "\n")
        fp.write("avg diff: " + str(start_end_diff/num_r) + "\n")
        fp.write("\"winners\": " + str(count_winners) + " | \"losers\": " + str(num_r - count_winners) + "\n")
        fp.write("broke: " + str(went_broke) + "\n")

    money_overround = []
    for i in range(len(results2[0])):
            robot = []
            for roun in results2:
                robot.append(roun[i][1])
            money_overround.append(robot)
    i = 0
    
    for y_values in money_overround:
        plt.plot(range(100), y_values, label = "bettor" + str(i))
        i += 1
    plt.xlabel('money')
    plt.ylabel('round')
    #plt.legend()
    plt.show()

def fib_test1(num_r=100):
    test2 = Table(num_r, 10000, 1000, 100, RouletteWheel())
    #100 Bettors, $10000 start, $1000 limit on bets, 100 rounds
    results2 = test2.run_fibonacci()

    count_winners = 0
    start_end_diff = 0
    went_broke = 0
    for robot in results2[-1]:

        if robot[1] >= 10000:
            count_winners += 1   
        elif robot[0] == "BROKE":
            went_broke += 1
        
        start_end_diff += robot[1] - 10000

    print("start vs. end: " + str(start_end_diff))
    print("avg diff: " + str(start_end_diff/num_r))
        
    print("winners: " + str(count_winners) + " | losers: " + str(num_r - count_winners))
    print("broke: " + str(went_broke))

    #Writing Results to a file
    i = 0
    with open("exploring_math_data_fib1.txt", "w") as fp:
        for roun in results2:
            fp.write("Round " + str(i) + ": " + str(roun) + "\n")
            i += 1
        fp.write("--------------------------------------------------------------------------------------------------------------\n")
        contestant = "winner"
        for j in range(len(results2[0])):
            robot = []
            for roun in results2:
                robot.append(roun[j])
            if(robot[-1][1] >= 10000):
                contestant = "winner"
            else:
                contestant = "loser"
            fp.write("Bettor " + str(j) + ": " + str(robot) + " | " + contestant + "\n")
        
        fp.write("--------------------------------------------------------------------------------------------------------------\n")
        fp.write("start vs. end: " + str(start_end_diff) + "\n")
        fp.write("avg diff: " + str(start_end_diff/num_r) + "\n")
        fp.write("\"winners\": " + str(count_winners) + " | \"losers\": " + str(num_r - count_winners) + "\n")
        fp.write("broke: " + str(went_broke) + "\n")

def dAlem_test1(num_r=100):
    test2 = Table(num_r, 10000, 1000, 100, RouletteWheel())
    #100 Bettors, $10000 start, $1000 limit on bets, 100 rounds
    results2 = test2.run_dAlembert(unit_ratio=0.001)
    #adjusted to start at 10 dollars

    count_winners = 0
    start_end_diff = 0
    went_broke = 0
    for robot in results2[-1]:

        if robot[1] >= 10000:
            count_winners += 1   
        elif robot[0] == "BROKE":
            went_broke += 1
        
        start_end_diff += robot[1] - 10000

    print("start vs. end: " + str(start_end_diff))
    print("avg diff: " + str(start_end_diff/num_r))
        
    print("winners: " + str(count_winners) + " | losers: " + str(num_r - count_winners))
    print("broke: " + str(went_broke))

    #Writing Results to a file
    i = 0
    with open("exploring_math_data_dAlem1.txt", "w") as fp:
        for roun in results2:
            fp.write("Round " + str(i) + ": " + str(roun) + "\n")
            i += 1
        fp.write("--------------------------------------------------------------------------------------------------------------\n")
        contestant = "winner"
        for j in range(len(results2[0])):
            robot = []
            for roun in results2:
                robot.append(roun[j])
            if(robot[-1][1] >= 10000):
                contestant = "winner"
            else:
                contestant = "loser"
            fp.write("Bettor " + str(j) + ": " + str(robot) + " | " + contestant + "\n")
        
        fp.write("--------------------------------------------------------------------------------------------------------------\n")
        fp.write("start vs. end: " + str(start_end_diff) + "\n")
        fp.write("avg diff: " + str(start_end_diff/num_r) + "\n")
        fp.write("\"winners\": " + str(count_winners) + " | \"losers\": " + str(num_r - count_winners) + "\n")
        fp.write("broke: " + str(went_broke) + "\n")

def par_test1(num_r=100):
    test2 = Table(num_r, 10000, 1000, 100, RouletteWheel())
    #100 Bettors, $10000 start, $1000 limit on bets, 100 rounds
    results2 = test2.run_parlay()

    count_winners = 0
    start_end_diff = 0
    went_broke = 0
    for robot in results2[-1]:

        if robot[1] >= 10000:
            count_winners += 1   
        elif robot[0] == "BROKE":
            went_broke += 1
        
        start_end_diff += robot[1] - 10000

    print("start vs. end: " + str(start_end_diff))
    print("avg diff: " + str(start_end_diff/num_r))
        
    print("winners: " + str(count_winners) + " | losers: " + str(num_r - count_winners))
    print("broke: " + str(went_broke))

    #Writing Results to a file
    i = 0
    with open("exploring_math_data_par1.txt", "w") as fp:
        for roun in results2:
            fp.write("Round " + str(i) + ": " + str(roun) + "\n")
            i += 1
        fp.write("--------------------------------------------------------------------------------------------------------------\n")
        contestant = "winner"
        for j in range(len(results2[0])):
            robot = []
            for roun in results2:
                robot.append(roun[j])
            if(robot[-1][1] >= 10000):
                contestant = "winner"
            else:
                contestant = "loser"
            fp.write("Bettor " + str(j) + ": " + str(robot) + " | " + contestant + "\n")
        
        fp.write("--------------------------------------------------------------------------------------------------------------\n")
        fp.write("start vs. end: " + str(start_end_diff) + "\n")
        fp.write("avg diff: " + str(start_end_diff/num_r) + "\n")
        fp.write("\"winners\": " + str(count_winners) + " | \"losers\": " + str(num_r - count_winners) + "\n")
        fp.write("broke: " + str(went_broke) + "\n")


#MAIN: Running tests

martin_test2()


    
    
    

