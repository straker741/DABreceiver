def klzavy_priemer(base = 10):
    try:
        # Altered values of PSD (KP=klzavy priemer)
        KP_hodnoty = []
        size = len(hodnoty)
        for i in range(size - base):
            sucet = 0
            for j in range(base):
                sucet += hodnoty[j+i]
            KP_hodnoty.append(sucet/base)
        
        # Creating Line2D object
        plt.figure()
        plt.xlabel('frequency')
        plt.ylabel('db')
        plt.plot(frekvencie, KP_hodnoty)

        # Save figure (Line2D object)
        plt.savefig('/var/www/html/obrazky/klzavy_priemer.png')

        # Clear figure
        plt.clf()
        hodnoty = KP_hodnoty
        return True
    except:
        print("Ending klzavy_priemer function.")
        return False
    pass