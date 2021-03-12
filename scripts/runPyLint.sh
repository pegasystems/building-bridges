#!/bin/sh
python3 -m pylint bridges --exit-zero -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"