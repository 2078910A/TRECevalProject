import subprocess
map = "nothing"
p10 = "nothing"
p20 = "nothing"
filename = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.bm25.0.50.res"
judgement = "~/TRECevalProject/TRECevalProject/TRECappProject/data/news/ap.trec.qrels"
command = "~/TRECevalProject/TRECevalProject/TRECappProject/trec_eval.8.1/trec_eval -c " + judgement + " " + filename
print "command = " + command + "\n"
output = subprocess.check_output([command],shell=True)
outputList = output.split('\n')
for lines in outputList:
	if "map" in lines:
		line = lines.split("\t")
		map = float(line[2])
	if "P10" in lines:
		line = lines.split("\t")
		if line[0] == "P10":
			p10 = float(line[2])
	if "P20" in lines:
		line = lines.split("\t")
		if line[0] == "P20":
			p20 = float(line[2])
print type(output) 
print "\n"
print output
print map
print "\t"
print p10
print "\t"
print p20
