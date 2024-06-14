import sys

def combine(const, newCoeff, expression):
    combinedCoeff = const * newCoeff
    if expression == '':
        return str(combinedCoeff)
    return f'{combinedCoeff}*{expression}'

def diff(sym):
    ''' 
    Try to match between a*x^b
    '''
    # Check if constant
    if sym.isalpha() or sym.isnumeric():
        return '0'

    terms = sym.split('*')
    constant = 1 if len(terms) == 1 else int(terms[0])
    variableTerm = terms[0] if len(terms) == 1 else terms[1]
    base, power = variableTerm.split('^')
    # convert power to an integer
    power = int(power)

    ### differentiate
    newVariableTerm = ''
    if power > 1:
        newCoeff, newVariableTerm = power, f'{base}^{power-1}'
    else:
        newCoeff, newVariableTerm = 1, ''

    return combine(constant, newCoeff, newVariableTerm)

def parse(input):
    return input.split(' ')

def process(info):
    parsed = parse(info)
    res = []
    for sym in parsed:
        if sym in ["+", "-"]:
            res.append(sym)
        else:
            res.append(diff(sym))
    cleanedRes = cleanUp(res)
    return ' '.join(cleanedRes)

def cleanUp(finalTerms):
    # Get rid of any trailing 0s
    if len(finalTerms) > 2 and finalTerms[-1] == '0':
        return finalTerms[:-2]
    return finalTerms

def main(args):
    if len(args) < 2:
        print("The script requires a polynomial input string")
        return 
    inputPolynomial = args[1]
    print(process(inputPolynomial))
    return 

if __name__ == "__main__":
    main(sys.argv)