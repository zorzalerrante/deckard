# -*- coding: utf-8 -*-
import os
import sys
import regex as re
import subprocess

import Wire
import justext
import lxml
from BeautifulSoup import BeautifulSoup

import htmlentitydefs
import datetime

## http://effbot.org/zone/re-sub.htm#unescape-html
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

## generator to iterate over the documents of a wire index
class Collection( Wire.Index ):
    def __init__( self, index_dir, stopwords ):
	Wire.Index.__init__( self, index_dir )
	self.stopwords = stopwords
	
    def documents( self, doc_id_start = 1, max_doc_id = None ):
	if max_doc_id == None:
	    max_doc_idx = self.count_doc()
	    
	for i in range( doc_id_start, max_doc_idx ):
	    doc = self.doc_retrieve( i )
	    if not doc.mime_type() == Wire.MIME_TEXT_HTML:
		continue
	  
	    text = self.retrieve_text_by_docid(i)
	    try:
		paragraphs = justext.justext(text, self.stopwords)
	    except lxml.etree.XMLSyntaxError:
		#print idx.url_by_docid(i), "bad html"
		continue
	    except lxml.etree.ParserError:
		#print idx.url_by_docid(i), "bad html"
		continue
	    except TypeError:
		#print idx.url_by_docid(i), "caused error"
		continue
	    
	    good_text = filter( lambda x: x['class'] == 'good', paragraphs )
	    if not good_text:
		continue
	    content = [ unescape(p['text']) for p in good_text ]
	    
	    soup = BeautifulSoup( text )
	    title_node = soup.find('title')

	    if title_node:
		title = unescape( title_node.getText().rstrip().lstrip() )
	    if not title_node:
		title = ''
		
	    meta_nodes = soup.findAll('meta')
	    description = ''
	    
	    for m in meta_nodes:
		try:
		    if m['name'] == 'description' and m['content']:
			description = m['content']
			break
		except KeyError:
		    continue
	    #print meta_nodes
	    '''
	    if meta_nodes:
		description = meta_nodes[0]['content']
	    else:
		description = ''
	    '''
	    #description = ''
	    
	    url = self.url_by_docid(i).decode('ascii', 'ignore')
	    site = url.split('/')[0]
	    
	    doc_data = { 'title': unicode(title), 'url': unicode(url), 'site': site, 'content': content, 'description': description }
	    yield doc_data
	    
def load_config( wire_conf ):
    os.environ['WIRE_CONF'] = wire_conf
    Wire.MetaIndex.loadConfig()

#la clase que nos permite ejecutar el crawler

class Crawler:
    # wire_conf => full path to wire config file
    # wire_path => full path to wire folder, the one that contains bot and info folder
    def __init__(self, wire_conf, wire_path=None):
	self.conf_path = wire_conf
	os.environ['WIRE_CONF'] = wire_conf
	
	if wire_path:
	    os.environ['PATH'] = os.environ['PATH'] + ":" + wire_path + "/bot" + ":" + wire_path + "/info"
      
    def import_seeds(self, filename):
	subprocess.check_call("wire-bot-seeder --start {0}".format(filename), shell=True, stdout=sys.stdout, stderr=sys.stderr)
            
    def export_seeds(self, filename):
	with open(filename, 'w') as seeds_file:
	    subprocess.check_call("wire-info-extract --seeds {0}".format(filename), shell=True, stdout=seeds_file)
   
    def calc_stats(self, analyze_links=False):
	options = ["--doc-statistics", "--site-statistics"]
	if analyze_links:
	    options.append("--link-analysis")
	subprocess.check_call("wire-info-analysis --seeds {0}".format(filename), shell=True, stdout=sys.stdout, stderr=sys.stderr)
	
    def run_command(self, name):
	now = datetime.datetime.now()
	print now.strftime("[%Y/%m/%d %H:%M]"), 'Running', name.title()
	subprocess.check_call("wire-bot-{0}".format(name), shell=True, stdout=sys.stdout, stderr=sys.stderr)
            
    def steps(self, count=1):
	for i in xrange(0, count):
	    self.run_command('manager')
	    self.run_command('harvester')
	    self.run_command('gatherer')
	    self.run_command('seeder')
	
    def reset(self):
	subprocess.check_call("wire-bot-reset", shell=True, stdout=sys.stdout, stderr=sys.stderr)
	
    def rollback_step(self):
	subprocess.check_call("wire-bot-manager --cancel", shell=True, stdout=sys.stdout, stderr=sys.stderr)
      
