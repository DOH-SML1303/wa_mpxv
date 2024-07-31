rule fix_metadata_file_name:
    """
    Fix metadata file name to be input for next rule
    """
    input:
        metadata="data/metadata.tsv",
    output:
        metadata="data/starting_metadata.tsv"
    shell:
        """
        cp data/metadata.tsv data/starting_metadata.tsv
        """

rule add_wa_metadata:
    """
    Adding WA metadata
    """
    input:
        metadata="data/starting_metadata.tsv",
        wa_old_dates="data/doh_metadata_running_linkedWDRS.csv",
        wa_new_dates="data/mpox_seq_results_june2024.csv",
    output:
        metadata="data/metadata.tsv"
    shell:
        """
        python3 wa_mpxv/wa-mpxv-metadata-update-3.py {input.metadata} {input.wa_old_dates} {input.wa_new_dates} {output.metadata}
        """

ruleorder: add_wa_metadata > fix_metadata_file_name > decompress
