# -*- coding: utf-8 -*-
# !/usr/bin/env python3


# --- LOGGING TO A FILE ---

import os
import logging
import account

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler that logs into a file into the current folder
logfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),'account.log')
handler = logging.FileHandler(logfile)
handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Attach the handler to the logger
logger.addHandler(handler)


acc = account.Account('EUR', logger)
acc.deposit(100.0)
acc.deposit('20.0')
acc.withdraw(4000.0)
acc.withdraw(30.0)
logger.warning('Final amount is: {}'.format(acc.balance))
