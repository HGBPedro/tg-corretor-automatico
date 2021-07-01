import viterbi_tagger, perceptron_tagger
from nltk.corpus import mac_morpho, brown

if __name__ == '__main__':

    # Verify the if AP tagger is ready to function
    taggerAP = perceptron_tagger.AP_Tagger(False)
    print ("If the averaged perceptron tagger is not trained, train it and cache the results.")
    try:
        taggerAP.APTaggerTesting()
    except IOError:
        taggerAP.APTaggerTraining()
        taggerAP.APTaggerTesting()


    viterbi_tagger = viterbi_tagger.PartOfSpeechTagger()
    print ("The tests will take a while.")
    print ("Test of accuracy: mac_morpho corpus.")
    viterbi_tagger.buildProbDist(mac_morpho)
    viterbi_tagger.testAgainstCorpus(mac_morpho)