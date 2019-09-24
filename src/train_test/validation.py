"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.

FALCON: FAst and Lightweight CONvolution

File: train_test/validation.py
 - Contain validation code for execution for model.

Version: 1.0
"""

import torch
import torch.nn.functional as F

import time


def validation(net, val_loader, log=None):
    """
    Validation process.
    :param net: model to be trained
    :param val_loader: validation data loader
    :param log: log dir
    """

    # set testing mode
    net.eval()

    correct = 0
    total = 0
    inference_start = time.time()
    with torch.no_grad():
        for i, data in enumerate(val_loader, 0):
            inputs, labels = data
            outputs, outputs_conv = net(inputs.cuda())
            _, predicted = torch.max(F.softmax(outputs, -1), 1)
            total += labels.size(0)
            correct += (predicted == labels.cuda()).sum()
    inference_time = time.time() - inference_start
    accuracy = float(100) * float(correct) / float(total)

    print("*************** Validation ***************")
    print('Accuracy of the network validation images: %f %%' % accuracy)
    print('Validation time is: %fs' % inference_time)

    if log != None:
        log.write("*************** Validation ***************\n")
        log.write('Accuracy of the network validation images: %f %%\n' % accuracy)
        log.write('Validation time is: %fs\n' % inference_time)

    return accuracy
