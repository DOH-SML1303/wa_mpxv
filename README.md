# wa_mpxv
WA-focused config files for mpxv nextstrain

# Setup
First, install the [monkeypox nextstrain pipeline](https://github.com/nextstrain/monkeypox) and clone the monkeypox repository using `git clone https://github.com/nextstrain/monkeypox.git` or `gh repo clone nextstrain/monkeypox`.

Next, clone this repository in the `monkeypox/config` folder. You can do this in the command-line terminal by navigating to the `monkeypox` repository using `cd monkeypox/config` and then cloning the repository using `git clone https://github.com/DOH-SML1303/wa_mpxv.git` or `gh repo clone DOH-SML1303/wa_mpxv`.

Alternatively, it is possible to bypass the installation of Nextstrain using Docker by following the Ambient instructions and later running the pipeline using `Snakemake`. Install the [monkeypox nextstrain pipeline](https://github.com/nextstrain/monkeypox), but follow the Ambient instructions when installing [Nextstrain](https://docs.nextstrain.org/en/latest/install.html). After the installations are completed, run the global pipeline with the command `snakemake -j 1 -p --configfile config/config_hmpxv1.yaml`.

If you encounter an error related to the tsv-filter, install tsv_utils by using  `mamba install tsv-utils`. The next error you might encounter might have to do with seqkit which can be fixed by using the command `mamba install seqkit`. Try running the pipeline again, and remember to clean the outputs by executing `snakemake clean --cores 2` before running the pipeline. The pipeline might still throw an error when trying to execute Nextalign. This is an error that is generated by the snakemake file, but you can execute Nextalign directly in the command line to force the output to be created by using:
```
nextalign run --jobs 3 --reference config/reference.fasta --genemap config/genemap.gff --max-indel 10000 --seed-spacing 1000 --retry-reverse-complement --output-fasta - --output-insertions results/hmpxv1/insertions.fasta results/hmpxv1/reversed.fasta | seqkit seq -i > results/hmpxv1/aligned.fasta`
```
Execute the pipeline again with the command `snakemake -j 1 -p --configfile config/config_hmpxv1.yaml`. This time do not run `snakemake clean --cores 2` as the output by Nextalign will need to be used.

# Retrieving sequencing and metadata files for the monkeypox nextstrain
The monkeypox sequencing data is maintained by the Nextstrain team and can be retrieved using `wget`. To retrieve the sequencing and metadata files, navigate to the `monkeypox/data` folder. While in the `data` folder in the terminal window, run the command `wget https://data.nextstrain.org/files/workflows/monkeypox/sequences.fasta.xz` to download the sequencing data and `wget https://data.nextstrain.org/files/workflows/monkeypox/metadata.tsv.gz` to download the metadata.

# Updating the metadata to include metadata for WA cases
The python script [wa-mpxv-metadata-update.py](https://github.com/DOH-SML1303/wa_mpxv/blob/main/wa-mpxv-metadata-update.py) will allow you to update the metadata in the nextstrain `metadata.tsv.gz` file with data from a separate spreadsheet containing the metadata for the WA cases. You may need to update the file path for the WA metadata on line 12. You can update the script as necessary (especially if the variables are different) in order to get the script to run.

To run the python script, use the command `python3 ~/monkeypox/config/wa_mpxv/wa-mpxv-metadata-update.py`. The `metadata.tsv.gz` will automatically replace the old metadata file.

Next, you will need to subset the hMPXV-1 cases in the master metadata file.* To run the python script, use the command `python3 ~/monkeypox/config/wa_mpxv/select-hMPXV-1-nextstrain.py`. This will automatically replace the `metadata.tsv.gz` file. *Please note that this step has been included as the filter step in the `wa_config_hmpxv1.yaml` on line 25 `filters: "--exclude-where outbreak!=hMPXV-1"` has been replaced with the filter step `filters: "--include-where 'division=Washington'"` to include all Washington state sequences.

# Running the WA-focused monkeypox build in nextstrain
Go through the proper steps of activating the `nextstrain` environment in the terminal window using `conda activate nextstrain` and then navigate to the monkeypox repository using `cd monkeypox`. Run the command `nextstrain build --docker --cpus 6 . --configfile config/wa_mpxv/wa_config_hmpxv1.yaml` to run the pipeline.

If you are bypassing the use of Docker and using Ambient in combination with snakemake, use the following commands to run the WA-focused monkeypox build `snakemake -j 1 -p --configfile config/config_hmpxv1.yaml`. If you continue to get the error related to Nextalign, run:
```
 nextalign run --jobs 3 --reference config/reference.fasta --genemap config/genemap.gff --max-indel 10000 --seed-spacing 1000 --retry-reverse-complement --output-fasta - --output-insertions results/wa_hmpxv1/insertions.fasta results/wa_hmpxv1/reversed.fasta | seqkit seq -i > results/wa_hmpxv1/aligned.fasta
 ```
followed by `snakemake -j 1 -p --configfile config/wa_mpxv/wa_config_hmpxv1.yaml`

# Visualizing the results
`nextstrain view auspice/`
