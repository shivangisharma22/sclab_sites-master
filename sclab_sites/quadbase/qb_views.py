from flask import render_template, redirect, url_for, request, jsonify
from utilities import pretty_seq_display, get_seq_from_das, shift_cords_to_tss
from quad_finder import quad_finder
from qb_forms import GeneForm, G4Config, SelectTx, UserInput
from config import variable_stems, gene_list_dict, assemblies_data,assemblies2_data
from sclab_sites import app
from operator import itemgetter
from ucsc_gene import UcscGene
import ast



@app.route("/quadbase", methods=('GET', 'POST'))
def qb_index():
    # Initialize Forms for data entry
    gene_form = GeneForm()
    user_input_form = UserInput()
    # The third form contains default values for each field and hence doesnt need validation
    g4_form = G4Config(stem=3, loop_min=1, loop_max=7)
    if request.method == "POST":
        g4_config = {'stem': g4_form.stem.data, 'loop_min': int(g4_form.loop_min.data),
                     'loop_max': int(g4_form.loop_max.data), 'strand': g4_form.strand.data,
                     'overlapping_quads': g4_form.overlapping_quads.data,
                     'maximize_quads': g4_form.maximize_quads.data}
        # If User selected a gene name
        if gene_form.gene.data:
            # Get information on Transcripts present for the gene
            gene_name = gene_form.gene.data
            database = gene_form.assemblies.data
            promoter_up = gene_form.promoter_up.data
            promoter_down = gene_form.promoter_down.data
            gene = UcscGene(gene_name, database)
            # If more than one transcripts are present then redirect for transcript selection
            if len(gene.transcript_ids) > 1:
                select_info = {}
                for i in gene.transcript_ids:
                    select_info[i] = [gene.get_chromosome(i), gene.get_tss(i), gene.get_tes(i),
                                      gene.get_cds_start(i), gene.get_cds_stop(i), gene.get_strand(i)]
                return redirect(url_for('qb_select_transcript', gene_name=gene_name,
                                        database=database, promoter_up=promoter_up,
                                        promoter_down=promoter_down, select_info=select_info, g4_config=g4_config))
            # Else searching quad after fetching sequence to Sequence getting function
            else:
                tx_id = gene.transcript_ids[0]
                up_coord, down_coord = gene.get_tss_offsets(tx_id, promoter_up, promoter_down)
                sequence = get_seq_from_das(database, gene.get_chromosome(tx_id), up_coord, down_coord)
                return redirect(url_for('qb_quad_search', sequence=sequence, tx_id=tx_id, gene_name=gene_name,
                                        database=database, promoter_up=promoter_up, promoter_down=promoter_down,
                                        g4_config=g4_config))
        # If user entered/pasted Nucleotide sequence of Uploaded a file
        else:
            userseq = user_input_form.userseq.data
            if userseq:
                return redirect(url_for('qb_user_quad_search', sequence=userseq, g4_config=g4_config))
            else:
                fastafile = request.files['fastafile']
                fasta_data = fastafile.read()
                if fasta_data:
                    return redirect(url_for('qb_user_quad_search', sequence=fasta_data, g4_config=g4_config))
    return render_template('qb_index.html', gene_form=gene_form, user_input_form=user_input_form, g4_form=g4_form)


@app.route("/quadbase/get_assembly", methods=['POST'])
def get_assembly():
    return jsonify({'assemblies': assemblies_data['vertebrates'][request.json['organism']]})


@app.route("/quadbase/get_assemblies", methods=['POST'])
def get_assemblies():
    return jsonify({'assemblies':assemblies2_data['vertebrates'][request.json['organism']]})

@app.route("/quadbase/get_genes", methods=['POST'])
def get_genes():
    return jsonify({'gene_list': gene_list_dict[request.json['db']]})


@app.route("/quadbase/SelectTranscript", methods=('GET', 'POST'))
def qb_select_transcript():
    gene_name = request.args['gene_name']
    database = request.args['database']
    promoter_up = request.args['promoter_up']
    promoter_down = request.args['promoter_down']
    select_info = request.args['select_info']
    g4_config = request.args['g4_config']
    form = SelectTx()
    form.transcripts.choices = []
    for tx, value in ast.literal_eval(select_info).iteritems():
        choice_value = "<td>%s</td>" % tx
        for i in value:
            choice_value += "<td>" + str(i) + "</td>"
        form.transcripts.choices.append((tx, choice_value))
    if request.method == 'POST':
        gene = UcscGene(gene_name, database)
        tx_id = form.transcripts.data
        up_coord, down_coord = gene.get_tss_offsets(tx_id, promoter_up, promoter_down)
        sequence = get_seq_from_das(database, gene.get_chromosome(tx_id), up_coord, down_coord)
        return redirect(url_for('qb_quad_search', sequence=sequence, tx_id=tx_id, gene_name=gene_name,
                                database=database, promoter_up=promoter_up, promoter_down=promoter_down,
                                g4_config=g4_config))
    return render_template('qb_select_transcript.html', gene_name=gene_name, form=form)

@app.route("/quadbase/QuadSearch", methods=('GET',))
def qb_quad_search():
    sequence = request.args['sequence']
    tx_id = request.args['tx_id']
    gene_name = request.args['gene_name']
    database = request.args['database']
    promoter_up = request.args['promoter_up']
    promoter_down = request.args['promoter_down']
    g4_config = ast.literal_eval(request.args['g4_config'])
    gene = UcscGene(gene_name, database)
    if str(g4_config['stem']) in variable_stems:
        variable_stem = True
    else:
        variable_stem = False
    quads = quad_finder(gene_name, sequence, g4_config['stem'], g4_config['loop_min'],
                        g4_config['loop_max'], g4_config['strand'], variable_stem,
                        g4_config['overlapping_quads'], g4_config['maximize_quads'])
    quads = sorted(quads, key=itemgetter(1))
    tss_quads = shift_cords_to_tss(quads, promoter_up, promoter_down, gene.get_strand(tx_id))
    sequence = pretty_seq_display(sequence, quads, tss_quads, promoter_up, promoter_down, gene.get_strand(tx_id))
    return render_template('qb_result.html', sequence=sequence, quads=tss_quads)


@app.route("/quadbase/Quad", methods=('GET',))
def qb_user_quad_search():
    sequence = request.args['sequence']
    g4_config = ast.literal_eval(request.args['g4_config'])
    seq_name = 'User-defined'
    if g4_config['stem'] in variable_stems:
        variable_stem = True
    else:
        variable_stem = False
    quads = quad_finder(seq_name, sequence, g4_config['stem'], g4_config['loop_min'],
                        g4_config['loop_max'], g4_config['strand'], variable_stem,
                        g4_config['overlapping_quads'], g4_config['maximize_quads'])
    quads = sorted(quads, key=itemgetter(1))
    if len(quads) > 0:
        sequence = pretty_seq_display(sequence, quads, quads, len(sequence), 0, '+')
    return render_template('qb_result.html', sequence=sequence, quads=quads)