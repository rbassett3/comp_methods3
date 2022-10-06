import numpy as np
from numba import jit, prange

@jit(nopython=True, cache=True, parallel=True)
def check_stable_marriage(female_prefs, male_prefs, match):
    '''A function to check if your matching is stable.

    female_prefs[i,:] gives female i's preference order for the males.

    male_prefs[i,:] gives male i's preference order for the females.

    match is a proposed matching, input as an nparray of length nwomen.
      match[i]==j means that female i matches w/ male j.

    note that this function requires nwomen==nmen.
    
    '''
    stable = True
    nwomen = female_prefs.shape[0]
    nmen = male_prefs.shape[0]
    man1 = match[0]
    man2 = match[0]
    #0 undecided, 1 means yes, -1 means no
    woman1_prefers_man2 = 0
    woman2_prefers_man1 = 0
    man2_prefers_woman1 = 0
    man1_prefers_woman2 = 0
    assert nwomen==nmen
    for woman1 in prange(nwomen):
        man1 = match[woman1]
        #only need to go up through woman1, else we consider duplicates
        #since the roles of (woman1, man1) and (woman2, man2) are symmetric
        for woman2 in range(woman1): 
            man2 = match[woman2]
            for male_pref in range(nwomen):
                if female_prefs[woman1][male_pref] == man1: #woman1 prefers man1
                    if woman1_prefers_man2 == 0:
                        woman1_prefers_man2 == -1
                        if woman2_prefers_man1 != 0:
                            break
                if female_prefs[woman1][male_pref] == man2: #woman1 prefers man2
                     if woman1_prefers_man2 == 0:
                        woman1_prefers_man2 == 1 
                        if woman2_prefers_man1 != 0:
                            break
                if female_prefs[woman2][male_pref] == man2: #woman2 prefers man2
                     if woman2_prefers_man1 == 0:
                        woman1_prefers_man2 == -1
                        if woman1_prefers_man2 != 0:
                            break
                if female_prefs[woman2][male_pref] == man1: #woman2 prefers man1
                     if woman2_prefers_man1 == 0:
                        woman2_prefers_man1 == 1
                        if woman1_prefers_man2 != 0:
                            break
            for female_pref in range(nwomen):
                if male_prefs[man1][female_pref] == woman1: #man1 prefers woman1
                    if man1_prefers_woman2 == 0:
                        woman1_prefers_man2 == -1
                        if man2_prefers_woman1 != 0:
                            break
                if male_prefs[man1][female_pref] == woman2: #man1 prefers woman2
                     if man1_prefers_woman2 == 0:
                        man1_prefers_woman2 == 1 
                        if man2_prefers_woman1 != 0:
                            break
                if male_prefs[man2][female_pref] == woman2: #man2 prefers woman2
                     if man2_prefers_woman1 == 0:
                        man2_prefers_woman1 == -1
                        if man1_prefers_woman2 != 0:
                            break
                if male_prefs[man2][female_pref] == woman1: #man2 prefers woman1
                     if man2_prefers_woman1 == 0:
                        man2_prefers_woman1 == 1
                        if man1_prefers_woman2 != 0:
                            break
            if woman1_prefers_man2==1 and man2_prefers_woman1==1:
                stable = False
                print("Unstable Pair!")
                print(f"Woman {woman1} is matched to {man1} but prefers {man2}")
                print(f"Man {man2} is matched to {woman2} but prefers {woman1}")

            if woman2_prefers_man1==1 and man1_prefers_woman2==1:
                stable = False
                print("Unstable Pair!")
                print(f"Woman {woman2} is matched to {man2} but prefers {man1}")
                print(f"Man {man1} is matched to {woman1} but prefers {woman2}")
    return stable
