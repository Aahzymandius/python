def proteins(strand):
    protein=[]
    links={
          "AUG":"Methionine",
          "UUU":"Phenylalanine", "UUC":"Phenylalanine",
          "UUA":"Leucine", "UUG":"Leucine",
          "UCU":"Serine", "UCC":"Serine", "UCA":"Serine", "UCG":"Serine",
          "UAU":"Tyrosine", "UAC":"Tyrosine",
          "UGU":"Cysteine", "UGC":"Cysteine",
          "UGG":"Tryptophan"
          }
    for i in range(len(strand)):
      codon = str(strand[(i*3):(i*3)+3])
      if codon == "UAA" or codon == "UAG" or codon == "UGA":
        return protein
      x = links[codon]
      protein.append(x)
    return protein
