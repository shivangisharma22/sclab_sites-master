def quad_finder(seq_name, sequence, stem, loop_start, loop_stop,
                strand, variable_stem, overlapping, maximization):

    import re
    quad_motifs_bed = []
    if strand == 'both':
        strands = ["+", "-"]
    else:
        strands = [strand]
    for strand in strands:
        make_motifs_result = make_motif(stem, loop_start, loop_stop, strand,
                                        variable_stem, overlapping, maximization)
        quad_motif = make_motifs_result[0]
        quad_signature = make_motifs_result[1]
        quad_regex = re.compile(quad_motif, flags=re.IGNORECASE)
        quad_object = quad_regex.finditer(sequence)
        if overlapping:
            for quads in quad_object:
                quad_motifs_bed.append([seq_name, quads.start(), quads.start()+len(quads.group(1)),
                                        len(quads.group(1)), quad_signature, quads.group(1)])
        else:
            for quads in quad_object:
                quad_motifs_bed.append([seq_name, quads.start(), quads.end(), quads.end()-quads.start(),
                                        quad_signature, quads.group()])
    return quad_motifs_bed


def make_motif(stem, loop_start, loop_stop, strand, variable_stem, overlapping, maximization):
    if strand == "+":
        base = 'G'
        invert_base = 'C'
    else:
        base = 'C'
        invert_base = 'G'

    if variable_stem is True:
        stem_start = int(stem.split('-')[0])
        stem_stop = int(stem.split('-')[1])
        quad_signature = base + str(stem_start) + "-" + str(stem_stop) + "L" + str(loop_start) \
                         + "-" + str(loop_stop) + "VNO"
        quad_motif = "(?:%s{%d,%d}[ATGCN]{%d,%d}){3}%s{%d,%d}" % (base, stem_start, stem_stop, loop_start,
                                                                loop_stop, base, stem_start, stem_stop)
    elif overlapping is True:
        stem = int(stem)
        if maximization is True:
            quad_signature = base + str(stem) + "L" + str(loop_start) + "-" + str(loop_stop) + "OMAX"
            quad_motif = r'(?=((%s{%d}[ATGCN]{%d,%d}){3}%s{%d}))' % (base, stem, loop_start,
                                                                     loop_stop, base, stem)
        elif maximization is False:
            quad_signature = base + str(stem) + "L" + str(loop_start) + "-" + str(loop_stop) + "OMIN"
            quad_motif = "(?=((?:%s{%d}[ATGCN](?:[ATN%s]|(?!%s{%d})%s){%d,%d}){3}%s{%d}))" % (base, stem,
                                   invert_base, base, stem-1, base, loop_start-1, loop_stop-1, base, stem)
    elif overlapping is False:
        stem = int(stem)
        quad_signature = base + str(stem) + "L" + str(loop_start) + "-" + str(loop_stop) + "NO"
        quad_motif = "(?:%s{%d}[ATGCN]{%d,%d}){3}%s{%d}" % (base, stem, loop_start, loop_stop, base, stem)

    return (quad_motif, quad_signature)