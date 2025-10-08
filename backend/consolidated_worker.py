#!/usr/bin/env python3
"""
Consolidated worker for all background tasks - Memory Optimized for Render Free Tier
This single process handles all worker tasks to minimize memory usage
"""

import asyncio
import logging
import signal
import sys
import gc
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import time
import os

# Configure logging to reduce memory overhead
logging.basicConfig(
    level=logging.WARNING,  # Only warnings and errors
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class ConsolidatedWorker:
    """Single worker process that handles all background tasks"""
    
    def __init__(self):
        self.running = True
        self.executor = ThreadPoolExecutor(max_workers=2)  # Limit concurrent threads
        self.tasks = []
        
    def setup_signal_handlers(self):
        """Setup graceful shutdown handlers"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down gracefully...")
            self.running = False
            
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
    
    async def weather_worker_task(self):
        """Weather verification worker task"""
        try:
            from worker import WeatherWorker
            worker = WeatherWorker()
            
            while self.running:
                try:
                    await worker.process_messages()
                    await asyncio.sleep(30)  # Check every 30 seconds
                except Exception as e:
                    logger.error(f"Weather worker error: {e}")
                    await asyncio.sleep(60)  # Wait longer on error
                    
        except ImportError as e:
            logger.error(f"Failed to import weather worker: {e}")
        except Exception as e:
            logger.error(f"Weather worker task failed: {e}")
    
    async def general_worker_task(self):
        """General worker task for report processing"""
        try:
            from worker import Worker
            worker = Worker()
            
            while self.running:
                try:
                    await worker.process_messages()
                    await asyncio.sleep(20)  # Check every 20 seconds
                except Exception as e:
                    logger.error(f"General worker error: {e}")
                    await asyncio.sleep(45)  # Wait on error
                    
        except ImportError as e:
            logger.error(f"Failed to import general worker: {e}")
        except Exception as e:
            logger.error(f"General worker task failed: {e}")
    
    async def peer_notification_task(self):
        """Peer notification worker task"""
        try:
            from peer_notif_worker import PeerNotificationWorker
            worker = PeerNotificationWorker()
            
            while self.running:
                try:
                    await worker.process_messages()
                    await asyncio.sleep(45)  # Check every 45 seconds
                except Exception as e:
                    logger.error(f"Peer notification error: {e}")
                    await asyncio.sleep(90)  # Wait longer on error
                    
        except ImportError as e:
            logger.error(f"Failed to import peer notification worker: {e}")
        except Exception as e:
            logger.error(f"Peer notification task failed: {e}")
    
    def run_ai_worker(self):
        """AI worker in separate thread to avoid blocking"""
        try:
            from ai.worker import AIWorker
            worker = AIWorker()
            
            while self.running:
                try:
                    # Run AI worker synchronously in thread
                    worker.process_messages()
                    time.sleep(60)  # Check every minute
                except Exception as e:
                    logger.error(f"AI worker error: {e}")
                    time.sleep(120)  # Wait longer on error
                    
        except ImportError as e:
            logger.error(f"Failed to import AI worker: {e}")
        except Exception as e:
            logger.error(f"AI worker thread failed: {e}")
    
    async def memory_monitor_task(self):
        """Monitor memory usage and force garbage collection"""
        import psutil
        process = psutil.Process()
        
        while self.running:
            try:
                memory_mb = process.memory_info().rss / 1024 / 1024
                logger.info(f"Memory usage: {memory_mb:.1f}MB")
                
                # Force garbage collection if memory > 400MB
                if memory_mb > 400:
                    logger.warning("High memory usage detected, forcing garbage collection")
                    gc.collect()
                    
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error(f"Memory monitor error: {e}")
                await asyncio.sleep(300)
    
    async def run_async_workers(self):
        """Run all async workers concurrently"""
        async_tasks = [
            self.weather_worker_task(),
            self.general_worker_task(), 
            self.peer_notification_task(),
            self.memory_monitor_task()
        ]
        
        # Run all async tasks concurrently
        await asyncio.gather(*async_tasks, return_exceptions=True)
    
    def run(self):
        """Main entry point - start all workers"""
        logger.info("Starting consolidated worker...")
        self.setup_signal_handlers()
        
        try:
            # Start AI worker in thread (if it's synchronous)
            ai_thread = Thread(target=self.run_ai_worker, daemon=True)
            ai_thread.start()
            
            # Run async workers
            asyncio.run(self.run_async_workers())
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error(f"Consolidated worker failed: {e}")
        finally:
            self.running = False
            self.executor.shutdown(wait=True)
            logger.info("Consolidated worker stopped")


if __name__ == "__main__":
    # Force garbage collection on startup
    gc.collect()
    
    worker = ConsolidatedWorker()
    worker.run()