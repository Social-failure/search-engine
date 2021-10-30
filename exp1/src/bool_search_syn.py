from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from basic_operation_syn import *


# get input
message = input("What do you want to search?\n")
inputs = word_tokenize(message)

# get stem of each input
stemmer = PorterStemmer()
tokens = []
for each_input in inputs:
    tokens.append(stemmer.stem(each_input))
# add '#' as the last token to signal its end
tokens.append('#')

# scan all tokens, and get the result of the BOOL expression using 2 stacks
# stack 1: store operators, including not, and, or, '(', ')', '#'
# stack 2: store ID list of each token or analyzed expression
operator_stack = []
id_list_stack = []

token_index = 0
# initialize the stack
operator_stack.append('#')
# stack top pointer
operator_stack_top = 0
id_list_stack_top = 0
current_token = tokens[token_index]
token_index += 1

# when encountering '#' both in operator_stack and tokens, it ends
while current_token != '#' or operator_stack[operator_stack_top] != '#':
    # if it is not an operator, push the id list of the token into id_list_stack
    if not operator_or_not(current_token):
        id_list_stack.append(syn_id_list(current_token))
        id_list_stack_top += 1
        # If the stack top is 'not', we need to calculate the correct id list immediately.
        # Our principle is to immediately calculate the correct id list when pushing
        # a new id_list into id_list_stack with 'not' in the operator_stack top.
        while operator_stack[operator_stack_top] == 'not':
            id_list = id_list_stack.pop()
            id_list_stack_top -= 1
            new_id_list = not_list(id_list)
            id_list_stack.append(new_id_list)
            id_list_stack_top += 1
            operator_stack.pop()
            operator_stack_top -= 1
        current_token = tokens[token_index]
        token_index += 1
    # if it is an operator
    else:
        # the operator priority is lower in the stack, push the current_token into the stack
        if get_priority(operator_stack[operator_stack_top], current_token) == '<':
            operator_stack.append(current_token)
            operator_stack_top += 1
            current_token = tokens[token_index]
            token_index += 1
        # the operator priority is equal in the stack, it is ')', so pop the '('
        elif get_priority(operator_stack[operator_stack_top], current_token) == '=':
            operator_stack.pop()
            operator_stack_top -= 1
            current_token = tokens[token_index]
            token_index += 1
        # the operator priority is higher in the stack, calculate them
        elif get_priority(operator_stack[operator_stack_top], current_token) == '>':

            op = operator_stack.pop()
            operator_stack_top -= 1

            if op == 'and':
                id_list2 = id_list_stack.pop()
                id_list_stack_top -= 1
                id_list1 = id_list_stack.pop()
                id_list_stack_top -= 1
                new_id_list = and_list(id_list1, id_list2)
                id_list_stack.append(new_id_list)
                id_list_stack_top += 1
                # Similarly, if the stack top is 'not', we need to calculate the correct id list immediately
                while operator_stack[operator_stack_top] == 'not':
                    id_list = id_list_stack.pop()
                    id_list_stack_top -= 1
                    new_id_list = not_list(id_list)
                    id_list_stack.append(new_id_list)
                    id_list_stack_top += 1
                    operator_stack.pop()
                    operator_stack_top -= 1

            elif op == 'or':
                id_list2 = id_list_stack.pop()
                id_list_stack_top -= 1
                id_list1 = id_list_stack.pop()
                id_list_stack_top -= 1
                new_id_list = or_list(id_list1, id_list2)
                id_list_stack.append(new_id_list)
                id_list_stack_top += 1
                while operator_stack[operator_stack_top] == 'not':
                    id_list = id_list_stack.pop()
                    id_list_stack_top -= 1
                    new_id_list = not_list(id_list)
                    id_list_stack.append(new_id_list)
                    id_list_stack_top += 1
                    operator_stack.pop()
                    operator_stack_top -= 1


# get the boundary num between blogs and news
with open("../output/doclist.txt", "r") as f:
    total_id_list = f.readlines()
    blog_news_boundary = int(total_id_list.pop())

# transform the num (about ID) into the real name of the blog/news
for each_id in id_list_stack[0]:
    if each_id > blog_news_boundary:
        print(news_name(each_id - blog_news_boundary))
    else:
        print(blog_name(each_id))
print(len(id_list_stack[0]))