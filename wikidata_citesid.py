WIKIDATA_REQUEST1ID = """SELECT DISTINCT ?item ?itemLabel ?nomscientifique ?rangtaxinomique ?rangtaxinomiqueLabel ?taxonsuperieur ?taxonsuperieurLabel ?identifiantSPECIES ?image ?value ?valueLabel
WHERE
{
  ?item wdt:P2040 """


WIKIDATA_REQUEST2ID =  """ ;
        rdfs:label ?itemLabel .
  OPTIONAL { ?item wdt:P18 ?image. }   
  OPTIONAL { ?item wdt:P225 ?nomscientifique. } 
  OPTIONAL { ?item wdt:P105 ?rangtaxinomique. 
             ?rangtaxinomique rdfs:label ?rangtaxinomiqueLabel filter (lang(?rangtaxinomiqueLabel) = "fr") .  
           }   
  OPTIONAL { ?item wdt:P171 ?taxonsuperieur. 
             ?taxonsuperieur rdfs:label ?taxonsuperieurLabel filter (lang(?taxonsuperieurLabel) = "fr") .  
           }            
  OPTIONAL { ?item wdt:P2040 ?identifiantSPECIES. } 
  
  FILTER (LANG(?itemLabel)="fr") }"""
