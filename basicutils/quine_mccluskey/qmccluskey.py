import sys
#sys.path.append("F:/py/SelfMadeMiraiPythonScript/quine_mccluskey")
sys.path.append('./quine_mccluskey')
from colorclass import Windows
from .core.qm.qm import QM
# TODO
# add validation for variables from CLI and GUI

# enable colours on terminal for windows

if sys.platform == "win32":
    Windows.enable(auto_colors=True)


# used to check if a string can be an integer
def representsInt(s):
    # checks if the string s represents an integer
    try:
        int(s)
        return True
    except ValueError:
        return False

def maid(argssop='',argsdont_cares='',argsvariables='',minterms=[]):
    
    if argssop:
        sop = argssop.split('+')
        
        varSet = set()
        for _ in sop:
            for __ in _:
                if __ != "'":varSet.add(__)
        argsvariables = ','.join(varSet)

        variables = argsvariables.split(',')

        number_list = {}
        for num in range(len(variables) ** 2 - 1):
            bin_num = str(bin(num)[2:])
            while len(bin_num) < len(variables):
                bin_num = '0' + bin_num
            number_list[bin_num] = num

        dic = {}
        list_dic = []
        for product in sop:

            for variable in product:

                if ord(variable) in range(65, 123) and product.index(variable) + 1 < len(product) and product[
                    product.index(variable) + 1] == "'":
                    dic[variable] = 0

                elif ord(variable) in range(65, 123):
                    dic[variable] = 1

            list_dic.append(dic)
            dic = {}
        result = []
        for mt in list_dic:
            for num in number_list:
                count = 0
                for i in range(len(variables)):
                    if variables[i] in mt and int(num[i]) == mt[variables[i]]:
                        count += 1
                if len(mt) == count:
                    result.append(number_list[num])
        minterms = list(set(result))

    # make sure all the values in the values entered for minterms are valid integers
    if not minterms:
        return 'Error: sum of product values expected for minterms'

    for mt in minterms:
        # if it is not a whitespace and it is not an integer
        if (mt and not representsInt(mt)) or ((mt and representsInt(mt)) and int(mt) < 0):
            return 'Error: Integer values expected for minterms'

    # make sure all the values in the values entered for dont cares are valid integers
    if argsdont_cares:
        dcares = argsdont_cares.split(',')
        # make sure the don't cares are all integer values
        for dc in dcares:
            if (dc and not representsInt(dc)) or ((dc and representsInt(dc)) and int(dc) < 0):
                return 'Error : Integer values expected for don\'t cares'

            # a term cannot be a don't care and a minterm at the same time
            if dc in minterms:
                return 'Error: A term cannot be a minterm and a don\'t care at the same time'

    else:
        dcares = []

    ##################################add validation for variables here ####################
    if argsvariables:
        variables = argsvariables.split(',')

        # filter out duplicates in the variables entered

        # if there were duplicate terms then let the user know
        if len(variables) != len(list(set(variables))):
            return "Error: Duplicate terms not allowed for variables"
        # make sure the variables entered are enough to represent the expression
        # else raise a value error exception and close the program

        # check the number of variables needed
        # take into consideration the minter's as well

        mterms = map(lambda x: int(x), minterms)
        dcs = map(lambda x: int(x), dcares)
        max_minterm = max(list(mterms) + list(dcs))

        max_minterm = bin(max_minterm)[2:]

        if len(variables) != len(max_minterm):
            return "Error: Number of variables entered is not enough to represent expression"
    else:
        variables = []

    qm = QM(minterms, dcares, variables)
    sols = qm.minimize()
    outputStr='\n'.join(sols)

    return outputStr
