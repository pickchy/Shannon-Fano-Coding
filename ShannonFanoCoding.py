from math import log2
def ShannonFano(n,j,p,CodeSymbols,start_index):
    if n<1:
        return 
    else:
        sum1=float(p[0])
        sum2=float(p[-1])
        NewP0=[]
        NewP1=[]
        N1=1
        N2=1
        for i in range(1,n):
            if sum1>sum2:
                sum2+=float(p[-i])
                N2+=1
            elif sum1 == sum2:
                sum1+=float(p[i])
                N1+=1
            else:
                sum1+=float(p[i])
                N1+=1
        for i in range(0,N1):
            CodeSymbols[start_index+i][j]=0
        for i in range(0,N2):
            CodeSymbols[start_index+i+N1][j]=1  
    if N1>1:
        for i in range(N1):
            NewP0.append(p[i])
    if N2>1:
        for i in range(N2):
            NewP1.append(p[i+N1])
    ShannonFano(N1-1,j+1,NewP0,CodeSymbols,start_index)
    ShannonFano(N2-1,j+1,NewP1,CodeSymbols,start_index + N1)

def DestroyAllMinus(CodeSymbols): #минус минусы + строка
    Result=[]
    for i in range(len(CodeSymbols)):
        code = ''.join(map(str, CodeSymbols[i])).replace('-', '')
        Result.append(code)
    return Result

def KraftInequality(CodeSymbols): # неравенство Крафта'
    summ=0
    for code in CodeSymbols:
        summ+=pow(2,-len(code))
    if summ<=1:
        return 1
    else:
        return 0

def AVGWord(CodeSymbols, p): #средняя длина кодового слова
    Ltotal=0
    # n=len(CodeSymbols)
    LAVG=0
    for i in range(len(CodeSymbols)):
        Ltotal=len(CodeSymbols[i])
        LAVG+=Ltotal*float(p[i])
    return LAVG

def Redundancy(p): # избыточность
    H=0
    Hmax=log2(len(p))
    for num in p:
        if float(num)==0:
            continue
        H+=float(num)*log2(float(num))
    K=1-H/Hmax
    return K

# Основная функция кодирования
def encode(alphabet, p):
    CodeSymbols=[['-'] * len(p) for _ in range(len(p))]
# Создаем пары (вероятность, буква) и сортируем по убыванию вероятностей
    paired = sorted(zip(p, alphabet), reverse=True, key=lambda x: x[0])
    
    # Разделяем обратно на вероятности и алфавит
    p, alphabet = zip(*paired)
    ShannonFano(len(p) - 1, 0, p, CodeSymbols, 0)
    CodeSymbols = DestroyAllMinus(CodeSymbols)

    # Вычисление параметров
    avg_len = AVGWord(CodeSymbols, p)
    redundancy = Redundancy(p)
    kraft = KraftInequality(CodeSymbols)

    return CodeSymbols, avg_len, redundancy, kraft, alphabet

# Функция декодирования
def decode(alphabet, encoded_message, p):
    # Инициализация кодов
    CodeSymbols = [['-' for _ in range(len(alphabet))] for _ in range(len(alphabet))]
    ShannonFano(len(alphabet) - 1, 0, p, CodeSymbols, 0)

    # Удаляем лишние элементы
    CodeSymbols = DestroyAllMinus(CodeSymbols)

    # Преобразуем коды в строки и создаём словарь
    code_dict = {}
    for i, symbol_code in enumerate(CodeSymbols):
        code_as_string = ''.join(symbol_code)  # Преобразуем список символов в строку
        code_dict[code_as_string] = alphabet[i]  # Сопоставляем код и символ

    # Декодирование сообщения
    decoded_message = ''
    temp_code = ''
    for bit in encoded_message:
        temp_code += bit
        if temp_code in code_dict:
            decoded_message += code_dict[temp_code]  # Найден символ для текущего кода
            temp_code = ''  # Сбрасываем буфер

    return decoded_message

# with open('alphabet.txt', 'r') as f:
#     alphabet = f.read()
# with open('p1.txt', 'r') as f:
#     p1 = f.read()
# # with open('text.txt', 'r') as f:
# #     text = f.read()
# p=p1.split()
# p.sort(reverse=True)
# CodeSymbols=[['-'] * len(p) for _ in range(len(p))]
# ShannonFano(len(p)-1,0,p,CodeSymbols,0)
# CodeSymbols=DestroyAllMinus(CodeSymbols)

# for row in CodeSymbols:
#     print(row)
# # print(encode(alphabet,p))