#Usage: python iPCRess.py urine_SRX2805362.txt urine.csv urine.fasta

import re
import pandas as pd
import sys

input = sys.argv[1]
#print(input)
output_csv = sys.argv[2]
#print(output_csv)
output_fasta = sys.argv[3]

#List of necessary regex expressions
regex_dict={
    'sequence': re.compile(r'(?P<sequence>\A>{1}.*[0-9]$|\A[ACTG]+$)'),
    'strain': re.compile(r'Target: (?P<strain>.*$)'),           #(?P<name>) captures the text matched by the regex under the group 'name' - basically a backreference
    'matches':re.compile(r'Matches: (?P<matches>.*$)'),  #match everything up until bp  https://stackoverflow.com/questions/7124778/how-to-match-anything-up-until-this-sequence-of-characters-in-a-regular-expres
    'misc': re.compile(r'ipcress: (?P<misc>.*$)')
}


#function to check each reg expression
def _parse_line(line):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    """
    for key, rx in regex_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None

def main():
    data=[]
    fasta=[]
    with open(input, 'r') as file:
        line = file.readline()
        #print(line)
        if line.strip('\n ') == ('-- completed ipcress analysis'):
            print ('No PCR products found for {sample}!' .format(sample=input))
            with open(output_csv, 'w') as a, open(output_fasta, 'w') as b:
                pass
            file.close()            
        else:
            while line:
                line = line.strip()   #strip leading and trailing whitespaces and tabs
                #print(line)
                # at each line check for a match with a regex
                key, match = _parse_line(line)

                # extract strain
                if key == 'strain':
                    strain = match.group('strain')

                # extract matches for F and R
                elif key == 'matches':
                    matches = match.group('matches')

                # extract gene, length start/stop, direction
                elif key == 'misc':
                    misc = match.group('misc')
                    gene = misc.split()[1]
                    size = misc.split()[2]
                    start = misc.split()[4]
                    stop = misc.split()[7]
                    direction = misc.split()[9]

                    row = {                                    # create a dictionary containing row of data
                            'Gene': gene,
                            'Strain': strain,
                            'Size in bp': size,
                            'Direction': direction,
                            'Primer matches': matches,
                            'Start position': start,
                            'Stop position': stop,
                    }

                    #print(row)
                    data.append(row)     # append the row to the data list

                #extract fasta
                elif key =='sequence':
                    sequence = match.group('sequence')
                    #print(sequence)
                    fasta.append(sequence + '\n')

                line = file.readline()

            #print(data)    # create a pandas DataFrame from the list of dicts
            data=pd.DataFrame(data)   #is there a way to keep order of dicts, when converting list of dicts to dataframe
            #print(data)
            data=data.sort_values('Gene')
            col_order = ['Gene', 'Strain','Size in bp','Direction', 'Start position', 'Stop position', "Primer matches"]  #order columns correctly
            data = data[col_order]
            #print(data)
            data.to_csv(output_csv)

            fasta_file=open(output_fasta,'w')
            fasta_file.writelines(fasta)
            fasta_file.close()



if __name__ == '__main__':
    main()


