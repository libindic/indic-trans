===========
indic-trans
===========

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

a. Text:
""""""""

.. code:: python

    >>> from indictrans import transliterator
    >>> trn = transliterator(source='hin', target='eng')
    >>> 
    >>> text = """कांग्रेस पार्टी अध्यक्ष सोनिया गांधी, तमिलनाडु की मुख्यमंत्री जयललिता और रिज़र्व बैंक के गवर्नर रघुराम राजन के बीच एक समानता है.
    ... ये सभी अलग-अलग कारणों से भारतीय जनता पार्टी के राज्यसभा सांसद सुब्रमण्यम स्वामी के निशाने पर हैं.
    ... उनके जयललिता और सोनिया गांधी के पीछे पड़ने का कारण कथित भ्रष्टाचार है.
    ... उनका ताज़ा शिकार हैं रघुराम राजन. दो सप्ताह पहले सुब्रमण्यम स्वामी ने प्रधानमंत्री को लिखी एक चिठ्ठी में गवर्नर को तुरंत हटाने की मांग की थी. तब से उन्होंने अपनी इस मांग को कई बार दुहराया है. मीडिया और सार्वजनिक सभाओं में इसकी चर्चा की है.
    ... आखिर स्वामी राजन का विरोध क्यों कर रहे हैं? या जैसा कि एक साथी ने कहा, एक तमिल ब्राह्मण दूसरे तमिल ब्राह्मण के पीछे हाथ धोकर क्यों पड़ा है?
    ... ज़ाहिरा तौर पर इसका कारण प्रधानमंत्री को भेजी गयी उनकी चिठ्ठी में दर्ज है. अपनी इस चिट्ठी में उन्होंने आरोप लगाया है कि रघुराम राजन मानसिक रूप से पूरी तरह भारतीय नहीं हैं और उन्होंने जानबूझ कर भारतीय अर्थव्यवस्था को नुक़सान पहुँचाया है.
    ... सुब्रमण्यम स्वामी ने ये भी इल्ज़ाम लगाया कि दो सालों में सरकारी बैंकों का 'बैड लोन' बढ़कर साढ़े तीन लाख करोड़ हो गया है. स्वामी ने राजन को तुरंत हटाए जाने की मांग करते हुए कहा कि उनके पास ग्रीन कार्ड है, जिसे रिन्यू कराने के लिए वो अमरीका भी गए थे.
    ... हालाँकि, ग्रीन कार्ड अमरीका में बेरोकटोक रहने और काम करने के लिए विदेश से आए लोगों को दिया जाता है. ग्रीन कार्ड किसी के अमरीका का नागरिक होने का प्रमाण नहीं है. फ़िलहाल रघुराम राजन ने स्वामी के आरोपों के बारे में सार्वजनिक तौर पर कोई टिप्पणी नहीं की है.
    ... सितंबर 2013 में तत्कालीन यूपीए की सरकार ने रघुराम राजन को तीन साल के लिए रिजर्व बैंक का गवर्नर नियुक्त किया था. उनका कार्यकाल सितम्बर में ख़त्म हो रहा है, इस बात को लेकर अटकलें लगाई जा रही हैं कि उनका कार्यकाल बढ़ाया जाएगा या नहीं.
    ... सुब्रमण्यम स्वामी और रघुराम राजन में कई बातें सामान हैं. दोनों तमिल ब्राह्मण होने के अलावा अमरीका में प्रसिद्ध यूनिवर्सिटियों में पढ़ने और पढ़ाने का लंबा अनुभा रखते हैं.
    ... राजन अपनी यूनिवर्सिटी से तीन साल की छुट्टी पर हैं. दोनों प्रतिभाशाली और मेधावी हैं, दोनों अर्थशास्त्र में महारत रखते हैं और दो टूक शब्दों में बोलने के लिए जाने जाते हैं.
    ... लेकिन स्वामी और राजन के बीच समानता के बावजूद इनके बीच कई बातें असमान हैं. स्वामी विवादास्पद बयानों में महारत रखते हैं. उनका चरित्र साफ़ है लेकिन दिमाग़ में क्रोध है. अहंकार उनकी एक बड़ी कमज़ोरी मानी जाती है.
    ... दूसरी तरफ राजन भी बोलने के लिए जाने जाते हैं लेकिन वो अपनी सीमाएं पार करके बयानबाज़ी नहीं करते, डंका पीटे बगैर अपनी बातें कह डालते हैं. उनकी मौद्रिक नीति में कमियां हो सकती हैं लेकिन वो इसे आसानी से नहीं मानते.
    ... दिलचस्प बात ये है कि स्वामी के हमलों से राजन की लोकप्रियता बढ़ी है. भाजपा में स्वामी को अधिकतर नेता पसंद नहीं करते, वित्त मंत्री राजन के पक्ष में सामने आए हैं. भाजपा अध्यक्ष अमित शाह ने उन्हें सार्वजनिक तौर पर समर्थन नहीं दिया है. प्रधानमंत्री ने गवर्नर की प्रशंसा की है.
    ... कहा जाता है कि स्वामी की राज्यसभा में लाने के पीछे आरएसएस का हाथ है, आरएसएस के वो काफी करीब रहे हैं.
    ... दोनों की लड़ाई में जीत किसकी होगी ये बताना मुश्किल है. ये हार जीत की लड़ाई लगती भी नहीं है लेकिन अब तक इससे नुकसान केवल स्वामी को ही हुआ है."""
    >>>
    >>> print trn.transform(text)
    congress party adhyaksh soniya gandhi, tamilnadu kee mukhyamantri jayalalita or reserve baink kee governor raghuram rajan kee bich ek samaantha he.
    ye sabhi alag-alag kaaranon se bhaarateey janatha party kee rajyasabha saansad subramanyam swaami kee nishaane par hem.
    unke jayalalita or soniya gandhi kee peeche padane kaa kaaran kathith bhrashtachar he.
    unka taza shikaar hem raghuram rajan. do saptah pehale subramanyam swaami nae pradhanmantri ko likhi ek chiththi mem governor ko turant hataane kee mang kee thi. tab se unhonne apane is mang ko kai bar duharaya he. media or sarvajanik sabhaon mem isaki charcha kee he.
    akhir swaami rajan kaa virodh kyon kar rahe hem? ya jaisaa ki ek saathi nae kahaa, ek tamil brahman doosare tamil brahman kee peeche haath dhokar kyon pada he?
    zahira tor par iskaa kaaran pradhanmantri ko bheji gayi unki chiththi mem darj he. apane is chitthi mem unhonne arope lagaaya he ki raghuram rajan maansik ruup se poori tarah bhaarateey nahin hem or unhonne janbujh kar bhaarateey arthvyavastha ko nuqasaan pahunchaaya he.
    subramanyam swaami nae ye bhee ilzaam lagaaya ki do saalo mem sarakaari bainkon kaa 'bed lon' badhakar saadhe tin lakh karod ho gaya he. swaami nae rajan ko turant hataaye jane kee mang karate hue kahaa ki unke paas green card he, jise rineau karaane kee lie wo america bhee gae the.
    haalaanki, green card america mem berocatok rahene or kaam karane kee lie videsh se aae logo ko diya jaata he. green card kaise kee america kaa naagarik hone kaa praman nahin he. filhal raghuram rajan nae swaami kee aropon kee bare mem sarvajanik tor par koi tippni nahin kee he.
    sitamber 2013 mem tatkalin upie kee sarakaar nae raghuram rajan ko tin sal kee lie reserve baink kaa governor niyukt kiya tha. unka kaaryakaal sitambar mem katm ho raha he, is baat ko leekar atakalen lagaay zaa rahi hem ki unka kaaryakaal badhaayaa jaaega ya nahin.
    subramanyam swaami or raghuram rajan mem kai baten saaman hem. dono tamil brahman hone kee alaava america mem prasiddh uniwarsitiyon mem padhane or padhaane kaa lanbaa anubha rakhte hem.
    rajan apane uniwarsity se tin sal kee chhutti par hem. dono pratibhashali or medhaavi hem, dono arthshastra mem maharath rakhte hem or do tuuk shabdon mem bolane kee lie jane jate hem.
    lekin swaami or rajan kee bich samaantha kee bawajood inke bich kai baten asaman hem. swaami vivaadaspad bayaanon mem maharath rakhte hem. unka charitra saaf he lekin dimaag mem krodh he. ahankaar unki ek badi kamazori maani jaate he.
    duusari taraf rajan bhee bolane kee lie jane jate hem lekin wo apane simaaen paar karake bayanbazi nahin karate, danka peete bagair apane baten kah daalate hem. unki maudrik neeti mem kamiyaan ho sakati hem lekin wo ise aasaani se nahin maante.
    dilachasp baat ye he ki swaami kee hamalon se rajan kee locapriyata badhi he. bhajpa mem swaami ko adhiktar netaa pasand nahin karate, vitt mantri rajan kee paksha mem samne aae hem. bhajpa adhyaksh amit shah nae unhen sarvajanik tor par samarthan nahin diya he. pradhanmantri nae governor kee prashansa kee he.
    kahaa jaata he ki swaami kee rajyasabha mem laane kee peeche areses kaa haath he, areses kee wo caphi karib rahe hem.
    dono kee ladaayi mem jeet kisaki hogee ye bataana mushkil he. ye haar jeet kee ladaayi lagati bhee nahin he lekin ab tak isse nuksaan keval swaami ko hee hua he.
    >>> 

