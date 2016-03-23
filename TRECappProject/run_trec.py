import os
retvalue = os.system("cd ~/TRECevalProject/TRECevalProject/TRECappProject/trec_eval.8.1/")
print retvalue
retvalue = os.system("make")
print retvalue
filename = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.bm25.0.50.res"
judgement = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.qrels"
command = "./trec_eval -c " + judgement + " " + filename
print command
retvalue = os.system(command).readlines()
print retvalue
