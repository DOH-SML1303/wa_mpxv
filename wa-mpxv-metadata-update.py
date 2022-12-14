# this script is to take the mpxv nextstrain metadata and
# join with WA mpxv metadata to show the metadata in the
# mpxv nextstrain build
# Author: Stephanie Lunn
# Date: 221005

# import pandas
import pandas as pd

# read in csv files
nextstrain = pd.read_csv('~/monkeypox/data/metadata.tsv.gz', sep='\t', compression='gzip', parse_dates=['date'])
wa = pd.read_csv('~/monkeypox/data/doh_metadata_running_linkedWDRS.csv', parse_dates=['SPECIMEN__COLLECTION__DATE'])

# rename columns in wa metadata to match nextstrain
wa = wa.rename(columns={
    'SPECIMEN__COLLECTION__DATE': 'date',
    'GENBANK_ID': 'genbank_accession_rev',
    'PATIENT__AGE': 'age',
    'PATIENT__ADMINISTRATIVE__SEX': 'sex',
    'PATIENT__ADDRESS__CORRECTED__COUNTY': 'county',
    'TRAVEL__LAST_3__WEEKS': 'travel'})

# set index
nextstrain = nextstrain.set_index('genbank_accession_rev')
wa = wa.set_index('genbank_accession_rev')

# convert collect_date to YYYY-MM-DD
wa['date'] = pd.to_datetime(wa['date']).dt.strftime('%Y-%m-%d')

# replace wa collection dates
nextstrain_dates = pd.DataFrame(nextstrain.loc[:, 'date'])
wa_dates = pd.DataFrame(wa.loc[:, 'date'])
new_dates = wa_dates.append(nextstrain_dates)

# remove duplicate entries in the index
new_dates = pd.DataFrame(new_dates)
new_dates = new_dates[~new_dates.index.duplicated(keep='first')]

# replace new_df dates with updated dates
new_df = pd.DataFrame(nextstrain)
new_df[['date']] = new_dates[['date']]

# add age, sex, and county columns
new_df[['age', 'sex', 'county', 'travel']] = wa[['age', 'sex', 'county', 'travel']]

# select just the hMPXV-1 cases for the build
hMPXV = new_df[new_df['outbreak'] == 'hMPXV-1']

# write out to gzip compressed tsv file
hMPXV.to_csv('~/monkeypox/data/metadata.tsv.gz', sep='\t', compression='gzip')

print('Success! Exit Code 0')
print('Do not worry about the append() warning.')
print('Metadata has been updated for WA cases in the Nextstrain metadata file')

