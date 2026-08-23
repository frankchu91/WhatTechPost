<!--
REVIEW NOTES (delete before publishing)
- COVER: assets/2026-08-23-pika-audio.png
- Facts (research 2026-08-19/20): Pika launched 4 audio models under "Pika Audio" (~Aug 14), priced up to 20x lower than competitors: Pika Soundtrack (video-to-audio sync), Pika Music (prompt+lyric songs up to 6 min), Pika SFX (natural-language sound effects), Pika Speech (expressive TTS + voice cloning). VERIFY pricing claim wording ("up to 20x lower") before publishing.
- Weekend post — creative-AI-for-builders angle. Voice-cloning gets a responsible-use note.
- No AI-disclosure line (policy).
-->

---
title: "AI audio just got up to 20x cheaper, and that's the part builders should notice"
published: false
description: "Pika shipped four audio models — music, SFX, TTS with voice cloning, video-to-audio — at a fraction of the going rate. Cheap audio APIs change which apps are worth building."
tags: ai, audio, webdev, indiehackers
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/2026-08-23-pika-audio.png
---

Most of the AI attention this month went to models and agents, so a launch aimed at a different sense slipped past a lot of feeds: Pika shipped four audio models under the Pika Audio brand, and the headline isn't a capability, it's a price — up to 20x lower than competitors. When a whole media type gets an order of magnitude cheaper, the interesting question isn't "how good is it," it's "what does that make buildable."

## What's in the box

Four models, each pointed at a distinct job. Pika Soundtrack does video-to-audio — score and sound that syncs to footage. Pika Music generates songs from a prompt and lyrics, up to six minutes. Pika SFX turns natural-language descriptions into sound effects ("a heavy door creaking shut, distant rain"). And Pika Speech is expressive text-to-speech with voice cloning.

Individually, none of these is a first — text-to-speech, music generation, and SFX all had credible players already. The move here is bundling the audio stack and undercutting the going rate. The "up to 20x" headline is the SFX model specifically; the rest vary — Music lands around 10x cheaper, and Speech is roughly 9x cheaper than ElevenLabs v3 (less against faster tiers). They're live through the Pika API Club, a $10/month aggregator where you pay per generation. Different multiples per model, same direction: price, not novelty, is the product.

## Why cheap changes the calculus

I've watched this pattern play out with text and images, and it always goes the same way. When a capability is expensive, it's a premium feature you ration — you use TTS on the marketing page, not on every user's every interaction. When it drops 20x, it stops being a feature you ration and becomes a default you sprinkle everywhere. The threshold question flips from "is this worth the cost" to "why isn't there audio here."

Concretely, cheap audio makes a bunch of previously-silly ideas reasonable. Per-user generated soundtracks. Sound effects on every state change in a game prototype without a licensing budget. Voiceover for content that could never justify a voice actor. Accessibility audio generated on the fly instead of pre-produced. None of these were impossible before; they were just not worth the line item. A 20x cut is exactly the kind of move that turns "not worth it" into "why not," and the builders who notice first get a window before it's table stakes.

## The voice-cloning asterisk

I can't write about expressive TTS with voice cloning and skip the obvious. Cheap, good voice cloning is a genuinely useful accessibility and localization tool and a genuinely effective fraud and impersonation tool, and it's the same feature either way. The 20x price cut lowers the barrier for both.

If you build with it: get real consent for any cloned voice, keep provenance markings on generated audio rather than stripping them, and remember that the EU AI Act's transparency rules — live as of this month — point directly at synthesized media that could pass for real. This isn't a reason to avoid the tool. It's a reason to be the kind of builder who uses it in daylight. Cheap capability and responsible use aren't in tension; the cheapness is exactly why the responsibility has to be deliberate.

## Where I land

I haven't put these through real production use, so treat this as "worth an afternoon," not a review. But the price is the signal, and the signal is clear: audio is joining text and images in the pile of media types that are now nearly free to generate. If you've been treating audio as too expensive or too niche to build around, that assumption just expired.

If you ship something that leans on cheap generated audio, I'd like to hear what it unlocked — especially the ideas that only made sense once the cost fell out of the way.
