import sys
import pandas as pd

input_file_1 = sys.argv[1]
input_file_2 = sys.argv[2]
input_file_3 = sys.argv[3]
output_file = sys.argv[4]


# read in csv files
nextstrain = pd.read_csv(input_file_1, sep='\t', parse_dates=['date'])
wa_dates_old = pd.read_csv(input_file_2, parse_dates=['SPECIMEN__COLLECTION__DATE'])
wa_dates_new = pd.read_csv(input_file_3, parse_dates=['Lab_Collection_Date'])


# rename columns in wa metadata to match nextstrain
wa_dates_old = wa_dates_old.rename(columns={
    'SPECIMEN__COLLECTION__DATE': 'date',
    'GENBANK_ID': 'genbank_accession_rev',
    'PATIENT__AGE': 'age',
    'PATIENT__ADMINISTRATIVE__SEX': 'sex',
    'PATIENT__ADDRESS__CORRECTED__COUNTY': 'county',
    'TRAVEL__LAST_3__WEEKS': 'travel'})

wa_dates_new = wa_dates_new.rename(columns={
    'Lab_Collection_Date': 'date',
    'genbank_id': 'accession'})

# remove the rows that don't have a genbank sequence
value_to_remove = 'Not found in GenBank. Used raw FASTA file.'
wa_dates_new_cleaned = wa_dates_new[wa_dates_new['accession'] != value_to_remove]

# the new dates doesn't have a matching index for the genbank_accession_rev column so will have to create one
wa_dates_new_cleaned['genbank_accession_rev'] = wa_dates_new_cleaned['accession'] + '.1'

# set indexgenbank_accession_rev
nextstrain = nextstrain.set_index('genbank_accession_rev')
wa_dates_old = wa_dates_old.set_index('genbank_accession_rev')
wa_dates_new_cleaned = wa_dates_new_cleaned.set_index('genbank_accession_rev')

# join the old and new dates
append_dates = wa_dates_old.append(wa_dates_new)

# convert collect_date to YYYY-MM-DD
append_dates['date'] = pd.to_datetime(append_dates['date']).dt.strftime('%Y-%m-%d')

# replace wa collection dates
nextstrain_dates = pd.DataFrame(nextstrain.loc[:, 'date'])
wa_dates = pd.DataFrame(append_dates.loc[:, 'date'])
new_dates = wa_dates.append(nextstrain_dates)

# remove duplicate entries in the index
new_dates = pd.DataFrame(new_dates)
new_dates = new_dates[~new_dates.index.duplicated(keep='first')]

# replace new_df dates with updated dates
new_df = pd.DataFrame(nextstrain)
new_wa_df = pd.DataFrame(append_dates)
new_df[['date']] = new_dates[['date']]

# add age, sex, and county column
new_df[['age', 'sex', 'county', 'travel']] = new_wa_df[['age', 'sex', 'county', 'travel']]

# write out to tsv
new_df.to_csv(output_file, sep='\t')

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 wa_mpxv/wa-nextstrain-update-location-genbank.py data/metadata.tsv data/doh_metadata_running_linkedWDRS.csv data/mpox_seq_results_june2024.csv data/metadata.tsv")
        sys.exit(1)


print('Success! Exit Code 0')
print('Do not worry about the append() warning.')
print('Metadata has been updated for WA cases in the Nextstrain metadata file')
