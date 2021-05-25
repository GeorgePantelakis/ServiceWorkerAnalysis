import os
import sys
import tarfile

                                
def process_results(source_dir):
        dest_dir = './processed_results/'
        count = 0

        if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
        
        listOfDirs = [x[0] for x in os.walk(source_dir)]
        for directory in listOfDirs:
                if directory == source_dir:
                        continue
                dirComponments = directory.split('/')
                id = dirComponments[len(dirComponments) - 1].split('_')[1]
                try:
                        t = tarfile.open(directory + '/logs.tar','r')
                        log_name = 'logs/'+id+'_sw.log'   
                        if log_name in t.getnames():
                                log_file = t.extractfile(log_name)
                                data = log_file.read()
                                if (data.find('Service Worker') > -1):
                                        if(data.count("registered") > 1):
                                                print(directory)
                                        count += 1
                                        Lines = data.splitlines()
                                        linesOfInterest = [x for x in Lines if x.find('Request URL') > -1]
                                        visitedURLs = [x.split(' ')[3] for x in linesOfInterest]
                                        outfp = open(dest_dir + id + '_sw.txt', "w")
                                        for URL in visitedURLs:
                                                domain = URL.split('/')[2]
                                                outfp.write(domain + '\n')
                                        outfp.close()

                except Exception as e:
                        print(id + ': ' + str(e))
        print(count)


if __name__ == '__main__':
        process_results(sys.argv[1])
               

