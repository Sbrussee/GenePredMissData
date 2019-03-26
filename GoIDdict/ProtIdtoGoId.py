import json

def checker(newlist):
    dictionaryforwrite = dict()
    writeout = open('UniprotKBandGoID.txt','w+')
    with open('goa_rat.gaf','r') as q:
         for line in q:
             if line[0] != '!':
                 compareline = line.strip().split('\t')
                 strs = list(filter(None, compareline))
                 for xs in newlist:
                     if xs == strs[1]:
                         if 'GO:' in strs[3]:
                             if xs in dictionaryforwrite:
                                 dictionaryforwrite[xs].append(strs[3])
                             else:
                                 dictionaryforwrite[xs] = [strs[3]]                           
                         elif 'GO:' in strs[4]:
                             if xs in dictionaryforwrite:
                                 dictionaryforwrite[xs].append(strs[4])
                             else:
                                 dictionaryforwrite[xs] = [strs[4]]
    writeout.write(json.dumps(dictionaryforwrite))
    writeout.close()


def main():
     openit = open('Refseqtouniprotkb.txt','r')
     files = openit.readlines()
     test = [x.strip().split(" ") for x in files]
     newlist = []
     for value in test:
         newlist.append(value[1])
     checker(newlist)    
main()
