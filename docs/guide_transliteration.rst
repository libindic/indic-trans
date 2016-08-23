Transliteration
===============

.. _example-trans:

Transliterate
-------------

In order to transliterate raw text, you can use the :class:`indictrans.Transliterator` which uses already trained models to transliterate the text. If the input text contains repeating words, which raw text generally does, make sure to set ``build_lookup`` flag to ``True``. As the name indicates this builds lookup for transliterated words and thus avoids repeated transliteration of same words. This saves a lot of time if the input corpus is too big. 

.. code-block:: python

    >>> from indictrans import Transliterator
    >>> trn = Transliterator(source='hin', target='eng', build_lookup=True)
    >>> hin = """कांग्रेस पार्टी अध्यक्ष सोनिया गांधी, तमिलनाडु की मुख्यमंत्री
    ... जयललिता और रिज़र्व बैंक के गवर्नर रघुराम राजन के बीच एक समानता
    ... है. ये सभी अलग-अलग कारणों से भारतीय जनता पार्टी के राज्यसभा सांसद
    ... सुब्रमण्यम स्वामी के निशाने पर हैं. उनके जयललिता और सोनिया गांधी के
    ... पीछे पड़ने का कारण कथित भ्रष्टाचार है."""
    >>> eng = trn.transform(hin)
    >>> print(eng)
    congress party adhyaksh sonia gandhi, tamilnadu kii mukhyamantri
    jayalalita our reserve baink ke governor raghuram rajan ke beech ek samanta
    hai. ye sabi alag-alag carnon se bharatiya janata party ke rajyasabha saansad
    subramanyam swami ke nishane par hain. unke jayalalita our sonia gandhi ke
    peeche padane ka kaaran kathith bhrashtachar hai.
    >>> trn = Transliterator(source='eng', target='hin')
    >>> hin_ = trn.transform(eng)
    >>> print(hin_)
    कांग्रेस पार्टी अध्यक्ष सोनिया गांधी, तमिलनाडु की मुख्यमांत्री
    जयललिता और रिज़र्व बैंक के गवर्नर रघुराम राजन के बीच एक समानता
    है. ये सभी अलग-अलग कार्नों से भारतीय जनता पार्टी के राज्यसभा संसद
    सुब्रमण्यम स्वामी के निशाने पर हैं. उनके जयललिता और सोनिया गांधी के
    पीछे पड़ने का कारण कथित भ्रष्टाचार है.

K-Best Transliterations
-----------------------

You can generate ``k-best`` outputs for a given sequence by changing the default decoder ``viterbi`` to ``beamsearch`` and then set the ``k_best`` parameter to the desired value.

.. code-block:: python
    
    >>> from indictrans import Transliterator
    >>> r2i = Transliterator(source='eng', target='mal', decode='beamsearch')
    >>> words = '''sereleskar morocco calendar bhagyalakshmi bhoolokanathan medical
    ...         ernakulam kilometer vitamin management university naukuchiatal'''.split()
    >>> for word in words:
    >>>     print('%s -> %s' % (word, '  '.join(r2i.transform(word, k_best=5))))
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

ML and Rule-Based systems for Indic Scripts
-------------------------------------------

For Indic scripts except Urdu you can use rule-based as well as machine learning (ML) system for transliteration. Rule based systems are very fast than ML systems and seem more accurate too. But for some language pairs ML systems generates better results.

.. code-block:: python

    >>> from indictrans import Transliterator
    >>> rom_text = 'indictrans libindic hyderabad university bhagyalakshmi bharat morocco'.split()
    >>> r2h = Transliterator(source='eng', target='hin')
    >>> hin_text = list(map(r2h.transform, rom_text))
    >>> hin_text
    ['इंडिक्ट्रांस', 'लिबिंदिक', 'हैदराबाद', 'यूनिवर्सिटी', 'भाग्यालक्ष्मी', 'भारत', 'मोरोक्को']
    >>> h2t_rb = Transliterator(source='hin', target='tel', rb=True) # Rule-Based
    >>> h2m_rb = Transliterator(source='hin', target='mal', rb=True) # Rule-Based
    >>> h2ta_rb = Transliterator(source='hin', target='tam', rb=True) # Rule-Based
    >>> h2t_ml = Transliterator(source='hin', target='tel', rb=False) # ML
    >>> h2m_ml = Transliterator(source='hin', target='mal', rb=False) # ML
    >>> h2ta_ml = Transliterator(source='hin', target='tam', rb=False) # ML
    >>> list(map(h2t_ml.transform, hin_text))
    ['ఇండిక్ట్రాంస్', 'లిబిందిక', 'హైదరాబాద్', 'యూనివర్శిటీ', 'భాగ్యాలక్ష్మి', 'భారత్', 'మోరోక్కో']
    >>> list(map(h2t_rb.transform, hin_text))
    ['ఇండిక్ట్రాంస', 'లిబిందిక', 'హైదరాబాద', 'యూనివర్సిటీ', 'భాగ్యాలక్ష్మీ', 'భారత', 'మోరోక్కో']
    >>> list(map(h2ta_rb.transform, hin_text))
    ['இங்டிக்ட்ராங்ஸ', 'லிபிங்திக', 'ஹைதராபாத', 'யூநிவர்ஸிடீ', 'பாக்யாலக்ஷ்மீ', 'பாரத', 'மோரோக்கோ']
    >>> list(map(h2ta_ml.transform, hin_text))
    ['இண்டிக்ட்ராங்ஸ்', 'லிபிந்திக்', 'ஹைதராபாத்', 'யூனிவர்சிடி', 'பாக்யாலக்ஷ்மி', 'பாரதப்', 'மோரோக்கோ']
    >>> list(map(h2m_rb.transform, hin_text))
    ['ഇംഡിക്ട്രാംസ', 'ലിബിംദിക', 'ഹൈദരാബാദ', 'യൂനിവര്സിടീ', 'ഭാഗ്യാലക്ഷ്മീ', 'ഭാരത', 'മോരോക്കോ']
    >>> list(map(h2m_ml.transform, hin_text))
    ['ഇന്ഡിക്ട്രാംസ്', 'ലിബിന്ദിക', 'ഹൈദരാബാദ്', 'യൂനിവര്സിടി', 'ഭാഗ്യാലക്ഷ്മി', 'ഭാരത', 'മോരോക്കോ']

Transliterate from Console
--------------------------

You can transliterate text files directly using the console shortcut ``indictrans``.

.. code-block:: bash

    $ indictrans --h

    -h, --help          show this help message and exit
    -v, --version       show program's version number and exit
    -s, --source        select language (3 letter ISO-639 code) {hin, guj, pan,
                        ben, mal, kan, tam, tel, ori, eng, mar, nep, bod, kok,
                        asm, urd}
    -t, --target        select language (3 letter ISO-639 code) {hin, guj, pan,
                        ben, mal, kan, tam, tel, ori, eng, mar, nep, bod, kok,
                        asm, urd}
    -b, --build-lookup  build lookup to fasten transliteration
    -i, --input         <input-file>
    -o, --output        <output-file>


    $ indictrans < hindi.txt --s hin --t eng --build-lookup > hindi-rom.txt
    $ indictrans < roman.txt --s hin --t eng --build-lookup > roman-hin.txt

    $ echo 'indictrans libindic hyderabad university bhagyalakshmi bharat morocco' |\\
     indictrans -s eng -t hin | indictrans -s hin -t tel -r # RULE-BASED
    ఇండిక్ట్రాంస లిబిందిక హైదరాబాద యూనివర్సిటీ భాగ్యాలక్ష్మీ భారత మోరోక్కో
