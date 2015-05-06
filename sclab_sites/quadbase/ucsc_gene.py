class UcscGene():
    def __init__(self, gene_name, assembly):
        import pymysql
        db = pymysql.connect(host="genome-mysql.cse.ucsc.edu", user="genome", db=assembly)
        cur = db.cursor()
        cur.execute('SELECT * from refFlat WHERE geneName="%s"' % gene_name)
        result = cur.fetchall()
        if len(result) > 0:
            self.status = 'Valid'
            self.db = assembly
        else:
            self.status = 'Invalid'
        if self.status == 'Valid':
            self.transcript_ids = []
            self.transcripts_info = {}
            for i in result:
                self.transcript_ids.append(i[1])
                self.transcripts_info[i[1]] = i

    def get_chromosome(self, transcript_id):
        if transcript_id in self.transcripts_info:
            return self.transcripts_info[transcript_id][2]
        else:
            raise KeyError('Invalid transcript id')

    def get_strand(self, transcript_id):
        if transcript_id in self.transcripts_info:
            return self.transcripts_info[transcript_id][3]
        else:
            raise KeyError('Invalid transcript id')

    def get_tss(self, transcript_id):
        if transcript_id in self.transcripts_info:
            if self.get_strand(transcript_id) == "+":
                return self.transcripts_info[transcript_id][4]
            else:
                return self.transcripts_info[transcript_id][5]
        else:
            raise KeyError('Invalid transcript id')

    def get_tes(self, transcript_id):
        if transcript_id in self.transcripts_info:
            if self.get_strand(transcript_id) == "+":
                return self.transcripts_info[transcript_id][5]
            else:
                return self.transcripts_info[transcript_id][4]
        else:
            raise KeyError('Invalid transcript id')

    def get_tx_type(self, transcript_id):
        if transcript_id in self.transcripts_info:
            if transcript_id[:2] == "NM":
                return "coding"
            elif transcript_id[:2] == "NR":
                return "noncoding"
            else:
                return "Unknown"
        else:
            raise KeyError('Invalid transcript id')

    def get_cds_start(self, transcript_id):
        if self.get_tx_type(transcript_id) == "coding":
            return self.transcripts_info[transcript_id][6]
        else:
            return -1

    def get_cds_stop(self, transcript_id):
        if self.get_tx_type(transcript_id) == "coding":
            return self.transcripts_info[transcript_id][7]
        else:
            return -1

    def get_utr5_start(self, transcript_id):
        if self.get_tx_type(transcript_id) == "coding":
            if self.get_strand(transcript_id) == "+":
                return self.get_tss(transcript_id)
            else:
                return self.get_cds_stop(transcript_id)
        else:
            return -1

    def get_utr5_stop(self, transcript_id):
        if self.get_tx_type(transcript_id) == "coding":
            if self.get_strand(transcript_id) == "+":
                return self.get_cds_start(transcript_id)
            else:
                return self.get_tss(transcript_id)
        else:
            return -1

    def get_utr3_start(self, transcript_id):
        if self.get_tx_type(transcript_id) == "coding":
            if self.get_strand(transcript_id) == "+":
                return self.get_cds_stop(transcript_id)
            else:
                return self.get_tes(transcript_id)
        else:
            return -1

    def get_utr3_stop(self, transcript_id):
        if self.get_tx_type(transcript_id) == "coding":
            if self.get_strand(transcript_id) == "+":
                return self.get_tes(transcript_id)
            else:
                return self.get_cds_start(transcript_id)
        else:
            return -1

    def get_num_exons(self, transcript_id):
        if transcript_id in self.transcripts_info:
            return self.transcripts_info[transcript_id][8]
        else:
            raise KeyError('Invalid transcript id')

    def get_exons_span(self, transcript_id):
        if transcript_id in self.transcripts_info:
            exons_start = self.transcripts_info[transcript_id][9].split(',')[:-1]
            exons_end = self.transcripts_info[transcript_id][10].split(',')[:-1]
            return [s+'-'+e for s, e in zip(exons_start, exons_end)]
        else:
            raise KeyError('Invalid transcript id')

    def get_tss_offsets(self, transcript_id, up_offset, down_offset):
        up_offset = int(up_offset)
        down_offset = int(down_offset)
        if transcript_id in self.transcripts_info:
            if self.get_strand(transcript_id) == "+":
                start = self.get_tss(transcript_id) - up_offset
                end = self.get_tss(transcript_id) + down_offset
            else:
                start = self.get_tss(transcript_id) - down_offset
                end = self.get_tss(transcript_id) + up_offset
            return start, end
        else:
            raise KeyError('Invalid transcript id')


if __name__ == '__main__':
    import sys
    gene = UcscGene(sys.argv[1], sys.argv[2])
    for tx_id in gene.transcript_ids:
        print gene.get_tss_offsets(tx_id, 500, 500)
