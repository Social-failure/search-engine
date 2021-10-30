import json
from nltk.corpus import wordnet


# get ID lists of the token pointer
def id_list(pointer):
    token_id_list = [pointer[1]]
    next_pointer = pointer[0]
    with open("../output/inv_list_bool.txt", "r") as f:
        next_id_list = f.readlines()
        while next_pointer != 1:
            token_id_list.append(token_id_list[len(token_id_list) - 1] - int(next_id_list[next_pointer + 1]))
            next_pointer -= int(next_id_list[next_pointer])
    return token_id_list


# get the id list and syn token id list of the token
def syn_id_list(token):
    syn_tokens = [token]
    with open("../output/index.json", "r") as f:
        token_pointer_dict = json.load(f)

    # initialize the syn_token_id_list with the original token
    pointer = token_pointer_dict[token]
    syn_token_id_list = id_list(pointer)

    for synset in wordnet.synsets(token):
        for syn in synset.lemma_names():
            try:
                pointer = token_pointer_dict[syn]
                syn_tokens.append(syn)
                set(syn_tokens)
            except KeyError:
                continue

    for syn_token in syn_tokens:
        pointer = token_pointer_dict[syn_token]
        syn_token_id_list = or_list(syn_token_id_list, id_list(pointer))

    return syn_token_id_list


# AND operation
def and_list(id_list_a, id_list_b):
    and_id_list = []
    a = 0
    b = 0
    while (a < len(id_list_a)) and (b < len(id_list_b)):
        if id_list_a[a] == id_list_b[b]:
            and_id_list.append(id_list_a[a])
            a = a + 1
            b = b + 1
        elif id_list_a[a] > id_list_b[b]:
            a = a + 1
        elif id_list_a[a] < id_list_b[b]:
            b = b + 1
    return and_id_list


# OR operation
def or_list(id_list_a, id_list_b):
    or_id_list = []
    a = 0
    b = 0
    while (a < len(id_list_a)) and (b < len(id_list_b)):
        if id_list_a[a] == id_list_b[b]:
            or_id_list.append(id_list_a[a])
            a = a + 1
            b = b + 1
        elif id_list_a[a] > id_list_b[b]:
            or_id_list.append(id_list_a[a])
            a = a + 1
        elif id_list_a[a] < id_list_b[b]:
            or_id_list.append(id_list_b[b])
            b = b + 1
    while a < len(id_list_a):
        or_id_list.append(id_list_a[a])
        a = a + 1
    while b < len(id_list_b):
        or_id_list.append(id_list_b[b])
        b = b + 1
    return or_id_list


# NOT operation
def not_list(delete_id_list):
    # initially, no_id_list is all id list
    with open("../output/doclist.txt", "r") as f:
        not_id_list = f.readlines()
        not_id_list.pop()
        not_id_list.reverse()

    index = 0
    while index < len(not_id_list):
        not_id_list[index] = int(not_id_list[index])
        index += 1

    index = 0
    while index < len(delete_id_list):
        if delete_id_list[index] in not_id_list:
            not_id_list.remove(delete_id_list[index])
        index += 1
    return not_id_list


# if it is an operator, return True; else, return False
def operator_or_not(token):
    if token == 'not':
        return True
    elif token == 'and':
        return True
    elif token == 'or':
        return True
    elif token == '(':
        return True
    elif token == ')':
        return True
    elif token == '#':
        return True
    else:
        return False


# get the priority between 2 operators
def get_priority(op1, op2):
    # set the priority array of all operators
    priority = \
        [['<', ' ', ' ', '<', ' ', ' '],
         ['<', '>', '>', '<', '>', '>'],
         ['<', '<', '>', '<', '>', '>'],
         ['<', '<', '<', '<', '=', ' '],
         [' ', '>', '>', ' ', '>', '>'],
         ['<', '<', '<', '<', ' ', '=']]
    op = ['not', 'and', 'or', '(', ')', '#']

    # get the coordinate of op1, op2
    x = op.index(op1)
    y = op.index(op2)

    return priority[x][y]


# transform the num (about ID) into the real name of the blog
def blog_name(id):
    idstr = str(id)
    idlen = len(idstr)
    for length in range(1, 8 - idlen):
        idstr = '0' + idstr
    idname = '../dataset/2018_01/blogs_' + idstr + '.json'

    return idname


# transform the num (about ID) into the real name of the news
def news_name(id):
    idstr = str(id)
    idlen = len(idstr)
    for length in range(1, 8 - idlen):
        idstr = '0' + idstr
    idname = '../dataset/2018_01/news_' + idstr + '.json'

    return idname