import random

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
    def __init__(self, pocket='deep', wheel=RouletteWheel()):
        self.money = pocket
        self.wheel = wheel
    
    def single_bet(self, amount, num=1):
        #Operates on a 35 to 1

        if self.money != 'deep':
            self.money = self.money - amount
        
        if num == self.wheel.spin():
            if self.money != 'deep':
                self.money = self.money + (amount * 35) + amount
            outcome = (True, ((amount * 35) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome

    def two_bet(self, amount, nums=(1,2)):
        #Operates on a 17 to 1
        if self.money != 'deep':
            self.money = self.money - amount
        
        if  self.wheel.spin() in nums:
            if self.money != 'deep':
                self.money = self.money + (amount * 17) + amount
            outcome = (True, ((amount * 17) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome
    
    def three_bet(self, amount, nums=(1,2,3)):
        #Operates on an 11 to 1
        if self.money != 'deep':
            self.money = self.money - amount
        
        if  self.wheel.spin() in nums:
            if self.money != 'deep':
                self.money = self.money + (amount * 11) + amount
            outcome = (True, ((amount * 11) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome
    
    def four_bet(self, amount, nums=(1,2,4,5)):
        #Operates on an 8 to 1
        if self.money != 'deep':
            self.money = self.money - amount
        
        if  self.wheel.spin() in nums:
            if self.money != 'deep':
                self.money = self.money + (amount * 8) + amount
            outcome = (True, ((amount * 8) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome
    
    def five_bet(self, amount, nums=(-1,0,1,2,3)):
        if(self.wheel.style == 'European'):
            return 'No five bet for Europe'
        
        #Operates on a 6 to 1 (according to online resources)
        if self.money != 'deep':
            self.money = self.money - amount
        
        if  self.wheel.spin() in nums:
            if self.money != 'deep':
                self.money = self.money + (amount * 6) + amount
            outcome = (True, ((amount * 6) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome
    
    def six_bet(self, amount, nums=(1,2,3,4,5,6)):     
        #Operates on a 5 to 1 
        if self.money != 'deep':
            self.money = self.money - amount
        
        if  self.wheel.spin() in nums:
            if self.money != 'deep':
                self.money = self.money + (amount * 5) + amount
            outcome = (True, ((amount * 5) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome
    
    def twelve_bet(self, amount, nums=(1,2,3,4,5,6,7,8,9,10,11,12)):     
        #Operates on a 2 to 1 
        if self.money != 'deep':
            self.money = self.money - amount
        
        if  self.wheel.spin() in nums:
            if self.money != 'deep':
                self.money = self.money + (amount * 2) + amount
            outcome = (True, ((amount * 2) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome
    
    def half_bet(self, amount, nums=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18)):     
        #Operates on a 1 to 1 
        if self.money != 'deep':
            self.money = self.money - amount
        
        if  self.wheel.spin() in nums:
            if self.money != 'deep':
                self.money = self.money + (amount * 1) + amount
            outcome = (True, ((amount * 1) + amount))
        else:
            outcome = (False, -1 * amount)
        
        return outcome
    
class Table:
    def __init__(self, num_b=10, wealth='deep' bet_limit='stagger', round_limit=30, wheel=RouletteWheel())
        self.bettors = []
        for i in range(num_b):
            self.bettors.append(Bettor(wealth, wheel))
        
        if bet_limit='stagger':
            self.limit = (2500, 5000, 7500, 10000, 12500, 15000, 50000, 50000)
        else:
            self.limit = (bet_limit, bet_limit, bet_limit, bet_limit, bet_limit, bet_limit, bet_limit, bet_limit)
        self.rounds = round_limit
    
    def run_table(self):

        
#MAIN

    

    
    
    

