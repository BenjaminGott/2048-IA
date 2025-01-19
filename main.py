import game

if __name__ == "__main__":
    currentGame = game.Game_value()
    state = game.start_game(currentGame)
    print(f"Score : {currentGame.score}")
