import sys

def is_number(s):
    ''' 
    Check if a Python object is a number
    '''
    if not s:
        return False 
    try:
        float(s)
        return True 
    except ValueError:
        return False
    
def product_formatting(val):
    ''' 
    If a number is an int return it as an int otherwise as float
    '''
    if val % 1 == 0:
        return int(val)
    return val

def multiply(expr1, expr2):
    ''' 
    Code for multiplying simple expressions
    '''
    if expr1 == '0' or expr2 == '0':
        return '0'
    if expr1 == '1':
        return expr2 
    if expr2 == '1':
        return expr1
    # Make expr2 contain the variable
    if expr2.isnumeric():
        expr1, expr2 = expr2, expr1 
    exprSplit = expr2.split('*')
    if len(exprSplit) == 1: # there is not coefficient
        return f'{expr1}*{expr2}'
    return f'{product_formatting(float(expr1) * float(exprSplit[0]))}*{exprSplit[1]}'

def sum_expressions(expr1, expr2):
    '''
    Formatting for adding expressions
    '''
    if expr1 == '0':
        return expr2
    if expr2 == '0':
        return expr1 
    return f'{expr1} + {expr2}'

def poly_term(expr):
    '''
    Differentiate polynomial terms like x^a
    '''
    if len(expr) == 1:
        return '1' # it must be a single variable like 'x'
    base, power = expr.split('^')
    if power == '1':
        return '1'
    elif power == '2':
        return f'{power}*{base}'
    return f'{power}*{base}^{int(power)-1}'

def diff_simple_terms(expr):
    ''' 
    Differentiaties the most basic terms like x^a for a >= 1 and constants
    '''
    if is_number(expr):
        return '0'
    else: # assuming for now we are only dealing with polynomials
        return poly_term(expr)

def parse(input):
    '''
    Currently parsing an input string on the spaces
    '''
    return input.split(' ')

def clean_up(finalTerms):
    '''
    Format the final string to not include any trailing zeros
    '''
    if len(finalTerms) > 2 and finalTerms[-1] == '0':
        return finalTerms[:-2]
    return finalTerms

def is_not_sum(expr):
    return '+' not in expr

def is_simple_term(expr):
    return (('+' not in expr and '-' not in expr and '*' not in expr) or is_number(expr)) and not (is_coefficient(expr) > -1 and not is_number(expr))

def is_coefficient(expr):
    '''
    4x^2
    '''
    maxInd = -1
    for i in range(len(expr)):
        currCoef = expr[:i+1]
        #print(currCoef)
        if not is_number(currCoef):
            return maxInd 
        maxInd += 1
        
    return maxInd    

def differentiate(expr):
    ''' 
    Recursively call using the product and sum rules until we get to simple expressions and build from there
    Uses:
    (f1 + f2 + f3)' = f1' + f2' + f3'
    (fg)' = f'g + fg'
    '''
    if is_simple_term(expr):
        return diff_simple_terms(expr)
    
    if is_not_sum(expr):
        if '*' in expr:
            terms = expr.split('*')
        else:
            tempRes = is_coefficient(expr)
            terms = [expr[:tempRes + 1], expr[tempRes + 1:]]

        left = differentiate(terms[0])
        right = differentiate('*'.join([terms[1]]))
        return sum_expressions(multiply(left, terms[1]), multiply(terms[0], right))

    parsed = parse(expr)
    res = []
    for sym in parsed:
        if sym in ["+", "-"]:
            res.append(sym)
        else:
            res.append(differentiate(sym))
    cleanedRes = clean_up(res)
    return ' '.join(cleanedRes)

def main(args):
    if len(args) < 2:
        print("The script requires a polynomial input string")
        return 
    inputPolynomial = args[1]
    print(differentiate(inputPolynomial))
    return 

if __name__ == "__main__":
    # test_cases = [
    #     'x^2 + -1*x + 1',
    #     '2*x^3 + -3*x^2 + 1*x + -5',
    #     '-1*x^4 + 2*x^3 + -1*x + 4',
    #     '3*x^2 + -2*x + 2',
    #     '4*x^5 + -1*x^3 + 3*x^2 + -1*x + 7',
    #     '-2*x^3 + 5*x + -1',
    #     '1*x^6 + -3*x^4 + 1*x^3 + -4*x + 9',
    #     '5*x^2 + 4*x + -3',
    #     '-3*x^3 + 1*x^2 + -2*x + 1',
    #     '1*x^4 + -4*x^3 + 6*x^2 + -4*x + 1',
    #     '7*x^5 + -2*x^4 + 3*x^2 + -4',
    #     '1*x^3 + -1*x + 2',
    #     '2*x^4 + -1*x^2 + 3*x + -6',
    #     '-1*x^5 + 4*x^3 + -3*x^2 + 2',
    #     '6*x^4 + -2*x^3 + 5*x + -8',
    #     '3*x^3 + 2*x^2 + -1*x + 4',
    #     '-1*x^2 + 4*x + -5',
    #     '2*x^5 + -3*x^4 + 4*x^2 + -1*x + 1',
    #     '1*x^4 + -2*x^3 + 1*x + -1',
    #     '3*x^2 + -1*x + 7',
    #     '0.5*x^3 + -1.25*x^2 + 0.75*x + -2.5',
    #     '1.5*x^4 + -0.5*x^3 + 2.25*x^2 + -1.75*x + 3.5',
    #     '-2.5*x^3 + 3.75*x^2 + -0.5*x + 1.25',
    #     '0.1*x^5 + -0.2*x^4 + 0.3*x^3 + -0.4*x^2 + 0.5*x + -0.6',
    #     '1.1*x^2 + -2.2*x + 3.3'
    #     'x^2*x + x^5*5 + x*x'
    #     ]
    # for test_case in test_cases:
    #     print(differentiate(test_case))
    main(sys.argv)


  

