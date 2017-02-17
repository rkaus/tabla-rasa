import random
def create_model(tokens, n):
    '''Creates a markov model from list of tokens'''
    model = dict()
    if len(tokens) < n:
        return model
    for i in range(len(tokens) - n):
        gram = tuple(tokens[i:i+n])
        next_word = tokens[i:i+n]
        if gram in model:
            model[gram].append(next_word)
        else:
            model[gram] = [next_word]
    last_word = tuple(tokens[len(tokens)-n:])
    if last_word in model:
        model[last_word].append(None)
    else:
        model[last_word] = [None]
    model.pop(('e1','e2'), None)
    model.pop(('e2','s1'), None)
    return model


def generate(model, n, seed=None, max_iterations=100):
    if seed is None:
        seed = random.choice(model.keys())
    output = list(seed)
    current = tuple(seed)
    for i in range(max_iterations):
        if current in model:
            possible_next_words = model[current]
            next_word = random.choice(possible_next_words)
            if next_word is None: break
            while next_word in ['e1','e2','s1','s2']:
                next_word = random.choice(possible_next_words)
            output.extend(next_word)
            current = tuple(output[-n:])
        else:
            break
    return output
