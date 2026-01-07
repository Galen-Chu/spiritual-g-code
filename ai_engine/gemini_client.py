"""
Google Gemini AI Client for Spiritual G-Code.
"""

import google.generativeai as genai
from typing import Dict, List, Optional
from django.conf import settings
import json
import re


class GeminiGCodeClient:
    """
    Custom Gemini client for G-Code generation and interpretation.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini client with API key."""
        self.api_key = api_key or settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    def generate_daily_gcode(
        self,
        natal_data: Dict,
        transit_data: Dict,
        user_preferences: Optional[Dict] = None
    ) -> Dict:
        """
        Generate Daily G-Code interpretation.

        Args:
            natal_data: User's natal chart data
            transit_data: Current transit data
            user_preferences: User's preferences (tone, etc.)

        Returns:
            Dictionary with interpretation, themes, affirmation, etc.
        """
        prompt = self._build_daily_prompt(
            natal_data,
            transit_data,
            user_preferences or {}
        )

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text

            # Parse AI response
            return self._parse_daily_response(response_text, transit_data)

        except Exception as e:
            raise Exception(f"Error generating daily G-Code: {str(e)}")

    def generate_spiritual_patch_note(
        self,
        daily_gcode: Dict,
        platform: str = 'twitter',
        custom_instructions: str = ''
    ) -> Dict:
        """
        Generate social media content (Spiritual Patch Note).

        Args:
            daily_gcode: Daily G-Code data
            platform: Target platform (twitter, instagram, etc.)
            custom_instructions: Additional instructions

        Returns:
            Dictionary with generated content
        """
        template = self._load_template(f'patch_note_{platform}')
        prompt = template.format(
            themes=', '.join(daily_gcode.get('themes', [])),
            score=daily_gcode.get('g_code_score', 50),
            interpretation=daily_gcode.get('interpretation', '')[:200]
        )

        if custom_instructions:
            prompt += f"\n\nAdditional instructions: {custom_instructions}"

        try:
            response = self.model.generate_content(prompt)

            return {
                'content_type': 'patch_note',
                'title': f"Spiritual Patch Note - {daily_gcode.get('transit_date', 'Today')}",
                'body': response.text,
                'platform': platform,
                'hashtags': self._extract_hashtags(response.text),
            }

        except Exception as e:
            raise Exception(f"Error generating patch note: {str(e)}")

    def generate_content(
        self,
        transit_data: Dict,
        content_type: str,
        platform: str,
        user_preferences: Dict,
        custom_instructions: str = ''
    ) -> Dict:
        """
        Generate various types of content.

        Args:
            transit_data: Transit data
            content_type: Type of content to generate
            platform: Target platform
            user_preferences: User preferences
            custom_instructions: Additional instructions

        Returns:
            Dictionary with generated content
        """
        template = self._load_template(f'content_{content_type}')
        tone = user_preferences.get('tone', 'inspiring')

        prompt = template.format(
            content_type=content_type,
            platform=platform,
            tone=tone,
            custom_instructions=custom_instructions
        )

        try:
            response = self.model.generate_content(prompt)

            return {
                'content_type': content_type,
                'title': self._generate_title(content_type, response.text),
                'body': response.text,
                'platform': platform,
                'hashtags': self._extract_hashtags(response.text),
            }

        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}")

    def _build_daily_prompt(
        self,
        natal_data: Dict,
        transit_data: Dict,
        user_preferences: Dict
    ) -> str:
        """Build prompt for daily G-Code generation."""
        base_template = self._load_template('daily_gcode_base')

        # Format transit data for prompt
        major_transits = self._format_transits(transit_data)

        prompt = base_template.format(
            sun_sign=natal_data.get('sun_sign', 'Unknown'),
            moon_sign=natal_data.get('moon_sign', 'Unknown'),
            ascendant=natal_data.get('ascendant', 'Unknown'),
            major_transits=major_transits,
            tone=user_preferences.get('tone', 'inspiring')
        )

        return prompt

    def _parse_daily_response(self, response_text: str, transit_data: Dict) -> Dict:
        """Parse AI response into structured data."""
        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                return {
                    'interpretation': data.get('interpretation', response_text),
                    'themes': data.get('themes', []),
                    'affirmation': data.get('affirmation', ''),
                    'practical_guidance': data.get('practical_guidance', []),
                    'g_code_score': data.get('score', self._calculate_gcode_score(transit_data)),
                }
            except json.JSONDecodeError:
                pass

        # Fallback: parse text response
        return {
            'interpretation': response_text,
            'themes': self._extract_themes(response_text),
            'affirmation': self._extract_affirmation(response_text),
            'practical_guidance': [],
            'g_code_score': self._calculate_gcode_score(transit_data),
        }

    def _format_transits(self, transit_data: Dict) -> str:
        """Format transit data for prompt."""
        # Extract major planetary positions
        planets = transit_data.get('planets', {})
        aspects = transit_data.get('aspects', [])

        formatted = []
        for planet, position in planets.items():
            formatted.append(f"{planet}: {position}")

        if aspects:
            formatted.append("\nMajor Aspects:")
            for aspect in aspects[:5]:  # Limit to 5 major aspects
                formatted.append(f"- {aspect}")

        return "\n".join(formatted)

    def _calculate_gcode_score(self, transit_data: Dict) -> int:
        """Calculate G-Code intensity score (1-100)."""
        # Simple heuristic based on aspect intensity
        aspects = transit_data.get('aspects', [])
        score = 50  # Base score

        for aspect in aspects:
            if 'conjunction' in aspect.lower():
                score += 10
            elif 'opposition' in aspect.lower():
                score += 8
            elif 'square' in aspect.lower():
                score += 6
            elif 'trine' in aspect.lower():
                score += 4

        return min(max(score, 1), 100)  # Clamp between 1-100

    def _extract_themes(self, text: str) -> List[str]:
        """Extract themes from AI response."""
        # Look for hashtags or capitalized phrases
        themes = []
        hashtag_pattern = r'#(\w+)'
        hashtags = re.findall(hashtag_pattern, text)
        themes.extend([f"#{tag}" for tag in hashtags])

        return themes[:5] if themes else ['#DailyGCode', '#SpiritualGCode']

    def _extract_affirmation(self, text: str) -> str:
        """Extract affirmation from AI response."""
        # Look for sentences starting with "I" or affirmative statements
        sentences = text.split('.')
        for sentence in sentences:
            if sentence.strip().startswith('I '):
                return sentence.strip() + '.'

        return "I am aligned with cosmic energies today."

    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text."""
        hashtag_pattern = r'#(\w+)'
        hashtags = re.findall(hashtag_pattern, text)
        return [f"#{tag}" for tag in hashtags]

    def _generate_title(self, content_type: str, body: str) -> str:
        """Generate title from content."""
        # Use first sentence or first 60 chars as title
        first_sentence = body.split('.')[0]
        if len(first_sentence) > 60:
            return first_sentence[:57] + '...'
        return first_sentence

    def _load_template(self, template_name: str) -> str:
        """Load prompt template from file."""
        try:
            from pathlib import Path
            template_path = Path(__file__).parent / 'prompts' / f'{template_name}.txt'
            with open(template_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            # Fallback to default template
            return self._get_default_template(template_name)

    def _get_default_template(self, template_name: str) -> str:
        """Get default template if file not found."""
        if 'daily_gcode' in template_name:
            return """You are the Spiritual G-Code interpreter.

## Natal Configuration
- Sun Sign: {sun_sign}
- Moon Sign: {moon_sign}
- Ascendant: {ascendant}

## Current Transits
{major_transits}

## Your Task
Provide a Daily G-Code interpretation that includes:
1. Key theme of the day
2. Cosmic weather explanation
3. Practical guidance
4. Three key themes as hashtags
5. G-Code intensity score (1-100)

## Tone
{tone}, precise, poetic, and practical.

## Output Format
Return your response in this JSON format:
{{
  "theme": "Theme of the day",
  "interpretation": "Full interpretation",
  "themes": ["#theme1", "#theme2", "#theme3"],
  "affirmation": "Daily affirmation",
  "practical_guidance": ["tip1", "tip2"],
  "score": 75
}}
"""
        elif 'patch_note' in template_name:
            return """Create a spiritual patch note for social media.

Themes: {themes}
G-Code Score: {score}

Create a concise, inspiring post (under 280 characters) that:
1. Mentions the key themes
2. Provides a quick insight
3. Ends with relevant hashtags

Make it {tone} and engaging.
"""
        else:
            return "Generate {content_type} content for {platform} in a {tone} tone."
