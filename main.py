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

  nextToken, idx, n = term(line, nextToken, i, next_token, token_string)
  nextToken, idx, n = term_tail(line, nextToken, idx, next_token, token_string, n)

  return nextToken, idx, n


def term(line, nextToken, i, next_token, token_string):

  nextToken, idx, n = factor(line, nextToken, i, next_token, token_string)
  nextToken, idx, n = factor_tail(line, nextToken, idx, next_token, token_string, n)

  return nextToken, idx, n


def term_tail(line, nextToken, i, next_token, token_string, n):

  if nextToken == 3: # <add_op>
    nextToken, idx = lexical(line, i, next_token, token_string)

    if nextToken == 3:
      error.append('(Warning) "중복연산자 제거"')
      nextToken, idx = lexical(line, idx, next_token, token_string)
      del line[idx-2]
      idx = idx-1 # 인덱스 하나 줄었으니까 같이 마이너스

    nextToken, idx, m =  term(line, nextToken, idx, next_token, token_string)
    nextToken, idx, m = term_tail(line, nextToken, idx, next_token, token_string, m)

    if n == 'Unknown' or m == 'Unknown':
      n = 'Unknown'
    else:
      if line[i-1] == '+':
        n = int(n)+int(m)
      else:
        n = int(n)-int(m)
  
  else:
    idx = i
  
  # print("Exit <term>")

  return nextToken, idx, n


def factor(line, nextToken, i, next_token, token_string):
  # print("Enter <factor>")

  n = 'Unknown'

  if nextToken == 8 or nextToken == 7: # <ident> or <const>
    if nextToken == 8: # <ident>
      if line[i-1] in symbol_table: # 존재하는데
        if symbol_table[line[i-1]] == 'Unknown': # 정의되지 않은 ident이면
          n = 'Unknown'
        else: # 정의된 ident이면
          n = symbol_table[line[i-1]]
      else:
        error.append('(Error) "정의되지 않은 변수({})가 참조됨."'.format(line[i-1]))
        # print(line[i-1])
        symbol_table[line[i-1]] = 'Unknown'
        n = 'Unknown'
    else: # <const>
      n = int(line[i-1])

    nextToken, idx = lexical(line, i, next_token, token_string)
  
  elif nextToken == 5: #<left_paren>
    nextToken, idx = lexical(line, i, next_token, token_string)
    nextToken, idx, n =  expr(line, nextToken, idx, next_token, token_string)

    if nextToken == 6: # <right_paren>
      nextToken, idx = lexical(line, idx, next_token, token_string)
    else:
      error.append('(Warning) "왼쪽 괄호 후 오른쪽 괄호가 들어오지 않음"')
      line.insert(idx-1, ')') # Warning 띄우고 오른쪽 괄호 삽입한 후 파서 계속 진행
      nextToken, idx = lexical(line, idx, next_token, token_string)
  
  else:
    error.append('(Error) "식별자 또는 숫자 또는 왼쪽 괄호가 들어오지 않음"')
    nextToken, idx = lexical(line, i, next_token, token_string)
  
  return nextToken, idx, n


def factor_tail(line, nextToken, i, next_token, token_string, n):

  if nextToken == 4: # <mult_op>
    nextToken, idx = lexical(line, i, next_token, token_string)
    nextToken, idx, m =  factor(line, nextToken, idx, next_token, token_string)
    nextToken, idx, m = factor_tail(line, nextToken, idx, next_token, token_string, m)
    
    if n == 'Unknown' or m == 'Unknown':
      n = 'Unknown'
    else:
      if line[i-1] == '*':
        n = int(n)*int(m)
      else:
        n = int(n)/int(m)
  
  else:
    idx = i

  # print("Exit <factor>")

  return nextToken, idx, n
  

# file_path = sys.argv[1]
# input = open(file_path)

cwd = os.getcwd()
path = os.path.join(cwd, "프로그래밍언어론\input4.txt")
input = open(path)

symbol_table = dict() # 현재 ident 

for line in input.readlines():

  error = []

  line = line.split() # 공백 기준 분할

  next_token = [] # 정수 배열 초기화
  token_string = [] # 문자열 배열 초기화

  nextToken, idx = lexical(line, 0, next_token, token_string)
  # print(line[idx-1])
  idt = line[idx-1]

  if nextToken != 8: # <ident>
    error.append('(Error) "식별자로 시작하지 않음"')

  nextToken, idx = lexical(line, idx, next_token, token_string)

  if nextToken != 1: # <assignment_op>
    error.append('(Error) ":= 왼쪽에 <expr>이 올 수 없음"') # warning으로 바꿀 수 있을 듯..?
    
  nextToken, idx = lexical(line, idx, next_token, token_string)
  nextToken, idx, num = expr(line, nextToken, idx, next_token, token_string)
  # print(num)
  symbol_table[idt] = num
  

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
  # print(symbol_table)
  
print()
print(symbol_table)


  