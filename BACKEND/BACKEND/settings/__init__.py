#  from .local import *  # local mode
from .deploy import *  # deploy mode


"""
local mode <-> deploy mode 스위치 때 수정해야할 곳

1. BACKEND/settings/__init__.py 
# from .local import *  # local mode
from .deploy import *  # deploy mode

2. accountapp/views.py
from BACKEND.settings.local import SECRET_KEY # local mode
from BACKEND.settings.deploy import SECRET_KEY  # deploy mode

3. adminapp/views.py
# from BACKEND.settings.local import TEAM_PW  # local mode  
from BACKEND.settings.deploy import TEAM_PW  # deploy mode
"""