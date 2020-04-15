def fHrana(value):
    samples = len(frekvencie)
    f = [-1, -1]
    for i in range(samples):
        if value < hodnoty[i]:
            if f[0] == -1:
                f[0] = i
                f[0] = priamka(frekvencie[i-1], hodnoty[i-1], frekvencie[i], hodnoty[i], y=value)
        elif value > hodnoty[i]:
            if f[0] != -1:
                if f[1] == -1:
                    f[1] = i
                    f[1] = priamka(frekvencie[i-1], hodnoty[i-1], frekvencie[i], hodnoty[i], y=value)        
        else:
            # BINGO!
            if f[0] == -1:
                f[0] = frekvencie[i]
            elif f[1] == -1:
                f[1] = frekvencie[i]                  
        
        if not (f[0] == -1 or f[1] == -1):
            # Nemusim dalej nic testovat, ak uz mam obidva frekvencie
            break

    return f
    pass

hodnoty = [1, 1.1, 2, 3, 1, 5, 6, 9, 10, 10, 10, 9, 9.5, 10.1, 8, 5, 2, 2.1, 3, 1]
frekvencie = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119]

mid = 5
print(hodnoty)
print("freq1/2:", fHrana(mid))