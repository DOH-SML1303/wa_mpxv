import sys
import pandas as pd

# read in the metadata files to be used for updating
def read_files(input_file_1, input_file_2, input_file_3):
    nextstrain = pd.read_csv(input_file_1, sep='\t', parse_dates=['date'])
    wa_dates_old = pd.read_csv(input_file_2, parse_dates=['SPECIMEN__COLLECTION__DATE'])
    wa_dates_new = pd.read_csv(input_file_3, parse_dates=['Lab_Collection_Date'])
    return nextstrain, wa_dates_old, wa_dates_new

# rename the columns in the WA metadata files to be consistent with the nextstrain metadata file
def rename_columns(wa_dates_old, wa_dates_new):
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
    return wa_dates_old, wa_dates_new

# clean up the wa dates by removing the duplicate entry "Not found in GenBank. Used raw FASTA file."
# and making a new column for the "genbank_accession_rev" using the "accession column"
def clean_wa_dates_new(wa_dates_new):
    value_to_remove = 'Not found in GenBank. Used raw FASTA file.'
    wa_dates_new_cleaned = wa_dates_new[wa_dates_new['accession'] != value_to_remove].copy()
    filtered_dates = wa_dates_new_cleaned['accession'] + '.1'
    wa_dates_new_cleaned.loc[:,'genbank_accession_rev'] = filtered_dates
    #wa_dates_new_cleaned.loc[:, 'genbank_accession_rev'] = wa_dates_new_cleaned['accession'] + '.1'
    return wa_dates_new_cleaned

# set indexes for for joining
def set_indexes(nextstrain, wa_dates_old, wa_dates_new_cleaned):
    nextstrain = nextstrain.set_index('genbank_accession_rev')
    wa_dates_old = wa_dates_old.set_index('genbank_accession_rev')
    wa_dates_new_cleaned = wa_dates_new_cleaned.set_index('genbank_accession_rev')
    return nextstrain, wa_dates_old, wa_dates_new_cleaned

# append the wa metadata into one file
def append_and_clean_dates(wa_dates_old, wa_dates_new_cleaned):
    append_dates = pd.concat([wa_dates_old, wa_dates_new_cleaned])
    append_dates['date'] = pd.to_datetime(append_dates['date']).dt.strftime('%Y-%m-%d')
    return append_dates

# replace the collection dates to be added in the nextstrain metadata file
def replace_wa_collection_dates(nextstrain, append_dates):
    nextstrain_dates = pd.DataFrame(nextstrain.loc[:, 'date'])
    wa_dates = pd.DataFrame(append_dates.loc[:, 'date'])
    new_dates = pd.concat([wa_dates, nextstrain_dates])
    new_dates = new_dates[~new_dates.index.duplicated(keep='first')]
    return new_dates

# update the dates in the metadata file
def update_nextstrain(nextstrain, new_dates, append_dates):
    new_df = nextstrain.copy()
    new_df[['date']] = new_dates[['date']]
    new_df[['age', 'sex', 'county', 'travel']] = append_dates[['age', 'sex', 'county', 'travel']]
    return new_df

# function to process the metadata 
def main(input_file_1, input_file_2, input_file_3, output_file):
    nextstrain, wa_dates_old, wa_dates_new = read_files(input_file_1, input_file_2, input_file_3)
    wa_dates_old, wa_dates_new = rename_columns(wa_dates_old, wa_dates_new)
    wa_dates_new_cleaned = clean_wa_dates_new(wa_dates_new)
    nextstrain, wa_dates_old, wa_dates_new_cleaned = set_indexes(nextstrain, wa_dates_old, wa_dates_new_cleaned)
    append_dates = append_and_clean_dates(wa_dates_old, wa_dates_new_cleaned)
    new_dates = replace_wa_collection_dates(nextstrain, append_dates)
    new_df = update_nextstrain(nextstrain, new_dates, append_dates)
    new_df.to_csv(output_file, sep='\t')
    print('Success! Exit Code 0')
    print('Metadata has been updated for WA cases in the Nextstrain metadata file')

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 wa_mpxv/wa-mpxv-metadata-update.py data/metadata.tsv data/doh_metadata_running_linkedWDRS.csv data/mpox_seq_results_june2024.csv data/metadata.tsv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
