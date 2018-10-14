import csv
if __name__ == '__main__':    
    
    
    from_csv = '/scratch/ql819/Tweets/data/output_2014-11.csv'
    to_csv = '/scratch/ql819/Tweets/data/small_2014-11.csv'

    fp = open(to_csv, "a") 
    wr = csv.writer(fp, dialect='excel')
    
    with open(from_csv) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[-1] == 'en':
                wr.writerow([row[0], row[7]])
                            
    fp.close()
