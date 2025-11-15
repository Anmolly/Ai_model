# Quick Start Guide - AI Model

Get up and running with the Advanced AI Model in 5 minutes!

## 🚀 Installation (5 minutes)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/ai-model.git
cd ai_model
```

### Step 2: Setup Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python -c "from core.orchestrator import AIOrchestrator; print('✓ Installation successful!')"
```

## 📝 First Run - Web Search

Create a file `test_search.py`:

```python
import asyncio
from core.orchestrator import AIOrchestrator, TaskType

async def main():
    # Initialize AI Model
    orchestrator = AIOrchestrator()
    
    # Queue a web search
    print("🔍 Searching for 'artificial intelligence 2025'...")
    task_id = await orchestrator.queue_task(
        TaskType.WEB_SEARCH,
        "artificial intelligence 2025",
        {'num_results': 5, 'anonymous': True}
    )
    
    # Process the task
    await orchestrator.process_queue()
    
    # Display results
    tasks = orchestrator.get_all_tasks()
    print("\n✅ Search Results:")
    for task in tasks['completed']:
        if task['type'] == 'web_search':
            print(f"\nQuery: {task['command']}")
            results = task['result']['results']
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result.get('title', 'N/A')}")
                print(f"   URL: {result.get('url', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python test_search.py
```

## 🎤 Voice Command Example

Create `test_voice.py`:

```python
import asyncio
from modules.voice import VoiceProcessor

async def main():
    processor = VoiceProcessor()
    
    print("🎤 Listening for voice command (10 seconds)...")
    print("Try saying: 'search for machine learning'")
    
    result = await processor.listen_and_process(timeout=10)
    
    print(f"\n✅ Heard: {result.get('original_text', 'N/A')}")
    print(f"Command: {result.get('detected_command', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python test_voice.py
```

## 📊 Create a Presentation

Create `test_presentation.py`:

```python
import asyncio
from modules.presentation import PresentationGenerator

async def main():
    gen = PresentationGenerator()
    
    # Define presentation content
    content = [
        {
            'title': 'Welcome',
            'content': '<h2>Welcome to AI Model Presentation</h2><p>This is an automated presentation</p>'
        },
        {
            'title': 'Features',
            'content': '''
            <h2>Key Features</h2>
            <ul>
                <li>Web Search</li>
                <li>Device Control</li>
                <li>Research Engine</li>
                <li>Analytics</li>
                <li>Voice Commands</li>
            </ul>
            '''
        },
        {
            'title': 'Thank You',
            'content': '<h2>Thank You!</h2><p>Questions?</p>'
        }
    ]
    
    print("📊 Generating presentation...")
    result = await gen.generate(
        title="AI Model Demo",
        content=content,
        output_format='html',
        style='professional'
    )
    
    print(f"✅ Presentation created: {result['filename']}")
    print(f"   Format: {result['format']}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python test_presentation.py
```

## 🔬 Research Example

Create `test_research.py`:

```python
import asyncio
from modules.research import ResearchEngine

async def main():
    engine = ResearchEngine()
    
    print("🔬 Conducting research on 'Quantum Computing'...")
    
    result = await engine.conduct_research(
        topic="Quantum Computing",
        depth="medium",
        include_analysis=True
    )
    
    print(f"\n✅ Research Complete")
    print(f"Topic: {result['topic']}")
    print(f"Depth: {result['depth']}")
    print(f"Findings: {len(result['findings'])} sources")
    
    if result.get('analysis'):
        print(f"\nKey Insights:")
        for insight in result['analysis'].get('key_insights', []):
            print(f"  • {insight}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python test_research.py
```

## 📱 Android Device Control

Create `test_device.py`:

```python
import asyncio
from modules.device_control import DeviceController

async def main():
    controller = DeviceController()
    
    print("📱 Discovering Android devices...")
    devices = await controller.discover_devices()
    
    if devices:
        print(f"✅ Found {len(devices)} device(s)")
        for device in devices:
            print(f"  • {device['id']} ({device['type']})")
            
            # Get device info
            info = await controller.get_device_info(device['id'])
            print(f"    Status: {info.get('success', False)}")
    else:
        print("❌ No devices found. Make sure:")
        print("  1. Android device is connected via USB")
        print("  2. USB debugging is enabled")
        print("  3. ADB is installed and in PATH")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python test_device.py
```

## 📊 Data Analytics

Create `test_analytics.py`:

```python
import asyncio
from modules.analytics import AnalyticsEngine

async def main():
    engine = AnalyticsEngine()
    
    print("📊 Analyzing data...")
    
    result = await engine.analyze(
        data=[1, 2, 3, 4, 5],
        analysis_type='statistical',
        metrics=['mean', 'median', 'std_dev'],
        generate_report=True
    )
    
    print(f"✅ Analysis Complete")
    print(f"\nMetrics:")
    for metric, value in result['metrics'].items():
        print(f"  {metric}: {value}")
    
    print(f"\nInsights:")
    for insight in result['insights']:
        print(f"  • {insight}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python test_analytics.py
```

## 🐳 Docker Quick Start

```bash
# Build image
docker build -t ai-model:latest .

# Run container
docker run -it ai-model:latest

# Or with volume mount
docker run -it -v $(pwd)/data:/app/data ai-model:latest
```

## 🔧 Configuration

Create `.env` file:

```env
# Privacy Settings
PRIVACY_MODE=standard
SEARCH_ENGINE=duckduckgo

# Device Control
ANDROID_ADB_PATH=/usr/bin/adb

# Voice Settings
VOICE_LANGUAGE=en
VOICE_TIMEOUT=10

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/ai_model.log

# Storage
DATA_PATH=./data
CACHE_PATH=./cache
```

## 📚 Common Commands

```bash
# Run web search
python -c "
import asyncio
from core.orchestrator import AIOrchestrator, TaskType

async def search():
    orch = AIOrchestrator()
    await orch.queue_task(TaskType.WEB_SEARCH, 'python programming')
    await orch.process_queue()
    print(orch.get_all_tasks())

asyncio.run(search())
"

# List available capabilities
python -c "
from core.orchestrator import AIOrchestrator
orch = AIOrchestrator()
print('Available capabilities:')
for cap in orch.get_capabilities():
    print(f'  • {cap}')
"

# Check configuration
python -c "
from core.orchestrator import AIOrchestrator
orch = AIOrchestrator()
import json
print(json.dumps(orch.config, indent=2))
"
```

## 🆘 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'aiohttp'"
**Solution**: Run `pip install -r requirements.txt`

### Issue: "ADB not found"
**Solution**: 
- Linux: `sudo apt-get install android-tools-adb`
- Mac: `brew install android-platform-tools`
- Windows: Download from Android SDK

### Issue: "Microphone not detected"
**Solution**: 
- Linux: `sudo apt-get install portaudio19-dev`
- Mac: `brew install portaudio`
- Check system audio settings

### Issue: "No internet connection"
**Solution**: Check your network and firewall settings

## 📖 Next Steps

1. **Read Full Documentation**: See [README.md](README.md)
2. **Explore Examples**: Check `examples/` directory
3. **Configure Settings**: Edit `config.json`
4. **Deploy to Cloud**: See deployment guide
5. **Integrate with Your App**: Use as library

## 🎯 Common Use Cases

### Automated Research
```python
# Conduct deep research and generate report
result = await research_engine.conduct_research(
    topic="Your Topic",
    depth="deep",
    include_analysis=True
)
report = await research_engine.generate_report(result)
```

### Batch Processing
```python
# Process multiple tasks concurrently
for query in queries:
    await orchestrator.queue_task(TaskType.WEB_SEARCH, query)
await orchestrator.process_queue()
```

### Voice-Controlled Automation
```python
# Listen for commands and execute
result = await voice_processor.listen_and_process()
command = result['detected_command']
# Execute based on command
```

## 💡 Tips & Tricks

1. **Use async/await** for better performance
2. **Set privacy_mode='tor'** for anonymous searches
3. **Batch tasks** for concurrent processing
4. **Enable logging** for debugging
5. **Use virtual environment** to avoid conflicts

## 📞 Support

- **Issues**: GitHub Issues
- **Questions**: Check FAQ in docs
- **Contributions**: Pull requests welcome

---

**Happy coding! 🚀**

For more information, visit the [full documentation](README.md)