import commands
filename = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.bm25.0.50.res"
judgement = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.qrels"
command = "~/TRECevalProject/TRECevalProject/TRECappProject/trec_eval -c " + judgement + " " + filename
print command
retvalue = commands.getoutput(command)
print retvalue
