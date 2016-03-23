import commands
retvalue = commands.getoutput("cd ~/TRECevalProject/TRECevalProject/TRECappProject/trec_eval.8.1/")
print retvalue
retvalue = commands.getoutput("make")
print retvalue
filename = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.bm25.0.50.res"
judgement = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.qrels"
command = "./trec_eval -c " + judgement + " " + filename
print command
retvalue = commands.getoutput(command)
print retvalue
