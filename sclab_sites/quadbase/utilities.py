def pretty_seq_display(sequence, quads, tss_quads, up, down, strand, num_chars=60):
    sequence = list(sequence.upper())
    if strand == "+":
        tss = int(up)
    else:
        tss = int(down)
    for i, quad in enumerate(quads):
        if quad[1] > tss:
            insert_index = i
            break
    quads_with_tss = list(quads)
    tss_quads_with_tss = list(tss_quads)
    quads_with_tss.insert(insert_index, ["TSS", tss, tss+1, 1, "TSS", ""])
    tss_quads_with_tss.insert(insert_index, ["TSS", tss, tss+1, 1, "TSS", ""])
    for i, quad in enumerate(quads_with_tss):
        if quad[0] == "TSS":
            sequence.insert(quad[1]+(i*2), '<mark title="TSS" style="background-color: red;">')
        elif quad[4][0] == "G":
            sequence.insert(quad[1]+(i*2), '<mark title="%s : %s" style="background-color: yellow;">' %
                            (str(tss_quads_with_tss[i][1]), str(tss_quads_with_tss[i][2])))
        else:
            sequence.insert(quad[1]+(i*2), '<mark title="%s : %s" style="background-color: pink;">' %
                            (str(tss_quads_with_tss[i][1]), str(tss_quads_with_tss[i][2])))
        sequence.insert(quad[2]+(i*2)+1, '</mark>')

    ctr = 0
    list_break = []
    for i, letter in enumerate(sequence):
        if letter != r'<mark style="background-color: yellow;">' and letter != r'</mark>' \
                and letter != r'<mark style="background-color: pink;">':
            if ctr == num_chars:
                ctr = 0
                list_break.append(i)
            ctr += 1
    last_pos = 0
    formatted_seq = []
    for i in list_break:
        formatted_seq.append("".join(sequence[last_pos:i]))
        last_pos = i
    formatted_seq.append("".join(sequence[last_pos:-1]) + sequence[-1])
    return formatted_seq


def get_seq_from_das(assembly, chromosome, start, end):
    import urllib2
    coordinates = "%s:%s,%s" % (chromosome, start, end)
    das_url = "http://genome.ucsc.edu/cgi-bin/das/" + assembly + "/dna?segment=" + coordinates
    usock = urllib2.urlopen(das_url)
    das_data = usock.read()
    usock.close()
    seq_start_flag = False
    sequence = ""
    for line in das_data.split("\n"):
        if line.find("</DNA>") != -1:
            break
        if seq_start_flag:
            sequence += line
        if line.find("DNA length=") != -1:
            seq_start_flag = True
    return sequence


def shift_cords_to_tss(quads, up, down, strand):
    quad_result = []
    for i, quad in enumerate(quads):
        quad_result.append(list(quad))
        if strand == "+":
            mod_start = quad[1] - int(up)
            mod_stop = quad[2] - int(up)
        else:
            mod_start = quad[1] - int(down)
            mod_stop = quad[2] - int(down)
        quad_result[i][1] = mod_start
        quad_result[i][2] = mod_stop
    return quad_result