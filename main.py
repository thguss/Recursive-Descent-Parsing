import os
import sys
from typing import NamedTuple

ASSIGNMENT_OP = 1 # :=
SEMI_COLON = 2 # ;
ADD_OPERATOR = 3 # +|-
MULT_OPERATOR = 4 # *|/
LEFT_PAREN = 5 # (
RIGHT_PAREN = 6 # )
CONST = 7 # 수
IDENT = 8 # 식별자
UNKNOWN = 9 # 알 수 없는 token
EOF = 10

def lexical(line, i, next_token, token_string):

  if i >= len(line):
    next_token.append(10)
    token_string.append('EOF')

  else:
    token = line[i] # nextToken
    # print(token, end=" | ")

    if token == '\t' or token == '\0':
      return lexical(line, i+1)

    if token == ':=':
      next_token.append(1)
      token_string.append('ASSIGNMENT_OP')
    
    elif token == ';':
      next_token.append(2)
      token_string.append('SEMI_COLON')

    elif token == '+' or token =='-':
      next_token.append(3)
      token_string.append('ADD_OPERATOR')

    elif token == '*' or token == '/':
      next_token.append(4)
      token_string.append('MULT_OPERATOR')

    elif token == '(':
      next_token.append(5)
      token_string.append('LEFT_PAREN')

    elif token == ')':
      next_token.append(6)
      token_string.append('RIGHT_PAREN')

    elif token.isdecimal():
      next_token.append(7)
      token_string.append('CONST')

    else:
      next_token.append(8)
      token_string.append('IDENT')

  # print("Next token is: {} | Next lexeme is {}".format(next_token[-1], token_string[-1]))

  return next_token[-1], i+1 # 최근 체크한 토큰, 다음 인덱스 반환


def expr(line, nextToken, i, next_token, token_string):
  # print("Enter <expr>")

  nextToken, idx = term(line, nextToken, i, next_token, token_string)
  nextToken, idx = term_tail(line, nextToken, idx, next_token, token_string)

  # print("Exit <expr>")

  return nextToken, idx


def term(line, nextToken, i, next_token, token_string):
  # print("Enter <term>")

  nextToken, idx = factor(line, nextToken, i, next_token, token_string)
  nextToken, idx = factor_tail(line, nextToken, idx, next_token, token_string)

  return nextToken, idx


def term_tail(line, nextToken, i, next_token, token_string):

  if nextToken == 3: # <add_op>
    nextToken, idx = lexical(line, i, next_token, token_string)
    nextToken, idx =  term(line, nextToken, idx, next_token, token_string,)
    nextToken, idx = term_tail(line, nextToken, idx, next_token, token_string)
  
  else:
    idx = i
  
  # print("Exit <term>")

  return nextToken, idx


def factor(line, nextToken, i, next_token, token_string):
  # print("Enter <factor>")

  if nextToken == 8 or nextToken == 7: # <ident> or <const>
    if nextToken == 8 and (line[i-1] not in symbol_table):
      error.append('(Error) "정의되지 않은 변수({})가 참조됨."'.format(line[i-1]))
      symbol_table.append(line[i-1])

    nextToken, idx = lexical(line, i, next_token, token_string)
  
  elif nextToken == 5: #<left_paren>
    nextToken, idx = lexical(line, i, next_token, token_string)
    nextToken, idx =  expr(line, nextToken, idx, next_token, token_string)

    if nextToken == 6: # <right_paren>
      nextToken, idx = lexical(line, idx, next_token, token_string)
    else:
      error.append('(Error) "왼쪽 괄호 후 오른쪽 괄호가 들어오지 않음"')
      nextToken, idx = lexical(line, idx, next_token, token_string)
  
  else:
    error.append('(Error) "식별자 또는 숫자 또는 왼쪽 괄호가 들어오지 않음"')
    nextToken, idx = lexical(line, i, next_token, token_string)
  
  return nextToken, idx # <term>의 <factor_tail>로 전달


def factor_tail(line, nextToken, i, next_token, token_string):

  if nextToken == 4: # <mult_op>
    nextToken, idx = lexical(line, i, next_token, token_string)
    nextToken, idx =  factor(line, nextToken, idx, next_token, token_string)
    nextToken, idx = factor_tail(line, nextToken, idx, next_token, token_string)
  
  else:
    idx = i

  # print("Exit <factor>")

  return nextToken, idx
  

# file_path = sys.argv[1]
# input = open(file_path)

cwd = os.getcwd()
path = os.path.join(cwd, "프로그래밍언어론\input2.txt")
input = open(path)

symbol_table = [] # 현재 ident 

for line in input.readlines():

  error = []

  line = line.split() # 공백 기준 분할

  next_token = [] # 정수 배열 초기화
  token_string = [] # 문자열 배열 초기화

  nextToken, idx = lexical(line, 0, next_token, token_string)

  if nextToken == 8: # <ident>
    nextToken, idx = lexical(line, idx, next_token, token_string)

    if nextToken == 1: # ident := 형태이면 ident 저장
      symbol_table.append(line[idx-2])

  else:
    error.append('(Error) "식별자로 시작하지 않음"')

  if nextToken != 1: # <assignment_op>
    error.append('(Error) ":= 왼쪽에 <expr>이 올 수 없음"') # warning으로 바꿀 수 있을 듯..?
    
  nextToken, idx = lexical(line, idx, next_token, token_string)
  nextToken, idx = expr(line, nextToken, idx, next_token, token_string)
  

  for l in line:
    print(l, end=" ")

  print("\nID: {}; | CONST: {}; | OP: {};"
  .format(token_string.count('IDENT'), token_string.count('CONST'), token_string.count('ADD_OPERATOR')+token_string.count('MULT_OPERATOR')))

  if error:
    for e in error:
      print(e)

  else:
    print("<Yes>")
  
  print()
  

print(symbol_table)


  