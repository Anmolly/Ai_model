"""
Voice Processing Module - Speech-to-text and voice command processing
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class VoiceProcessor:
    """Process voice commands and convert speech to text"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logger
        self.supported_languages = ['en', 'es', 'fr', 'de', 'zh', 'ja']
        
    async def transcribe(self, audio_file: str, language: str = 'en') -> str:
        """
        Transcribe audio file to text
        
        Args:
            audio_file: Path to audio file
            language: Language code
            
        Returns:
            Transcribed text
        """
        try:
            self.logger.info(f"Transcribing audio: {audio_file}")
            
            # Using speech_recognition library
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
            
            try:
                text = recognizer.recognize_google(audio, language=language)
                self.logger.info(f"Transcribed: {text}")
                return text
            except sr.UnknownValueError:
                self.logger.error("Could not understand audio")
                return ""
            except sr.RequestError as e:
                self.logger.error(f"Transcription error: {str(e)}")
                return ""
                
        except Exception as e:
            self.logger.error(f"Transcribe error: {str(e)}")
            return ""
    
    async def parse_command(self, text: str) -> Dict[str, Any]:
        """
        Parse voice command text
        
        Args:
            text: Command text
            
        Returns:
            Parsed command structure
        """
        try:
            self.logger.info(f"Parsing command: {text}")
            
            # Simple command parsing
            text_lower = text.lower()
            
            command_map = {
                'search': ['search', 'find', 'look for'],
                'device': ['tap', 'swipe', 'click', 'touch'],
                'research': ['research', 'investigate', 'study'],
                'analytics': ['analyze', 'analyze data', 'statistics'],
                'presentation': ['create presentation', 'make slides', 'presentation'],
                'screenshot': ['screenshot', 'capture screen', 'take picture'],
                'install': ['install', 'download app'],
                'uninstall': ['uninstall', 'remove app'],
            }
            
            detected_command = None
            for cmd, keywords in command_map.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        detected_command = cmd
                        break
                if detected_command:
                    break
            
            return {
                'original_text': text,
                'detected_command': detected_command,
                'confidence': 0.85,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Parse command error: {str(e)}")
            return {'error': str(e)}
    
    async def text_to_speech(self, text: str, output_file: str = None,
                            language: str = 'en') -> Dict[str, Any]:
        """
        Convert text to speech
        
        Args:
            text: Text to convert
            output_file: Output audio file path
            language: Language code
            
        Returns:
            Result dictionary
        """
        try:
            self.logger.info(f"Converting text to speech: {text}")
            
            from gtts import gTTS
            
            tts = gTTS(text=text, lang=language, slow=False)
            
            if output_file:
                tts.save(output_file)
                return {
                    'success': True,
                    'output_file': output_file,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': True,
                    'text': text,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Text to speech error: {str(e)}")
            return {'error': str(e)}
    
    async def listen_and_process(self, timeout: int = 10) -> Dict[str, Any]:
        """
        Listen for voice input and process it
        
        Args:
            timeout: Listening timeout in seconds
            
        Returns:
            Processed command
        """
        try:
            self.logger.info("Listening for voice input...")
            
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=timeout)
            
            try:
                text = recognizer.recognize_google(audio)
                self.logger.info(f"Heard: {text}")
                
                parsed = await self.parse_command(text)
                return parsed
                
            except sr.UnknownValueError:
                return {'error': 'Could not understand audio'}
            except sr.RequestError as e:
                return {'error': f'Recognition error: {str(e)}'}
                
        except Exception as e:
            self.logger.error(f"Listen error: {str(e)}")
            return {'error': str(e)}