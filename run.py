from markov_model import create_model, generate
from scrape import read_bols
import pandas as pd


def run():
    '''Creates a markov model and prints out a sample generated bol'''
    tokens = read_bols()
    markov = create_model(tokens, 16)
    output =  generate(markov,3)
    print ' '.join(output)

run()
