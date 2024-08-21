import random
import pandas as pd


def split_data(df, pct_rand_both=None, nr_beg_both=None):
    """
    """
    tr_set = va_set = []
    
    if not pct_rand_both and not nr_beg_both: print('Set AT LEAST one parameter!')
    if pct_rand_both and nr_beg_both: print('Set ONLY one parameter!'); return ([],[])
    
    tr_df = df[df['usage']==False]  # 1st option
    va_df = df[df['usage_txt'].str.contains('val')]  # 2nd optin

    tr_len = tr_df.shape[0]
    va_len = va_df.shape[0]
    ##print(f'train={tr_len}, val={va_len}, total={tr_len + va_len}')

    #pct_beg = 0.1
    if pct_rand_both:
        assert pct_rand_both <= 1, " pct_beg must be smaller than 1!!!"
        tr_idx = random.choices(range(tr_len), k=round(pct_rand_both*tr_len))
        va_idx = random.choices(range(va_len), k=round(pct_rand_both*va_len))
        tr_set = tr_df.iloc[tr_idx, :]
        va_set = va_df.iloc[va_idx, :]
        # print(tr_set.shape, va_set.shape)
        #print(len(tr_idx), len(va_idx), len(tr_idx+va_idx), df.shape[0]*pct_beg)
        print(f'Original df={df.shape[0]}:\ttrain={tr_set.shape[0]}, val={va_set.shape[0]},\t'\
              f'train+val={len(tr_set) + len(va_set)}, df*pct_rand_both={pct_rand_both * df.shape[0]:.1f}')


    #nr_beg = 1000
    if nr_beg_both:
        tr_beg = nr_beg_both if tr_len > nr_beg_both else tr_len
        va_beg = nr_beg_both if va_len > nr_beg_both else va_len
        tr_set = tr_df.iloc[:nr_beg_both, :]
        va_set = va_df.iloc[:nr_beg_both, :]
        print(f'Original df={df.shape[0]}:\ttrain={tr_set.shape[0]}, val={va_set.shape[0]},\ttrain+val={len(tr_set) + len(va_set)}')
    return pd.concat([tr_set, va_set])
