#!/usr/bin/env python
import sys
import os
from dotenv import load_dotenv

import os
os.environ["OPENAI_API_KEY"] = "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"

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hocusfocus.crew import HocusfocusCrew

def run():
    """
    Run the crew simulation for the high, medium, and low usage agents.
    """
    hocusfocus_crew = HocusfocusCrew()
    hocusfocus_crew.run_simulation(days=7)

    
if __name__ == "__main__":
    run()

