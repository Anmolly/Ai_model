# Complete Installation & Deployment Guide

## 📋 Table of Contents
1. [Local Installation](#local-installation)
2. [Cloud Deployment](#cloud-deployment)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)

---

## Local Installation

### Prerequisites
- Python 3.9+
- pip package manager
- Git
- 4GB RAM minimum
- Internet connection

### Step-by-Step Installation

#### 1. Clone Repository
```bash
git clone https://github.com/yourusername/ai-model.git
cd ai_model
```

#### 2. Create Virtual Environment
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y \
    python3-dev \
    portaudio19-dev \
    android-tools-adb \
    build-essential \
    libssl-dev \
    libffi-dev
```

**macOS:**
```bash
brew install portaudio
brew install android-platform-tools
brew install python@3.11
```

**Windows:**
- Download Android SDK Platform Tools from [here](https://developer.android.com/studio/releases/platform-tools)
- Add to PATH environment variable
- Install Visual C++ Build Tools

#### 5. Verify Installation
```bash
# Test imports
python -c "
from core.orchestrator import AIOrchestrator
from modules.web_search import WebSearchEngine
from modules.device_control import DeviceController
from modules.voice import VoiceProcessor
from modules.presentation import PresentationGenerator
from modules.research import ResearchEngine
from modules.analytics import AnalyticsEngine
print('✓ All modules imported successfully!')
"

# Test orchestrator
python -c "
from core.orchestrator import AIOrchestrator
orch = AIOrchestrator()
print(f'✓ Orchestrator initialized with {len(orch.get_capabilities())} capabilities')
"
```

---

## Cloud Deployment

### Docker Deployment

#### 1. Build Docker Image
```bash
docker build -t ai-model:latest .
docker tag ai-model:latest yourusername/ai-model:latest
```

#### 2. Run Locally with Docker
```bash
# Basic run
docker run -d \
  --name ai-model \
  -p 8000:8000 \
  ai-model:latest

# With volume mount
docker run -d \
  --name ai-model \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  ai-model:latest

# With environment variables
docker run -d \
  --name ai-model \
  -p 8000:8000 \
  -e PRIVACY_MODE=standard \
  -e SEARCH_ENGINE=duckduckgo \
  -e LOG_LEVEL=INFO \
  ai-model:latest
```

#### 3. Push to Docker Hub
```bash
docker login
docker push yourusername/ai-model:latest
```

### AWS Deployment

#### 1. Create EC2 Instance
```bash
# Launch Ubuntu 22.04 LTS instance
# Security group: Allow ports 22, 8000

# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip
```

#### 2. Install Docker
```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo usermod -aG docker ubuntu
```

#### 3. Deploy Container
```bash
docker run -d \
  --name ai-model \
  -p 8000:8000 \
  --restart always \
  yourusername/ai-model:latest
```

### Google Cloud Deployment

#### 1. Create Cloud Run Service
```bash
gcloud run deploy ai-model \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 4Gi \
  --timeout 3600
```

#### 2. Set Environment Variables
```bash
gcloud run services update ai-model \
  --set-env-vars PRIVACY_MODE=standard,SEARCH_ENGINE=duckduckgo
```

### Azure Deployment

#### 1. Create Container Registry
```bash
az acr create --resource-group myResourceGroup \
  --name myregistry --sku Basic
```

#### 2. Build and Push
```bash
az acr build --registry myregistry \
  --image ai-model:latest .
```

#### 3. Deploy to Container Instances
```bash
az container create \
  --resource-group myResourceGroup \
  --name ai-model \
  --image myregistry.azurecr.io/ai-model:latest \
  --cpu 2 --memory 4
```

---

## Configuration

### Environment Variables

Create `.env` file:

```env
# ===== CORE SETTINGS =====
MAX_CONCURRENT_TASKS=5
TASK_TIMEOUT=300
LOG_LEVEL=INFO

# ===== PRIVACY & SECURITY =====
PRIVACY_MODE=standard  # standard, tor, vpn
SEARCH_ENGINE=duckduckgo  # duckduckgo, searx, google, bing
ENABLE_ANONYMOUS_SEARCH=true

# ===== DEVICE CONTROL =====
ENABLE_DEVICE_CONTROL=true
ANDROID_ADB_PATH=/usr/bin/adb
DEVICE_TIMEOUT=30

# ===== VOICE SETTINGS =====
ENABLE_VOICE=true
VOICE_LANGUAGE=en
VOICE_TIMEOUT=10
VOICE_RECOGNITION_ENGINE=google

# ===== STORAGE =====
DATA_PATH=./data
CACHE_PATH=./cache
LOG_PATH=./logs

# ===== API KEYS (if needed) =====
GOOGLE_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# ===== PROXY SETTINGS =====
HTTP_PROXY=
HTTPS_PROXY=
SOCKS_PROXY=
```

### Configuration File

Create `config.json`:

```json
{
  "max_concurrent_tasks": 5,
  "task_timeout": 300,
  "enable_web_search": true,
  "enable_device_control": true,
  "enable_research": true,
  "enable_analytics": true,
  "enable_presentations": true,
  "privacy_mode": "standard",
  "search_engine": "duckduckgo",
  "storage_path": "./data",
  "log_level": "INFO",
  "voice": {
    "enabled": true,
    "language": "en",
    "timeout": 10
  },
  "device_control": {
    "enabled": true,
    "adb_path": "/usr/bin/adb",
    "timeout": 30
  }
}
```

---

## Verification

### Test Each Module

#### 1. Test Web Search
```bash
python -c "
import asyncio
from modules.web_search import WebSearchEngine

async def test():
    engine = WebSearchEngine()
    results = await engine.search('test', num_results=1)
    print(f'✓ Web search working: {len(results)} results')

asyncio.run(test())
"
```

#### 2. Test Device Control
```bash
python -c "
import asyncio
from modules.device_control import DeviceController

async def test():
    controller = DeviceController()
    devices = await controller.discover_devices()
    print(f'✓ Device control working: {len(devices)} devices found')

asyncio.run(test())
"
```

#### 3. Test Voice
```bash
python -c "
import asyncio
from modules.voice import VoiceProcessor

async def test():
    processor = VoiceProcessor()
    result = await processor.text_to_speech('Test', output_file='test.mp3')
    print(f'✓ Voice working: {result.get(\"success\", False)}')

asyncio.run(test())
"
```

#### 4. Test Presentations
```bash
python -c "
import asyncio
from modules.presentation import PresentationGenerator

async def test():
    gen = PresentationGenerator()
    result = await gen.generate(
        title='Test',
        content=[{'title': 'Slide 1', 'content': 'Test'}],
        output_format='html'
    )
    print(f'✓ Presentations working: {result.get(\"filename\", \"N/A\")}')

asyncio.run(test())
"
```

#### 5. Test Research
```bash
python -c "
import asyncio
from modules.research import ResearchEngine

async def test():
    engine = ResearchEngine()
    result = await engine.conduct_research('test', depth='shallow')
    print(f'✓ Research working: {len(result.get(\"findings\", []))} findings')

asyncio.run(test())
"
```

#### 6. Test Analytics
```bash
python -c "
import asyncio
from modules.analytics import AnalyticsEngine

async def test():
    engine = AnalyticsEngine()
    result = await engine.analyze([1,2,3], analysis_type='test')
    print(f'✓ Analytics working: {len(result.get(\"metrics\", {}))} metrics')

asyncio.run(test())
"
```

---

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError"
```bash
# Solution: Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### 2. "ADB not found"
```bash
# Linux
sudo apt-get install android-tools-adb

# Mac
brew install android-platform-tools

# Windows: Add to PATH manually
```

#### 3. "Microphone not detected"
```bash
# Linux
sudo apt-get install portaudio19-dev

# Mac
brew install portaudio

# Check permissions
sudo usermod -a -G audio $USER
```

#### 4. "Permission denied"
```bash
# Fix file permissions
chmod +x ai_model/core/orchestrator.py
chmod -R 755 ai_model/
```

#### 5. "Port already in use"
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python your_script.py
```

Check logs:
```bash
tail -f logs/ai_model.log
```

---

## Performance Optimization

### Recommended Settings

```json
{
  "max_concurrent_tasks": 10,
  "task_timeout": 600,
  "cache_enabled": true,
  "cache_ttl": 3600,
  "connection_pool_size": 20,
  "request_timeout": 30
}
```

### Resource Monitoring

```bash
# Monitor memory usage
watch -n 1 'ps aux | grep python'

# Monitor disk usage
df -h

# Monitor network
nethogs
```

---

## Security Hardening

### Firewall Configuration

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp
sudo ufw allow 8000/tcp
sudo ufw enable
```

### SSL/TLS Setup

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365
```

### API Key Management

```bash
# Use environment variables
export API_KEY=$(cat /path/to/secure/key)

# Or use secrets manager
aws secretsmanager get-secret-value --secret-id ai-model-keys
```

---

## Maintenance

### Regular Updates

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update Docker image
docker pull yourusername/ai-model:latest
```

### Backup

```bash
# Backup data
tar -czf backup_$(date +%Y%m%d).tar.gz data/

# Backup configuration
cp config.json config_backup_$(date +%Y%m%d).json
```

### Monitoring

```bash
# Check service status
systemctl status ai-model

# View logs
journalctl -u ai-model -f

# Health check
curl http://localhost:8000/health
```

---

## Support & Resources

- **Documentation**: [README.md](README.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Issues**: GitHub Issues
- **Community**: Discussions

---

**Last Updated**: 2025-01-15  
**Version**: 1.0.0