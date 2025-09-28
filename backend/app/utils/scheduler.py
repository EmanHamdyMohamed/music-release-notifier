"""
Scheduler utilities - disabled for serverless compatibility
Use external cron jobs or Vercel Cron for scheduled tasks
"""

class DummyScheduler:
    """Dummy scheduler for serverless environments"""
    def __init__(self):
        self.running = False
    
    def add_job(self, *args, **kwargs):
        pass
    
    def start(self):
        self.running = True
    
    def shutdown(self):
        self.running = False

# Use dummy scheduler in serverless environment
scheduler = DummyScheduler()