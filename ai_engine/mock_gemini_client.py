"""
Mock Gemini AI Client for Spiritual G-Code.
Provides simulated AI responses when Gemini API is not available.
Use this for development and testing.
"""

import random
from typing import Dict, List, Optional
from datetime import date


class MockGeminiGCodeClient:
    """
    Mock Gemini client for testing without API key.
    Generates consistent, meaningful responses based on input data.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize mock client (API key not required)."""
        self.api_key = api_key
        # Use random seed for consistency
        random.seed(42)

    def generate_daily_gcode(
        self,
        natal_data: Dict,
        transit_data: Dict,
        user_preferences: Optional[Dict] = None
    ) -> Dict:
        """
        Generate Daily G-Code interpretation (simulated).

        Args:
            natal_data: User's natal chart data
            transit_data: Current transit data
            user_preferences: User's preferences (tone, etc.)

        Returns:
            Dictionary with interpretation, themes, affirmation, etc.
        """
        try:
            # Extract key data
            sun_sign = natal_data.get('sun_sign', 'Unknown')
            moon_sign = natal_data.get('moon_sign', 'Unknown')
            ascendant = natal_data.get('ascendant', 'Unknown')

            # Calculate G-Code score
            score = self._calculate_gcode_score(transit_data)

            # Generate themes based on planetary positions
            themes = self._generate_themes(sun_sign, moon_sign, transit_data)

            # Generate interpretation
            interpretation = self._generate_interpretation(
                sun_sign, moon_sign, themes, score
            )

            # Generate affirmation
            affirmation = self._generate_affirmation(sun_sign, themes)

            # Generate practical guidance
            guidance = self._generate_guidance(themes, score)

            return {
                'interpretation': interpretation,
                'themes': themes,
                'affirmation': affirmation,
                'practical_guidance': guidance,
                'g_code_score': score,
            }

        except Exception as e:
            raise Exception(f"Error generating daily G-Code: {str(e)}")

    def generate_spiritual_patch_note(
        self,
        daily_gcode: Dict,
        platform: str = 'twitter',
        custom_instructions: str = ''
    ) -> Dict:
        """
        Generate social media content (simulated).

        Args:
            daily_gcode: Daily G-Code data
            platform: Target platform (twitter, instagram, linkedin)
            custom_instructions: Additional instructions

        Returns:
            Dictionary with generated content
        """
        themes = daily_gcode.get('themes', [])
        score = daily_gcode.get('g_code_score', 50)
        interpretation = daily_gcode.get('interpretation', '')

        # Generate content based on platform
        if platform == 'twitter':
            content = self._generate_twitter_content(themes, score, interpretation)
        elif platform == 'instagram':
            content = self._generate_instagram_content(themes, score, interpretation)
        elif platform == 'linkedin':
            content = self._generate_linkedin_content(themes, score, interpretation)
        else:
            content = self._generate_generic_content(themes, score, interpretation)

        return {
            'content_type': 'patch_note',
            'title': f"Spiritual Patch Note - {date.today().strftime('%Y-%m-%d')}",
            'body': content,
            'platform': platform,
            'hashtags': themes + ['#SpiritualGCode', '#DailyGCode']
        }

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
        tone = user_preferences.get('tone', 'inspiring')

        # Generate content based on type
        if content_type == 'insight':
            content = self._generate_insight_content(transit_data, tone)
        elif content_type == 'affirmation':
            content = self._generate_affirmation_content(transit_data, tone)
        else:
            content = self._generate_generic_content([], 50, '', tone)

        return {
            'content_type': content_type,
            'title': f"{content_type.replace('_', ' ').title()} - {date.today().strftime('%Y-%m-%d')}",
            'body': content,
            'platform': platform,
            'hashtags': ['#SpiritualGCode', '#DailyGuidance']
        }

    def _calculate_gcode_score(self, transit_data: Dict) -> int:
        """Calculate G-Code intensity score (1-100)."""
        aspects = transit_data.get('aspects', [])
        score = 50  # Base score

        # Score based on aspects
        for aspect in aspects:
            aspect_type = aspect.get('aspect', '')
            if aspect_type == 'conjunction':
                score += 10
            elif aspect_type == 'opposition':
                score += 8
            elif aspect_type == 'square':
                score += 6
            elif aspect_type == 'trine':
                score += 4
            elif aspect_type == 'sextile':
                score += 2

        # Add some randomness
        score += random.randint(-5, 5)

        return max(1, min(100, score))

    def _generate_themes(
        self,
        sun_sign: str,
        moon_sign: str,
        transit_data: Dict
    ) -> List[str]:
        """Generate relevant themes based on planetary positions."""
        theme_pool = [
            '#Transformation',
            '#Growth',
            '#Alignment',
            '#InnerWisdom',
            '#CosmicEnergy',
            '#Intuition',
            '#Creativity',
            '#Balance',
            '#Release',
            '#Manifestation',
            '#Healing',
            '#Connection',
            '#Clarity',
            '#Purpose',
            '#Harmony'
        ]

        # Select themes based on sun and moon signs
        selected = []
        selected.append(f'#{sun_sign}Season')
        selected.append(f'#{moon_sign}Energy')

        # Add 3 random themes
        available = [t for t in theme_pool if t not in selected]
        selected.extend(random.sample(available, 3))

        return selected

    def _generate_interpretation(
        self,
        sun_sign: str,
        moon_sign: str,
        themes: List[str],
        score: int
    ) -> str:
        """Generate daily interpretation."""
        intensity_text = ""
        if score < 25:
            intensity_text = "gentle and peaceful"
        elif score < 50:
            intensity_text = "moderately active"
        elif score < 75:
            intensity_text = "dynamic and transformative"
        else:
            intensity_text = "intense and powerful"

        interpretation = f"""Today's cosmic weather is {intensity_text}.

With your Sun in {sun_sign} and Moon in {moon_sign}, you're being called to embrace your authentic power and trust your inner knowing. The planetary alignments support deep transformation and personal growth.

Key energies at play:
{chr(10).join([f'  - {t[1:]}' for t in themes[:3]])}

This is a time to honor your journey, celebrate your growth, and align with your highest purpose. Trust that the universe is conspiring in your favor."""

        return interpretation

    def _generate_affirmation(self, sun_sign: str, themes: List[str]) -> str:
        """Generate daily affirmation."""
        affirmations = [
            f"I am aligned with the transformative power of {sun_sign}.",
            f"I trust my inner wisdom and embrace change with grace.",
            "I am worthy of all the abundance flowing into my life.",
            "I release what no longer serves me and welcome new beginnings.",
            "I am connected to universal wisdom and cosmic guidance.",
            f"I radiate the {themes[0][1:]} energy and attract positive experiences.",
            "I honor my journey and celebrate how far I've come.",
            "I am open to receiving the gifts the universe has for me.",
            "I embrace my power and create the life I desire.",
            "I am grounded, centered, and aligned with my purpose."
        ]

        return random.choice(affirmations)

    def _generate_guidance(self, themes: List[str], score: int) -> List[str]:
        """Generate practical guidance for the day."""
        guidance_pool = [
            f"Take time for meditation and connect with {themes[0][1:]} energy.",
            "Journal your thoughts and insights from the day.",
            "Practice gratitude for three specific things in your life.",
            "Set a clear intention for what you want to create.",
            "Connect with nature and ground your energy.",
            "Express yourself creatively without judgment.",
            "Reach out to someone who inspires you.",
            "Take a break from social media and be present.",
            "Do something that brings you joy and laughter.",
            "Review your goals and adjust your course if needed."
        ]

        return random.sample(guidance_pool, 3)

    def _generate_twitter_content(
        self,
        themes: List[str],
        score: int,
        interpretation: str
    ) -> str:
        """Generate Twitter content (max 280 chars)."""
        # Extract first sentence
        first_sentence = interpretation.split('.')[0] + '.'

        # Add themes
        content = f"{first_sentence}\n\n{' '.join(themes[:3])}\n\n"

        # Add score
        if score > 70:
            content += "G-Code Intensity: High "
        elif score > 40:
            content += "G-Code Intensity: Medium "
        else:
            content += "G-Code Intensity: Low "

        content += f"({score}/100)"

        # Ensure length
        if len(content) > 280:
            content = content[:277] + '...'

        return content

    def _generate_instagram_content(
        self,
        themes: List[str],
        score: int,
        interpretation: str
    ) -> str:
        """Generate Instagram content."""
        return f"""{interpretation}

{' '.join(themes[:4])}

G-Code Intensity: {score}/100

How are these energies showing up in your life today? Share in the comments!

#SpiritualGCode #DailyGCode #Astrology #NatalChart #CosmicWisdom #SpiritualJourney"""

    def _generate_linkedin_content(
        self,
        themes: List[str],
        score: int,
        interpretation: str
    ) -> str:
        """Generate LinkedIn content."""
        return f"""Daily G-Code Insights

Today's cosmic weather brings unique opportunities for growth and transformation.

Key themes to consider:
{chr(10).join([f'  {t[1:]}' for t in themes[:3]])}

G-Code Intensity: {score}/100

Understanding these cosmic patterns can help us navigate our personal and professional lives with greater awareness and intention.

What cosmic patterns are you noticing in your life?

#PersonalDevelopment #GrowthMindset #SpiritualIntelligence #CosmicAwareness"""

    def _generate_generic_content(
        self,
        themes: List[str],
        score: int,
        interpretation: str,
        tone: str = 'inspiring'
    ) -> str:
        """Generate generic content."""
        if not interpretation:
            interpretation = f"Today's energies support growth and transformation."

        return f"""{interpretation}

{' '.join(themes) if themes else '#DailyGCode #SpiritualGCode'}

G-Code Score: {score}/100

Tune into the cosmic weather and align your actions with universal flow.
"""

    def _generate_insight_content(
        self,
        transit_data: Dict,
        tone: str
    ) -> str:
        """Generate insight content."""
        return f"""Cosmic Insight for Today

The planetary alignments offer us a unique opportunity to pause and reflect. When we tune into cosmic patterns, we gain clarity about our path and purpose.

Take a moment today to:
  Connect with your breath
  Listen to your intuition
  Trust the timing of your life

The universe supports your journey.
"""

    def _generate_affirmation_content(
        self,
        transit_data: Dict,
        tone: str
    ) -> str:
        """Generate affirmation content."""
        return f"""Daily Affirmation

"I am aligned with universal wisdom and cosmic flow."

Repeat this affirmation throughout the day, especially when you feel uncertain or overwhelmed. Let it remind you of your connection to something greater.

Remember: You are exactly where you need to be.
"""


# Convenience function
def get_gemini_client(api_key: Optional[str] = None):
    """
    Get appropriate Gemini client.
    Returns mock client for development/testing.
    """
    return MockGeminiGCodeClient(api_key)
