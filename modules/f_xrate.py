def xrate( tt, M, Y):
    from time import sleep
    import pandas as pd
    from datetime import date
    import forex_python.converter 
    from forex_python.converter  import RatesNotAvailableError
    import numpy as np
    #converted=[]
    #exrate=[]
    #wrong={yr:set() for yr in range(1880,2025)}
    #test=[]
    #tconst=[]
    if (np.isnan(Y)==False) & (M is not np.nan):
        try:
            exrate = forex_python.converter.get_rate(str(M).strip().replace('£', 'GBP').replace( '€','EUR').replace( '$','USD'), 'USD', date_obj=date(int(Y), 1, 1))
            converted = True
            print(tt, M,Y,exrate)
            tconst = tt
        except TypeError as e:
    
            exrate = np.nan
            converted = [e,M,Y]
            print(tt, e, M, Y)
            tconst = tt
        except RatesNotAvailableError as e:
    
            exrate = np.nan
            converted = [e,M,Y]      
            tconst = tt
            test = [M,Y]
            #wrong[Y].update([M,Y])
            print(tt, e, M, Y)
            
        except ValueError as e:
    
            exrate = np.nan
            converted = [e,M,Y]
            tconst = tt
            test = [M,Y]        #if np.isnan(Y)==False:
            #wrong[Y].update([M,Y])   
            print(tt, e, M, Y)
    else:
        exrate = np.nan
        converted = [M,Y] 
        tconst = tt

    #return exrate    
    return {'tt':tconst, 'rate':exrate, 'exchanged':converted}