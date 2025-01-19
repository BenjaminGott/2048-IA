import random



MOVES = ["left", "right", "up","down"]

def generate_random_individual(length=10):
    ''' Genere une sequence de mouvement aleatoires pour chaque individu'''
    return [random.choice(MOVES) for _ in range (length)]


def generate_population(size = 100, move_length =60):
    ''' Genere un tableau d'individu'''
    return[generate_random_individual(move_length) for _ in range(size)]


    
    
    


