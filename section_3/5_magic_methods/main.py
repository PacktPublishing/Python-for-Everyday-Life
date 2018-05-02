# -*- coding: utf-8 -*-
# !/usr/bin/env python3

if __name__ == '__main__':
    import money

    # crafting money
    euro = money.Money(1.0, 'EUR')
    five_euros = money.Money(5.0, 'EUR')
    ten_euros = money.Money(10.0, 'EUR')
    dollar = money.Money(1.0, 'USD')

    # money algebra
    eleven_euros = euro + ten_euros
    sixteen_euros = euro + five_euros + ten_euros
    six_euros = sixteen_euros - ten_euros

    # money comparisons
    print('11 EUR > 6 EUR ? {}'.format(eleven_euros > six_euros))
    print('11 EUR == (10 EUR + 1 EUR) ? {}'.format(eleven_euros == ten_euros + euro))
    print('11 EUR > 50 EUR ? {}'.format(eleven_euros > money.Money(50.0, 'EUR')))

    # playing with a wallet
    wallet = money.Wallet('My Wallet')
    wallet.add(euro)
    wallet.add(ten_euros)
    wallet.add(dollar)

    print('\n{} has {} items:'.format(str(wallet), len(wallet)))
    for item in wallet:
        print('{}'.format(str(item)))
