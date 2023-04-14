# Flashcards_game
A game to learn definitions of words.  
Working through terminal, able to import or export cards - words and their definitions.  
  
  
## How to use  
1. Launch file flashcards.py from the terminal.  
Acceptable arguments: --import_from and --export_to  
Acceptable input: txt file  

```
> python flashcards.py --import_from=marketing_def.txt --export_to=marketing_def1.txt
```

2. Choose action  
add - add card and definition to flashcards dictionary  
remove - remove card from the dictionary  
import - import file if you forgot to do it in the first stage  
export - export cards to desired destination  
ask - start a test  
log - save history logs to a file  
hardest card - show statistics with card is the hardest to memorise  
reset stats - empty all history and start again  
exit - exit program  

```
> Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats): hardest card  
> The hardest card is "Python". You have 1 error answering it.  
> Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats): exit  
> Bye bye!  
```
