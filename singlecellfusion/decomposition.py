"""
Functions used to perform dimensionality reduction on loom files

Written by Wayne Doyle

(C) 2018 Mukamel Lab GPLv2
"""
import loompy
import numpy as np
import pandas as pd
from sklearn.decomposition import IncrementalPCA
from fitsne import FItSNE
import umap
import logging
import time
from . import loom_utils
from . import general_utils

# Start log
decomp_log = logging.getLogger(__name__)


def prep_pca(view,
             layer,
             row_idx,
             scale_attr=None):
    """
    Performs data processing for PCA on a given layer
    
    Args:
        view (object): Slice of loom file
        layer (str): Layer in view
        row_idx (array): Features to use
        scale_attr (str): If true, scale cells by this attribute
            Typically used in snmC-seq to scale by a cell's mC/C
    
    Returns:
        dat (matrix): Scaled data for PCA
    """
    dat = view.layers[layer][row_idx, :].copy()
    if scale_attr is not None:
        rel_scale = view.ca[scale_attr]
        dat = np.divide(dat, rel_scale)
    dat = dat.transpose()
    return dat


def batch_pca(loom_file,
              layer,
              out_attr='PCA',
              col_attr=None,
              row_attr=None,
              scale_attr=None,
              n_pca=50,
              drop_first=False,
              batch_size=512,
              verbose=False):
    """
    Performs incremental PCA on a loom file
    
    Args:
        loom_file (str): Path to loom file
        layer (str): Layer containing data for PCA
        out_attr (str): Name of PCA attribute
            Valid_{out_attr} will also be added to indicate used cells
        col_attr (str): Optional, only use cells specified by col_attr
        row_attr (str): Optional, only use features specified by row_attr
        scale_attr (str): Optional, attribute specifying cell scaling factor
        n_pca (int): Number of components for PCA
        drop_first (bool): Drops first PC
            Useful if the first PC correlates with a technical feature
            If true, a total of n_pca is still generated and added to loom_file
            If true, the first principal component will be lost
        batch_size (int): Number of elements per chunk
        verbose (bool): If true, print logging messages
    
    Returns:
        Adds componenets to ds.ca.{out_attr}
        Adds quality control to ds.ca.Valid_{out_attr}
    """
    if verbose:
        decomp_log.info('Fitting PCA')
        t_start = time.time()
    if drop_first:
        n_tmp = n_pca + 1
    else:
        n_tmp = n_pca
    pca = IncrementalPCA(n_components=n_tmp)
    with loompy.connect(loom_file) as ds:
        ds.ca[out_attr] = np.zeros((ds.shape[1], n_pca), dtype=float)
        n = ds.ca[out_attr].shape[0]
        # Get column and row indices
        col_idx = loom_utils.get_attr_index(loom_file=loom_file,
                                            attr=col_attr,
                                            columns=True,
                                            inverse=False)
        row_idx = loom_utils.get_attr_index(loom_file=loom_file,
                                            attr=row_attr,
                                            columns=False,
                                            inverse=False)
        # Fit model
        layers = loom_utils.make_layer_list(layers=layer)
        for (_, _, view) in ds.scan(items=col_idx,
                                    layers=layers,
                                    axis=1,
                                    batch_size=batch_size):
            dat = prep_pca(view=view,
                           layer=layer,
                           row_idx=row_idx,
                           scale_attr=scale_attr)
            pca.partial_fit(dat)
        if verbose:
            t_fit = time.time()
            time_run, time_fmt = general_utils.format_run_time(t_start, t_fit)
            decomp_log.info('Fit PCA in {0:.2f} {1}'.format(time_run, time_fmt))
        # Transform
        for (_, selection, view) in ds.scan(items=col_idx,
                                            layers=layers,
                                            axis=1,
                                            batch_size=batch_size):
            dat = prep_pca(view=view,
                           layer=layer,
                           row_idx=row_idx,
                           scale_attr=scale_attr)
            dat = pca.transform(dat)
            if drop_first:
                dat = dat[:, 1:]
            mask = selection == np.arange(n)[:, None]
            ds.ca[out_attr] += mask.dot(dat)
        # Add to file
        if col_attr:
            ds.ca['Valid_{}'.format(out_attr)] = ds.ca[col_attr]
        else:
            ds.ca['Valid_{}'.format(out_attr)] = np.ones((ds.shape[1],),
                                                         dtype=int)
        # Log
        if verbose:
            t_tran = time.time()
            time_run, time_fmt = general_utils.format_run_time(t_fit, t_tran)
            decomp_log.info(
                'Reduced dimensions in {0:.2f} {1}'.format(time_run, time_fmt))


