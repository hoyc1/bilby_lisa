Installation instructions
=========================

``bilby_lisa`` can be installed through a variety of methods, see below.
Independent of the method chosen, we recommend installing ``bilby_lisa`` within
a conda environment. For speed, we recommend creating an environment with
`mamba <https://mamba.readthedocs.io/en/latest/>`_. An environment can be
created with,

.. code-block:: console

    $ mamba create --name bilby-lisa python=3.10

``bilby_lisa`` can then be installed with,

.. tabs::

    .. tab:: mamba

        .. code-block::

             $ mamba install -c conda-forge bilby_lisa

    .. tab:: PyPI

        If installing with ``pip``, additional dependencies need to be
        installed for compatibility with the
        `bbhx <https://github.com/mikekatz04/BBHx>`_ package (a package used for
        waveform generation). The additional dependencies can be installed with,

        .. code-block:: console

            $ mamba install numpy schwimmbad gcc_linux-64 gxx_linux-64 gsl lapack=3.6.1 Cython

        .. note::

            If on MACOSX, substitue ``gcc_linux-64`` and ``gxx_linux-64`` with
            ``clang_osx-64`` and ``clangxx_osx-64``.

        ``bilby_lisa`` can then be installed with,

        .. code-block::

            $ python -m pip install bilby_lisa[parallel]

        .. note::

            If you do not wish to use/install ``parallel_bilby``, you can
            remove ``[parallel]`` from the ``pip install`` command above.

    .. tab:: From source

        If installing with ``pip``, additional dependencies need to be
        installed for compatibility with the
        `bbhx <https://github.com/mikekatz04/BBHx>`_ package (a package used for
        waveform generation). The additional dependencies can be installed with,

        .. code-block:: console

            $ mamba install numpy schwimmbad gcc_linux-64 gxx_linux-64 gsl lapack=3.6.1 Cython

        .. note::

            If on MACOSX, substitue ``gcc_linux-64`` and ``gxx_linux-64`` with
            ``clang_osx-64`` and ``clangxx_osx-64``.

        ``bilby_lisa`` can then be installed with,

        .. code-block::

            $ git clone git@github.com:hoyc1/bilby_lisa.git
            $ cd bilby_lisa
            $ python -m pip install .[parallel]

        .. note::

            If you do not wish to use/install ``parallel_bilby``, you can
            remove ``[parallel]`` from the ``pip install`` command above.

Once ``bilby_lisa`` has been installed, non-released versions of ``bilby``,
``bilby_pipe`` and ``parallel_bilby`` need to be installed. This is because we
are waiting for required code to be merged into the main ``bilby``,
``bilby_pipe`` and ``parallel_bilby`` code bases. Please see the following
merge requests for details:

* `bilby!1314 <https://git.ligo.org/lscsoft/bilby/-/merge_requests/1314>`_
* `bilby_pipe!583 <https://git.ligo.org/lscsoft/bilby_pipe/-/merge_requests/583>`_
* `bilby_pipe!586 <https://git.ligo.org/lscsoft/bilby_pipe/-/merge_requests/586>`_
* `parallel_bilby!137 <https://git.ligo.org/lscsoft/parallel_bilby/-/merge_requests/137>`_
* `parallel_bilby!138 <https://git.ligo.org/lscsoft/parallel_bilby/-/merge_requests/138>`_

The required non-released versions of ``bilby``, ``bilby_pipe`` and
``parallel_bilby`` can be installed with:

.. tabs::

    .. tab:: pip

        .. code-block:: console

            $ python -m pip install --force-reinstall "git+https://git.ligo.org/charlie.hoy/bilby.git@ifo_plugin" "git+https://git.ligo.org/charlie.hoy/bilby_pipe.git@input_plus_det_plugin" "git+https://git.ligo.org/charlie.hoy/parallel_bilby.git@input_plus_parser"

    .. tab:: From source

        .. code-block:: console

            $ git clone git@github.com:hoyc1/bilby_lisa.git
            $ cd bilby_lisa
            $ python -m pip install -r requirements.txt --force-reinstall

Finally, the `bbhx <https://github.com/mikekatz04/BBHx>`_ package used for
waveform generation can be installed with,

.. code-block:: console

    $ python -m pip install "git+https://github.com/mikekatz04/BBHx.git"

The non-released versions of ``bilby``, ``bilby_pipe`` and ``parallel_bilby``
are rebased onto the following tags:

* ``bilby``: `v2.2.2 <https://git.ligo.org/lscsoft/bilby/-/tags/v2.2.2>`_
* ``bilby_pipe``: `v1.3.0 <https://git.ligo.org/lscsoft/bilby_pipe/-/tags/v1.3.0>`_
* ``parallel_bilby``: `v2.0.2 <https://git.ligo.org/lscsoft/parallel_bilby/-/tags/v2.0.2>`_
