import random
import nltk
from nltk.corpus import machado, floresta

class DynamicTextGenerator:
    def __init__(self, corpora):
        self.corpora = corpora
        self.n_gram_counts = {}
        self.n = 3
        self.grammars = {
            'default': nltk.CFG.fromstring("""
                S -> NP VP | NP VP Conj VP
                NP -> DET ADJ N | DET N | PRON
                VP -> V NP | V PP | V NP PP | V Adv
                DET -> 'o' | 'a' | 'algum'
                ADJ -> 'grande' | 'pequeno' | 'vermelho' | 'verde'
                N -> 'cão' | 'gato' | 'rato' | 'queijo'
                V -> 'corre' | 'pula' | 'come' | 'dorme'
                Adv -> 'rapidamente' | 'silenciosamente' | 'bem'
                PP -> P NP
                P -> 'em' | 'sobre' | 'sob'
                Conj -> 'e' | 'ou' | 'mas'
                PRON -> 'ele' | 'ela' | 'eles'
            """),
            'story': nltk.CFG.fromstring("""
                S -> NP VP | NP VP Conj VP | S Conj S
                NP -> DET ADJ N | DET N | PRON
                VP -> V NP | V PP | V NP PP | V Adv
                DET -> 'o' | 'a' | 'algum'
                ADJ -> 'misterioso' | 'antigo' | 'colorido' | 'encantado'
                N -> 'floresta' | 'castelo' | 'dragão' | 'aventura'
                V -> 'explora' | 'descobre' | 'encontra' | 'sonha'
                Adv -> 'magicamente' | 'inesperadamente' | 'corajosamente'
                PP -> P NP
                P -> 'em' | 'sobre' | 'sob'
                Conj -> 'e' | 'ou' | 'mas'
                PRON -> 'ele' | 'ela' | 'eles'
            """),
            'sci-fi': nltk.CFG.fromstring("""
                S -> NP VP | NP VP Conj VP | S Conj S
                NP -> DET ADJ N | DET N | PRON
                VP -> V NP | V PP | V NP PP | V Adv
                DET -> 'o' | 'a' | 'algum'
                ADJ -> 'futurista' | 'alienígena' | 'avançado' | 'intergaláctico'
                N -> 'nave' | 'robô' | 'planeta' | 'galáxia'
                V -> 'explora' | 'descobre' | 'encontra' | 'viaja'
                Adv -> 'cientificamente' | 'imprevisivelmente' | 'audaciosamente'
                PP -> P NP
                P -> 'em' | 'sobre' | 'sob'
                Conj -> 'e' | 'ou' | 'mas'
                PRON -> 'ele' | 'ela' | 'eles'
            """),
            # Add more grammars for different themes as needed
        }

    def set_n(self, n):
        self.n = n

    def generate_text(self, length, themes=None):
        theme = random.choice(themes) if themes else 'default'
        text_generated = []

        # Start with a random n-gram from the corpus
        n_gram = random.choice(list(self.n_gram_counts.keys()))
        text_generated.extend(n_gram)

        for _ in range(length - self.n):
            # Get the next word based on the current n-gram
            next_word = self._get_next_word(n_gram, theme)
            text_generated.append(next_word)

            # Update the n-gram
            n_gram = n_gram[1:] + (next_word,)

        return " ".join(text_generated)

    def _get_next_word(self, n_gram, theme):
        # Calculate probabilities for the next word based on the current n-gram and theme
        next_word_probabilities = {}
        for next_word in self.corpora:
            next_n_gram = n_gram + (next_word,)
            if next_n_gram in self.n_gram_counts:
                next_word_probabilities[next_word] = self.n_gram_counts[next_n_gram]

        # Normalize probabilities
        total_probability = sum(next_word_probabilities.values())
        for next_word in next_word_probabilities.keys():
            next_word_probabilities[next_word] /= total_probability

        # Sample the next word based on probabilities
        next_word = random.choices(list(next_word_probabilities.keys()), weights=next_word_probabilities.values())[0]

        return next_word


def generate_story(length, themes=None):
    # Load the corpora
    corpus = machado.words() + floresta.words()

    # Create a text generator with multiple grammars
    text_generator = DynamicTextGenerator(corpus)

    # Generate a story with the specified theme
    story = text_generator.generate_text(length, themes)

    # Print the story
    print(story)


if __name__ == "__main__":
    # Example: Generate a story with themes 'story' and 'sci-fi'
    generate_story(500, themes=['story', 'sci-fi'])
