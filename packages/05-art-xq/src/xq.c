/* art-xq: вычисление выражения XPath над XML-файлом (libxml2)
 *   art-xq FILE XPATH */
#include <stdio.h>
#include <libxml/parser.h>
#include <libxml/xpath.h>

int main(int argc, char **argv)
{
    xmlDocPtr doc;
    xmlXPathContextPtr ctx;
    xmlXPathObjectPtr res;
    int rc = 0;

    if (argc != 3) {
        fprintf(stderr, "usage: art-xq FILE XPATH\n");
        return 2;
    }
    doc = xmlReadFile(argv[1], NULL, XML_PARSE_NONET);
    if (!doc)
        return 1;
    ctx = xmlXPathNewContext(doc);
    res = xmlXPathEvalExpression((const xmlChar *)argv[2], ctx);
    if (!res) {
        rc = 1;
    } else if (res->type == XPATH_NODESET) {
        xmlNodeSetPtr ns = res->nodesetval;
        for (int i = 0; ns && i < ns->nodeNr; i++) {
            xmlChar *s = xmlNodeGetContent(ns->nodeTab[i]);
            printf("%s\n", s ? (char *)s : "");
            xmlFree(s);
        }
    } else {
        xmlChar *s = xmlXPathCastToString(res);
        printf("%s\n", (char *)s);
        xmlFree(s);
    }
    xmlXPathFreeObject(res);
    xmlXPathFreeContext(ctx);
    xmlFreeDoc(doc);
    xmlCleanupParser();
    return rc;
}
