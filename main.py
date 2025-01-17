import game

if __name__ == "__main__":
    n = game.Game_value()
    state = game.start_game(n)
    
    print(f"Score : {n.score}")
