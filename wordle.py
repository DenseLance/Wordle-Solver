class WordleSolver:
    def __init__(self):
        # Word List
        self.word_list = set()
        with open("words.txt", "r") as f:
            for line in f:
                self.word_list.add(line[:-1])
            f.close()

        # Possibilities and Statistics
        self.hash_table = {}
        for ascii_code in range(ord("A"), ord("Z") + 1):
            self.hash_table[chr(ascii_code)] = {}
            for pos in range(5):
                self.hash_table[chr(ascii_code)][pos] = set()
        for word in self.word_list:
            for pos in range(5):
                self.hash_table[word[pos]][pos].add(word)

        # Current Guesses
        self.done = False
        while not self.done:
            self.add_guess()

    def add_guess(self):
        print("[BEST GUESSES]:", self.find_best_guess())
        print()
        
        guess = input("Your guess (type FINISH to complete guess): ").upper()
        print()
        if guess == "FINISH":
            self.done = True
        elif guess.isalpha() and len(guess) == 5:
            print("Input G if letter is in the target word and in the correct space.")
            print("Input Y if letter is in the word but is not in the correct space.")
            print("Input W if letter is not in the word.")
            print("If target word is 'FOUND' and guess is 'DOWNS', result returned is 'YGWGW'.")
            result = input("Result returned: ").upper()
            if result.isalpha() and len(result) == 5 and set(result).issubset({"G", "Y", "W"}):
                to_remove = set()
                for pos in range(5):
                    # When letter is in the target word and in the correct space:
                    # 1. Other letters for that space are incorrect, which are to be eliminated.
                    if result[pos] == "G":
                        for ascii_code in range(ord("A"), ord("Z") + 1):
                            if chr(ascii_code) != guess[pos]:
                                try:
                                    to_remove.update(self.hash_table[chr(ascii_code)].pop(pos))
                                except:
                                    pass
                    # When letter is in the word but is not in the correct space:
                    # 1. Letter for that space is incorrect, which is to be eliminated.
                    # 2. Words without that letter are incorrect, which are to be eliminated.
                    if result[pos] == "Y":
                        try:
                            to_remove.update(self.hash_table[guess[pos]].pop(pos))
                        except:
                            pass
                        for word in self.word_list:
                            if guess[pos] not in word: # naive method, does not consider target word having 2 of the same letter
                                to_remove.add(word)
                    # When letter is not in the word:
                    # 1. Words with that letter are incorrect, which are to be eliminated.
                    if result[pos] == "W":
                        all_pos = [pos_2 for pos_2 in range(5)]
                        g = []
                        y = []
                        for pos_2 in range(5):
                            if guess[pos_2] == guess[pos] and result[pos_2] == "G":
                                g.append(pos_2)
                            if guess[pos_2] == guess[pos] and result[pos_2] == "Y":
                                y.append(pos_2)
                        if y:
                            all_pos = y
                            all_pos.append(pos)
                        elif g:
                            for pos_2 in g:
                                all_pos.remove(pos_2)
                        for pos_2 in all_pos:
                            try:
                                to_remove.update(self.hash_table[guess[pos]].pop(pos_2))
                            except:
                                pass
                self.word_list.difference_update(to_remove)
                if result == "GGGGG":
                    self.done = True
            else:
                raise ValueError
        else:
            raise ValueError

    def find_best_guess(self):
        # Frequency Analysis
        # Repeated letters are penalised
        return sorted(self.word_list, key = lambda word: len(self.word_list.intersection(set().union(*[self.hash_table[word[pos]][pos] for pos in range(5)]))) / (6 - len(set(word))), reverse = True)[:10]

done = False
while not done:
    solver = WordleSolver()
    cont = input("Do you want to play again (Y/N):").upper()
    if cont == "N":
        done = True
