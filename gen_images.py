import os
from google import genai
from google.genai import types
from PIL import Image
import io

# Initialize the new Google GenAI Client
# It will automatically pick up the GEMINI_API_KEY from your environment variables
client = genai.Client()

def call_nano_banana():
    """
    Executes the batch image generation for the Cloud Fronts Group service pages
    using the new google-genai SDK and Imagen 3.
    """
    print("Initiating Nano Banana sequence...")
    
    # Target aesthetic appended to every prompt to maintain brand consistency
    style_guide = (
        "High-quality 3D render, landscape orientation. "
        "Color palette strictly features dark navy (#003a70) backgrounds, gold (#d4a017) accents, "
        "and teal/cyan highlights. Dark glassmorphism design aesthetic, sleek and professional."
    )

    image_prompts = {
        "domain-names": "Earth globe viewed from above with a magnifying glass hovering over a bright spot. Floating domain tags (.com, .org, .net, .io, .co) orbit the globe with soft trailing glows. Fiber-optic arcs between them. Small 'Available!' badge near the focused spot.",
        "site-hosting": "Isometric illustration. Top: translucent cloud silhouette containing a glowing server rack with green activity lights. Blue and gold data streams flow down to a laptop, tablet, and phone (all showing a website loading). Shield + checkmark icon. '99.9% Uptime' badge. Circular monitoring radiation pattern.",
        "marketing": "Top-down flat-lay on dark wood desk. Open leather notebook with hand-drawn charts (upward line graph, sales funnel), customer persona sketch. Tablet with real-time analytics. Gold/blue/teal markers. Coffee mug with CF logo. Sticky notes: 'Audience,' 'Positioning,' 'ROI.' Glowing lightbulb above.",
        "political-advertisements": "Campaign desk arrangement. Large yard sign with candidate name + 'VICTORY 2026' slogan (white on navy, gold star). Tilted smartphone with social campaign ad + 'VOTE' CTA. Tri-fold mail piece partially open. Tablet with media placement calendar. Subtle American flag bunting in corner. Non-partisan, professional.",
        "social-media-opener": "Split screen. Left: content calendar grid with post thumbnails, smartphone showing Instagram feed with branded lifestyle photos. Right: analytics dashboard with engagement charts, follower growth line graph trending up, sentiment emoji icons. Central 'share/connect' icon with radial lines.",
        "social-media-mid": "Overhead desk layout. Printed monthly content calendar with color-coded sticky notes (gold=launches, blue=engagement, green=spotlights). Phone showing post preview with notifications. Stylus, ring light, branded content swipe file. Soft window lighting from left.",
        "ppc-opener": "Search results page with gold-highlighted PPC ad at top (headline, sitelinks, CTA button). Floating translucent metrics: CPC, impressions, quality score (9/10), conversion rate badge. Corner graph showing ROAS trending up over 30 days. Small gold coins with up-arrows.",
        "ppc-mid": "Funnel left-to-right. User visits site (laptop) -> leaves -> dotted-loop 'Retargeting Ad' (phone showing follow-up ad) -> returns and converts (cart + checkmark). Below: horizontal bar graph before vs after retargeting (small bar vs tall bar with % increase). Timer icons: 'within 24h.'",
        "document-mgmt-opener": "Left-to-right transformation. Left: filing cabinet + paper pile + clock icon (time wasted). Center: scanner with blue digital arrow through it. Right: digital folder interface (Contracts, Invoices, HR), search bar finding a file, security shield + lock. Speedometer: 'before' slow -> 'after' fast.",
        "document-mgmt-mid": "Central cloud icon with secure glowing lines to laptop (remote worker), tablet (field), phone (on-the-go). File icons (PDF, DOC, spreadsheet) inside cloud. Role-based access panel with user profiles + permission badges (Admin, Editor, Viewer). 'Encrypted' green badge. Vault door icon in corner.",
        "publishing-opener": "Mid-air composition. Center: 3D eBook mockup with geometric navy/gold cover. Orbiting: open magazine with pull quotes and full-bleed photos, tablet with interactive digital edition, stylus pen. Digital particles between formats suggesting cross-platform flow.",
        "publishing-mid": "Hub-and-spoke diagram. Center: glowing 'Core Content' icon (document with star). Spokes to: blog post -> social cards (Instagram, X, LinkedIn); video -> transcript + podcast; webinar -> PDF guide; research data -> infographic + slide deck. Recycling arrow around whole diagram. Calendar in corner showing consistent cadence."
    }

    # Generate images
    for filename, prompt in image_prompts.items():
        print(f"Generating {filename}...")
        full_prompt = f"{prompt} {style_guide}"
        
        try:
            # Using the new Client-based syntax and the latest Imagen 3 model
            response = client.models.generate_images(
                model="imagen-3.0-generate-001",
                prompt=full_prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="16:9",
                    output_mime_type="image/jpeg"
                )
            )
            
            # The new SDK returns response.generated_images
            for generated_image in response.generated_images:
                # Access the bytes directly
                image = Image.open(io.BytesIO(generated_image.image.image_bytes))
                
                # Resize exactly to 700x400 to meet your layout specs
                image = image.resize((700, 400), Image.Resampling.LANCZOS)
                
                # Save out as WebP
                output_path = f"{filename}.webp"
                image.save(output_path, "webp", quality=90)
                print(f"Saved: {output_path}")
                
        except Exception as e:
             print(f"Error generating {filename}: {e}")

if __name__ == "__main__":
    call_nano_banana()
