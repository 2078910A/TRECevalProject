import subprocess as sub
filename = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.bm25.0.50.res"
judgement = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.qrels"
command = "~/TRECevalProject/TRECevalProject/TRECappProject/trec_eval -c " + judgement + " " + filename
p = sub.Popen(['./trec_eval.8.1/trec_eval -c ' + judgement + " " + filename],stdout=sub.PIPE,stderr=sub.PIPE)
output, errors = p.communicate()