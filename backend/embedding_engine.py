import numpy as np
from rdflib import Graph
import networkx as nx
from node2vec import Node2Vec
from backend.vocab import EX


class EmbeddingEngine:
    def __init__(self, rdf_file: str):
        self.g = Graph()
        self.g.parse(rdf_file, format="turtle")
        self.nx_graph = nx.Graph()
        self.model = None
        self.embeddings = {}

        for s, p, o in self.g:
            self.nx_graph.add_edge(str(s), str(o))
        self._train_embeddings()


    def _train_embeddings(self):

        movie_nodes = [str(s) for s in self.g.subjects(predicate=EX.title)]

        node2vec = Node2Vec(
            self.nx_graph,
            dimensions=32,      # smaller vector size
            walk_length=10,      # shorter walks
            num_walks=10,        # fewer walks per node
            workers=4,          # limited CPU cores
            quiet=False
        )

        # Train Word2Vec directly using Node2Vec
        self.model = node2vec.fit(
            window=5,           # context window
            min_count=1,
            workers=4,
            sg=1                # skip-gram
        )

        # Keep only embeddings for movies
        self.embeddings = {node: self.model.wv[node] for node in movie_nodes}
        self.get_similar_movies("http://example.org/movie/10_Days_of_a_Curious_Man")
        self.get_similar_movies("http://example.org/movie/10DANCE")
        self.get_similar_movies("http://example.org/movie/107_Mothers")


    def get_similar_movies(self, target_movie_uri: str, top_n: int = 10):
        if target_movie_uri not in self.embeddings:
            return []

        target_vec = self.embeddings[target_movie_uri]
        sims = []
        for movie_uri, vec in self.embeddings.items():
            if movie_uri == target_movie_uri:
                continue
            sim = np.dot(target_vec, vec) / (np.linalg.norm(target_vec) * np.linalg.norm(vec))
            sims.append((movie_uri, sim))

        sims.sort(key=lambda x: x[1], reverse=True)
        print(sims[:top_n])
        return sims[:top_n]