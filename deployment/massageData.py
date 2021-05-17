def getInfo(song, SongList):
    for row in SongList:
        if song == row[0]:
            print(row[2:])
            return row[2:]
    # fromt he billboard 

def makeTestPoint():
    # fill in the blank not on billboard hits 
    return 0
