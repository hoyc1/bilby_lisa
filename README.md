# bilby_lisa

## Description

Plug in for [`bilby`](https://lscsoft.docs.ligo.org/bilby/) to perform Bayesian
inference with LISA. See [this paper](https://arxiv.org/abs/2312.13039) for
details.

## Citing

If you make use of this code, please cite the
[`bilby_lisa` paper](https://arxiv.org/abs/2312.13039)

```
@article{Hoy:2023ndx,
    author = "Hoy, Charlie and Nuttall, Laura K.",
    title = "{BILBY in space: Bayesian inference for transient gravitational-wave signals observed with LISA}",
    eprint = "2312.13039",
    archivePrefix = "arXiv",
    primaryClass = "astro-ph.IM",
    month = "12",
    year = "2023"
}
```

## Installation instructions

We recommend installing `bilby_lisa` with
[`mamba`](https://mamba.readthedocs.io/en/latest/). To install `bilby_lisa`
with mamba, simply run,

```bash
$ mamba create --name bilby-lisa python=3.10 -c conda-forge bilby_lisa
```

To install `bilby_lisa` with PyPI, an environment must first be created with
certain required dependencies in order to compile
[`bbhx`](https://github.com/mikekatz04/BBHx). An environment can be created
with,

```bash
$ mamba create --name bilby-lisa python=3.10 numpy schwimmbad gcc_linux-64 gxx_linux-64 gsl lapack=3.6.1 Cython
```

If on MACOSX, substitue `gcc_linux-64` and `gxx_linux-64` with `clang_osx-64`
and `clangxx_osx-64`. The latest stable release of `bilby_lisa` can then be
installed with PyPI,

```bash
(bilby-lisa)$ python -m pip install bilby_lisa
```

If you wish to install from source, you can clone the git repository, navigate
to the root source directory and run,

```bash
(bilby-lisa)$ python -m pip install .
```

Once `bilby_lisa` has been installed, non-released versions of `bilby`,
`bilby_pipe` and `parallel_bilby` need to be installed. This is because we
are waiting for required code to be merged into the main `bilby`, `bilby_pipe`
and `parallel_bilby` code bases. Please see the following merge requests for
details:

* [bilby!1314](https://git.ligo.org/lscsoft/bilby/-/merge_requests/1314)
* [bilby_pipe!583](https://git.ligo.org/lscsoft/bilby_pipe/-/merge_requests/583)
* [bilby_pipe!586](https://git.ligo.org/lscsoft/bilby_pipe/-/merge_requests/586)
* [parallel_bilby!137](https://git.ligo.org/lscsoft/parallel_bilby/-/merge_requests/137)
* [parallel_bilby!138](https://git.ligo.org/lscsoft/parallel_bilby/-/merge_requests/138)

The required non-released versions of `bilby`, `bilby_pipe` and
`parallel_bilby` can be installed with:

```bash
$ python -m pip install --force-reinstall "git+https://git.ligo.org/charlie.hoy/bilby.git@ifo_plugin" "git+https://git.ligo.org/charlie.hoy/bilby_pipe.git@input_plus_det_plugin" "git+https://git.ligo.org/charlie.hoy/parallel_bilby.git@input_plus_parser"
```

and the [`bbhx`](https://github.com/mikekatz04/BBHx) package can be installed
with,

```bash
$ python -m pip install "git+https://github.com/mikekatz04/BBHx.git"
```

Alternatively, you can clone the git repository, navigate to the root
source directory and run,

```bash
$ python -m pip install -r requirements.txt --force-reinstall
```

The non-released versions of `bilby`, `bilby_pipe` and `parallel_bilby` are
rebased onto the following tags:

* `bilby`: [v2.2.2](https://git.ligo.org/lscsoft/bilby/-/tags/v2.2.2)
* `bilby_pipe`: [v1.3.0](https://git.ligo.org/lscsoft/bilby_pipe/-/tags/v1.3.0)
* `parallel_bilby`: [v2.0.2](https://git.ligo.org/lscsoft/parallel_bilby/-/tags/v2.0.2)
