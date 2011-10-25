# -*- coding: utf-8 -*-
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

import whoosh.index
from whoosh.qparser import QueryParser

def search(indexdir, indexname, query_str):
    whoosh_idx = whoosh.index.open_dir(indexdir, indexname=indexname)

    with whoosh_idx.searcher() as s:
	qp = QueryParser("content", schema=whoosh_idx.schema)
	q = qp.parse(unicode(query_str))

	results = s.search(q, terms=True)
	# Allow larger fragments
	results.formatter.maxchars = 350

	# Show more context before and after
	results.formatter.surround = 70
	
	for r in results:
	    print r['title']
	    print r.highlights("content", top=3)
	    print r['url']
	    print ''
    
	return results

if __name__ == "__main__":
    import sys
    import os
    import argparse
    parser = argparse.ArgumentParser(description='Deckard Search Script.')

    parser.add_argument('--indexdir',
      type=str, default='', required=True,
      help='directory for storing the index'
    )
      
    parser.add_argument('--indexname',
      type=str, default='main',
      help='name for the stored index'
    )

    parser.add_argument('--query',
      type=str, default='', required=True,
      help='your query'
    )

    #TODO: from and to results, number of results, paging, etc

    args = parser.parse_args()
    print args

    search(os.path.abspath(args.indexdir), args.indexname, args.query)
