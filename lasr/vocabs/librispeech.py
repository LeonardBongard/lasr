# MIT License
#
# Copyright (c) 2021 Soohwan Kim
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from lasr.vocabs import Vocabulary


class LibriSpeechVocabulary(Vocabulary):
    def __init__(self, vocab_path, model_path):
        super(LibriSpeechVocabulary, self).__init__()
        try:
            import sentencepiece as spm
        except ImportError:
            raise ImportError("Please install sentencepiece: `pip install sentencepiece`")
        self.pad_id = 0
        self.sos_id = 1
        self.eos_id = 2

        self.vocab_path = vocab_path

        self.sp = spm.SentencePieceProcessor()
        self.sp.Load(model_path)

    def __len__(self):
        count = 0
        with open(self.vocab_path, encoding='utf-8') as f:
            for _ in f.readlines():
                count += 1
        return count

    def label_to_string(self, labels):
        if len(labels.shape) == 1:
            return self.sp.DecodeIds([l for l in labels])

        sentences = list()
        for batch in labels:
            sentence = str()
            for label in batch:
                sentence = self.sp.DecodeIds([l for l in label])
            sentences.append(sentence)
        return sentences
