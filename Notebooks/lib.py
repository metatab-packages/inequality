from contextlib import contextmanager
import matplotlib.pyplot as plt 
import pandas as pd
import metapack as mp

def remove_version(name):
    import re 
    p = re.compile('\-\d+\.\d+\.\d+$')
    
    return re.sub(p, '', name)


def make_cpi(pkg):
    # Convert CPI to be referenced to current dollars
    cpi=pkg.reference('cpi').dataframe()
    cpi['date'] = pd.to_datetime(cpi.DATE)
    cpiy = cpi.groupby(cpi.date.dt.year).CPIAUCSL.mean()
    cpiy = (cpiy/cpiy.max()).reset_index()
    cpiy.columns = ['year','cpi']
    return cpiy

@contextmanager
def new_plot(title, source=None, figsize=(10,8), xlabel=None, ylabel=None, x_label_rot=0, y_label_rot=90,
            panes=1, layout=[0, 0.03, 1, 0.95]):
    
    
    
    if panes == 1:
        fig, ax = plt.subplots(figsize=figsize)
    elif panes == 2:
        fig, ax = plt.subplots(2, figsize=figsize)
    elif panes == 3:
        fig = plt.figure(figsize=figsize)
        ax = [
            plt.subplot2grid((2, 2), (0, 0)),
            plt.subplot2grid((2, 2), (0, 1)),
            plt.subplot2grid((2, 2), (1, 0), colspan=2)
        ]
    else:
        fig, ax = plt.subplots(panes, figsize=figsize)
    
    
        
    fig.suptitle(title, fontsize=20)
    
    yield fig, ax
    
    if panes==1:
        ax = [ax]
    
    if source: 

        fig.text(1,0, "Source: "+source, horizontalalignment='right',verticalalignment='top')
        #fig.text(1,-.18, "Source: "+source,
        #    horizontalalignment='right',verticalalignment='top', transform=ax.transAxes)
    

    if xlabel is not None:
    
        if isinstance(xlabel, str):
            xlabel = [xlabel]*len(ax)
            
        for a,x,y in zip(ax, xlabel, ylabel):
            if x:
                a.set_xlabel(x, rotation=x_label_rot)
            
    if ylabel is not None:
            
        if isinstance(ylabel, str):
            ylabel = [ylabel]*len(ax)

        for a,x,y in zip(ax, xlabel, ylabel):
            if y:
                a.set_ylabel(y, rotation=y_label_rot)

    fig.tight_layout(rect=layout)
            
    plt.show()
            
def make_descriptive_df(df):
    """Get the inheritance set, remove all races ecept black and white, and munge some values"""

    df = df[df.race.isin(['white','black'])].copy()

    # Count parent's bachelors degrees

    def count_bach(r):
        """Count the number of bachelors degrees"""
        return \
            int(r.ed_father_1 == 'bachelors') + \
            int(r.ed_father_2 == 'bachelors') + \
            int(r.ed_mother_1 == 'bachelors') + \
            int(r.ed_mother_2 == 'bachelors')

    #df['n_bach'] = df.apply(count_bach, axis=1)
    df['agecl'] = df.agecl.astype(pd.CategoricalDtype([ '<35', '35-44', '45-54', '55-64', '65-74', '>=75',], ordered=True))
    df['edcl'] = df.edcl.astype(pd.CategoricalDtype(['No HS', 'HS/GED', 'Some College', 'College'], ordered = True))

    # From the extract macro: 
    #  %PCTL(VAR=NETWORTH,PPOINTS=0 25 50 75 90,TAG=NW);
    #  %PCTL(VAR=INCOME,PPOINTS=0 20 40 60 80 90,TAG=INC);
    #  %PCTL(VAR=ASSET,PPOINTS=0 20 40 60 80 90,TAG=ASSET);
    #  %PCTL(VAR=NORMINC,PPOINTS=0 20 40 60 80 90,TAG=NINC);
    #  %PCTL(VAR=NORMINC,PPOINTS=0 50 90,TAG=NINC2);
    #  %PCTL(VAR=NETWORTH,PPOINTS=0 10 20 30 40 50 60 70 80 90 95 99,TAG=NWPCTLE);
    #  %PCTL(VAR=INCOME,PPOINTS=  0 10 20 30 40 50 60 70 80 90 95 99,TAG=INCPCTLE);
    #  %PCTL(VAR=NORMINC,PPOINTS= 0 10 20 30 40 50 60 70 80 90 95 99,TAG=NINCPCTLE);
    #  %PCTL(VAR=INCOME,PPOINTS=0 25 50 75,TAG=INCQRT);
    #  %PCTL(VAR=NORMINC,PPOINTS=0 25 50 75,TAG=NINCQRT);
    
    # Remap the nwpctlecat category numbers to percentile numbers
    m = dict(zip(list(sorted(df.nwpctlecat.unique())),'0 10 20 30 40 50 60 70 80 90 95 99'.split()))
    df['nwpctlecat'] = pd.to_numeric(df.nwpctlecat.replace(m))

    m = dict(zip(list(sorted(df.nincpctlecat.unique())),'0 10 20 30 40 50 60 70 80 90 95 99'.split()))
    df['nincpctlecat'] = pd.to_numeric(df.nincpctlecat.replace(m))
    
    o, gi_sum_bins = pd.qcut(df[df.gi_value_cd > 0].gi_value_cd, 10 , retbins = True)
    gi_sum_bins[0] = 0 # So zero gets included in a bin
    df['gi_value_cd_decile']  = pd.cut(df.gi_value_cd, gi_sum_bins, labels=False).fillna(0)

    o, gi_sum_bins = pd.qcut(df[df.gi_value_cd > 0].gi_value_cd, 100 , retbins = True, duplicates='drop')
    #gi_sum_bins[0] = 0 # So zero gets included in a bin
    df['gi_value_cd_pctle']  = pd.cut(df.gi_value_cd, gi_sum_bins, labels=False).fillna(0)

    o, gi_sum_bins = pd.qcut(df[df.networth > 0].networth, 100 , retbins = True, duplicates='drop')
    #gi_sum_bins[0] = 0 # So zero gets included in a bin
    df['networth_pctle']  = pd.cut(df.networth, gi_sum_bins, labels=False).fillna(0)

   
    return df
    