




def GetScores():
# GET HIGHSCORES
    HighScores = []
    with open('f1.txt') as f:

    	for line in f:
    		
        	data = line.split()
        	if line:

        		line = [i for i in line]
        		line = ''.join(line)
        		#print line
        		HighScores.append(line)
    for x in range(len(HighScores)):
    	HighScores[x] = int(HighScores[x])

    HighScores.sort()
    HighScores.reverse()
    return HighScores

def PrintScores():
	pass

Scores = GetScores()
print Scores




