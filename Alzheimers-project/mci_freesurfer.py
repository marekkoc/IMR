"""
Auxiliary functions to deal with FreeSurfer features.

(C) MCI group.

Created: 2021.04.05
Updated: 2021.04.16
"""
import numpy as np
import ipywidgets
import matplotlib.pyplot as plt
import mci_utils as mutils


def shorten_FS_long_names(df_long, verbose=False):
    """
    Shorten long FreeSurfer column namse.
    
    C: 2021.04.05 / U:2021.04.16
    """
    cols = df_long.columns
    if verbose: print('Rename the following column names:\n')
    
    if 'Left-Lateral-Ventricle_long' in cols:
        df_long.rename({'Left-Lateral-Ventricle_long':'LLV_long'}, axis='columns', inplace=True)
        if verbose: print('\tLeft-Lateral-Ventricle-long ---> LLV_long')
    
    if 'Right-Lateral-Ventricle_long' in cols:
        df_long.rename({'Right-Lateral-Ventricle_long':'RLV_long'}, axis='columns', inplace=True)
        if verbose: print('\tRight-Lateral-Ventricle_long ---> RLV_long')
        
    if 'Left-Lateral-Ventricle_cross' in cols:
        df_long.rename({'Left-Lateral-Ventricle_cross':'LLV_cross'}, axis='columns', inplace=True)
        if verbose: print('\tLeft-Lateral-Ventricle_cross ---> LLV_cross')
    
    if 'Right-Lateral-Ventricle_cross' in cols:
        df_long.rename({'Right-Lateral-Ventricle_cross':'RLV_cross'}, axis='columns', inplace=True)
        if verbose: print('\tRight-Lateral-Ventricle_cross ---> RLV_cross')
    
    if verbose:  print()    
    
    if 'Left-Hippocampus_cross' in cols:
        df_long.rename({'Left-Hippocampus_cross':'LHHC_cross'}, axis='columns', inplace=True)
        if verbose: print('\tLeft-Hippocampus_cross ---> LHHC_cross')    
        
    if 'Right-Hippocampus_cross' in cols:
        df_long.rename({'Right-Hippocampus_cross':'RHHC_cross'}, axis='columns', inplace=True)
        if verbose: print('\tRight-Hippocampus_cross ---> RHHC_cross')    
        
    if 'Left-Hippocampus_long' in cols:
        df_long.rename({'Left-Hippocampus_long':'LHHC_long'}, axis='columns', inplace=True)
        if verbose: print('\tLeft-Hippocampus_long ---> LHHC_long')    
        
    if 'Right-Hippocampus_long' in cols:
        df_long.rename({'Right-Hippocampus_long':'RHHC_long'}, axis='columns', inplace=True)
        if verbose: print('\tRight-Hippocampus_long ---> RHHC_long')
    
    return df_long 


def compare_eTIV_x_and_eTIV_y(df_long, verbose=False):
    """
    For long and cross:
        - finds number of NaN,
        - compare eTIV_x with e_TIV_y,
        - if both are equalled then:
            - rename e_TIV_x to e_TIV
            - drop e_TIV_y from the table
    
    C: 2021.04.05 / U:2021.04.16
    """
    
    #feature type: cross/long
    for ft in ['cross', 'long']:
        
        if f'eTIV_x_{ft}' in df_long.columns:
            if verbose: 
                mutils.textWrap(ft)
                print('\nEmpty values:')
                print(f"  eTIV_x_{ft}: #NaN = {df_long[f'eTIV_x_{ft}'].isna().sum()} ")
        if f'eTIV_y_{ft}' in df_long.columns:
            if verbose: print(f"  eTIV_y_{ft}: #NaN = {df_long[f'eTIV_y_{ft}'].isna().sum()} ")

        if f'eTIV_x_{ft}' in df_long.columns:
            equal = df_long[f'eTIV_x_{ft}'].equals(df_long[f'eTIV_y_{ft}'])
            if verbose: print(f'Compare values in eTIV_x_{ft} and eTIV_y_{ft}:\n  All equall: {equal}')

            if equal:    
                if f'eTIV_x_{ft}' in df_long.columns:
                    df_long.rename({f'eTIV_x_{ft}':f'eTIV_{ft}'}, axis='columns', inplace=True)
                    if verbose: print(f"  Rename eTIV_x_{ft} ---> eTIV_{ft}")
                if f'eTIV_y_{ft}' in df_long.columns:
                    df_long.drop(columns=f'eTIV_y_{ft}', inplace=True)
                    if verbose: print(f'  Drop eTIV_y_{ft} from the dataframe' )
            else:
                print(f'e_TIV_x_{ft} NOT equalled to e_TIV_y_{ft} - CHECK IT!!!')
    return df_long

def calculate_sum_of_vetricle_volumes(df_long, verbose=False):
    """
    Calculate sum of left and right vetricle volumes, and normalized sum.
    
    C: 2021.04.06 / U: 2021.04.01
    """
    # ### long
    # (left + right) laeral vetnrical volume
    df_long['LRLV_long'] = df_long.LLV_long.to_numpy() + df_long.RLV_long.to_numpy()
    # normalized
    df_long['LRLV_n_long'] = (df_long.LLV_long.to_numpy() + df_long.RLV_long.to_numpy()) / df_long.eTIV_long.to_numpy()
    if verbose: 
        print(f'Added a new column: LRLV_long')
        print(f'Added a nem column: LRLV_n_long\n')
    
    # ### cross
    # (left + right) laeral vetnrical volume
    df_long['LRLV_cross'] = df_long.LLV_cross.to_numpy() + df_long.RLV_cross.to_numpy()
    # normalized
    df_long['LRLV_n_cross'] = (df_long.LLV_cross.to_numpy() + df_long.RLV_cross.to_numpy()) / df_long.eTIV_cross.to_numpy()
    if verbose: 
        print(f'Added a new column: LRLV_cross')
        print(f'Added a new column: LRLV_n_cross')    
    return df_long

def calculate_sum_of_hippocampus_volumes(df_long, verbose=False):
    """
    Calculate sum of left and right hippocampus volumes, and normalized sum.
    
    C: 2021.04.16 / U: 2021.04.16
    """
    # ### long
    # (left + right) hippocampus
    df_long['LRHHC_long'] = df_long.LHHC_long.to_numpy() + df_long.RHHC_long.to_numpy()
    # normalized
    df_long['LRHHC_n_long'] = (df_long.LHHC_long.to_numpy() + df_long.RHHC_long.to_numpy()) / df_long.eTIV_long.to_numpy()
    if verbose: 
        print(f'Added a new column: LRHHC_long')
        print(f'Added a nem column: LRHHC_n_long\n')
    
    # ### cross
    # (left + right) laeral hippocampus volume
    df_long['LRHHC_cross'] = df_long.LHHC_cross.to_numpy() + df_long.RHHC_cross.to_numpy()
    # normalized
    df_long['LRHHC_n_cross'] = (df_long.LHHC_cross.to_numpy() + df_long.RHHC_cross.to_numpy()) / df_long.eTIV_cross.to_numpy()
    if verbose: 
        print(f'Added a new column: LRHHC_cross')
        print(f'Added a new column: LRHHC_n_cross')    
    return df_long


def stats_measures(df_long, ft, verbose=False):
    """
    
    C: 2021.04.06 / U: 2021.04 06
    """
    for r in df_long.RID.unique():
        pat = df_long.loc[df_long.RID == r]

        # difference betweeen longa and cross
        diff = pat[f'{ft}_long'].to_numpy() - pat[f'{ft}_cross'].to_numpy()
        # diff finite - without NaN
        diff_fin = diff[np.isfinite(diff)] 

        # MAE - Mean absolute error
        abs_diff_fin = np.abs(diff_fin)
        df_long.loc[df_long.RID == r, f'{ft}_MAE_'] = abs_diff_fin.sum() / len(abs_diff_fin)

        # RMSE - Root Mean Square Error
        diff_fin_pow2 = diff_fin**2
        df_long.loc[df_long.RID == r, f'{ft}_RMSE_'] = np.sqrt(diff_fin_pow2.sum() / len(diff_fin_pow2))

    if verbose: 
        print(f'Added a new column with "Mean absolute error": {ft}_MAE_ ')
        print(f'Added a new column with "Root Mean Square Error (RMSE)": {ft}_RMSE_ ')
        print()
    return df_long


def _plot(df_long, k, rids, out, feature_prefix):
    """
    C: 2021.04.05 / U: 2021.04.05
    """
    
    feat_cross = feature_prefix + '_cross'
    feat_long = feature_prefix + '_long'
    title = f'{feature_prefix} (long vs cross)'
    
    f, ax = plt.subplots(1,1,figsize=(18,6))
    #out.clear_output(True)
    ax = plt.gca()
    pat = df_long[df_long.RID == rids[k]]

    x = pat.Age_at_scan_.to_numpy()        
    #clong
    yl = pat[feat_long].to_numpy()
    xlf = x[~np.isnan(yl)]
    ylf = yl[~np.isnan(yl)]

    # cross
    yc = pat[feat_cross].to_numpy()
    xcf = x[~np.isnan(yc)]
    ycf = yc[~np.isnan(yc)]

    ax.plot(xlf, ylf,'-o', lw=4, markersize=16, label='long')
    ax.plot(xcf, ycf, '^-', lw=4, markersize=16, label='cross')
    ax.set_xlabel('Age at scan', fontsize = 20)
    ax.set_ylabel(feature_prefix, fontsize = 20)

    tit = f'RID:{pat.RID.values[0]} - {title}'
    ax.set_title(tit, fontsize=24, fontweight='bold')
    ax.grid(True)
    ax.legend()

    plt.ticklabel_format(axis="y", style="sci", scilimits=(0,3))
    plt.tick_params(labelsize=16)
    plt.legend(loc=0, handlelength=3, prop={'size': 18})
    plt.show()
    
    
def iterate_patient_GUI_with_plot(df, column='RID', name='data frame', rid=None, feature_prefix='LLV', sh=False):
    """
    
    Iterate over patients.
    
    parameters
    ========================
    df - a dataframe to iterate by
    column - a column to iterate on,
    
    
    C: 2020.10.11
    M: 2021.04.05
    """     
    global k, df1    
    subjects = df[column].unique()
    
    if rid in subjects:
        k = np.where(subjects==rid)[0][0]  
    else:
        k = 0
    df11 = df.loc[df[column] == subjects[k]]   
#     # https://stackoverflow.com/questions/61359214/how-to-center-align-headers-and-values-in-a-dataframe-and-how-to-drop-the-index
    df1 = df11.style.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
    df1.set_properties(**{'text-align': 'center'}).hide_index()


    
    right = ipywidgets.Button(description='Next',button_style='', tooltip='Click me', icon='hand-o-right')
    rand =  ipywidgets.Button(description='Random',disabled=False,button_style='',tooltip='Random subject',icon='random')
    left =  ipywidgets.Button(description='Prev.',disabled=False,button_style='',tooltip='Click me',icon='hand-o-left')
    reset = ipywidgets.Button(description='Reset',disabled=False,button_style='',tooltip='Reset subject',icon='eraser')
    hide = ipywidgets.Button(description='Hide',disabled=False,button_style='',tooltip='Reset subject',icon='eye-slash')
    output = ipywidgets.Output(overflow_x='auto')
    with output:
        display(df1) 
        _plot(df, k, subjects, output, feature_prefix)
           

    
    def on_button_clicked(but):
        global k
        output.clear_output()            
            
        if but.description == 'Next':
            k += 1            
        if but.description == 'Prev.':
            k -= 1            
        if but.description == 'Random':
            k = np.random.choice(range(len(subjects)))
        if but.description == 'Reset':
            k = 0
        if but.description == 'Hide':         
            output.hide()
            
            
        k %= len(subjects)
        df11 = df.loc[df[column] == subjects[k]] 
        df1 = df11.style.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
        df1.set_properties(**{'text-align': 'center'}).hide_index()
        with output:
            display(df1)
            _plot(df, k, subjects, output, feature_prefix)    
            
    
    
    buttons = [right, left, rand, reset, hide]
    [b.on_click(on_button_clicked) for b in buttons]
   
    if sh:
        minfo.df_info(df, -1, name)
    
#     hbox = widgets.HBox([widgets.HBox([left, rand, right, reset, hide])])
    hbox = ipywidgets.HBox([left, rand, right, reset, hide])    
    display(ipywidgets.VBox([hbox, output]))