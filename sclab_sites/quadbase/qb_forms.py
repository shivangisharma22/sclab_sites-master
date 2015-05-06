import wtforms as wtf
from flask_wtf import Form
from itertools import chain
from collections import OrderedDict
from config import assemblies_data, promoter_options, assemblies2_data
from config import quad_stem_options, quad_loop_options, quad_strand_options


class GeneForm(Form):
    gene = wtf.SelectField(u'Official Gene symbol', choices=[])
    organisms = wtf.SelectField(u'Choose organism', choices=[(x,x) for x in (assemblies2_data['vertebrates'].keys() + sorted(assemblies_data['vertebrates'].keys()))])
    assemblies = wtf.SelectField(u'Genome assembly', choices=[])
    promoter_up = wtf.SelectField(u'Promoter Upstream Offset', choices=promoter_options)
    promoter_down = wtf.SelectField(u'Promoter Downstream Offset', choices=promoter_options)


class UserInput(Form):
    userseq = wtf.TextAreaField(u'Please enter/paste DNA sequence in plain text')
    fastafile = wtf.FileField(u'Or Upload FASTA file')


class G4Config(Form):
    stem = wtf.SelectField(u'Stem length', choices=quad_stem_options)
    loop_min = wtf.SelectField(u'Min loop length', choices=quad_loop_options)
    loop_max = wtf.SelectField(u'Max loop length', choices=quad_loop_options)
    strand = wtf.SelectField(u'Strand to search?', choices=quad_strand_options)
    overlapping_quads = wtf.fields.BooleanField(u'Search Overlapping  G4 motifs?')
    maximize_quads = wtf.fields.BooleanField(u'Maximize motif length?')


class SelectTx(Form):
    transcripts = wtf.RadioField()