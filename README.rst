SingleCellFusion
================

SingleCellFusion is a package for computational integration and analysis of single cell multiomics data sets, including  transcriptom (RNA-Seq), DNA methylome (mC-Seq), and chromatin accessibility (ATAC-Seq). For a given pair of data sets, SingleCellFusion finds the best matching pairs of cells in each modality (i.e. nearest neighbors) by taking advantage of the correlation of gene expression with epigenomic marks across the gene body. Neighbors are used to impute counts for each data set. For example, if integrating scRNA-seq and snATAC-seq cells, SingleCellFusion will generate imputed
scRNA-seq counts for the snATAC-seq profiled cells and snATAC-seq counts for the scRNA-seq profiled cells.
Cells profiled by each technique can then be analyzed together in a joint, lower dimensional space.


The package is still under active development and function parameters will continue to change over time.


Requirements
------------
* python 3
* loompy
* numpy
* scikit-learn
* scipy
* pandas
* numba


Installation
------------
Currently, the only method of installing SingleCellFusion is to clone the github repository.
Enter the directory where you would like to install SingleCellFusion and enter
the following commands on the command line::

    git clone https://github.com/mukamel-lab/SingleCellFusion.git
    cd SingleCellFusion
    python setup.py install

If you have trouble with dependencies, we have a
`guide <https://github.com/mukamel-lab/mop/blob/master/docs/mop_conda_guide.rst>`_
to generating a usable conda environment in SingleCellFusion's sister repository
`MoP <https://github.com/mukamel-lab/mop/>`_.

Basic Usage
-----------
SingleCellFusion is built on a loompy backbone, an efficient file format for storing multiomics data
developed by the Sten Linnarsson Lab (`loompy.org <http://loompy.org/>`_). SingleCellFusion requires
that for each pair of data sets (X and Y), there is a loom file with with a layer containing the
observed count data for that data set (typically normalized), and a row attribute containing unique
feature identifiers.

For each pair of samples, imputed counts can be generated by running the following code::

    import SingleCellFusion as scf
    scf.recipes.pairwise_impute(loom_x,
                                observed_x,
                                imputed_x,
                                pca_attr_x,
                                loom_y,
                                observed_y,
                                imputed_y,
                                pca_attr_y,
                                correlation='positive',
                                neighbor_method='mnn',
                                perform_pca_x=True,
                                perform_pca_y=True,
                                n_pca=50,
                                var_measure_x='vmr',
                                var_measure_y='vmr')


For the passed parameters:

    * loom_x and loom_y are the paths to the loom files for each data set
    * observed_x and observed_y are the layers containing the observe ddata
    * imputed_x and imputed_y are the names for the output layers containing imputed counts
    * pca_attr_x and pca_attr_y are column attributes containing principal components
    * perform_pca_x and perform_pca_y specifies if pca_attr_x and pca_attr_y should be generated by SingleCellFusion
    * n_pca is the number of principal components if perform_pca_x or perform_pca_y
    * correlation is the expected correlation in counts between data X and data (positive or + for transcriptome and chromatin accessibility, negative or - for methylome and transcriptome)
    * neighbor_method is the method for finding nearest neighbors across modalities (mnn for direct mutual nearest neighbors, rescue for direct and indirect mutual nearest neighbors, knn for k-nearest neighbors)
    * var_measure_x and var_measure_y define the method for identifying highly variable features in the data (vmr for variance mean ration, sd for standard deviation)

After this function is run it will add imputed_x to loom_x and imputed_y to loom_y.
These imputed counts can be used to perform clustering and data reduction in the space of data X
(using imputed counts for data Y and observed counts for data X), or in the space of data Y.

Tutorials and FAQs
-------------------
Our `FAQs <docs/faqs.rst>`_ have some basic information on running SingleCellFusion.

For a brief description of how SingleCellFusion works please check out this
`link <docs/scf_description.rst>`_.

If you need information on performing preliminary analyses on loom files, please check out
SingleCellFusion's sister repository `MoP <https://github.com/mukamel-lab/mop/>`_.


Authors
-------

`SingleCellFusion` was written by `Wayne Doyle <widoyle@ucsd.edu>`_,
`Fangming Xie <f7xie@ucsd.edu>`_, `Ethan Armand <earmand@ucsd.edu>`_.
All authors are members of the `Mukamel Lab <https://brainome.ucsd.edu>`_.


Acknowledgments
---------------
We are grateful for support from the Chan-Zuckerberg Initiative and from the NIH
BRAIN Initiative U19 Center for Epigenomics of the Mouse Brain Atlas
(`CEMBA <https://biccn.org/teams/u19-ecker/>`_).
