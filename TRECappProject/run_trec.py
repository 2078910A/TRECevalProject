import os
os.popen(cd)
filename = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.bm25.0.50.res"
judgement = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.qrels"
command = "~/TRECevalProject/TRECevalProject/TRECappProject/trec_eval.8.1/trec_eval -c " + judgement + " " + filename
retvalue = os.popen(command).readlines()
print retvalue
