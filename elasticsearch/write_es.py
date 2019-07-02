import json, os, time
from tqdm import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan, bulk, parallel_bulk

def action_generator(file_list):
    """
    Builds an elasticsearch action generator, so no need to load all actions in memory.
    -Args:
        @file_list: a list of all json files (in absolute path) to be written in elasticsearch instance
    -Return:
        None
    """
    for f in tqdm(file_list):
        id=0
        for line in open(f,'r'): # writes an records into elasticsearch instance
            yield {
                '_op_type': 'create',
                '_index': idx_name,
                '_type': doc_type,
                '_id': f+'_line_'+str(id),
                '_body': json.loads(line)
            }
            id += 1

def get_f_list(year):
    """
    Get the list of all stripped json files in one year's database
    -Args:
        @ year: a string that is either '2014' or '2015'
    -Return:
        A dictionary in format {file name: absolute path}
    """
    f_abs = []
    f_abb = []
    yr_path = os.path.join('/scratch/xz2448/es_twitter', year)
    dir_list = [os.path.join(yr_path, d) for d in os.listdir(yr_path)]
    for d in dir_list:
            f_abs += [os.path.join(d, f) for f in list(filter(lambda x: x[-4:] == 'json', os.listdir(d)))]
            f_abb += list(filter(lambda x: x[-4:] == 'json', os.listdir(d)))
    return dict(zip(f_abb, f_abs))

def main()
    idx_name = 'twitter1415'
    doc_type = 'tweets'
    es = Elasticsearch() # create an elasticsearch instance
    print(es.info()) # check whether elasticsearch is working

    # Create an elasticsearch index (NOTE: ONLY NEED TO CREATE THE INDEX DURING THE FIRST TIME RUNNING THE SCRIPT)
    # To delete an index, run: es.indices.delete(idx_name) (WARNING: NO WAY TO RESTORE AN INDEX ONCE DELETE)
    es.indices.create(index=idx_name, body={
        'settings' : {
            'index' : {
                    'number_of_shards':12
                }
            }
    })

    # Get a list of all stripped json files in 2014 and 2015 database
    f_dict = {}
    for year in ['2014', '2015']:
        f_dict.update(get_f_list(year))

    f_togo = list(f_dict.keys())
    f_list = [f_dict.get(f) for f in f_togo]

    # Write json objects into elasticsearch instance as bulk (NOTE: while setting thread_count and chunk_size high can 
    # faster the process, too high values will overwhelm the elasticsearch server and cause connection error.)
    for _ in parallel_bulk(es, action_generator(f_list), thread_count = 5, chunk_size=5000):
        pass

if __name__ == "__main__":
    main()
