===========
indic-trans
===========

|travis| |coverage|

.. |travis| image:: https://travis-ci.org/irshadbhat/indic-trans.svg?branch=master
   :target: https://travis-ci.org/irshadbhat/indic-trans
   :alt: travis-ci build status

.. |coverage| image:: https://coveralls.io/repos/github/irshadbhat/indic-trans/badge.svg?branch=master 
   :target: https://coveralls.io/github/irshadbhat/indic-trans?branch=master
   :alt: coveralls.io build status


The project aims on adding a state-of-the-art transliteration module for cross transliterations among all Indian languages including English.

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
  * English

Installation
============

Dependencies
~~~~~~~~~~~~

`indictrans`_ requires `cython`_, and `SciPy`_.

.. _`indictrans`: https://github.com/irshadbhat/indictrans

.. _`cython`: http://docs.cython.org/src/quickstart/install.html

.. _`Scipy`: http://www.scipy.org/install.html

Install dependencies:

::

    pip install -r requirements.txt

Download
~~~~~~~~

Download **indictrans**  from `github`_.

.. _`github`: https://github.com/libindic/indic-trans

Install
~~~~~~~

::

    pip install git+git://github.com/irshadbhat/indic-trans.git   or 
    pip install git+git://github.com/libindic/indic-trans.git    

Examples
~~~~~~~~

1. From Console:
^^^^^^^^^^^^^^^^

.. parsed-literal::

    indictrans --h

    --v         show program's version number and exit
    --source    select language (3 letter ISO-639 code)
                [hin|ben|guj|pan|mal|kan|tam|tel|ori|eng|mar|asm|kok|bod|nep]
    --target    select language (3 letter ISO-639 code)
                [hin|ben|guj|pan|mal|kan|tam|tel|ori|eng|mar|asm|kok|bod|nep]
    --input     <input-file>
    --output    <output-file>


    Example ::

	indictrans < hindi.txt --s hin --t eng > hindi-rom.txt
	indictrans < roman.txt --s hin --t eng > roman-hin.txt

2. Using Python:
^^^^^^^^^^^^^^^^

.. code:: python

    >>> from indictrans import transliterator
    >>> trn = transliterator(source='hin', target='eng')
    >>> 
    >>> hin = """कांग्रेस पार्टी अध्यक्ष सोनिया गांधी, तमिलनाडु की मुख्यमंत्री जयललिता और रिज़र्व बैंक के गवर्नर रघुराम राजन के बीच एक समानता है.
    ... ये सभी अलग-अलग कारणों से भारतीय जनता पार्टी के राज्यसभा सांसद सुब्रमण्यम स्वामी के निशाने पर हैं.
    ... उनके जयललिता और सोनिया गांधी के पीछे पड़ने का कारण कथित भ्रष्टाचार है."""
    >>>
    >>> eng = trn.transform(hin)
    >>> print(eng)
    congress party adhyaksh sonia gandhi, tamilnadu kii mukhyamantri jayalalita our reserve baink ke governor raghuram rajan ke beech ek samanta hai.
    ye sabi alag-alag carnon se bharatiya janata party ke rajyasabha saansad subramanyam swami ke nishane par hain.
    unke jayalalita our sonia gandhi ke peeche padane ka kaaran kathith bhrashtachar hai.
    >>> 
    >>> trn = transliterator(source='eng', target='hin')
    >>> 
    >>> hin_ = trn.transform(eng)
    >>> 
    >>> print(hin_)
    कांग्रेस पार्टी अध्यक्ष सोनिया गांधी, तमिलनाडु की मुख्यमांत्री जयललिता और रिज़र्व बैंक के गवर्नर रघुराम राजन के बीच एक समानता है.
    ये सभी अलग-अलग कार्नों से भारतीय जनता पार्टी के राज्यसभा स्Mसद सुब्रमण्यम स्वामी के निशाने पर हैं.
    उनके जयललिता और सोनिया गांधी के पीछे पड़ने का कारण कथित भ्रष्टाचार है.
    >>>

