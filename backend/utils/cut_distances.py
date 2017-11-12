import sys
from utils import file_lines
from tqdm import tqdm


filename = sys.argv[1]
cut = float(sys.argv[2])
fin = open(filename)
fout = open(filename+'.cut', 'w')
with tqdm(total=file_lines(filename)) as pbar:
    for l in fin:
        word, card, score = l[:-1].split(' ')
        if float(score) < cut:
            fout.write(l)
        pbar.update()
fin.close()
fout.close()
