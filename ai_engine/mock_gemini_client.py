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

            # Generate asteroid interpretations
            asteroid_insights = self._generate_asteroid_insights(
                natal_data, transit_data
            )

            # Generate lunar node interpretations
            node_insights = self._generate_lunar_node_insights(
                natal_data, transit_data
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
                'asteroid_insights': asteroid_insights,
                'node_insights': node_insights,
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

    def _generate_asteroid_insights(
        self,
        natal_data: Dict,
        transit_data: Dict
    ) -> Dict:
        """
        Generate interpretations for the four major asteroids.

        Returns insights for Ceres, Pallas, Juno, and Vesta.
        """
        asteroids = ['ceres', 'pallas', 'juno', 'vesta']
        insights = {}

        # Asteroid archetype interpretations
        asteroid_meanings = {
            'ceres': {
                'name': 'Ceres',
                'symbol': '⚳',
                'themes': ['nurturing', 'abundance', 'grief', 'mother-child bonds'],
                'interpretation': 'Ceres represents how you nurture and care for others, as well as your relationship with abundance and loss. This asteroid shows where you find fulfillment through caregiving and what你必须 release to experience renewal.'
            },
            'pallas': {
                'name': 'Pallas Athena',
                'symbol': '⚴',
                'themes': ['wisdom', 'strategy', 'justice', 'creative intelligence'],
                'interpretation': 'Pallas Athena reveals your strategic mind and problem-solving abilities. This asteroid shows how you channel wisdom into creative action and fight for justice in your unique way.'
            },
            'juno': {
                'name': 'Juno',
                'symbol': '⚵',
                'themes': ['partnership', 'commitment', 'equality', 'soul contracts'],
                'interpretation': 'Juno illuminates your approach to committed partnerships and what you need in relationships to feel truly seen and valued. She reveals the balance between independence and intimacy.'
            },
            'vesta': {
                'name': 'Vesta',
                'symbol': '⚶',
                'themes': ['devotion', 'sacred work', 'focus', 'inner fire'],
                'interpretation': 'Vesta represents your sacred devotion and what you\'re willing to dedicate yourself to completely. This asteroid shows where you find meaning through focused service and keeping your inner flame alive.'
            }
        }

        natal_chart = natal_data.get('chart_data', {})
        transit_planets = transit_data.get('planets', {})

        for asteroid_key in asteroids:
            if asteroid_key in natal_chart:
                natal_pos = natal_chart[asteroid_key]
                meaning = asteroid_meanings.get(asteroid_key, {})

                insights[asteroid_key] = {
                    'name': meaning.get('name', asteroid_key.title()),
                    'symbol': meaning.get('symbol', ''),
                    'natal_sign': natal_pos.get('sign', 'Unknown'),
                    'natal_degree': natal_pos.get('degree', 0),
                    'themes': meaning.get('themes', []),
                    'interpretation': meaning.get('interpretation', ''),
                }

                # Check for transits to asteroid
                if asteroid_key in transit_planets:
                    transit_pos = transit_planets[asteroid_key]
                    insights[asteroid_key]['transit_sign'] = transit_pos.get('sign', 'Unknown')
                    insights[asteroid_key]['transit_activation'] = self._get_asteroid_transit_message(asteroid_key, transit_pos.get('sign'))

        return insights

    def _get_asteroid_transit_message(self, asteroid: str, sign: str) -> str:
        """Generate transit activation message for asteroid."""
        messages = {
            'ceres': f'Ceres in {sign} activates your nurturing energy. Focus on self-care and supporting others while maintaining healthy boundaries.',
            'pallas': f'Pallas in {sign} sharpens your strategic mind. Trust your creative intelligence to solve problems and see patterns others miss.',
            'juno': f'Juno in {sign} highlights relationship dynamics. Examine your commitments and ensure your partnerships reflect your true needs.',
            'vesta': f'Vesta in {sign} focuses your devotion. Clarify what truly matters to you and dedicate yourself wholeheartedly to your sacred work.'
        }
        return messages.get(asteroid, f'{asteroid.title()} is active in {sign}.')

    def _generate_lunar_node_insights(
        self,
        natal_data: Dict,
        transit_data: Dict
    ) -> Dict:
        """
        Generate interpretations for the lunar nodes.

        Returns insights for North Node (life path) and South Node (past karma).
        """
        insights = {
            'north_node': {
                'name': 'North Node',
                'symbol': '☊',
                'themes': ['life purpose', 'destiny', 'growth', 'soul evolution'],
                'interpretation': self._generate_north_node_message(natal_data)
            },
            'south_node': {
                'name': 'South Node',
                'symbol': '☋',
                'themes': ['past karma', 'comfort zone', 'old patterns', 'release'],
                'interpretation': self._generate_south_node_message(natal_data)
            }
        }

        # Check for nodal transits
        aspects = transit_data.get('aspects', [])
        nodal_transits = [a for a in aspects if a.get('natal_planet') in ['sun', 'moon', 'ascendant']
                         and a.get('transit_planet') in ['north_node', 'south_node']]

        if nodal_transits:
            insights['nodal_transits'] = [
                {
                    'aspect': t['aspect'],
                    'orb': t['orb'],
                    'meaning': self._get_nodal_transit_meaning(t)
                } for t in nodal_transits[:3]  # Top 3 most significant
            ]

        return insights

    def _generate_north_node_message(self, natal_data: Dict) -> str:
        """Generate North Node interpretation based on sign."""
        # In a real implementation, this would use the actual nodal position
        # For now, generate based on Sun sign (simplified)
        sun_sign = natal_data.get('sun_sign', 'Unknown')

        nodal_guidance = {
            'Aries': 'Your destiny calls you to embrace courageous leadership and initiate new beginnings. Trust your instincts and pioneer your own path.',
            'Taurus': 'Your path forward involves building stability and cultivating self-worth. Create lasting value through patience and persistence.',
            'Gemini': 'Your soul\'s journey involves communication and learning. Share your ideas and stay curious about the world.',
            'Cancer': 'Your destiny lies in emotional intelligence and creating family. Nurture others while honoring your own need for security.',
            'Leo': 'Your path involves creative self-expression and leadership. Shine your light and inspire others through authenticity.',
            'Virgo': 'Your growth comes through service and refinement. Use your analytical skills to improve systems and help others.',
            'Libra': 'Your destiny involves partnership and harmony. Create balance in your relationships and seek fairness in all interactions.',
            'Scorpio': 'Your path involves transformation and depth. Embrace change and trust the process of death and rebirth.',
            'Sagittarius': 'Your soul\'s journey involves expansion and wisdom. Seek truth, explore philosophy, and share your knowledge.',
            'Capricorn': 'Your destiny involves mastery and achievement. Build structures that last and take responsibility for your ambitions.',
            'Aquarius': 'Your path involves innovation and humanitarian service. Break free from convention and envision new possibilities.',
            'Pisces': 'Your growth comes through compassion and transcendence. Trust your intuition and merge with something greater than yourself.'
        }

        return nodal_guidance.get(sun_sign, 'Your North Node reveals your soul\'s direction for growth and fulfillment in this lifetime.')

    def _generate_south_node_message(self, natal_data: Dict) -> str:
        """Generate South Node interpretation based on sign."""
        # In a real implementation, this would use the actual nodal position
        # For now, generate based on Sun sign (simplified, opposite sign)
        sun_sign = natal_data.get('sun_sign', 'Unknown')

        past_pattern_guidance = {
            'Aries': 'You\'re mastering the art of cooperation. Release the need to always lead first and learn to consider others\' needs.',
            'Taurus': 'You\'re learning to embrace change. Let go of attachment to material security and trust in transformation.',
            'Gemini': 'You\'re deepening your emotional understanding. Move beyond superficial connections and explore the depths of feeling.',
            'Cancer': 'You\'re developing independence. Release over-identification with others\' emotions and claim your own identity.',
            'Leo': 'You\'re learning humility and service. Let go of constant need for recognition and find value in quiet contribution.',
            'Virgo': 'You\'re embracing wholeness. Release perfectionism and accept yourself and others with all your humanity.',
            'Libra': 'You\'re cultivating self-reliance. Let go of excessive people-pleasing and develop your own inner compass.',
            'Scorpio': 'You\'re learning to lighten up. Release intensity and control, embrace peace and openness.',
            'Sagittarius': 'You\'re developing focus and commitment. Let go of scattered interests and dedicate yourself to what truly matters.',
            'Capricorn': 'You\'re learning to play and trust. Release over-identification with achievement and allow yourself to rest.',
            'Aquarius': 'You\'re deepening your emotional connections. Let go of detachment and embrace vulnerability and intimacy.',
            'Pisces': 'You\'re developing discernment and practical action. Release escapism and engage with reality directly.'
        }

        return past_pattern_guidance.get(sun_sign, 'Your South Node reveals past patterns and gifts you\'re being asked to transcend in this lifetime.')

    def _get_nodal_transit_meaning(self, transit_aspect: Dict) -> str:
        """Generate interpretation for nodal transit aspect."""
        aspect = transit_aspect.get('aspect', 'conjunction')
        planet = transit_aspect.get('natal_planet', 'sun')

        meanings = {
            'conjunction': f'North Node conjunct your {planet} marks a powerful destiny activation. Pay attention to synchronicities and opportunities aligned with your life path.',
            'square': f'North Node square your {planet} indicates tension between old patterns and soul growth. Embrace the discomfort as you evolve.',
            'trine': f'North Node trine your {planet} brings flow to your life path. Opportunities for growth arise naturally—trust and say yes.',
            'opposition': f'North Node opposite your {planet} highlights the balance between past and future. Release South Node patterns to embrace your destiny.'
        }

        return meanings.get(aspect, f'Nodal activation involving {planet} supports your soul\'s evolution.')


# Convenience function
def get_gemini_client(api_key: Optional[str] = None):
    """
    Get appropriate Gemini client.
    Returns mock client for development/testing.
    """
    return MockGeminiGCodeClient(api_key)
