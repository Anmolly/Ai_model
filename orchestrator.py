"""
Advanced AI Orchestrator - Main AI Model
Handles multi-capability AI operations including web search, device control, research, analytics, and presentations
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from enum import Enum
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Enumeration of supported task types"""
    WEB_SEARCH = "web_search"
    DEVICE_CONTROL = "device_control"
    RESEARCH = "research"
    ANALYTICS = "analytics"
    PRESENTATION = "presentation"
    DATA_ANALYSIS = "data_analysis"
    VOICE_COMMAND = "voice_command"
    CUSTOM = "custom"


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task:
    """Represents a single task to be executed"""
    
    def __init__(self, task_type: TaskType, command: str, params: Dict[str, Any] = None):
        self.id = str(uuid.uuid4())
        self.task_type = task_type
        self.command = command
        self.params = params or {}
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None
        self.priority = self.params.get('priority', 5)  # 1-10, higher = more important
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'type': self.task_type.value,
            'command': self.command,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'result': self.result,
            'error': self.error,
            'priority': self.priority
        }


class AIOrchestrator:
    """
    Main AI Orchestrator - Coordinates all AI capabilities
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._load_default_config()
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.running_tasks: Dict[str, Task] = {}
        self.capabilities: Dict[str, Callable] = {}
        self.max_concurrent_tasks = self.config.get('max_concurrent_tasks', 5)
        self.logger = logger
        
        # Initialize capabilities
        self._initialize_capabilities()
        
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            'max_concurrent_tasks': 5,
            'task_timeout': 300,  # 5 minutes
            'enable_web_search': True,
            'enable_device_control': True,
            'enable_research': True,
            'enable_analytics': True,
            'enable_presentations': True,
            'privacy_mode': 'standard',  # standard, tor, vpn
            'search_engine': 'duckduckgo',  # duckduckgo, searx, google
            'storage_path': './data',
            'log_level': 'INFO'
        }
    
    def _initialize_capabilities(self):
        """Initialize all AI capabilities"""
        self.logger.info("Initializing AI capabilities...")
        
        # Register capability handlers
        self.capabilities = {
            TaskType.WEB_SEARCH.value: self._handle_web_search,
            TaskType.DEVICE_CONTROL.value: self._handle_device_control,
            TaskType.RESEARCH.value: self._handle_research,
            TaskType.ANALYTICS.value: self._handle_analytics,
            TaskType.PRESENTATION.value: self._handle_presentation,
            TaskType.DATA_ANALYSIS.value: self._handle_data_analysis,
            TaskType.VOICE_COMMAND.value: self._handle_voice_command,
        }
        
        self.logger.info(f"Initialized {len(self.capabilities)} capabilities")
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a single task"""
        try:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            self.running_tasks[task.id] = task
            
            self.logger.info(f"Executing task {task.id}: {task.task_type.value}")
            
            # Get the appropriate handler
            handler = self.capabilities.get(task.task_type.value)
            if not handler:
                raise ValueError(f"Unknown task type: {task.task_type.value}")
            
            # Execute the handler
            result = await handler(task.command, task.params)
            
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            
            self.logger.info(f"Task {task.id} completed successfully")
            
        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now()
            self.logger.error(f"Task {task.id} failed: {str(e)}")
            
        finally:
            if task.id in self.running_tasks:
                del self.running_tasks[task.id]
            self.completed_tasks.append(task)
        
        return task.to_dict()
    
    async def queue_task(self, task_type: TaskType, command: str, 
                        params: Dict[str, Any] = None) -> str:
        """Queue a new task for execution"""
        task = Task(task_type, command, params)
        self.task_queue.append(task)
        self.logger.info(f"Task {task.id} queued: {task_type.value}")
        return task.id
    
    async def process_queue(self):
        """Process queued tasks with concurrency control"""
        while self.task_queue:
            # Sort by priority
            self.task_queue.sort(key=lambda t: t.priority, reverse=True)
            
            # Execute up to max_concurrent_tasks
            tasks_to_execute = []
            while self.task_queue and len(self.running_tasks) < self.max_concurrent_tasks:
                task = self.task_queue.pop(0)
                tasks_to_execute.append(self.execute_task(task))
            
            if tasks_to_execute:
                await asyncio.gather(*tasks_to_execute)
            
            # Small delay to prevent busy waiting
            await asyncio.sleep(0.1)
    
    # ==================== Capability Handlers ====================
    
    async def _handle_web_search(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle web search operations"""
        from modules.web_search import WebSearchEngine
        
        search_engine = WebSearchEngine(
            privacy_mode=self.config.get('privacy_mode'),
            search_provider=self.config.get('search_engine')
        )
        
        results = await search_engine.search(
            query=command,
            num_results=params.get('num_results', 10),
            anonymous=params.get('anonymous', True)
        )
        
        return {
            'type': 'web_search',
            'query': command,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
    
    async def _handle_device_control(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle device control operations"""
        from modules.device_control import DeviceController
        
        controller = DeviceController(config=self.config)
        
        result = await controller.execute_command(
            device_type=params.get('device_type', 'android'),
            command=command,
            device_id=params.get('device_id'),
            args=params.get('args', {})
        )
        
        return {
            'type': 'device_control',
            'device_type': params.get('device_type'),
            'command': command,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
    
    async def _handle_research(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle research operations"""
        from modules.research import ResearchEngine
        
        research_engine = ResearchEngine(config=self.config)
        
        research_result = await research_engine.conduct_research(
            topic=command,
            depth=params.get('depth', 'medium'),  # shallow, medium, deep
            sources=params.get('sources', []),
            include_analysis=params.get('include_analysis', True)
        )
        
        return {
            'type': 'research',
            'topic': command,
            'research': research_result,
            'timestamp': datetime.now().isoformat()
        }
    
    async def _handle_analytics(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle analytics operations"""
        from modules.analytics import AnalyticsEngine
        
        analytics_engine = AnalyticsEngine(config=self.config)
        
        analysis = await analytics_engine.analyze(
            data=params.get('data'),
            analysis_type=params.get('analysis_type', 'general'),
            metrics=params.get('metrics', []),
            generate_report=params.get('generate_report', True)
        )
        
        return {
            'type': 'analytics',
            'analysis_type': params.get('analysis_type'),
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }
    
    async def _handle_presentation(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle presentation generation"""
        from modules.presentation import PresentationGenerator
        
        gen = PresentationGenerator(config=self.config)
        
        presentation = await gen.generate(
            title=command,
            content=params.get('content', []),
            style=params.get('style', 'professional'),
            output_format=params.get('output_format', 'html'),  # html, pptx, pdf
            theme=params.get('theme', 'default')
        )
        
        return {
            'type': 'presentation',
            'title': command,
            'presentation': presentation,
            'timestamp': datetime.now().isoformat()
        }
    
    async def _handle_data_analysis(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle data analysis operations"""
        from modules.data_analysis import DataAnalyzer
        
        analyzer = DataAnalyzer(config=self.config)
        
        analysis = await analyzer.analyze_data(
            data=params.get('data'),
            analysis_type=command,
            visualize=params.get('visualize', True),
            export_format=params.get('export_format', 'json')
        )
        
        return {
            'type': 'data_analysis',
            'analysis_type': command,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }
    
    async def _handle_voice_command(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle voice commands"""
        from modules.voice import VoiceProcessor
        
        processor = VoiceProcessor(config=self.config)
        
        # Convert voice to text if needed
        if params.get('audio_file'):
            text_command = await processor.transcribe(params['audio_file'])
        else:
            text_command = command
        
        # Parse and execute the voice command
        parsed_command = await processor.parse_command(text_command)
        
        return {
            'type': 'voice_command',
            'original_command': command,
            'parsed_command': parsed_command,
            'timestamp': datetime.now().isoformat()
        }
    
    # ==================== Utility Methods ====================
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        # Check running tasks
        if task_id in self.running_tasks:
            return self.running_tasks[task_id].to_dict()
        
        # Check completed tasks
        for task in self.completed_tasks:
            if task.id == task_id:
                return task.to_dict()
        
        # Check queued tasks
        for task in self.task_queue:
            if task.id == task_id:
                return task.to_dict()
        
        return None
    
    def get_all_tasks(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all tasks organized by status"""
        return {
            'queued': [t.to_dict() for t in self.task_queue],
            'running': [t.to_dict() for t in self.running_tasks.values()],
            'completed': [t.to_dict() for t in self.completed_tasks]
        }
    
    def get_capabilities(self) -> List[str]:
        """Get list of available capabilities"""
        return list(self.capabilities.keys())
    
    def update_config(self, new_config: Dict[str, Any]):
        """Update configuration"""
        self.config.update(new_config)
        self.logger.info(f"Configuration updated: {new_config}")
    
    async def shutdown(self):
        """Gracefully shutdown the orchestrator"""
        self.logger.info("Shutting down AI Orchestrator...")
        
        # Cancel running tasks
        for task_id in list(self.running_tasks.keys()):
            task = self.running_tasks[task_id]
            task.status = TaskStatus.CANCELLED
            del self.running_tasks[task_id]
        
        self.logger.info("AI Orchestrator shutdown complete")


# ==================== Main Entry Point ====================

async def main():
    """Example usage of the AI Orchestrator"""
    
    # Initialize the orchestrator
    orchestrator = AIOrchestrator()
    
    # Queue some example tasks
    task_id_1 = await orchestrator.queue_task(
        TaskType.WEB_SEARCH,
        "latest AI developments 2025",
        {'num_results': 5, 'anonymous': True}
    )
    
    task_id_2 = await orchestrator.queue_task(
        TaskType.RESEARCH,
        "Machine Learning applications in healthcare",
        {'depth': 'deep', 'include_analysis': True}
    )
    
    # Process the queue
    await orchestrator.process_queue()
    
    # Get results
    print("\n=== Task Results ===")
    print(json.dumps(orchestrator.get_all_tasks(), indent=2, default=str))
    
    # Shutdown
    await orchestrator.shutdown()


if __name__ == "__main__":
    asyncio.run(main())