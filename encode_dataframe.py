import os
import glob
import pandas


def mirror_metadata_files(genome, basedir='.'):
    """
    Mirrors all of the `files.txt` files from the assembly's encodeDCC section
    on UCSC's servers.

    `genome` is the assembly name (hg19, mm9)

    Supply an optional `basedir` to download the data somewhere else.
    """
    cmds = """

    (
        cd {basedir} &&
        wget \\
            -r \\
            -A "files.txt" \\
            "http://hgdownload.cse.ucsc.edu/goldenPath/{genome}/encodeDCC" \\
            -e robots=off \\
            -R "*html*" \\
            -I "/goldenPath/{genome}/encodeDCC" \\
            -np \\
            -l 2
    )
    """.format(**locals())
    print cmds
    os.system(cmds)


def metadata_to_dataframe(fn):
    """
    Converts a single `files.txt` file to a pandas.DataFrame.
    """
    data = []
    for line in open(fn):
        d = {}
        toks = line.strip().split('\t')
        filename, kvs = toks
        url = os.path.join(
            'http://' + os.path.dirname(fn[fn.index('hgdownload.cse.ucsc.edu'):]),
            filename)

        d['url'] = url
        d['filename'] = filename
        for kv in kvs.split('; '):
            k, v = kv.split('=', 1)
            d[k] = v
        data.append(d)
    return pandas.DataFrame(data)


def encode_dataframe(genome, basename='.'):
    """
    Returns a large pandas.DataFrame containing metadata from all identified
    ENCODE data for the assembly.

    Specifically, this concatenates all of the parsed `files.txt` files into
    a single data frame. Assumes `mirror_metadata_files` has been called
    already to mirror data.
    """
    filenames = glob.glob(
        os.path.join(
            basename,
            'hgdownload.cse.ucsc.edu/goldenPath/'
            '{genome}/encodeDCC/*/files.txt'.format(genome=genome)
        )
    )
    dfs = [metadata_to_dataframe(fn) for fn in filenames]
    df = pandas.concat(dfs)
    df.index = df.filename
    return df

if __name__ == "__main__":

    df = encode_dataframe('mm9')
    interesting = (
        (df.cell == 'MEL')
        & (df.type == 'bam')
        & (df.treatment != 'DMSO_2.0pct')
        & (df.dataType.isin(['ChipSeq', 'DnaseSeq']))
        & (df.replicate == '1')
        & df.objStatus.isnull()
    )
    m = df.ix[interesting]
