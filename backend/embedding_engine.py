import csv
import numpy as np

class EmbeddingEngine:
    def __init__(self, embedding_file: str):
        self.embeddings = {}

        #Open embeddings CSV file
        with open(embedding_file, newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  #Skip header row

            for row in reader:
                uri = row[0]  #First column is movie URI

                #The rest are vectors
                vec = np.array([complex(x) for x in row[1:]], dtype=np.complex64)

                #Adds vector with the URI as key
                self.embeddings[uri] = vec

    #Retrieve similar movies
    def get_similar_movies(self, target_movie_uri: str, top_n: int = 10):
        #Returns an empty list if the movie URI does not exist in embeddings
        if target_movie_uri not in self.embeddings:
            return []

        target_vec = self.embeddings[target_movie_uri]
        sims = []

        #Compare target movie to all other movies
        for movie_uri, vec in self.embeddings.items():
            if movie_uri == target_movie_uri:
                continue #Skip itself

            #Using cosine similarity do calculate similarity score
            sim = np.dot(target_vec, vec) / (np.linalg.norm(target_vec) * np.linalg.norm(vec))
            sims.append((movie_uri, sim))

        #Sort movies by descending similarity score
        sims.sort(key=lambda x: x[1], reverse=True)
        print(sims[:top_n])
        return sims[:top_n]