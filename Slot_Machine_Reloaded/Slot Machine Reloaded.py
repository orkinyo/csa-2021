#!/usr/bin/env python3

import random
import collections
import math
from .secret import flag


PRINTABLE = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+-/:.;<=>?@[]^_`{}"
flag_len = len(flag)
NO_COINS = "NO MORE COINS! GOODBYE."
NOT_ENOUGH_COINS = "YOU DON'T HAVE ENOUGH COINS!"
INVALID_COIN_NUMBER = "COIN NUMBER CAN'T BE NEGATIVE"
INITIAL_COINS = 10


class Slotmachine(object):
    def __init__(self):
        seed = random.SystemRandom().getrandbits(64) # Using SystemRandom is slow, use only for seed.
        self.random = random.Random(seed) # This will make sure no one messes with my seeds!
        self.slots = [list(PRINTABLE) for i in range(flag_len)]
        self.attempt_num = 0
        self.total_coins = INITIAL_COINS
        self.last_result = ""
        self.last_gamble = 0

    def get_prize(self):
        result = self.last_result
        prize = sum([x for x in collections.Counter(result).values() if x > 2])
        prize *= self.last_gamble
        self.total_coins += prize
        return prize

    def prepend_flag(self):
        for i in range(flag_len):
            self.slots[i].remove(flag[i])
            self.slots[i] = [flag[i]] + self.slots[i]

    def check_invalid_input(self, coins):
        if self.total_coins <= 0:
            self.last_result = ""
            return NO_COINS
        if self.total_coins < coins:
            self.last_result = ""
            return NOT_ENOUGH_COINS
        if coins < 0:
            self.last_result = ""
            return INVALID_COIN_NUMBER
        return None

    # My cat wrote this function
    def choice(self):
        rand_num = format(self.random._randbelow((1 << (flag_len*len(f'{len(PRINTABLE) - 1:b}'))) - 1),
            '#0%db' % (len(self.slots)*int(math.log(len(PRINTABLE), 2)) + 2))[2:]
        result = ""
        j = 0
        for i in range(0,len(rand_num),len(f'{len(PRINTABLE) - 1:b}')):
            result += self.slots[j][int(rand_num[i:i+len(f'{len(PRINTABLE) - 1:b}')],2)]
            j += 1
        return result

    def spin(self, coins):
        invalid_message = self.check_invalid_input(coins)
        if invalid_message:
            return invalid_message.center(flag_len)
        
        self.last_gamble = coins
        self.total_coins -= coins

        if self.attempt_num == 200:
            self.prepend_flag()
        self.attempt_num += 1

        result = self.choice()
        self.last_result = result
        return result


def main():
    slotmachine = Slotmachine()
    print(f"You have {slotmachine.total_coins} coins")
    get_next_num = True
    while get_next_num:
        try:
            prize = 0
            coins = int(input("Enter number of coins:\n"))
            result = slotmachine.spin(coins)
            if result == NO_COINS:
                get_next_num = False
            elif result != NOT_ENOUGH_COINS:
                prize = slotmachine.get_prize()
            print(result)
            print(f"You won {prize} coins!")
            print(f"{slotmachine.total_coins} coins left.")

        except ValueError:
            get_next_num = False
        except NameError:
            get_next_num = False


if __name__ == "__main__":
    main()
