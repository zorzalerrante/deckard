/* 
   imported from WIRE 0.11
 */

#ifdef SWIG

// metaidx.h
enum metaidx_status_t {
        METAIDX_OK         = 0,
        METAIDX_ERROR,
        METAIDX_EOF
};

enum doc_status_t {
        STATUS_DOC_ALL                  = 0,
        STATUS_DOC_NEW                  = 1,
        STATUS_DOC_ASSIGNED             = 2,
        STATUS_DOC_GATHERED             = 3,
        STATUS_DOC_INDEXED              = 4,
        STATUS_DOC_EXCLUSION    = 5,
        STATUS_DOC_IGNORED              = 99  // Must be ignored
};

enum site_status_t {
        STATUS_SITE_NEW                 = 10,
        STATUS_SITE_VISITED             = 11
};

enum mime_type_t {
        MIME_UNKNOWN                    = 0,
        MIME_REDIRECT                   = 1,
        MIME_ROBOTS_TXT                 = 2,
        MIME_ROBOTS_RDF                 = 3,
        MIME_TEXT_HTML                  = 10,
        MIME_TEXT_PLAIN                 = 11,
        MIME_APPLICATION_FLASH  = 12,
        MIME_APPLICATION                = 13,
        MIME_AUDIO                              = 14,
        MIME_IMAGE                              = 15,
        MIME_VIDEO                              = 16,
        MIME_TEXT_WAP                   = 17,
        MIME_TEXT_RTF                   = 18,
        MIME_TEXT_XML                   = 19,
        MIME_TEXT_TEX                   = 20,
        MIME_TEXT_CHDR                  = 21
};

// storage.h
enum storage_status_t {
        STORAGE_OK                      = 0,
        STORAGE_NOT_FOUND       = 1,
        STORAGE_DUPLICATE       = 2,
        STORAGE_UNCHANGED
};

#endif
