import random
import os
import logging
import argparse


class Flashcards:
    """Class to manipulate dictionary of words and definitions"""
    def __init__(self):
        self.cards_dict = {}
        self.errors = {}

    def add_card(self):
        print("The card: ")
        while True:
            card = input()
            if card not in self.cards_dict.keys():
                logging.info("The card: %s", card)
                break
            else:
                print(f'The term "{card}" already exists. Try again:')
                logging.info('The term "%s" already exists. Try again:', card)
        print("The definition of the card:")
        while True:
            definition = input()
            if definition not in self.cards_dict.values():
                self.cards_dict[card] = definition
                self.errors[card] = 0
                logging.info("The definition of the card: %s", definition)
                break
            else:
                print(f'The definition "{definition}" already exists. Try again:')
                logging.info('The definition "%s" already exists. Try again:', definition)
        print('The pair ("{}":"{}") has been added.\n'.format(card, definition))
        logging.info('The pair ("%s":"%s") has been added.', card, definition)

    def remove_card(self):
        card = input("Which card?\n")
        logging.info("Which card? %s", card)
        if card in self.cards_dict.keys():
            del self.cards_dict[card]
            del self.errors[card]
            print("The card has been removed.\n")
            logging.info("The card has been removed.")
        else:
            print(f'Can\'t remove "{card}": there is no such card.\n')
            logging.info('Can\'t remove "%s": there is no such card.', card)

    def from_file(self, arg):
        name = arg if arg else input("File name: \n")
        logging.info("File name: %s", name)
        count = 0
        if os.access(name, os.F_OK):
            with open(name, "r") as file:
                for line in file:
                    c, d, e = line.strip().split(": ")
                    self.cards_dict[c] = d
                    self.errors[c] = int(e)
                    count += 1
            print(f"{count} cards have been loaded.\n")
            logging.info("%d cards have been loaded", count)
        else:
            print("File not found.\n")
            logging.info("File not found.")

    def to_file(self, arg):
        name = arg if arg else input("File name: \n")
        logging.info("File name: %s", name)
        with open(name, "w") as file:
            for card, error in zip(self.cards_dict.items(), self.errors.items()):
                file.write(f"{card[0]}: {card[1]}: {error[1]}\n")
        number = len(list(self.cards_dict.keys()))
        print(f"{number} cards have been saved.\n")
        logging.info("%d cards have been saved.", number)

    def stats(self, action):
        if action == "reset stats":
            self.errors = {key: 0 for key in list(self.cards_dict.keys())}
            print("Card statistics have been reset.\n")
            logging.info("Card statistics have been reset.")
        elif action == "hardest card":
            try:
                max_error = max(list(self.errors.values()))
                if max_error == 0:
                    raise ValueError
            except ValueError:
                logging.info("There are no cards with errors.\n")
                print("There are no cards with errors.\n")
            else:
                hardest = ['"' + key + '"' for key, value in self.errors.items() if value == max_error]
                error_num = "error" if max_error == 1 else "errors"
                if len(hardest) == 1:
                    name = ''.join(hardest)
                    print(f'The hardest card is {name}. You have {max_error} {error_num} answering it.\n')
                    logging.info('The hardest card is %s. You have %d %s answering it.', name,
                                 max_error, error_num)
                else:
                    names = ', '.join(hardest)
                    print(f'The hardest cards are {names}. You have {max_error} {error_num} answering them.\n')
                    logging.info('The hardest cards are %s. You have %d %s answering them.', hardest,
                                 max_error, error_num)

    def save_logs(self):
        name = input("File name:\n")
        logging.info("File name: %s", name)
        logging.shutdown()
        os.rename("flash_log.txt", name)
        print("The log has been saved.")

    def check_meaning(self):
        if len(self.cards_dict) == 0:
            logging.debug("There are no cards. Add one\n")
            print("There are no cards. Add one\n")
        else:
            number = input("How many times to ask?\n")
            logging.info("How many times to ask? %s", number)
            for i in range(int(number)):
                card = random.choice(list(self.cards_dict.keys()))
                result = self.cards_dict[card]
                answer = input(f'Print the definition of "{card}":\n')
                logging.info('Print the definition of "%s": %s', card, answer)
                if answer in self.cards_dict.values():
                    if answer == result:
                        print("Correct!\n")
                        logging.info("Correct!")
                    else:
                        self.errors[card] += 1
                        right_key = list(self.cards_dict.keys())[list(self.cards_dict.values()).index(answer)]
                        print('Wrong. The right answer is "{}", but your definition is correct \
for "{}" card.\n'.format(result, right_key))
                        logging.info('Wrong. The right answer is "%s", \
but your definition is correct for "%s" card.\n', result, right_key)
                else:
                    self.errors[card] += 1
                    print(f'Wrong. The right answer is "{result}".\n')
                    logging.info('Wrong. The right answer is "%s".\n', result)


def main():
    """Actual menu to learn words and definitions"""
    game = Flashcards()
    logging.basicConfig(filename="flash_log.txt",
                        filemode='a',
                        format='%(message)s',
                        level='INFO')
    parser = argparse.ArgumentParser(description="Learn words and their meaning \
by adding them to this program")
    parser.add_argument("--import_from")
    parser.add_argument("--export_to")
    args = parser.parse_args()
    if args.import_from:
        game.import_from(args.import_from)
    while True:
        action = input("Input the action (add, remove, import, export, ask, exit, \
log, hardest card, reset stats):\n")
        logging.info("Input the action (add, remove, import, export, ask, exit, \
log, hardest card, reset stats): %s", action)
        if action == "add":
            game.add_card()
        elif action == "remove":
            game.remove_card()
        elif action == "import":
            game.import_from(args.import_from)
        elif action == "export":
            game.to_file(args.export_to)
        elif action == "ask":
            game.check_meaning()
        elif action in ["hardest card", "reset stats"]:
            game.stats(action)
        elif action == "log":
            game.save_logs()
        elif action == "exit":
            logging.info("Bye bye!")
            if args.export_to:
                game.to_file(args.export_to)
            print("Bye bye!\n")
            break
        else:
            print("There are no such action. Try again\n")


if __name__ == "__main__":
    main()
