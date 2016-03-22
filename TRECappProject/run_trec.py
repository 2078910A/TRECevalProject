import os
os.popen("cd ~/TRECevalProject/TRECevalProject/TRECappProject/trec_eval.8.1/")
os.popen("make")
filename = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.bm25.0.50.res"
judgement = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.qrels"
command = "./trec_eval -c " + judgement + " " + filename
retvalue = os.popen(command).readlines()
print retvalue
