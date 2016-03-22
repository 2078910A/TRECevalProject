import os
filename = "~/home/tierney12/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.bm25.0.50.res"
judgement = "~/home/tierney12/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.qrels"
command = "~/home/tierney12/TRECevalProject/TRECevalProject/TRECappProject/trec_eval.8.1/trec_eval -c " + judgement + " " + filename
retvalue = os.popen(command).readlines()
print retvalue
