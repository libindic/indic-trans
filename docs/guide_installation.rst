Installation
============

Dependencies
~~~~~~~~~~~~

`indictrans`_ requires `cython`_, and `SciPy`_.

.. _`indictrans`: https://github.com/libindic/indic-trans

.. _`cython`: http://docs.cython.org/src/quickstart/install.html

.. _`Scipy`: http://www.scipy.org/install.html

Install dependencies:
---------------------

::

    pip install -r requirements.txt


Download
~~~~~~~~

Download **indictrans**  from `github`_.

.. _`github`: https://github.com/libindic/indic-trans


Direct Install
~~~~~~~~~~~~~~

::

    pip install git+git://github.com/irshadbhat/indic-trans.git
    ----------------------------OR-----------------------------
    pip install git+git://github.com/libindic/indic-trans.git    


Clone and Install
~~~~~~~~~~~~~~~~~

::

    Clone the repository:
        git clone https://github.com/libindic/indictrans.git
        ------------------------OR--------------------------
        git clone https://github.com/irshadbhat/indictrans.git
    Change to the cloned directory:
        cd indictrans
    Run setup.py to create installable source:
        python setup.py sdist
    Install using pip:
        pip install dist/indictrans*.tar.gz
