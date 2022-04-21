indic-trans
===========

|travis| |coverage| |CircleCI| |Documentation Status|

----

The project aims on adding a state-of-the-art transliteration module for cross transliterations among all Indian languages including English and Urdu.

The module currently supports the following languages:

  * Hindi       
  * Bengali
  * Gujarati
  * Punjabi
  * Malayalam
  * Kannada
  * Tamil
  * Telugu
  * Oriya
  * Marathi
  * Assamese
  * Konkani
  * Bodo
  * Nepali
  * Urdu
  * English

Links & References
------------------

* `Official source code repo <https://github.com/libindic/indic-trans>`_
* `HTML documentation <http://indic-trans.readthedocs.org>`_
* `Transliteration Blog <http://irshadbhat.github.io/gsoc>`_
* Mailing list: silpa-discuss@nongnu.org
* IRC channel: ``#silpa`` at ``irc.freenode.net``

Installation
------------

Dependencies
^^^^^^^^^^^^

`indictrans`_ requires `cython`_, and `SciPy`_.

.. _`indictrans`: https://github.com/libindic/indic-trans

.. _`cython`: http://docs.cython.org/src/quickstart/install.html

.. _`Scipy`: http://www.scipy.org/install.html

Clone & Install
^^^^^^^^^^^^^^^

::

    Clone the repository:
        git clone https://github.com/libindic/indic-trans.git
        ------------------------OR--------------------------
        git clone https://github.com/irshadbhat/indictrans.git

    Change to the cloned directory:
        cd indic-trans
        pip install -r requirements.txt
        cd ..
	pip install indic-trans/

Examples
--------

1. From Console:
^^^^^^^^^^^^^^^^

.. parsed-literal::

    indictrans --h

    -h, --help          show this help message and exit
    -v, --version       show program's version number and exit
    -s, --source        select language (3 letter ISO-639 code) {hin, guj, pan,
                        ben, mal, kan, tam, tel, ori, eng, mar, nep, bod, kok,
                        asm, urd}
    -t, --target        select language (3 letter ISO-639 code) {hin, guj, pan,
                        ben, mal, kan, tam, tel, ori, eng, mar, nep, bod, kok,
                        asm, urd}
    -b, --build-lookup  build lookup to fasten transliteration
    -m, --ml            use ML system for transliteration
    -r, --rb            use rule-based system for transliteration
    -i, --input         <input-file>
    -o, --output        <output-file>


    Example ::

	indictrans < hindi.txt --s hin --t eng --build-lookup > hindi-rom.txt
	indictrans < roman.txt --s hin --t eng --build-lookup > roman-hin.txt

If the input text contains repeating words, which raw text generally does, make sure to set ``build_lookup``. As the name indicates this builds lookup for transliterated words and thus avoids repeated transliteration of same words. This saves a lot of time if the input corpus is too big.

Note that ``ml`` and ``rb`` are mutually exclusive arguments. If none of these is set, then the sytem defaults to ``rb``.

2. Using Python:
^^^^^^^^^^^^^^^^

.. code:: python

    >>> from indictrans import Transliterator
    >>> trn = Transliterator(source='hin', target='eng', build_lookup=True)
    >>> 
    >>> hin = """कांग्रेस पार्टी अध्यक्ष सोनिया गांधी, तमिलनाडु की मुख्यमंत्री
    ... जयललिता और रिज़र्व बैंक के गवर्नर रघुराम राजन के बीच एक समानता
    ... है. ये सभी अलग-अलग कारणों से भारतीय जनता पार्टी के राज्यसभा सांसद
    ... सुब्रमण्यम स्वामी के निशाने पर हैं. उनके जयललिता और सोनिया गांधी के
    ... पीछे पड़ने का कारण कथित भ्रष्टाचार है."""
    >>>
    >>> eng = trn.transform(hin)
    >>> print(eng)
    congress party adhyaksh sonia gandhi, tamilnadu kii mukhyamantri
    jayalalita or reserve bank ke governor raghuram rajan ke bich ek samanta
    he. ye sabhi alag-alag kaarnon se bhartiya janata party ke rajyasabha saansad
    subramanyam swami ke nishane par hai. unke jayalalita or sonia gandhi ke
    peeche padane kaa kaaran kathith bhrashtachar he.
    >>> 
    >>> trn = Transliterator(source='eng', target='hin')
    >>> 
    >>> hin_ = trn.transform(eng)
    >>> 
    >>> print(hin_)
    कांग्रेस पार्टी अध्यक्ष सोनिया गांधी, तमिलनाडु की मुख्यमंत्री
    जयललिता और रिज़र्व बैंक के गवर्नर रघुराम राजन के बीच एक समनता
    है. ये सभी अलग-अलग कारनों से भारतीय जनता पार्टी के राज्यसभा सांसद
    सुब्रमण्यम स्वामी के निशाने पर हैं. उनके जयललिता और सोनिया गांधी के
    पीछे पड़ने का कारण कथित भ्रष्टाचार है.
    >>>

3. K-Best Transliterations
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> from indictrans import Transliterator
    >>> r2i = Transliterator(source='eng', target='mal', decode='beamsearch')
    >>> words = '''sereleskar morocco calendar bhagyalakshmi bhoolokanathan
    ...         medical ernakulam kilometer vitamin management university
    ...         naukuchiatal'''.split()
    >>> for word in words:
    ...     print('%s -> %s' % (word, 
    ...                         '  '.join(r2i.transform(word, k_best=5))))
    ... 
    sereleskar -> സേറെലേസ്കാര്  സെറെലേസ്കാര്  സേറെലേസ്കാര  സെറെലേസ്കാര  സേറെലേസ്കര്
    morocco -> മൊറോക്കോ  മൊറോക്ഡോ  മൊരോക്കോ  മോറോക്കോ  മൊറോക്കൂ
    calendar -> കേലെന്ദര  കേലെന്ഡര  കേലെന്ദ്ര  കേലെന്ദാര  കേലെന്ഡ്ര
    bhagyalakshmi -> ഭാഗ്യലക്ഷ്മീ  ഭാഗ്യലക്ഷ്മി  ഭഗ്യലക്ഷ്മീ  ഭാഗ്യാലക്ഷ്മീ  ഭഗ്യലക്ഷ്മി
    bhoolokanathan -> ഭൂലോകനാഥന  ഭൂലോകാനാഥന  ഭൂലോക്കനാഥന  ബൂലോകനാഥന  ഭൂലോകനാതന
    medical -> മെഡിക്കല്  മെഡിക്കലും  മെഡിക്കില്  മ്മഎഡിക്കല്  മേഡിക്കല്
    ernakulam -> എറണാകുളം  ഈറണാകുളം  എറണാകുലം  എറണാകുളഅം  എറണാകുളാം
    kilometer -> കിലോമീറ്റര്  കിലോഈറ്റര്  കിലോമീറ്റ്ര്  കിലോമീറ്ററ്  കിലോമീടര്
    vitamin -> വിറ്റാമിന്  വിറ്റമിന്  വൈറ്റാമിന്  വിതാമിന്  വിതആമിന്
    management -> മാനേജ്മെന്റ്  മാനേജ്ഞ്മെന്റ്  മാനേഗ്മെന്റ്  മാംനേജ്മെന്റ്  മാനേജ്മെതുറ്
    university -> യൂണിവേഴ്സിറ്റി  യൂണിവേര്സിറ്റി  യുണിവേഴ്സിറ്റി  യൂനിവേഴ്സിറ്റി  യൂണിവേഴ്സിറ്റീ
    naukuchiatal -> നകുചിയാറ്റാള്  നകുചിയാറ്റാല്  നകുചിയാറ്റാല  നകുചിയാറ്റള്  നകുചിയറ്റാള്

Cite
^^^^

If you use this code for a publication, please cite the following paper:

@inproceedings{Bhat:2014:ISS:2824864.2824872,
 author = {Bhat, Irshad Ahmad and Mujadia, Vandan and Tammewar, Aniruddha and Bhat, Riyaz Ahmad and Shrivastava, Manish},
 title = {IIIT-H System Submission for FIRE2014 Shared Task on Transliterated Search},
 booktitle = {Proceedings of the Forum for Information Retrieval Evaluation},
 series = {FIRE '14},
 year = {2015},
 isbn = {978-1-4503-3755-7},
 location = {Bangalore, India},
 pages = {48--53},
 numpages = {6},
 url = {http://doi.acm.org/10.1145/2824864.2824872},
 doi = {10.1145/2824864.2824872},
 acmid = {2824872},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {Information Retrieval, Language Identification, Language Modeling, Perplexity, Transliteration},
}

----

|travis| |coverage| |CircleCI| |Documentation Status|

.. |travis| image:: https://travis-ci.org/libindic/indic-trans.svg?branch=master
   :target: https://travis-ci.org/libindic/indic-trans
   :alt: travis-ci build status

.. |coverage| image:: https://coveralls.io/repos/github/libindic/indic-trans/badge.svg?branch=master 
   :target: https://coveralls.io/github/libindic/indic-trans?branch=master
   :alt: coveralls.io coverage status
   
.. |CircleCI| image:: https://circleci.com/gh/libindic/indic-trans.svg?style=svg
    :target: https://circleci.com/gh/libindic/indic-trans

.. |Documentation Status| image:: https://readthedocs.org/projects/indic-trans/badge/?version=latest
    :target: http://indic-trans.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
