from Levenshtein import distance as levenshtein_distance


class OCREvaluator:

    @staticmethod
    def word_accuracy(truth: list[str], prediction: list[str]):
        hit, miss = 0, 0
        for t_word, p_word in zip(truth, prediction):
            if t_word == p_word:
                hit += 1
            else:
                miss +=1
        return hit / (hit + miss)

    @staticmethod
    def word_sim(truth: list[str], prediction: list[str]):
        result = 0
        for t_word, p_word in zip(truth, prediction):
            result += levenshtein_distance(t_word, p_word)
        return result / len(truth)
