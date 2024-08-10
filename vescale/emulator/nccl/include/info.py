################################################################################
#
# Copyright 2023 ByteDance Ltd. and/or its affiliates. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
################################################################################
# Some code comes from info.h in NCCL
# Original license:
# Copyright (c) 2016-2022, NVIDIA CORPORATION. All rights reserved.
#
# See LICENSE.txt for license information
################################################################################

from dataclasses import dataclass
from typing import Any

import torch

from vescale.emulator.nccl.constants import NcclFunc, NcclPattern
from vescale.emulator.nccl.include.comm import NcclComm


@dataclass
class NcclInfo:
    coll: NcclFunc
    comm: NcclComm
    chunkSteps: int
    sliceSteps: int
    nChannels: int = 0
    nThreads: int = 0
    nBytes: int = 0
    algorithm: int = -1
    protocol: int = -1
    count: int = 0
    datatype: Any = torch.float32
    pattern: NcclPattern = NcclPattern.Ring
    nstepsPerLoop: int = 1
    nchunksPerLoop: int = 1


def nccl_info_set_derived(info: NcclInfo, nRanks: int):
    info.nBytes = info.count * info.datatype.itemsize
    if info.coll == NcclFunc.ncclFuncAllGather or info.coll == NcclFunc.ncclFuncBroadcast:
        info.count = info.nBytes
        info.datatype = torch.int8
    if info.coll == NcclFunc.ncclFuncAllGather or info.coll == NcclFunc.ncclFuncReduceScatter:
        info.nBytes *= nRanks
    return info
