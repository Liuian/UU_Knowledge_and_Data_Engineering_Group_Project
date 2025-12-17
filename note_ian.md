Files to use: `./data/wiki_db_cleaned.csv`, `./data/wiki_db_cleaned.ttl`

## Processing Steps
**1. Query from Wikidata**
- Query and download from Wikidata.
- Link: https://query.wikidata.org
- Data used: Years 2020-2025, 10 genres. Located in the folder `./data/wiki_5y/`

```sparql
SELECT ?movie
       (SAMPLE(?label) AS ?title)
       (SAMPLE(?year) AS ?year)
       #(SAMPLE(?imdbID) AS ?imdbID)
       (SAMPLE(?runtime) AS ?runtime)
       #(GROUP_CONCAT(DISTINCT ?countryLabel; separator=", ") AS ?countries)
       #(GROUP_CONCAT(DISTINCT ?languageLabel; separator=", ") AS ?languages)
       #(GROUP_CONCAT(DISTINCT ?productionLabel; separator=", ") AS ?productionCompanies)
       #(GROUP_CONCAT(DISTINCT ?screenwriterLabel; separator=", ") AS ?screenwriters)
       #(GROUP_CONCAT(DISTINCT ?composerLabel; separator=", ") AS ?composers)
       #(GROUP_CONCAT(DISTINCT ?seriesLabel; separator=", ") AS ?series)
       #(GROUP_CONCAT(DISTINCT ?ratingLabel; separator=", ") AS ?ratings)
       (GROUP_CONCAT(DISTINCT ?directorLabel; separator=", ") AS ?directors)
       (GROUP_CONCAT(DISTINCT ?actorLabel; separator=", ") AS ?actors)
       #(SAMPLE(?budget) AS ?budget)
       #(SAMPLE(?gross) AS ?gross)
WHERE {
  ?movie wdt:P31 wd:Q11424 ;           # instance of film
         wdt:P136 ?genre ;             # genre
         wdt:P577 ?publicationDate ;
         wdt:P345 ?imdbID .            # IMDb ID

  ?genre wdt:P279* wd:Q24925 .         # genre

  OPTIONAL { ?movie wdt:P2047 ?runtime . }
  #OPTIONAL { ?movie wdt:P495 ?country . ?country rdfs:label ?countryLabel FILTER(LANG(?countryLabel)="en") }
  #OPTIONAL { ?movie wdt:P364 ?language . ?language rdfs:label ?languageLabel FILTER(LANG(?languageLabel)="en") }
  #OPTIONAL { ?movie wdt:P272 ?production . ?production rdfs:label ?productionLabel FILTER(LANG(?productionLabel)="en") }
  #OPTIONAL { ?movie wdt:P58 ?screenwriter . ?screenwriter rdfs:label ?screenwriterLabel FILTER(LANG(?screenwriterLabel)="en") }
  #OPTIONAL { ?movie wdt:P86 ?composer . ?composer rdfs:label ?composerLabel FILTER(LANG(?composerLabel)="en") }
  #OPTIONAL { ?movie wdt:P179 ?series . ?series rdfs:label ?seriesLabel FILTER(LANG(?seriesLabel)="en") }
  #OPTIONAL { ?movie wdt:P1259 ?rating . ?rating rdfs:label ?ratingLabel FILTER(LANG(?ratingLabel)="en") }
  OPTIONAL { ?movie wdt:P57 ?director . ?director rdfs:label ?directorLabel FILTER(LANG(?directorLabel)="en") }
  OPTIONAL { ?movie wdt:P161 ?actor . ?actor rdfs:label ?actorLabel FILTER(LANG(?actorLabel)="en") }
  #OPTIONAL { ?movie wdt:P2130 ?budget . }
  #OPTIONAL { ?movie wdt:P2142 ?gross . }

  BIND(YEAR(?publicationDate) AS ?year)
  FILTER(?year >= 2015 && ?year <= 2025)

  ?movie rdfs:label ?label .
  FILTER(LANG(?label) = "en")
}
GROUP BY ?movie
```

| Genre                | Q-id          |5y (2020-2025)|10y (2015-2025)|
| -------------------- | ------------- | ------------ | ------------- |
| Science fiction film | **Q24925**    | V            | V             |
| Adventure film       | **Q319221**   | V            | V             |
| Drama film           | **Q130232**   | V            | V             |
| Comedy film          | **Q157443**   | V            | X             |
| Horror film          | **Q200092**   | V            | V             |
| Thriller film        | **Q2484376**  | V            | X             |
| Crime Thriller film  | **Q19367312** | V            | V             |
| Romance film         | **Q1054574**  | V            | V             |
| Crime film           | **Q959790**   | V            | V             |
| Animated film        | **Q202866**   | V            | V             |

**2. Merge the 10 CSV files**
- Using the script: `merge_csv_files.py`
- Output file: `./data/merged.csv`

**3. Use QID to find corresponding data from DBpedia**
- Using the script: `wikidata_to_dbpedia_movies.py`
- Output file: `./data/wiki_db.csv`

**4. Perform data preprocessing**
- Using the script: `data_preprocessing.py`
- Output file: `./data/wiki_db_cleaned.csv`

**5. Convert to a Turtle file**
- Using the script: `csv_to_rdf.py`
- Output file: `./data/wiki_db_cleaned.ttl`