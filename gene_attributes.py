# For extracting gene attributes from the GTF file 
def extract_gene_attributes(gtf_file, gene_id_file, output_file):
    gene_attributes = {}

    # Read gene ID file
    with open(gene_id_file, 'r') as gene_id_input:
        gene_ids = gene_id_input.read().splitlines()

    # Read GTF file and extract gene attributes
    with open(gtf_file, 'r') as gtf_input:
        for line in gtf_input:
            if line.startswith("#"):
                continue
            fields = line.strip().split('\t')
            if fields[2] == 'CDS' or fields[2] == 'gene':
                attributes = fields[8]
                gene_id = attributes.split('gene_id "')[1].split('";')[0]
                if gene_id in gene_ids:
                    transcript_id = attributes.split('transcript_id "')[1].split('";')[0]
                    ensemble_id = "-"
                    protein_id = "-"
                    ccds_id = "-"
                    if 'Ensembl:' in attributes:
                        ensemble_ids = attributes.split('Ensembl:')
                        for id in ensemble_ids[1:]:
                            ensemble_id = id.split('";')[0]
                            if gene_id not in gene_attributes:
                                gene_attributes[gene_id] = []
                            gene_attributes[gene_id].append([transcript_id, ensemble_id, protein_id, ccds_id])
                    if 'protein_id "' in attributes:
                        protein_ids = attributes.split('protein_id "')
                        for id in protein_ids[1:]:
                            protein_id = id.split('";')[0]
                            if gene_id not in gene_attributes:
                                gene_attributes[gene_id] = []
                            gene_attributes[gene_id].append([transcript_id, ensemble_id, protein_id, ccds_id])
                    if 'CCDS:' in attributes:
                        ccds_ids = attributes.split('CCDS:')
                        for id in ccds_ids[1:]:
                            ccds_id = id.split('";')[0]
                            if gene_id not in gene_attributes:
                                gene_attributes[gene_id] = []
                            gene_attributes[gene_id].append([transcript_id, ensemble_id, protein_id, ccds_id])

    # Write output file
    with open(output_file, 'w') as output:
        output.write("gene_id\ttranscript_id\tEnsemble\tProtein ID\tCCDS ID\n")
        for gene_id in gene_ids:
            if gene_id in gene_attributes:
                for attributes in gene_attributes[gene_id]:
                    output.write("{}\t{}\t{}\t{}\t{}\n".format(gene_id, *attributes))
            else:
                output.write("{}\t-\t-\t-\t-\n".format(gene_id))

    print("Extraction complete. Output file generated successfully.")

# Example usage
gtf_file = 'input.gtf'
gene_id_file = 'input_gene_ids.txt'
output_file = 'output_file.txt'

extract_gene_attributes(gtf_file, gene_id_file, output_file)
