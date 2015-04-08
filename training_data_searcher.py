#!/user/bin/python
import sys, re

class Sentence(object):
    def __init__(self, lines):
        self.fulltext = "\n".join(lines)
        self.words = map(Word, lines)

    def __str__(self):
        return " ".join(map(str, self.words))

    def matches(self, string):
        words = string.split(" ")
        for si in range(len(self.words)-len(words)):
            match = True
            for (i, word) in enumerate(words):
                if not self.words[si+i].matches(word):
                    match = False
                    break
            if match:
                return True
        return False


class Word(object):
    all_pos = set(["CC","CD","DT","EX","FW","IN","JJ","JJR","JJS","LS","MD","NN","NNS","NNP","NNPS",
            "PDT","POS","PRP","PRP$","RB","RBR","RBS","RP","SYM","TO","UH","VB","VBD","VBG","VBN",
            "VBP","VBZ","WDT","WP","WP$","WRB","PUNCT"])

    all_upos = set(["ADJ","ADV","INTJ","NOUN","PROPN","VERB","ADP","AUX","CONJ","DET","NUM","PART",
            "PRON","SCONJ","PUNCT","SYM","X"])

    all_rel = set(["nsubj","nsubjpass","dobj","iobj","csubj","csubjpass","ccomp","xcomp","nummod",
            "appos","nmod","nmod:npmod","nmod:tmod","nmod:poss","acl","acl:relcl","amod","det",
            "det:predet","neg","case","advcl","advmod","compound","compound:prt","name",
            "mwe","foreign","goeswith","list","dislocated","parataxis","remnant","reparandum",
            "vocative","discourse","expl","aux","auxpass","cop","mark","punct","conj","cc","root",
            "cc:preconj","dep"])

    def __init__(self, line):
        items = line.split("\t")
        self.word = items[1]
        self.pos = items[3]
        self.rel = items[7]

    def __str__(self):
        return self.word

    def matches(self, string):
        if string.isupper() and string != "I":
            return string == self.pos
        if string == self.rel:
            return True
        restring = "^" + string + "$"
        return re.match(restring, self.word, re.I)


def lines_to_sentences(lines):
    sentences = []
    current_sentence = []
    for line in map(lambda line: line.strip(), lines):
        if not line:
            if len(current_sentence) > 0:
                sentences.append(Sentence(current_sentence))
                current_sentence = []
            continue
        if line[0] != '#':
            current_sentence.append(line)
    return sentences


if __name__ == "__main__" and len(sys.argv) > 1:
    phrase = sys.argv[1].strip("\"")
    if len(sys.argv) > 2 and sys.argv[2].startswith("--corpus="):
        corpus = sys.argv[2].split("=")[1]
    else:
        corpus = "English.train.conllu"
    f = open(corpus, "r")
    lines = f.read().split("\n")
    sentences = lines_to_sentences(lines)
    matches = filter(lambda s: s.matches(phrase), sentences)
    if matches:
        print len(matches), "matching sentences:\n"
        for s in matches:
            print s
            print s.fulltext + "\n"

    else:
        print "no matches found"
