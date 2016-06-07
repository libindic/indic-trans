===========
indic-trans
===========

|Build Status| |Coverage Status|

.. |Build Status| image:: https://travis-ci.org/libindic/indic-trans.svg?branch=master
   :target: https://travis-ci.org/libindic/indic-trans

.. |Coverage Status| image:: https://coveralls.io/repos/github/libindic/indic-trans/badge.svg?branch=master 
   :target: https://coveralls.io/github/libindic/indic-trans?branch=master


The project aims on adding a state-of-the-art transliteration module for cross transliterations among all Indian languages including English.

Installation
============

Dependencies
~~~~~~~~~~~~

`indictrans`_ requires `cython`_, and `SciPy`_.

.. _`indictrans`: https://github.com/irshadbhat/indictrans

.. _`cython`: http://docs.cython.org/src/quickstart/install.html

.. _`Scipy`: http://www.scipy.org/install.html

To install the dependencies do something like (Ubuntu):

::

    pip install cython
    pip install python-scipy

Download
~~~~~~~~

Download **indictrans**  from `github`_.

.. _`github`: https://github.com/libindic/indic-trans

Install
~~~~~~~

::

    pip install git+git://github.com/libindic/indic-trans.git    

Examples
~~~~~~~~

1. From Console:
^^^^^^^^^^^^^^^^

.. parsed-literal::

    indictrans --h

    --v           show program's version number and exit
    --s source    select language (3 letter ISO-639 code) [hin|eng]
    --t target    select language (3 letter ISO-639 code) [hin|eng]
    --i input     <input-file>
    --o output    <output-file>

    Example ::

	indictrans < tests/hindi.txt --s hin --t eng > tests/hindi-rom.txt
	indictrans < tests/roman.txt --s hin --t eng > tests/roman-hin.txt

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

