def coins_reqd(value, coinage):
    """A version that doesn't use a list comprehension"""
    num_coins = [0] * (value + 1)
    for amt in range(1, value + 1):
        minimum = None
        for c in coinage:
            if c <= amt:
                coin_count = num_coins[amt - c]  # Num coins required to solve for amt - c
                if minimum is None or coin_count < minimum:
                    minimum = coin_count
        num_coins[amt] = 1 + minimum
        
    coins = {}
    remaining = value
    while remaining > 0:
        minimum = None
        mincoin = None
        for c in coinage:
            if minimum is None or num_coins[remaining - c] < minimum:
                minimum = num_coins[remaining - c]
                mincoin = c
        coins[mincoin] = coins.get(mincoin, 0) + 1
        remaining -= mincoin
        
    result = []
    for c, amount in coins.items():
        result.append((c, amount))
        
    return result

	
coinage = [1, 10, 25]
amount = 30
print(coins_reqd(amount, coinage))