import time
import numpy as np
np.random.seed(0) #for reproducibility

start = time.time()
#feel free to experiment w/ smaller values here at first
nmen = 10000
nwomen = 10000
female_prefs = np.tile(np.arange(nmen), (nwomen, 1))
#shuffle the female preferences
for female_pref in female_prefs:
    np.random.shuffle(female_pref)
male_prefs = np.tile(np.arange(nwomen), (nmen, 1))
#shuffle the male preferences
for male_pref in male_prefs:
    np.random.shuffle(male_pref)
print(f'Took {time.time() - start} seconds to declare preferences')

#now import your function and call it
import stable_marriage
matches = stable_marriage.match(female_prefs, male_prefs)
