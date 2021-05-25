import os
import multiprocessing as mp
import sys

from docker_config import *
from docker_monitor import *

export_path = './results/container_'

processes = []

def export_log_custom(id):
	container = client.containers.get('container_'+str(id))
	logging.info(get_time() + 'container_'+id+' exporting files!!')
	dir_path = './results/container_'+id+'/'
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	with open(dir_path+'logs.tar', 'w') as f:
		bits, stat = container.get_archive('/home/pptruser/logs/')
		for chunk in bits:
	    		f.write(chunk)
	log_tar_dir = 'results/container_'+id+'/logs.tar'
	t = tarfile.open(log_tar_dir,'r')
	log_name = 'logs/'+id+'_sw.log'
	res=-99
	err=-1
	if log_name in t.getnames():
		f = t.extractfile(log_name)
		data = f.read()
		res = data.find('Page Load Complete')
		err = data.find('Chromium Crashed')
	if err>-1:
		return -99
	stop_container(id)
	return res

def run_single_container(URL, id):
    initiate_container(URL, str(id), 'capture_notifications.js','0', TIMEOUT )
    stop_container(str(id))
    export_log_custom(str(id))
    time.sleep(WAIT_TIMEOUT)
    remove_container(str(id))

def run_containers(URL_list):
	for URL in URL_list:
		id = URL.split('/')[2]
		print('Runing container with id: ' + id + '...')
		run_single_container(URL, id)
		print('finished container with id: ' + id)

def read_file(filename):
	with open(filename) as fp:
		sites_unfiltered = fp.read().splitlines()
	sites = ['http://www.' + site.split(',')[0] for site in sites_unfiltered]
	return sites

def split_list(listToBeSplited):
	results = []
	for i in range(CRAWL_MAX_CONTAINERS):
		temp = []
		j = i
		while j < len(listToBeSplited):
			temp.append(listToBeSplited[j])
			j += CRAWL_MAX_CONTAINERS
		results.append(temp)
	return results

def main():
	#remove_containers()
	lists = split_list(read_file(sys.argv[1]))

	print('Lists have been splitted...')

	for i in range(CRAWL_MAX_CONTAINERS):
		process = mp.Process(target=run_containers, args=(lists[i],))
		processes.append(process)
		process.start()

	for process in processes:
		process.join()	

if __name__== "__main__":
    	main()
