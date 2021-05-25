import os
import tarfile

                                
def extract_csv_file():
        source_dir = './processed_results/'
        outputFile = open('sitesWithSw.csv', 'w')
        count = 0
        
        listOfFiles = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

        for SWfile in listOfFiles:
                if SWfile == source_dir:
                        continue
                outputFile.write(SWfile.split('/')[-1].split('_')[0] + '\n')
                count += 1

        outputFile.close()
        print(count)


if __name__ == '__main__':
        extract_csv_file()
               

