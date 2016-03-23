import subprocess as sub
filename = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.bm25.0.50.res"
judgement = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.qrels"
command = "~/TRECevalProject/TRECevalProject/TRECappProject/trec_eval -c " + judgement + " " + filename
print "\n"
print "command = " + command
p = sub.Popen([command],shell=True,stdout=sub.PIPE,stderr=sub.PIPE)
print p
output, errors = p.communicate()