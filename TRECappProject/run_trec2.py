import subprocess as sub
filename = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.bm25.0.50.res"
judgement = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.qrels"
command = "~/TRECevalProject/TRECevalProject/TRECappProject/trec_eval.8.1/trec_eval -c " + judgement + " " + filename
print "\n"
print "command = " + command
output = subprocess.check_output([command],shell=True)
print output
