/*
  C++ Wrapper for WIRE
 */

#include <cstdlib>
#include <string>
#include <map>
#include <fstream>
#include <assert.h>

using namespace std;

#include <WIRE-0.22/config.h>
#include "lib/xmlconf.h"
#if defined(SWIGPYTHON) || ! defined(SWIG_RUNTIME_VERSION)
#include "lib/xmlconf-main.h"
#endif
#include "utils.h"
#include "metaidx.h"
#include "urlidx.h"
#include "harvestidx.h"
#include "storage.h"
#include "linkidx.h"
#include "cleanup.h"
#include "sitelink.h"

namespace wire {

  class Doc {
  public:
    Doc() {
      doc = (doc_t *) malloc(sizeof(doc_t));
    };
    ~Doc() {
      free(doc);
    };
    doc_t* getdoc() { return doc; };
    unsigned long docid( unsigned long id ) {
      doc->docid = id;
      return (unsigned long) doc->docid;
    };
    unsigned long docid( void ) {
      return (unsigned long) doc->docid;
    };
    unsigned long siteid( unsigned long id ) {
      doc->siteid = id;
      return (unsigned long) doc->siteid;
    };
    unsigned long siteid( void ) {
      return (unsigned long) doc->siteid;
    };
    doc_status_t status() { return doc->status; };
    mime_type_t mime_type() { return doc->mime_type; };
    int http_status() { return doc->http_status; };
    unsigned int number_visits() { return doc->number_visits; };
    unsigned int number_visits_changed() { return doc->number_visits_changed; };
    int last_modified() { return doc->last_modified; };
    unsigned long raw_content_length() { return doc->raw_content_length; };
    unsigned long content_length() { return doc->content_length; };
    double pagerank() { return doc->pagerank; };
    int charset() { return doc->charset; };
  private:
    doc_t *doc;
  };

  class Index {
  public:
    Index(char *dir) {
      char* idxdir = (char *) malloc(sizeof(char) * strlen(dir) + 100);
      loadConfig();
      strcpy(idxdir, dir);
      strcat(idxdir, "/url/");
      urlidx = urlidx_open( idxdir, true );
      strcpy(idxdir, dir);
      strcat(idxdir, "/metadata/");
      metaidx = metaidx_open( idxdir, true );
      strcpy(idxdir, dir);
      strcat(idxdir, "/text/");
      storage = storage_open( idxdir, true );
      strcpy(idxdir, dir);
      strcat(idxdir, "/link/");
      linkidx = linkidx_open( idxdir, true );
      free(idxdir);
    };
    ~Index() {
      urlidx_close(urlidx);
      metaidx_close(metaidx);
      storage_close(storage);
      linkidx_close(linkidx);
    };
    static void loadConfig() {
      xmlconf_load();
    };
    char * retrieve_text_by_docid(unsigned long docid) {
      static char t[MAX_DOC_LEN];
      off_t size;
      storage_read( storage, docid, t, &size );
      return t;
    }
    unsigned long count_doc() {
      return (unsigned long) metaidx->count_doc;
    };
    unsigned long count_site() {
      return (unsigned long) metaidx->count_site;
    };
    unsigned long site_count() {
      return urlidx->site_count;
    };
    Doc* doc_retrieve( unsigned long id ) {
      Doc *d = new Doc();
      d->docid(id);
      metaidx_doc_retrieve( metaidx, d->getdoc() );
      d->docid(id);
      return d;
    }
    char * url_by_docid(unsigned long docid) {
      static char url[MAX_STR_LEN];
      urlidx_url_by_docid( urlidx, docid, url );
      return url;
    };
    char * sitename_by_siteid(unsigned long id) {
      site_t site;
      metaidx_status_t rc;
      site.siteid = id;
      rc = metaidx_site_retrieve( metaidx, &site );
      if ( rc == METAIDX_OK ) {
	static char sitename[MAX_STR_LEN];
	urlidx_site_by_siteid( urlidx, site.siteid, sitename );
	return sitename;
      } else {
	return NULL;
      }
    }
  private:
    urlidx_t *urlidx;
    metaidx_t *metaidx;
    storage_t *storage;
    linkidx_t *linkidx;
  };

  // the following classes is bad design, so it will be deprecated.
  class StorageText {
  public:
    StorageText() {
      buf = (char *) malloc(sizeof(char) * MAX_DOC_LEN);
      assert(buf != NULL);
      size = 0;
    };
    ~StorageText() {
      free(buf);
    }
    char* text() {
      return buf;
    }
    off_t *sizeptr() {
      return &size;
    };
    off_t getsize() {
      return size;
    }
  private:
    char* buf;
    off_t size;
  };
  class Storage {
  public:
    Storage(char* dir) {
      char* textdir = (char *) malloc(sizeof(char) * strlen(dir) + 50);
      strcpy(textdir, dir);
      strcat(textdir, "/text");
      storage = storage_open( textdir, true );
      free(textdir);
    };
    ~Storage() {
      storage_close( storage );
    };
    /*
    StorageText* fetch_byid(unsigned long docid) {
      StorageText *t = new StorageText();
      assert(t != NULL);
      storage_read( storage, docid, t->text(), t->sizeptr() );
      return t;
    };
    */
    char* fetch_byid(unsigned long docid) {
      //      char *t = (char *) malloc(sizeof(char) * MAX_DOC_LEN);
      static char t[MAX_DOC_LEN];
      off_t size;
      //      assert(t != NULL);
      storage_read( storage, docid, t, &size );
      return t;
    }
  private:
    storage_t *storage;
  };
  class MetaIndex {
  public:
    MetaIndex(char* dir) {
      char* metadir = (char *) malloc(sizeof(char) * strlen(dir) + 50);
      strcpy(metadir, dir);
      strcat(metadir, "/metadata/");
      metaidx = metaidx_open( metadir, true );
      free(metadir);
    };
    ~MetaIndex() {
      metaidx_close( metaidx );
    }
    static void loadConfig() {
      xmlconf_load();
    };
    const char* dirname() {
      return metaidx->dirname;
    }
    unsigned long count_doc() {
      return (unsigned long) metaidx->count_doc;
    };
    unsigned long count_site() {
      return (unsigned long) metaidx->count_site;
    };
    bool readonly() {
      return metaidx->readonly;
    }
    Doc* doc_retrieve( unsigned long id ) {
      Doc *d = new Doc();
      d->docid(id);
      metaidx_doc_retrieve( metaidx, d->getdoc() );
      d->docid(id);
      return d;
    }
  private:
    metaidx_t *metaidx;
  };

  class UrlIndex {
  public:
    UrlIndex(char* dir) {
      char* urldir = (char *) malloc(sizeof(char) * strlen(dir) + 50);
      strcpy(urldir, dir);
      strcat(urldir, "/url/");
      urlidx = urlidx_open( urldir, true );
      free(urldir);
    };
    ~UrlIndex() {
      urlidx_close( urlidx );
    };
    char * url_by_docid(unsigned long docid) {
      static char url[MAX_STR_LEN];
      urlidx_url_by_docid( urlidx, docid, url );
      return url;
    };
  private:
    urlidx_t *urlidx;
  };
};

#if defined(SWIGPYTHON) || ! defined(SWIG_RUNTIME_VERSION)
void cleanup()
{
}
#endif
