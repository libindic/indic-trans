Model Setup & Training
======================

.. _example-train:

Train and Test
--------------

Assuming your data is in ``tnt`` format you can encode the data ane train a :class:`indictrans.trunk.StructuredPerceptron` classifier.

.. code-block:: python

    >>> from indictrans import trunk
    >>> #load trianing data
    ... X, y = trunk.load_data('indictrans/trunk/tests/hin2rom.tnt')
    >>> #build ngram-context
    ... X = trunk.build_context(X, ngram=4)
    >>> #fit encoder
    ... enc, X = trunk.fit_encoder(X)
    >>> #train structured-perceptron model
    ... clf = trunk.train_sp(X, y, n_iter=5, verbose=2)
    Iteration 1 ...
    Train-set error = 1.5490
    Iteration 2 ...
    Train-set error = 1.0040
    Iteration 3 ...
    Train-set error = 0.8030
    Iteration 4 ...
    Train-set error = 0.6900
    Iteration 5 ...

This will train the perceptron for 5 epochs (specified via the ``n_iter`` parameter).

Then you can use the trained classifier as follows:

.. code-block:: python

    >>> #load testing data
    ... X_test, y = trunk.load_data('indictrans/trunk/tests/hin2rom.tnt')
    >>> #build ngram-context for testing data
    ... X_test = trunk.build_context(X_test, ngram=4) # ngram value should be same as for train-set
    >>> #encode test-set
    ... X_test = [enc.transform(x) for x in X_test]
    >>> #predict output sequences
    ... y_ = clf.predict(X_test)
    >>> y[10]  # True
    [u'c', u'l', u'a', u'ne', u'_']
    >>> y_[10]  # Predicted
    [u'c', u'l', u'a', u'n', u'_']
    >>> y_[100]  # True
    [u'p', u'a', u'r', u'aa', u'n', u'd', u'e']
    >>> y_[100]  # Predicted
    [u'p', u'a', u'r', u'aa', u'n', u'd', u'e']

Note that you need to ``build-context`` using the same ``ngram`` value as used for trainig data. Also you need to ``encode`` test data using the encoder ``enc`` developed on training data.

.. _example-train-from-console:

Train directly from Console
---------------------------

`indictrans-trunk` provides a much easier way to train, test and save models directly from console.

.. code-block:: bash

    user@indic-trans$ indictrans-trunk --help

    -d , --data-file      training data-file: set of sequences
    -o , --output-dir     output directory to dump trained models
    -n , --ngrams         ngram context for feature extraction: default 4
    -e , --lr-exp         The Exponent used for inverse scaling oflearning rate:
                          default 0.1
    -m , --max-iter       Maximum number of iterations for training: default 15
    -r , --random-state   Random seed for shuffling sequences within each
                          iteration.
    -l , --verbosity      Verbosity level: default 0 (quiet moe)
    -t , --test-file      testing data-file: optional: stores output sequences
                          in `test_file.out`

    user@indic-trans$ indictrans-trunk -d hin2rom.tnt -o /tmp/rom-ind/ -n 4 -e 0.1 -m 5 -l 3 -t hin2rom.tnt
    Iteration 1 ... 
    First sequence comparision: 0-27 0-95 0-30 0-10 ... loss: 4
    Train-set error = 1.8090
    Iteration 2 ... 
    First sequence comparision: 120-46 86-86 63-63 120-120 95-95 123-123 10-10 ... loss: 1
    Train-set error = 0.6560
    Iteration 3 ... 
    First sequence comparision: 123-123 110-110 40-40 46-46 ... loss: 0
    Train-set error = 0.3820
    Iteration 4 ... 
    First sequence comparision: 2-2 95-95 86-86 77-77 64-64 31-31 120-120 80-80 10-10 ... loss: 0
    Train-set error = 0.2240
    Iteration 5 ... 
    First sequence comparision: 40-40 120-120 31-31 120-120 125-125 120-120 123-123 117-117 31-31 120-120 ... loss: 0
    Train-set error = 0.1540

    Testing ...

Assuming ``hin2rom.tnt`` was given as ``test-file``, the output file will be generated with the name ``hin2rom.tnt.out``.
