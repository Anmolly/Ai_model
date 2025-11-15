"""
Device Control Module - Control smartphones and gadgets
Supports Android (ADB), iOS, and smart home devices
"""

import asyncio
import subprocess
import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class DeviceController:
    """Control various devices including smartphones and smart gadgets"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logger
        self.connected_devices: Dict[str, Dict[str, Any]] = {}
        
    async def discover_devices(self) -> List[Dict[str, Any]]:
        """Discover connected devices"""
        try:
            self.logger.info("Discovering devices...")
            devices = []
            
            # Discover Android devices via ADB
            android_devices = await self._discover_android_devices()
            devices.extend(android_devices)
            
            self.logger.info(f"Discovered {len(devices)} devices")
            return devices
            
        except Exception as e:
            self.logger.error(f"Device discovery error: {str(e)}")
            return []
    
    async def _discover_android_devices(self) -> List[Dict[str, Any]]:
        """Discover Android devices via ADB"""
        try:
            result = subprocess.run(
                ['adb', 'devices', '-l'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            devices = []
            lines = result.stdout.strip().split('\n')[1:]
            
            for line in lines:
                if line.strip() and 'device' in line:
                    parts = line.split()
                    device_id = parts[0]
                    
                    devices.append({
                        'id': device_id,
                        'type': 'android',
                        'status': 'connected',
                        'discovered_at': datetime.now().isoformat()
                    })
                    
                    self.connected_devices[device_id] = {
                        'type': 'android',
                        'status': 'connected'
                    }
            
            return devices
            
        except Exception as e:
            self.logger.warning(f"Android device discovery error: {str(e)}")
            return []
    
    async def execute_command(self, device_type: str, command: str, 
                             device_id: Optional[str] = None, 
                             args: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute command on device"""
        try:
            self.logger.info(f"Executing command on {device_type}: {command}")
            
            if device_type == 'android':
                result = await self._execute_android_command(command, device_id, args)
            else:
                result = {'error': f'Unknown device type: {device_type}'}
            
            return result
            
        except Exception as e:
            self.logger.error(f"Command execution error: {str(e)}")
            return {'error': str(e)}
    
    async def _execute_android_command(self, command: str, device_id: Optional[str],
                                       args: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute command on Android device via ADB"""
        try:
            args = args or {}
            adb_cmd = ['adb']
            if device_id:
                adb_cmd.extend(['-s', device_id])
            
            if command == 'tap':
                x, y = args.get('x', 0), args.get('y', 0)
                adb_cmd.extend(['shell', 'input', 'tap', str(x), str(y)])
                
            elif command == 'swipe':
                x1, y1 = args.get('x1', 0), args.get('y1', 0)
                x2, y2 = args.get('x2', 0), args.get('y2', 0)
                duration = args.get('duration', 500)
                adb_cmd.extend(['shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y2), str(duration)])
                
            elif command == 'text':
                text = args.get('text', '')
                adb_cmd.extend(['shell', 'input', 'text', text])
                
            elif command == 'screenshot':
                adb_cmd.extend(['shell', 'screencap', '-p', '/sdcard/screenshot.png'])
                
            elif command == 'install_app':
                app_path = args.get('app_path', '')
                adb_cmd.extend(['install', app_path])
                
            elif command == 'get_info':
                adb_cmd.extend(['shell', 'getprop'])
                
            else:
                return {'error': f'Unknown Android command: {command}'}
            
            result = subprocess.run(
                adb_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return {
                'success': result.returncode == 0,
                'command': command,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Android command error: {str(e)}")
            return {'error': str(e)}
    
    async def get_device_info(self, device_id: str, device_type: str = 'android') -> Dict[str, Any]:
        """Get device information"""
        try:
            if device_type == 'android':
                result = await self._execute_android_command('get_info', device_id)
                return result
            else:
                return {'error': f'Device type {device_type} not supported'}
                
        except Exception as e:
            self.logger.error(f"Get device info error: {str(e)}")
            return {'error': str(e)}
    
    async def take_screenshot(self, device_id: str, device_type: str = 'android',
                             save_path: str = None) -> Dict[str, Any]:
        """Take screenshot from device"""
        try:
            if device_type == 'android':
                result = await self._execute_android_command(
                    'screenshot',
                    device_id,
                    {'save_path': save_path}
                )
                return result
            else:
                return {'error': f'Device type {device_type} not supported'}
                
        except Exception as e:
            self.logger.error(f"Screenshot error: {str(e)}")
            return {'error': str(e)}
    
    async def install_app(self, device_id: str, app_path: str,
                         device_type: str = 'android') -> Dict[str, Any]:
        """Install app on device"""
        try:
            if device_type == 'android':
                result = await self._execute_android_command(
                    'install_app',
                    device_id,
                    {'app_path': app_path}
                )
                return result
            else:
                return {'error': f'Device type {device_type} not supported'}
                
        except Exception as e:
            self.logger.error(f"Install app error: {str(e)}")
            return {'error': str(e)}
    
    async def send_text(self, device_id: str, text: str,
                       device_type: str = 'android') -> Dict[str, Any]:
        """Send text to device"""
        try:
            if device_type == 'android':
                result = await self._execute_android_command(
                    'text',
                    device_id,
                    {'text': text}
                )
                return result
            else:
                return {'error': f'Device type {device_type} not supported'}
                
        except Exception as e:
            self.logger.error(f"Send text error: {str(e)}")
            return {'error': str(e)}
    
    async def tap_screen(self, device_id: str, x: int, y: int,
                        device_type: str = 'android') -> Dict[str, Any]:
        """Tap on screen at coordinates"""
        try:
            if device_type == 'android':
                result = await self._execute_android_command(
                    'tap',
                    device_id,
                    {'x': x, 'y': y}
                )
                return result
            else:
                return {'error': f'Device type {device_type} not supported'}
                
        except Exception as e:
            self.logger.error(f"Tap screen error: {str(e)}")
            return {'error': str(e)}