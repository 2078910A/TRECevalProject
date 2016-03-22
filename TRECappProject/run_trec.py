import os
filename = "data/news/ap.trec.bm.25.0.50.res"
judgement = "data/news/ap.trec.qrels"
command = "trec_eval -c " + judgement + " " + command
retvalue = os.popen(command).readlines()
print retvalue
