# wa_mpxv
Files for WA-Focused mpxv nextstrain build
- [Washington-focused mpox genomic analysis](https://nextstrain.org/groups/waphl/wa/mpox/2024)

# Setup
First, install the [mpox nextstrain pipeline](https://github.com/nextstrain/mpox.git) and clone the repository using `git close https://github.com/nextstrain/mpox.git` or `gh repo clone nextstrain/mpox`.

Next, clone this repository in the `mpox/phylogenetic` folder. You can do this in the command-line terminal by navigating to the `mpox/phylogenetic` folder of the repository using `cd mpox/phylogenetic` if you cloned the repo in your home directory. Next you clone the `wa_mpxv` repo by using `git clone https://github.com/DOH-SML1303/wa_mpxv.git` or `gh repo clone DOH-SML1303/wa_mpxv`.

# Running the build locally
`nextstrain build --cpus 6 . --configfile wa_mpxv/wa_config_hmpxv1.yaml`

