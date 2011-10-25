import wire
import datetime

import sys
import os
import subprocess
import index 

def start_crawl(conf, seeds_file):
    crawler = wire.Crawler(conf)
    crawler.reset()
    crawler.import_seeds(seeds_file)
  
def crawl(conf, count_steps):
    crawler = wire.Crawler(conf)
    try:
	crawler.steps(count_steps)
    except subprocess.CalledProcessError:
	crawler.rollback_step()

def export_seeds(conf, seeds_file):
    crawler = wire.Crawler(conf)
    crawler.export_seeds(seeds_file)
    
def build_index(conf, collection_path, indexdir, indexname, language, max_docs=-1):
    index.index_collection(conf, collection_path, indexdir, indexname, language=language, max_docs=max_docs)
    
if __name__ == "main":
    import argparse
    
    parser = argparse.ArgumentParser(description='Deckard Manager Script.')

    choices = ['crawl', 'start', 'export-seeds', 'build-index']

    parser.add_argument('--action', 
      type=str, choices=choices, required=True,
      help='action to perform')

    parser.add_argument('--steps', 
      type=int, default=1, const=1, nargs='?',
      help='number of crawling iterations')
      
    parser.add_argument('--seeds',
      type=str, default='',
      help='seeds file for importing/exporting (depends on action)'
    )

    parser.add_argument('--indexdir',
      type=str, default='',
      help='directory for storing the index'
    )
      
    parser.add_argument('--indexname',
      type=str, default='main',
      help='name for the stored index'
    )
    
    parser.add_argument('--wireconf',
      type=str, required=True,
      help='path to wire config file'
    )
      
    args = parser.parse_args()
    print args
    
    conf = os.path.abspath(args.wireconf)

    if args.action == 'start':
	if args.seeds:
	    start_crawl(conf, os.path.abspath(args.seeds))
	    sys.exit(0)
	else:
	    print 'invalid seeds file'
	    sys.exit(1)
	
    if args.action == 'crawl':
	if args.steps > 0:
	    crawl(conf, args.steps)
	    sys.exit(0)
	else:
	    print 'invalid steps'
	    sys.exit(1)

    if args.action == 'export-seeds':
	if args.seeds:
	    export_seeds(conf, os.path.abspath(args.seeds))
	    sys.exit(0)
	else:
	    print 'invalid seeds file'
	    sys.exit(1)
	    
    if args.action == 'build-index':
	if args.indexdir:
	    build_index(conf, collection_path, os.path.abspath(args.indexdir), args.indexname, language='Spanish')
	    sys.exit(0)
	else:
	    sys.exit(1)