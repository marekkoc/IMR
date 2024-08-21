"""
Auxiliary Linear Mixed Effect Modlel functions.

(C) MCI group.

Update:


Created: 2021.03.22 / Updated: 2021.03.22
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_not_nan_score_values(df, scoreName):
    """
    Remove from a dfm NaN values.
    
    C: 2021.02.26 / M:2021.02.06
    """
    print(f'***** {scoreName} *****\n')
    print(f'NaN values in {scoreName} column:')
    print(f'\t\tNaN: {df.isna()[scoreName].sum()}')
    print(f'\t\tNull:{df.isnull()[scoreName].sum()}')
    

    df2 = df[df[scoreName].notna()]
    print(f'\nRows in the df without NaN: {df2.shape[0]}')
    print(f'Rows in the full df (with NaN): {df.shape[0]}')
    return df2


def get_features_from_LMEM(score, df, mdf, save_dir, save_to_file=False):
    """
    
    C: 2021.02.07 / M:2021.02.17
    """


    data= []
    pats = df.RID.unique()

    for p in pats:
        # current patient
        cur = df.loc[df.RID == p]

        # get intercepts and slopes from fitted model (r-ranodm, f-fixed)
        ri, rs = mdf.random_effects[p]
        fi, fs = mdf.fe_params
        # get fitted values from a model for current subject
        fitted_values = mdf.fittedvalues.loc[cur.index]

        # fixed effect from model parameters fi and fs (intercept and slope)
        fixed_ef = fi + fs * cur.Age_at_scan_

        # random effect  ver.1
        ran_from_diff = fitted_values - fixed_ef

        # random effect ver. 2
        ran_eff_2 = ri + rs*cur.Age_at_scan_

        # GET extra parameters from fitted values (mainly for d-slope(s) )
        np_fit_val = fitted_values.to_numpy()
        np_cur_exam_age = cur.Age_at_scan_.to_numpy()
        np_fixed_ef = fixed_ef.to_numpy()
        np_ran_eff_2 = ran_eff_2.to_numpy()
        np_score = cur[score].to_numpy()    
        exam_age_delta = (np_cur_exam_age[-1] - np_cur_exam_age[0])

        fitted_values_slope = (np_fit_val[-1] - np_fit_val[0]) / exam_age_delta        
        cohort_effect_slope = (np_fixed_ef[-1] - np_fixed_ef[0]) / exam_age_delta
        random_effect_slope = (np_ran_eff_2[-1] - np_ran_eff_2[0]) / exam_age_delta
        d_slope = (np_score[-1] - np_score[0]) / exam_age_delta

        # print out some parameter values
        # fixed and random parameters: intercepts (fi, ri) and slopes (fs, rs)
        print_params = 0
        if print_params:   
            print('*** random effect for ', p, ' ***\n', mdf.random_effects[p])
            print()
            print('*** fixed effect ***\n', mdf.fe_params)
            print()    
            print(f'{p}: fitted_values_slope = {fitted_values_slope:.3f}')
            print(f'{p}: cohort_effect_slopt = {cohort_effect_slope:.3f}')
            print(f'{p}: random_effect_slope = {random_effect_slope:.3f}')
            print(f'{p}: d_slope = {d_slope:.3f}')
            print(f'\nfi={fi:.3f}, fs={fs:.3f}\nri={ri:.3f}, rs={rs:.3f}')

        #d-slope from a general line equation
        d_slope_eff = d_slope * cur.Age_at_scan_ - d_slope *  np_cur_exam_age[0] + np_score[0]


        age = np_cur_exam_age[0]        
        fit_val = np_fit_val[0]
        coh_val = fi + fs * age

        dev = fit_val - coh_val
        mixed_slope = fs + rs

        dct = {'RID':p,           
               'PTID':cur.PTID.values[0],
               'Subgroup_': cur.Subgroup_.values[0],
               'Score_name_': score,
               'PTID': cur.PTID.values[0],
               'Age_at_scan_': cur.Age_at_scan_.values[0],
               'Participation_length_yr_': exam_age_delta,
               f'{score.lower()}_fixed_i_': fi,
               f'{score.lower()}_fixed_s_': fs,
               f'{score.lower()}_random_i_': ri,
               f'{score.lower()}_random_s_': rs,
               f'{score.lower()}_mixed_s_' : mixed_slope,
               f'{score.lower()}_d_slope_': d_slope,
               f'{score.lower()}_dev_': dev        
              }
        data.append(dct)
        
    df_lmem = pd.DataFrame(data)
    if save_to_file:        
        name = save_dir / f'{score}_lmem_features.csv'
        df_lmem.to_csv(name)
        print(f'File saved to: {name}')
    
    return df_lmem


def plot_lmem(df_long,
              mdf,
              score,
              k=-1, 
              plot_score=1,  #plot subject score values
              plot_fitted_values=1, #fitter values from the model
              plot_fixed_from_model=0, 
              plot_ranodm_from_fitted_values=0,
              plot_random_from_model=0, 
              print_params=0,
              plot_deviation=0, 
              plot_fixed_effect_for_cohort=0,
              cohort_alpha = 0.7,
              title = '',
              xlabel = 'x label',
              ylabel = 'y label',
              legend=0,
              scale_y = 1):
    """
        Params
        ------------
        df:
        score:
        k - first patient numer, if k<0 print all patients [integer],
        plot_score - scor trajectory [0 or 1],
        plot_fitted_values - mixed effect (cohort + ranodm) [0 or 1],
        plot_fixed_from_model - fixed effect calculated based on model [0 or 1],
        plot_ranodm_from_fitted_values - random effect from fited values (fitted-cohort) [0 or 1],
        plot_random_from_model - random effect from model (ri, rs) [0 or 1],
        print_params - print out some parameters [0 or 1],
        plot_deviation - plot deviation [0 or 1],
        plot_fixed_effect_for_cohort - plot fixed effect fot the whole cohort [0 or 1],
        cohort_alpha - cohort line opacity [float: between 0 and 1]
        title - plot title [string],
        xlabel - xlabel [string],
        ylabel - ylabel [string], 
        legend = draw legend [0 or 1],
        scale_y = scale y axis values [float: default 1]



    C: 2021.02.05 / M: 2021.03.11
    """

    fig, ax = plt.subplots(figsize=(18,10))
    ax.grid()
    tit = title if len(title) else f'{score} vs. Exam_age'
    ax.set_title(tit, fontsize=22, weight='bold')
    ax.set_xlabel(xlabel, fontsize=20, weight='bold')
    ax.set_ylabel(ylabel, fontsize=20, weight='bold')

    if k>=0:
        smci = df_long.loc[df_long.Subgroup_ == 'sMCI',:]
        cad = df_long.loc[df_long.Subgroup_ == 'cAD',:]
        pat_smci = smci.RID.unique()[:k]
        pat_cad = cad.RID.unique()[:k]
        pat = np.concatenate([pat_smci,pat_cad])
        df_long = df_long.loc[df_long['RID'].isin(pat)]

    #https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.legend.html
    # Legeng
    line_lst = []
    label_lst = []
    
    pats = df_long.RID.unique()
    for p in pats:
        # current patient
        cur = df_long.loc[df_long.RID == p]
        
        # color (col) and dark color (colD) for sMCI vs cAD
        col = 'red' if cur.Subgroup_.values[0] == 'sMCI' else 'blue'
        colD = 'maroon' if cur.Subgroup_.values[0] == 'sMCI' else 'navy'

        # subject sMCI or cAD
        sub = 'sMCI' if cur.Subgroup_.values[0] == 'sMCI' else 'cAD'
        
        ### MODEL PARAMS
        # get intercepts and slopes from fitted model (r-ranodm, f-fixed)
        ri, rs = mdf.random_effects[p]
        fi, fs = mdf.fe_params
        
        # get fitted values from a model for current subject
        fitted_values = mdf.fittedvalues.loc[cur.index]
        
        ### SCORE e.g. ADAS13
        # plot current subject score trajectory with a line and circle points
        # Exam_Age <==> Age_at_scan_
        #plot_score = 1
        if plot_score:
            l, = ax.plot(cur.Age_at_scan_, cur[score], color=col, marker='o', linestyle='-')
            label = f'A subject trajectory ({sub})'
            if not label in label_lst:
                line_lst.append(l)
                label_lst.append(label)

        ### FITTED VALUE (MIXED EFFECT) - FROM THE MODEL
        # plot mixed effect (fixed+ranodom) overlayed on every subject
        #plot_fitted_values = 1
        if plot_fitted_values:        
            l, = ax.plot(cur.Age_at_scan_, fitted_values, color=col, alpha=0.3, linewidth=2)
            label = f'fitted_values (from the model:\nfixed + ranodm effects) ({sub})'
            if not label in label_lst:
                line_lst.append(l)
                label_lst.append(label)

        ### FIXED (COHORT) EFFECT FROM MODEL
        # fixed effect from model parameters fi and fs (intercept and slope)
        fixed_ef = fi + fs * cur.Age_at_scan_
        #plot_fixed_from_model = 1
        if plot_fixed_from_model:
            l, = ax.plot(cur.Age_at_scan_, fixed_ef, color=col, linewidth=4, alpha=1)
            label = f'subject coh. (from fi,fs) ({sub})'
            if not label in label_lst:
                line_lst.append(l)
                label_lst.append(label)

        ### RANDOM EFFECT AS A DIFFERENCE
        # random effect  ver.1
        #plot_ranodm_from_fitted_values = 1
        ran_from_diff = fitted_values - fixed_ef
        if plot_ranodm_from_fitted_values:            
            l, = ax.plot(cur.Age_at_scan_, ran_from_diff, color=col, linestyle='-.', alpha=0.9, linewidth=2)  # to jest rslope
            label = f'random1 (fitted - cohort) ({sub})'
            if not label in label_lst:
                line_lst.append(l)
                label_lst.append(label)
            
        ### RANDOM EFFECT FROM THE MODEL
        # random effect ver. 2
        ran_eff_2 = ri + rs*cur.Age_at_scan_
        #plot_random_from_model = 1
        if plot_random_from_model:
            l, = ax.plot(cur.Age_at_scan_, ran_eff_2, color=col, linewidth=2)
            label = f'random2 (from ri, rs) ({sub})'
            if not label in label_lst:
                line_lst.append(l)
                label_lst.append(label)
            
        # GET extra parameters from fitted values (mainly for d-slope(s) )
        np_fit_val = fitted_values.to_numpy()
        np_cur_exam_age = cur.Age_at_scan_.to_numpy()
        np_fixed_ef = fixed_ef.to_numpy()
        np_ran_eff_2 = ran_eff_2.to_numpy()
        np_score = cur[score].to_numpy()    
        exam_age_delta = (np_cur_exam_age[-1] - np_cur_exam_age[0])

        fitted_values_slope = (np_fit_val[-1] - np_fit_val[0]) / exam_age_delta
        cohort_effect_slope = (np_fixed_ef[-1] - np_fixed_ef[0]) / exam_age_delta
        random_effect_slope = (np_ran_eff_2[-1] - np_ran_eff_2[0]) / exam_age_delta
        d_slope = (np_score[-1] - np_score[0]) / exam_age_delta

        # print out some parameter values
        # fixed and random parameters: intercepts (fi, ri) and slopes (fs, rs)
        #print_params = 0
        if print_params:   
            print('*** random effect for ', p, ' ***\n', mdf.random_effects[p])
            print()
            print('*** fixed effect ***\n', mdf.fe_params)
            print()    
            print(f'{p}: fitted_values_slope = {fitted_values_slope:.3f}')
            print(f'{p}: cohort_effect_slopt = {cohort_effect_slope:.3f}')
            print(f'{p}: random_effect_slope = {random_effect_slope:.3f}')
            print(f'{p}: d_slope = {d_slope:.3f}')
            print(f'\nfi={fi:.3f}, fs={fs:.3f}\nri={ri:.3f}, rs={rs:.3f}')

        #d-slope from a general equation
        d_slope_eff = d_slope * cur.Age_at_scan_ - d_slope *  np_cur_exam_age[0] + np_score[0]
        #ax.plot(cur.Exam_Age, d_slope_eff, color='b',linestyle='dashed', linewidth=2, label='d_slope')


        age = np_cur_exam_age[0]        
        fit_val = np_fit_val[0]
        coh_val = fi + fs * age

        if fit_val > coh_val :
            start_min = coh_val
            end_max = fit_val
        else:
            start_min = fit_val
            end_max = coh_val

        #plot_deviation = 1
        if plot_deviation:
            #ax.vlines(age, start_min,  end_max, color=colD, linestyle='--', label='deviation')
            l, = ax.plot([age, age], [fit_val, coh_val], color=colD, marker='o')
            label = f'deviation ({sub})'
            if not label in label_lst:
                line_lst.append(l)
                label_lst.append(label)


        # test thick line : random eff. + cohort eff.
        #ax.plot(cur.Age_at_scan_, fixed_ef+ran_eff_2, 'g',linewidth=7)


    # plot cohort effect for the whole range of exam ages  
    #plot_fixed_effect_for_cohort = 0
    if plot_fixed_effect_for_cohort:
        l, = ax.plot(df_long.Age_at_scan_, fi + fs * df_long.Age_at_scan_, 'k', linewidth=3, alpha=cohort_alpha)
        label = f'cohort from (fi, fs) ({sub})'
        if not label in label_lst:
                line_lst.append(l)
                label_lst.append(label)
        
    #legend = 1
    if legend:
        ax.legend(line_lst, label_lst,handlelength=3, fontsize=11)
    
    return ax