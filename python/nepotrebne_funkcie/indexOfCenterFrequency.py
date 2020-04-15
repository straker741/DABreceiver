def indexOfCenterFrequency(centerFrequency):
    """Funkcia urci index na ktorom sa nachadza centralna frekvencia."""
    # Mohol by som urychlit vypocet tak, ze by som sa zacal pozerat az od nejakych 40% celej velkosti samplov
    # pretoze hladana hodnota sa bude nachadzat okolo 50% celej velkosti samplov
    samples = len(frekvencie)    
    for i in range(samples):
        # Prechadzam kazdu sample a zistujem na ktorom indexe sa nachadza centralna frekvencia
        print("frekvencie[" + str(i) + "]:", frekvencie[i])     
        if centerFrequency <= frekvencie[i]:
            # VZDY TO JE 512 !!!!!!!!!!!!!!
            return i
    else:
        print("No center frequency found!")
        return samples/2
    pass
