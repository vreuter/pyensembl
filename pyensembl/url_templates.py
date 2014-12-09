"""
Templates for URLs and paths to specific relase, species, and file type
on the Ensembl ftp server.

For example, the human chromosomal DNA sequences for release 77 are in:

    ftp://ftp.ensembl.org/pub/release-78/fasta/homo_sapiens/dna/

"""
from os.path import join

from species import normalize_species_name
from release_info import which_human_reference_name, check_release_number

ENSEMBL_FTP_SERVER = "ftp://ftp.ensembl.org"

# Example directories
# FASTA files: /pub/release-78/fasta/homo_sapiens/
# GTF annotation files: /pub/release-78/gtf/homo_sapiens/
SPECIES_SUBDIR_TEMPLATE = "/pub/release-%(release)d/%(filetype)s/%(species)s/"


def _species_subdir(
        ensembl_release,
        species='homo_sapiens',
        server=ENSEMBL_FTP_SERVER):
    """
    Assume ensembl_release has already been normalize by calling function
    but species might be either a common name or latin name.
    """
    return SPECIES_SUBDIR_TEMPLATE % {
        'release' : ensembl_release,
        'filetype' : 'gtf',
        'species' : species,
    }

def _normalize_release_properties(ensembl_release, species):
    """
    Make sure a given release is valid, normalize it to be an integer,
    normalize the species name, and get its associated reference.
    """
    ensembl_release = check_release_number(ensembl_release)
    species = normalize_species_name(species)
    # TODO: generalize this to species other than human
    assert species == 'homo_sapiens'
    reference_name = which_human_reference_name(ensembl_release)
    return ensembl_release, species, reference_name

def _join_url_subdir(server, subdir):
    """
    Wrote this helper since os.path.join
    doesn't work for "ftp://ftp.ensembl.org" + "/subdir",
    """
    assert not server.endswith("/")
    if subdir.startswith("/"):
        return server + subdir
    else:
        return server + "/" + subdir

# GTF annotation file example: Homo_sapiens.GTCh38.gtf.gz
GTF_FILENAME_TEMPLATE = "%(Species)s.%(reference)s.%(release)d.gtf.gz"

def gtf_url(ensembl_release, species, server=ENSEMBL_FTP_SERVER):
    """
    Returns a URL and a filename, which can be joined together.
    """
    ensembl_release, species, reference_name = _normalize_release_properties(
        ensembl_release, species)

    subdir = _species_subdir(
        ensembl_release,
        species=species,
        server=server)

    url_subdir = _join_url_subdir(server, subdir)

    filename = GTF_FILENAME_TEMPLATE % {
        'Species' : species.capitalize(),
        'reference' : reference_name,
        'release' : ensembl_release,
    }
    return url_subdir, filename

# DNA fasta file example: Homo_sapiens.GRCh38.dna.chromosome.1.fa.gz
FASTA_DNA_CHROMOSOME_FILENAME_TEMPLATE = \
    "%(Species)s.%(reference)s.%(sequence_type)s.chromosome.%(contig)s.fa.gz"

def fasta_dna_url(
        ensembl_release,
        species,
        contig,
        server=ENSEMBL_FTP_SERVER):
    """
    Construct URL to FASTA file with full sequence of a particular chromosome.
    Returns server_url/subdir and filename as tuple result.
    """
    ensembl_release, species, reference_name = _normalize_release_properties(
        ensembl_release, species)
    subdir = _species_subdir(ensembl_release, species, server=server)
    server_subdir = _join_url_subdir(server, subdir)

    server_sequence_subdir = join(server_subdir, 'dna')
    filename = FASTA_DNA_CHROMOSOME_FILENAME_TEMPLATE % {
        "Species" : species.capitalize(),
        "reference" : reference_name,
        "sequence_type" : "dna",
        "contig" : contig
    }
    return server_sequence_subdir, filename


# DNA fasta file example: Homo_sapiens.NCBI36.54.cdna.all.fa.gz
FASTA_CDNA_FILENAME_TEMPLATE = \
    "%(Species)s.%(reference)s.%(sequence_type)s.all.fa.gz"

def fasta_cdna_url(
        ensembl_release,
        species,
        server=ENSEMBL_FTP_SERVER):
    """
    Construct URL to FASTA file with cDNA sequences of each transcript.
    Returns server_url/subdir and filename as tuple result.
    """
    ensembl_release, species, reference_name = _normalize_release_properties(
        ensembl_release, species)
    subdir = _species_subdir(ensembl_release, species, server=server)
    server_subdir = _join_url_subdir(server, subdir)
    server_sequence_subdir = join(server_subdir, 'cdna')
    filename = FASTA_CDNA_FILENAME_TEMPLATE % {
        "Species" : species.capitalize(),
        "reference" : reference_name,
        "sequence_type" : "dna",
    }
    return server_sequence_subdir, filename