import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd    
import matplotlib.pyplot as plt
import plotly.express as px



def kpi_fig(cred,apli):
    credit = cred
    application = apli


    grouped = credit.groupby('ID')
    ### convertir datos de crédito a un formato amplio que cada ID es una fila
    pivot_tb = credit.pivot(index = 'ID', columns = 'MONTHS_BALANCE', values = 'STATUS')
    pivot_tb['open_month'] = grouped['MONTHS_BALANCE'].min() # mes de apertura
    pivot_tb['end_month'] = grouped['MONTHS_BALANCE'].max() # mes final
    pivot_tb['ID'] = pivot_tb.index
    pivot_tb = pivot_tb[['ID', 'open_month', 'end_month']]
    pivot_tb['window'] = pivot_tb['end_month'] - pivot_tb['open_month']
    pivot_tb.reset_index(drop = True, inplace = True)
    credit = pd.merge(credit, pivot_tb, on = 'ID', how = 'left')
    credit0 = credit.copy()
    credit = credit[credit['window'] > 20] # eliminar a los usuarios cuya ventana de observación menos de 20
    credit['status'] = np.where((credit['STATUS'] == '2') | (credit['STATUS'] == '3' )| (credit['STATUS'] == '4' )| (credit['STATUS'] == '5'), 1, 0) # analyze > 60 days past due 
    credit['status'] = credit['status'].astype(np.int8) # 1: overdue 0: not
    credit['month_on_book'] = credit['MONTHS_BALANCE'] - credit['open_month'] # calculate month on book: how many months after opening account
    credit.sort_values(by = ['ID','month_on_book'], inplace = True)

    ##### 
    denominator = pivot_tb.groupby(['open_month']).agg({'ID': ['count']}) # count how many users in every month the account was opened
    denominator.reset_index(inplace = True)
    denominator.columns = ['open_month','sta_sum']

    #####
    kpi = credit.groupby(['open_month','month_on_book']).agg({'ID': ['count']}) 
    kpi.reset_index(inplace = True)
    kpi.columns = ['open_month','month_on_book','sta_sum'] 
    kpi['due_count'] = np.nan
    kpi = kpi[['open_month','month_on_book','due_count']] # delete aggerate column
    kpi = pd.merge(kpi, denominator, on = ['open_month'], how = 'left') # join sta_sum colun to kpi table



    def calculate_observe(credit, command):
        '''calculate observe window
        '''
        id_sum = len(set(pivot_tb['ID']))
        credit['status'] = 0
        exec(command)
        #credit.loc[(credit['STATUS'] == '4' )| (credit['STATUS'] == '5'), 'status'] = 1
        credit['month_on_book'] = credit['MONTHS_BALANCE'] - credit['open_month']
        minagg = credit[credit['status'] == 1].groupby('ID')['month_on_book'].min()
        minagg = pd.DataFrame(minagg)
        minagg['ID'] = minagg.index
        obslst = pd.DataFrame({'month_on_book':range(0,61), 'rate': None})
        lst = []
        for i in range(0,61):
            due = list(minagg[minagg['month_on_book']  == i]['ID'])
            lst.extend(due)
            obslst.loc[obslst['month_on_book'] == i, 'rate'] = len(set(lst)) / id_sum 
        return obslst['rate']

    command = "credit.loc[(credit['STATUS'] == '0') | (credit['STATUS'] == '1') | (credit['STATUS'] == '2') | (credit['STATUS'] == '3' )| (credit['STATUS'] == '4' )| (credit['STATUS'] == '5'), 'status'] = 1"   
    morethan1 = calculate_observe(credit, command)
    command = "credit.loc[(credit['STATUS'] == '1') | (credit['STATUS'] == '2') | (credit['STATUS'] == '3' )| (credit['STATUS'] == '4' )| (credit['STATUS'] == '5'), 'status'] = 1"   
    morethan30 = calculate_observe(credit, command)
    command = "credit.loc[(credit['STATUS'] == '2') | (credit['STATUS'] == '3' )| (credit['STATUS'] == '4' )| (credit['STATUS'] == '5'), 'status'] = 1"
    morethan60 = calculate_observe(credit, command)
    command = "credit.loc[(credit['STATUS'] == '3' )| (credit['STATUS'] == '4' )| (credit['STATUS'] == '5'), 'status'] = 1"
    morethan90 = calculate_observe(credit, command)
    command = "credit.loc[(credit['STATUS'] == '4' )| (credit['STATUS'] == '5'), 'status'] = 1"
    morethan120 = calculate_observe(credit, command)
    command = "credit.loc[(credit['STATUS'] == '5'), 'status'] = 1"
    morethan150 = calculate_observe(credit, command)


    obslst = pd.DataFrame({'vencidos más de 30 días': morethan30,
                           'vencidos más de 60 días': morethan60,
                           'vencidos más de 90 días': morethan90,
                           'vencidos más de 120 días': morethan120,
                           'vencidos más de 150 días': morethan150
                            })


    fig_kpi=px.line(obslst,title='Analisis % de malos clientes',labels=dict(index="Historial (meses)", value="Acumulativo (%)", variable="Categoria vencidos"))
    return fig_kpi