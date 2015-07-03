# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import absolute_import, division, print_function

INCLUDES = """
#include <openssl/x509v3.h>

/*
 * This is part of a work-around for the difficulty cffi has in dealing with
 * `LHASH_OF(foo)` as the name of a type.  We invent a new, simpler name that
 * will be an alias for this type and use the alias throughout.  This works
 * together with another opaque typedef for the same name in the TYPES section.
 * Note that the result is an opaque type.
 */
#if OPENSSL_VERSION_NUMBER >= 0x10000000
typedef LHASH_OF(CONF_VALUE) Cryptography_LHASH_OF_CONF_VALUE;
#else
typedef LHASH Cryptography_LHASH_OF_CONF_VALUE;
#endif
typedef STACK_OF(ACCESS_DESCRIPTION) Cryptography_STACK_OF_ACCESS_DESCRIPTION;
typedef STACK_OF(DIST_POINT) Cryptography_STACK_OF_DIST_POINT;
typedef STACK_OF(POLICYQUALINFO) Cryptography_STACK_OF_POLICYQUALINFO;
typedef STACK_OF(POLICYINFO) Cryptography_STACK_OF_POLICYINFO;
typedef STACK_OF(ASN1_INTEGER) Cryptography_STACK_OF_ASN1_INTEGER;
typedef STACK_OF(GENERAL_SUBTREE) Cryptography_STACK_OF_GENERAL_SUBTREE;
"""

TYPES = """
typedef ... Cryptography_STACK_OF_ACCESS_DESCRIPTION;
typedef ... Cryptography_STACK_OF_POLICYQUALINFO;
typedef ... Cryptography_STACK_OF_POLICYINFO;
typedef ... Cryptography_STACK_OF_ASN1_INTEGER;
typedef ... Cryptography_STACK_OF_GENERAL_SUBTREE;

typedef struct {
    X509 *issuer_cert;
    X509 *subject_cert;
    ...;
} X509V3_CTX;

typedef void * (*X509V3_EXT_D2I)(void *, const unsigned char **, long);

typedef struct {
    ASN1_ITEM_EXP *it;
    X509V3_EXT_D2I d2i;
    ...;
} X509V3_EXT_METHOD;

static const int GEN_OTHERNAME;
static const int GEN_EMAIL;
static const int GEN_X400;
static const int GEN_DNS;
static const int GEN_URI;
static const int GEN_DIRNAME;
static const int GEN_EDIPARTY;
static const int GEN_IPADD;
static const int GEN_RID;

typedef struct {
    ...;
} OTHERNAME;

typedef struct {
    ...;
} EDIPARTYNAME;

typedef struct {
    int ca;
    ASN1_INTEGER *pathlen;
} BASIC_CONSTRAINTS;

typedef struct {
    Cryptography_STACK_OF_GENERAL_SUBTREE *permittedSubtrees;
    Cryptography_STACK_OF_GENERAL_SUBTREE *excludedSubtrees;
} NAME_CONSTRAINTS;


typedef struct {
    int type;
    union {
        char *ptr;
        OTHERNAME *otherName;  /* otherName */
        ASN1_IA5STRING *rfc822Name;
        ASN1_IA5STRING *dNSName;
        ASN1_TYPE *x400Address;
        X509_NAME *directoryName;
        EDIPARTYNAME *ediPartyName;
        ASN1_IA5STRING *uniformResourceIdentifier;
        ASN1_OCTET_STRING *iPAddress;
        ASN1_OBJECT *registeredID;

        /* Old names */
        ASN1_OCTET_STRING *ip; /* iPAddress */
        X509_NAME *dirn;       /* dirn */
        ASN1_IA5STRING *ia5;   /* rfc822Name, dNSName, */
                               /*   uniformResourceIdentifier */
        ASN1_OBJECT *rid;      /* registeredID */
        ASN1_TYPE *other;      /* x400Address */
    } d;
    ...;
} GENERAL_NAME;

typedef struct {
    GENERAL_NAME *base;
    ASN1_INTEGER *minimum;
    ASN1_INTEGER *maximum;
} GENERAL_SUBTREE;

typedef struct stack_st_GENERAL_NAME GENERAL_NAMES;

typedef struct {
    ASN1_OCTET_STRING *keyid;
    GENERAL_NAMES *issuer;
    ASN1_INTEGER *serial;
} AUTHORITY_KEYID;

typedef struct {
    ASN1_OBJECT *method;
    GENERAL_NAME *location;
} ACCESS_DESCRIPTION;

typedef ... Cryptography_LHASH_OF_CONF_VALUE;


typedef ... Cryptography_STACK_OF_DIST_POINT;

typedef struct {
    int type;
    union {
        GENERAL_NAMES *fullname;
        Cryptography_STACK_OF_X509_NAME_ENTRY *relativename;
    } name;
    ...;
} DIST_POINT_NAME;

typedef struct {
    DIST_POINT_NAME *distpoint;
    ASN1_BIT_STRING *reasons;
    GENERAL_NAMES *CRLissuer;
    ...;
} DIST_POINT;

typedef struct {
    ASN1_STRING *organization;
    Cryptography_STACK_OF_ASN1_INTEGER *noticenos;
} NOTICEREF;

typedef struct {
    NOTICEREF *noticeref;
    ASN1_STRING *exptext;
} USERNOTICE;

typedef struct {
    ASN1_OBJECT *pqualid;
    union {
        ASN1_IA5STRING *cpsuri;
        USERNOTICE *usernotice;
        ASN1_TYPE *other;
    } d;
} POLICYQUALINFO;

typedef struct {
    ASN1_OBJECT *policyid;
    Cryptography_STACK_OF_POLICYQUALINFO *qualifiers;
} POLICYINFO;
"""


FUNCTIONS = """
int X509V3_EXT_add_alias(int, int);
void X509V3_set_ctx(X509V3_CTX *, X509 *, X509 *, X509_REQ *, X509_CRL *, int);
X509_EXTENSION *X509V3_EXT_nconf(CONF *, X509V3_CTX *, char *, char *);
GENERAL_NAME *GENERAL_NAME_new(void);
int GENERAL_NAME_print(BIO *, GENERAL_NAME *);
GENERAL_NAMES *GENERAL_NAMES_new(void);
void GENERAL_NAMES_free(GENERAL_NAMES *);
void *X509V3_EXT_d2i(X509_EXTENSION *);
"""

MACROS = """
/* This is a macro defined by a call to DECLARE_ASN1_FUNCTIONS in the
   x509v3.h header. */
int i2d_BASIC_CONSTRAINTS(BASIC_CONSTRAINTS *, unsigned char **);
BASIC_CONSTRAINTS *BASIC_CONSTRAINTS_new(void);
void BASIC_CONSTRAINTS_free(BASIC_CONSTRAINTS *);
/* This is a macro defined by a call to DECLARE_ASN1_FUNCTIONS in the
   x509v3.h header. */
void AUTHORITY_KEYID_free(AUTHORITY_KEYID *);

NAME_CONSTRAINTS *NAME_CONSTRAINTS_new(void);
void NAME_CONSTRAINTS_free(NAME_CONSTRAINTS *);

void *X509V3_set_ctx_nodb(X509V3_CTX *);

int i2d_GENERAL_NAMES(GENERAL_NAMES *, unsigned char **);

int sk_GENERAL_NAME_num(struct stack_st_GENERAL_NAME *);
int sk_GENERAL_NAME_push(struct stack_st_GENERAL_NAME *, GENERAL_NAME *);
GENERAL_NAME *sk_GENERAL_NAME_value(struct stack_st_GENERAL_NAME *, int);

Cryptography_STACK_OF_ACCESS_DESCRIPTION *sk_ACCESS_DESCRIPTION_new_null(void);
int sk_ACCESS_DESCRIPTION_num(Cryptography_STACK_OF_ACCESS_DESCRIPTION *);
ACCESS_DESCRIPTION *sk_ACCESS_DESCRIPTION_value(
    Cryptography_STACK_OF_ACCESS_DESCRIPTION *, int
);
void sk_ACCESS_DESCRIPTION_free(Cryptography_STACK_OF_ACCESS_DESCRIPTION *);
int sk_ACCESS_DESCRIPTION_push(Cryptography_STACK_OF_ACCESS_DESCRIPTION *,
                               ACCESS_DESCRIPTION *);

X509_EXTENSION *X509V3_EXT_conf_nid(Cryptography_LHASH_OF_CONF_VALUE *,
                                    X509V3_CTX *, int, char *);

/* These aren't macros these functions are all const X on openssl > 1.0.x */
const X509V3_EXT_METHOD *X509V3_EXT_get(X509_EXTENSION *);
const X509V3_EXT_METHOD *X509V3_EXT_get_nid(int);

void sk_DIST_POINT_free(Cryptography_STACK_OF_DIST_POINT *);
int sk_DIST_POINT_num(Cryptography_STACK_OF_DIST_POINT *);
DIST_POINT *sk_DIST_POINT_value(Cryptography_STACK_OF_DIST_POINT *, int);

void sk_POLICYINFO_free(Cryptography_STACK_OF_POLICYINFO *);
int sk_POLICYINFO_num(Cryptography_STACK_OF_POLICYINFO *);
POLICYINFO *sk_POLICYINFO_value(Cryptography_STACK_OF_POLICYINFO *, int);

void sk_POLICYQUALINFO_free(Cryptography_STACK_OF_POLICYQUALINFO *);
int sk_POLICYQUALINFO_num(Cryptography_STACK_OF_POLICYQUALINFO *);
POLICYQUALINFO *sk_POLICYQUALINFO_value(Cryptography_STACK_OF_POLICYQUALINFO *,
                                        int);

void sk_GENERAL_SUBTREE_free(Cryptography_STACK_OF_GENERAL_SUBTREE *);
int sk_GENERAL_SUBTREE_num(Cryptography_STACK_OF_GENERAL_SUBTREE *);
GENERAL_SUBTREE *sk_GENERAL_SUBTREE_value(
    Cryptography_STACK_OF_GENERAL_SUBTREE *, int
);
int sk_GENERAL_SUBTREE_push(Cryptography_STACK_OF_GENERAL_SUBTREE *,
                            GENERAL_SUBTREE *);

void sk_ASN1_INTEGER_free(Cryptography_STACK_OF_ASN1_INTEGER *);
int sk_ASN1_INTEGER_num(Cryptography_STACK_OF_ASN1_INTEGER *);
ASN1_INTEGER *sk_ASN1_INTEGER_value(Cryptography_STACK_OF_ASN1_INTEGER *, int);

X509_EXTENSION *X509V3_EXT_i2d(int, int, void *);
"""

CUSTOMIZATIONS = """
"""

CONDITIONAL_NAMES = {}