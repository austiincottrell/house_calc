#Calculator to figure out if you should buy a multi family home

import locale
import sys
locale.setlocale(locale.LC_ALL, 'en_US')

rent_0b1b = {'U District':[98105, [950,1200]],  'N Seattle':[98115, [1000,1200]], 'WallingFDord':[98103, [1000,1200]], 'Lindley':[27408, [700,850]]}
rent_1b1b = {'U District':[98105, [1300,1800]], 'N Seattle':[98115, [1400,1800]], 'WallingFDord':[98103, [1400,1800]], 'Lindley':[27408, [700,850]]}
rent_2b1b = {'U District':[98105, [1500,1750]], 'N Seattle':[98115, [1800,2100]], 'WallingFDord':[98103, [1800,2000]], 'Lindley':[27408, [700,850]]}
rent_3b2b = {'U District':[98105, [2400,2500]], 'N Seattle':[98115, [2500,3000]], 'WallingFDord':[98103, [2500,3000]], 'Lindley':[27408, [700,850]]}

# Average interest Rate, LTV Ration, Term
interest_rate = float(0.0377 / 12)
ltv_ratio = float(.0090)
term = 246 #months

def apartment():
    rent = 0
    rent_max = 0
    bad_chars = ['k', 'm', 'K', 'M']
    static_location = ['U District', 'N Seattle', 'WallingFDord', 'Lindley']
    print("Lets calculate some Apartment Complex real estate!")

    ##############
    ### Income ###
    ##############
    print("[0] U District - "+ str(rent_0b1b['U District'][0]) +"\n[1] N Seattle - "+ str(rent_0b1b['N Seattle'][0]) +"\n[2] WallingFDord - "+ str(rent_0b1b['WallingFDord'][0]) +"\n[3] Lindley (NC) - "+ str(rent_0b1b['Lindley'][0]))
    location = int(input('Where is the property located? '))
    if location == 0:
        location = static_location[0]
    elif location == 1:
        location = static_location[1]
    elif location == 2:
        location = static_location[2]
    elif location == 3:
        location = static_location[3]

    studio_doors = int(input('How many studio units does the property have: '))
    one_bed_doors = int(input('How many 1b1b units does the property have: '))
    two_bed_doors = int(input('How many 2b1b units does the property have: '))
    three_bed_doors = int(input('How many 3b2b units does the property have: '))
    total_doors = studio_doors + one_bed_doors + two_bed_doors + three_bed_doors

    if total_doors <= 4:
        start = int(input('[0] False [1] True \nDo you want to continue as a personal loan instead of commercial loan? '))
        if start != 1:
            sys.exit("No need to continue")
        else:
            term = 360 #months
            ltv_ratio = float(.00965)
            interest_rate = float(0.02954 / 12)

    for door in range(studio_doors):
        rent = rent + rent_0b1b[location][1][0]
    for door in range(one_bed_doors):
        rent = rent + rent_1b1b[location][1][0]
    for door in range(two_bed_doors):
        rent = rent + rent_2b1b[location][1][0]
    for door in range(three_bed_doors):
        rent = rent + rent_3b2b[location][1][0]

    for door in range(studio_doors):
        rent_max = rent_max + rent_0b1b[location][1][1]
    for door in range(one_bed_doors):
        rent_max = rent_max + rent_1b1b[location][1][1]
    for door in range(two_bed_doors):
        rent_max = rent_max + rent_2b1b[location][1][1]
    for door in range(three_bed_doors):
        rent_max = rent_max + rent_3b2b[location][1][1]
    

    ################
    ### Expenses ###
    ################
    loan = str(input('How much is the property currently listed for: '))
    if 'K' in loan:
        loan = loan.replace('K','k')
    elif 'M' in loan:
        loan = loan.replace('M','m')
    elif 'k' in loan:
        for i in bad_chars:
            loan = loan.replace(i,'')
        loan = int(loan)
        loan = loan * 1000
    elif 'm' in loan:
        for i in bad_chars:
            loan = loan.replace(i,'')
        loan = float(loan)
        loan = loan * 1000000
    else: 
        loan = int(loan)

    if loan < 50000:
        print('This calculator is built for whole numbers \nPlease have a number larger than 50k')
        loan = str(input('How much is the property currently listed for: '))
        if 'K' in loan:
            loan = loan.replace('K','k')
        elif 'M' in loan:
            loan = loan.replace('M','m')
        elif 'k' in loan:
            for i in bad_chars:
                loan = loan.replace(i,'')
            loan = int(loan)
            loan = loan * 1000
        elif 'm' in loan:
            for i in bad_chars:
                loan = loan.replace(i,'')
            loan = float(loan)
            loan = loan * 1000000
    else:
        pass

    calc = pow((1 + interest_rate), term)
    payment = loan * ((interest_rate * calc) / (calc - 1))
    pmi = (loan * ltv_ratio) / 12
    payment = pmi + payment

    vacancy_rule = rent * .05
    vacancy_rule_max = rent_max * .05
    repairs_rule = rent * .05
    repairs_rule_max = rent_max * .05
    capex_rule = rent * .10
    capex_rule_max = rent_max * .10
    insurance_rule = rent * .06
    insurance_rule_max = rent_max * .06

    prop_tax = (loan * .01) /12

    total = payment + vacancy_rule + repairs_rule + capex_rule + insurance_rule + prop_tax

    cash_flow = rent - total

    print('Your total income from the property would be: '+ locale.format_string("%d",rent, grouping=True) + ' - ' + locale.format_string("%d",rent_max, grouping=True))
    print("Your monthly payment: " + locale.format_string("%d",payment, grouping=True))
    print('                      '+ locale.format_string("%d",vacancy_rule, grouping=True) + ' - ' + locale.format_string("%d",vacancy_rule_max, grouping=True) + ' Vacancy' + '\n                      ' 
    + locale.format_string("%d",repairs_rule, grouping=True)  + ' - ' + locale.format_string("%d",repairs_rule_max, grouping=True) + ' Repairs' + '\n                      '
    + locale.format_string("%d",capex_rule, grouping=True)  + ' - ' + locale.format_string("%d",capex_rule_max, grouping=True) + ' CapEx' + '\n                      '
    + locale.format_string("%d",insurance_rule, grouping=True)  + ' - ' + locale.format_string("%d",insurance_rule_max, grouping=True) + ' Insurance' + '\n                      '
    + locale.format_string("%d",prop_tax, grouping=True) + '       Property Tax')
    print('Total Expenses:\n                      ' + locale.format_string("%d",total, grouping=True))

    if rent < total:
        print('\n \nThis is not a good investment!!\n\nYou have a negative cashflow of: ' + locale.format_string("%d",cash_flow, grouping=True))
    else:
        print('\nThis is a good investment!!\n\nYou have a positive cashflow of: ' + locale.format_string("%d",cash_flow, grouping=True))



# Calling the function above
apartment()
