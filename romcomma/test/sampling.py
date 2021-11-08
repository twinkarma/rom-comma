#  BSD 3-Clause License.
#
#  Copyright (c) 2019-2021 Robert A. Milton. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this
#     software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
#  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Contains Sampling and Design of Experiments functionality. #

from __future__ import annotations

from romcomma.typing_ import *
import numpy as np
import scipy.stats


def latin_hypercube(N: int, M: int, is_centered: bool = False):
    """ Latin Hypercube Sample.

    Args:
        N: The number of samples (datapoints).
        M: The dimensionality of the hypercube.
        is_centered: Boolean value whether to centre each sample in its Latin Hypercube cell.
            Default is False, which locates the sample randomly within its cell.
    Returns: An (N,M) matrix of N datapoints of dimension M.
    """
    return scipy.stats.qmc.LatinHypercube(M, centered=is_centered).random(N)


def multivariate_gaussian_noise(N: int, variance: NP.MatrixLike) -> NP.Matrix:
    """ Generate N datapoints of L-dimensional Gaussian noise, sampled from N[0, variance].

    Args:
        N: Number of samples (datapoints).
        variance: Variance matrix. The given matrix must be symmetric positive-definite.
            A vector is interpreted as a diagonal matrix.
    Returns: An (N,L) noise matrix, where (L,L) is the shape of `variance`.
    """
    variance = np.atleast_2d(variance)
    if variance.shape[0] == 1 and len(variance.shape) == 2:
        variance = np.diagflat(variance)
    elif variance.shape[0] != variance.shape[1] or len(variance.shape) > 2:
        raise IndexError(f'variance.shape = {variance.shape} should be (L,) or (L,L).')
    result = scipy.stats.multivariate_normal.rvs(mean=None, cov=variance, size=N)
    result.shape = (N, variance.shape[1])
    return result
