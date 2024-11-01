from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://127.0.0.1:7200/repositories/F1")
sparql.setQuery("""
PREFIX f1: <http://example.org/f1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX schema1: <http://schema.org/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?driver ?code ?number ?birthDate ?nationality ?familyName ?givenName
WHERE {
    ?driver a f1:Driver ;
            f1:code ?code ;
            f1:number ?number ;
            schema1:birthDate ?birthDate ;
            schema1:nationality ?nationality ;
            foaf:familyName ?familyName ;
            foaf:givenName ?givenName .
    FILTER(?givenName = "Lewis")
}

""")
sparql.setReturnFormat(JSON)

results = sparql.query().convert()
print(results)