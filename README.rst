ENCODE dataframe
================

I wanted a better way of exploring and downloading raw data from the ENCODE
project.

For example, I'd like to get the BAM files for all ChIP-seq experiments done in
uninduced MEL cells (from the mm9 assembly).

One strategy would be to individually go through each track hub (e.g., histone
mods from LICR, http://genome.cit.nih.gov/cgi-bin/hgFileUi?db=mm9&g=wgEncodeLicrHistone), filter data, and download files individually.

Another strategy would be to go directly to the download page
(http://hgdownload.cse.ucsc.edu/goldenPath/mm9/encodeDCC/wgEncodeLicrHistone/)
and extract the files that end in `.bam`.

This small package takes advantage of the `files.txt` files (here's an `example
<http://hgdownload.cse.ucsc.edu/goldenPath/mm9/encodeDCC/wgEncodeLicrHistone/files.txt>`_)
that describe all the metadata on the download page.

The `files.txt` files are downloaded from each ENCODE track hub in the assembly
of interest.  Then these files are parsed and concatenated together into one
big `pandas.DataFrame` that can be used to find the data you care about.

Usage
-----
Mirror the files.  This may take a minute or so.  If you've cloned the git
repo, you already have a copy of the mm9 files.

>>> import encode_dataframe as edf
>>> edf.mirror_metadata_files('mm9')

Create a large DataFrame:

>>> df = edf.encode_dataframe('mm9')

>>> len(df)
5865

Armed with the dataframe, we can now slice and dice to get the data we care
about.  Eventually I'd like to run a ChromHMM segmentation on MEL cells, but
I need to get the data first . . .

Choose a cell type

>>> interesting = df.cell == 'MEL'

And only BAM files

>>> interesting &= df.type == 'bam'

And only ChIP- or DNase-seq

>>> interesting &= df.dataType.isin(['ChipSeq', 'DnaseSeq'])

And only untreated (in this case, uninduced) cells:

>>> interesting &= df.treatment != 'DMSO_2.0pct'

And only one replicate (some have 2 or 3)

>>> interesting &= df.replicate == '1'

And only those that don't have some issue with them (looks like older versions
have some text in the objStatus field):

>>> interesting &= df.objStatus.isnull()

How many do we have to work with?

>>> m = df[interesting]
>>> len(m)
60

Some of these are controls (input or IgG), and there are some duplicates (looks
like H3K4me3 ChIP-seq uses 2 different controls; CTCF was done by different
groups).  How many unique antibodies?

>>> len(m.antibody.unique())
46

So here are the files I should download:

>>> urls = m.url.values
