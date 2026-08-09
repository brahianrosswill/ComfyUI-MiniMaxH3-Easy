from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT.parent / "MiniMax-H3" / "skills"
GUIDES_ROOT = ROOT / "prompt_guides"


GUIDES = {
    "h3_general": ("h3-prompt-writing", "h3-general-prompt-guide"),
    "3d_animation_short": ("3d-animation-short-generator", "3d-animation-short-prompt-guide"),
    "brand_promo": ("brand-promo-video-generator", "brand-promo-video-prompt-guide"),
    "coop_game_intro": ("co-op-game-intro-generator", "co-op-game-intro-prompt-guide"),
    "handdrawn_live": ("handdrawn-live-video-generator", "handdrawn-live-video-prompt-guide"),
    "minimalist_product_ad": ("minimalist-product-ad-generator", "minimalist-product-ad-prompt-guide"),
    "music_video_subtitle": ("mv-subtitle-skill-confirmed", "music-video-subtitle-prompt-guide"),
    "paper_collage": ("paper-collage-explainer-generator", "paper-collage-explainer-prompt-guide"),
    "papercraft_stop_motion": ("papercraft-stop-motion-explainer", "papercraft-stop-motion-explainer-prompt-guide"),
}


# These sections are exclusively about an Agent runtime: tool availability,
# canvas delivery, staged user approval, external generation/editing dispatch,
# or final file delivery. Prompt-writing sections are deliberately not listed.
REMOVED_SECTIONS = {
    "3d_animation_short": {
        "## STEP 8: Full Film Assembly, BGM Match, and Final Output",
    },
    "brand_promo": {
        "## Tool Coverage Rule",
        "## STEP 3: Create a provenance manifest",
        "## STEP 7: Hard confirmation before generation",
        "## STEP 8: Produce Hub assets",
        "## STEP 10: Deliver",
    },
    "coop_game_intro": {
        "## STEP 4: Generate the first confirmation image",
        "## STEP 5: Wait for approval",
    },
    "handdrawn_live": {
        "## Step 5: Delivery",
    },
    "minimalist_product_ad": {
        "## Start Gate",
        "## STEP 10: Music Analysis, Beat-synced Editing, and Delivery Verification",
    },
    "music_video_subtitle": {
        "## Hub compatibility rules",
        "## STEP 8: Canvas delivery",
        "## STEP 9: Final MV generation and assembly workflow",
    },
    "paper_collage": {
        "## STEP 8: Optional Assembly, Music, Narration, and Delivery",
    },
    "papercraft_stop_motion": {
        "## Canvas Document Delivery Rule",
        "## Interaction Rule: Confirmation Cards Between Phases",
        "## STEP 17: Generate and Clean Voiceover Audio",
    },
}


EXACT_REPLACEMENTS = {
    "3d_animation_short": {
        "Core rule: **story first, ask screen size and total duration with choice cards immediately after user intake, ordered canvas artifacts, every required confirmation via choice card, fixed order after character/scene cards: six-column standardized shot table with per-second directives + audio cues + spatial anchor chain → shot-table self-check gate → one single text storyboards document with one section per shot (multi-panel pencil image only when user explicitly opts into visualization mode; any shot flagged for heavy iteration is extracted to a standalone text storyboard node) → video-model choice card (H3 default, Seedance 2.0 fallback) + resolution choice card → single-shot clips rendered by the chosen video model → full-film assembly with BGM; final video must remove all storyboard artifacts**.":
            "Core rule: **story first; use the node's aspect ratio, duration, mode, and connected-reference context; build a six-column standardized shot table with per-second directives, audio cues, and a spatial anchor chain; then produce one coherent H3 prompt with exact character, environment, continuity, camera, performance, dialogue, sound, and music instructions. The final video must contain no storyboard artifacts.**",
        "## STEP 0: Intake and Canvas Plan": "## STEP 0: Intake and Format Context",
        "Immediately after capturing the user's input, before Project Brief or any other next step, show choice cards to confirm production format:\n\nScreen size / aspect ratio card:\n\n- 16:9 landscape (recommended for cinematic short)\n- 9:16 vertical short\n- 1:1 square\n- 4:5 social portrait\n- Custom size / aspect ratio\n\nTotal duration card:\n\n- 30–60 seconds (recommended)\n- 15–30 seconds\n- 60–90 seconds\n- 90–180 seconds\n- Custom duration\n\nOnly proceed after the user chooses both screen size/aspect ratio and total duration, or explicitly supplies custom values. Store the approved screen size/aspect ratio and duration in the Project Brief and reuse them in shot timing, transition continuity, the standardized shot table with per-second directives, single-shot storyboards (text by default, pencil image when user opts in), single-shot video clips, assembly, BGM matching, and final composite settings.\n\nCreate or later update canvas artifacts in this order:\n\n1. Project Brief text node\n2. Story Outline text node\n3. Labeled Character Card image nodes\n4. Environment-only Scene Card image nodes\n5. Standardized Shot Information Table node with six columns; each row must include per-second directives inside `Shot Description`\n6. **Single text storyboards document** — one canvas text node named `<title> text storyboards` containing one section per shot (mirrors the half-narrated-drama storyboard structure). When the user flags a shot for heavy iteration, that section is extracted to a standalone text node and a `(extracted)` marker is left in the document. Pencil image storyboards, if opted in, are separate image nodes.\n7. Single-Shot Video Clip nodes (rendered by the video model selected in Step 7 — H3 default, Seedance 2.0 fallback)\n8. Assembled Main Video node\n9. Matched BGM audio node and Final BGM-Composited Video node\n\nDo not dump long production content only in chat. Put durable outputs on canvas as text, image, video, or audio nodes.":
            "Use the aspect ratio and total duration supplied by the node. Reuse them consistently in shot timing, transition continuity, per-second directives, dialogue timing, sound design, music planning, and final composition.",
        "Use this Skill when the user wants a complete story-first animated short workflow, from one-line idea to final edited video. The workflow must place every major artifact on the canvas in production order and pause at creative gates with user choice cards before expensive or high-impact steps.":
            "Use this Prompt Guide for a complete story-first animated short prompt, from a one-line idea through story, character, environment, shot, camera, performance, continuity, and audio planning.",
        "Produce a concise project brief and write it to a canvas text node named with the project title or `项目简报`.":
            "Produce a concise project brief.",
        "Create a story outline and write it to a canvas text node named `故事大纲` or `story-outline`.":
            "Create a story outline.",
        "Generate character reference cards and place each image on canvas. Recommended order:":
            "Define character reference cards in this recommended order:",
        "Generate scene reference cards and place them on canvas after character cards. Scene cards must show environments only: do not include characters, people, crowd figures, silhouettes, hands, faces, or character cameos. Character action belongs in the shot table, single-shot multi-panel pencil storyboards, and single-shot video clips, not scene cards.":
            "Define scene reference cards after character cards. Scene cards must show environments only: do not include characters, people, crowd figures, silhouettes, hands, faces, or character cameos. Character action belongs in the shot table, single-shot multi-panel pencil storyboards, and single-shot video clips, not scene cards.",
        "Create a canvas table node named `标准镜头信息表` or `standard-shot-table`.":
            "Create a standardized shot information table named `标准镜头信息表` or `standard-shot-table`.",
        "Then show a user choice card:\n\n- Continue with this direction (recommended)\n- Regenerate premise options\n- Revise emotional premise\n- Refine dialogue direction\n\nOnly proceed after the user chooses or explicitly says to continue.": "",
        "Then show a user choice card:\n\n- Approve story and continue (recommended)\n- Revise beats\n- Revise emotion curve\n- Revise dialogue beats\n- Return to premise": "",
        "After the main character cards are generated, show a user choice card:\n\n- Lock character designs and continue (recommended)\n- Regenerate protagonist card\n- Adjust specific visual details\n- Add another character card\n\nWarn the user that changing locked character designs later may require regenerating the shot table, single-shot storyboards, single-shot video clips, assembled main video, and final composite.":
            "Treat the defined character identity, costume, proportions, colors, and signature props as locked continuity anchors throughout the prompt.",
        "Then show a user choice card:\n\n- Lock scene design and continue (recommended)\n- Regenerate scene card\n- Add another scene angle\n- Adjust lighting or layout":
            "Treat the chosen environment layout, lighting state, continuity landmarks, and prop positions as locked spatial anchors throughout the prompt.",
        "Required reference: read and follow `references/shot-table-spec.md` for the exact six-column schema, per-second directive requirements, table-wide rules, user approval card, and mandatory Step 5.5 self-check gate.":
            "Required reference: read and follow `references/shot-table-spec.md` for the exact six-column schema, per-second directive requirements, table-wide rules, and mandatory Step 5.5 self-check.",
        "Then show the table approval/self-check choice cards defined in `references/shot-table-spec.md`.": "",
        "After the Step 5.5 self-check passes, show a storyboard-mode choice card before producing any storyboard artifact.":
            "After the Step 5.5 self-check passes, use the text-storyboard structure before writing the final H3 prompt.",
        "Required reference: read and follow `references/storyboard-guidelines.md` for the default single text storyboards document, optional multi-panel pencil storyboards, shot-level extraction/re-integration, storyboard approval cards, and visualization fallback rules.":
            "Required reference: read and follow `references/storyboard-guidelines.md` for the authoritative text-storyboard structure, optional visual-storyboard rules, shot-level detail, and visualization fallback rules.",
        "After all storyboards are approved, proceed to the video-model choice card.": "",
        "## STEP 7: Video-Model Choice Card + Single-Shot Video Clips": "## STEP 7: H3 Single-Shot Prompt Preparation",
        "Before any clip is rendered, show the video-model choice card and resolution choice card.": "",
        "After all clips render, place them on canvas in shot order, group them as `<title> shot clips`, and show the clip approval card defined in `references/model-selection.md`.": "",
    },
    "brand_promo": {
        "description: For marketers and creators producing promotional content for brands, products, websites, apps, shops, or personal projects. Users provide logos, product images, interface screenshots, official links, or other verifiable assets and confirm duration, aspect ratio, audience, and campaign focus. The Skill organizes brand facts and asset provenance, selects a narrative direction, plans precise beats and shots, generates needed imagery, video, voiceover, or music, and completes assembly and pre-delivery review. It outputs a promotional short that highlights product capabilities, use cases, and a call to action. Best for launches, website showcases, and social promotion; not for imitating real brand marks without authorized assets, inventing product claims, or producing long-form narrative films.":
            "description: For marketers and creators producing promotional content for brands, products, websites, apps, shops, or personal projects. The Prompt Guide uses connected logos, product images, interface screenshots, official links, duration, aspect ratio, audience, and campaign focus to organize verified brand facts, choose a narrative direction, plan precise beats, and write a polished MiniMax H3 promotional prompt. Best for launches, website showcases, and social promotion; not for imitating real brand marks without authorized assets, inventing product claims, or producing long-form narrative films.",
        "Create a polished short promo video for a brand, product, website, app, shop, or personal project. Use this Skill when the user has a logo, product images, screenshots, a website link, or just a clear idea and wants the agent to turn those materials into a clean brand reel.":
            "Create a polished short promo prompt for a brand, product, website, app, shop, or personal project using the supplied logo, product images, screenshots, links, and stated campaign intent.",
        "This Hub adaptation replaces third-party Vibe Motion / Remotion implementation details with Hub-native orchestration: source research, asset verification, story planning, image/video generation, optional speech or music, and editing assembly. Do not initialize external projects or depend on npm validators during normal execution.": "",
        "Present 2-3 concise creative directions when the user has not already chosen one, recommend one, and continue after confirmation. Use the product category to pick a spine:":
            "When the user has not already chosen a direction, infer the strongest concise creative direction from the product category and use the corresponding story spine:",
        "- The output is on the canvas and multi-asset outputs are grouped": "",
        "Before any story planning or generation, run a required user intake. Ask the user to upload or provide links to the elements that must be verified:":
            "Before story planning, resolve the available connected assets and any source links stated in the prompt:",
        "In the same opening intake, ask the user to choose:":
            "Use the node's duration and aspect ratio, together with any campaign constraints stated in the prompt:",
        "Also identify campaign focus, distribution channel, narration language, on-screen copy language, and visible copy needs when they are not already clear. Do not proceed to creative direction until the user has supplied the usable materials or explicitly confirms which elements are unavailable.":
            "Also identify campaign focus, distribution channel, narration language, on-screen copy language, and visible copy needs. Use only the available connected or explicitly described materials; do not invent missing identity-bearing assets.",
        "If a logo, product UI, person, mascot, packaging, font, color system, or other identity-bearing asset cannot be authenticated, stop and ask for an authorized original instead of generating a plausible substitute.":
            "If a logo, product UI, person, mascot, packaging, font, color system, or other identity-bearing asset cannot be authenticated from the connected media or prompt, do not generate a plausible substitute.",
        "## STEP 9: Verify before delivery": "## STEP 9: Verify the final prompt",
        "If the output fails an authenticity check, replace the questionable asset with an official/user-authorized source or stop and ask for the asset. Never improve an imitation.":
            "If the prompt fails an authenticity check, remove the questionable asset or require an official/user-authorized source. Never improve an imitation.",
        "- Wrong or approximate logo: remove it, locate the current official file or ask for the user's original, then regenerate or re-edit.":
            "- Wrong or approximate logo: remove it and use only a connected official or user-provided original.",
        "- Asset unavailable: ask for an authorized original; never guess.":
            "- Asset unavailable: omit it; never guess.",
    },
    "coop_game_intro": {
        "description: For users creating a two-player co-op game menu or opening animation. Users provide two player names, a game title, a target visual style, and optional character reference images. The Skill locks identity cues, generates an approval image from a fixed menu framework with coordinated color, buttons, icons, and typography, then uses the approved result to rebuild the character, UI-copy, and event timing instructions for the final video. It outputs a co-op game intro featuring two characters, player cards, and menu interaction motion. Best for game concepts, character-led menus, and social content; not for playable game development, complex multi-page UI, exact brand-logo replication, or generic character-free title sequences.":
            "description: For users creating a two-player co-op game menu or opening animation. The Prompt Guide locks identity cues from player names, game title, visual style, and optional character references, then builds coordinated color, buttons, icons, typography, UI copy, event timing, and motion instructions for the final H3 prompt. Best for game concepts, character-led menus, and social content; not for playable game development, complex multi-page UI, exact brand-logo replication, or generic character-free title sequences.",
        "Use this Skill when the user wants a co-op game intro video and wants to confirm the visual direction with one image before generating the final H3 video. The workflow collects style, player names, game title, and optional character refs, then creates a framework-preserving confirmation image before generating the H3 video.":
            "Use this Prompt Guide for a co-op game intro video. It combines the requested style, player names, game title, optional character references, framework-preserving menu design, and final H3 event timing.",
        "These two templates are mandatory runtime inputs, not optional background notes:":
            "These two templates are required prompt-writing references, not optional background notes:",
        "## STEP 1: Ask for visual style": "## STEP 1: Resolve the visual style",
        "Ask the user to choose a preset style or enter a custom style. This style has top priority and controls supplemental style language, palette language, background texture, character rendering, expression, outfit direction, UI colors, button/icon style, and typography texture.":
            "Resolve the requested preset or custom style from the prompt. This style has top priority and controls supplemental style language, palette language, background texture, character rendering, expression, outfit direction, UI colors, button/icon style, and typography texture.",
        "## STEP 2: Collect player and game info": "## STEP 2: Resolve player and game information",
        "Collect PLAYER 1 name, PLAYER 2 name, and game title.":
            "Resolve PLAYER 1 name, PLAYER 2 name, and the game title from the prompt.",
        "## STEP 6: Refill video prompt and generate with Minimax H3": "## STEP 6: Refill the Minimax H3 video prompt",
        "After approval, load `references/h3-video-prompt-template.md` and refill the final video prompt with confirmed style, character refs, player names, game title, UI text, event timing, motion directions, and negative constraints. Generate the final video with Minimax H3.":
            "Load `references/h3-video-prompt-template.md` and refill the final video prompt with the resolved style, character references, player names, game title, UI text, event timing, motion directions, and negative constraints.",
    },
    "handdrawn_live": {
        "This Skill **organizes the prompt in the user input language and recommends MiniMax H3 as the confirmed generation step**. Do not generate video until the user explicitly confirms H3 generation. Do not route to planner or executor for prompt-writing. The final prompt language must follow the dominant language of the user input: Chinese input produces Chinese, English input produces English, Japanese input produces Japanese; for mixed input, use the dominant language; when unclear, use the current conversation language. Only user-required proper nouns, model names, or literal parameters may remain unchanged.":
            "The final prompt language must follow the dominant language of the user input: Chinese input produces Chinese, English input produces English, Japanese input produces Japanese; for mixed input, use the dominant language; when unclear, use the current conversation language. Only user-required proper nouns, model names, or literal parameters may remain unchanged.",
        "- Unless the user asks for explanation, the final answer should contain the prompt text in the dominant language of the user input first, followed by one short next-step recommendation in the same language.":
            "- Unless the user asks for explanation, output only the prompt text in the dominant language of the user input.",
        "- The recommendation must invite the user, in the same language, to use MiniMax H3 to generate a 15-second 16:9 video from this prompt. Chinese example: `下一步建议：如果你确认这个 prompt，我可以继续用 H3 模型生成 15 秒 16:9 视频。`": "",
        "- Do not generate a video, image, audio, storyboard, or intermediate asset until the user explicitly confirms the H3 generation step.": "",
        "- Mention Seedance only as a target usage context when the user asks; do not add model parameters inside the creative prompt unless requested.": "",
    },
    "minimalist_product_ad": {
        "## Operating Principles":
            "## Input Context\n\nUse the media connected to the node as the available product materials. Use the node's duration and aspect ratio. Resolve product variant, main color, Apple-style template, and in-frame copy from the prompt; when unspecified, use one clearly stated recommended choice. MiniMax H3 is the target video model. Do not invent product identity, logos, materials, mechanisms, colors, or claims that are not visible in the connected media or stated in the prompt.\n\n## Operating Principles",
        "4. **Progress must be visible**\n   - After each step, show what was produced and what decision is needed next.\n   - Do not auto-run the entire pipeline without user confirmation.": "",
        "After the user confirms the copy, proceed to anchor generation. If the user says “you decide,” choose the recommended copy and continue.": "",
        "Show the three independent anchor photos and ask the user to approve, edit, or regenerate a specific photo before proceeding to the precise beat storyboard.": "",
        "After the user confirms the storyboard table, proceed to video generation.": "",
        "Video generation defaults to MiniMax-H3 native audio first, and the Apple-style tech BGM direction below should be written into the video prompt. If H3's native music is unpleasant, too loud, too weak, out of sync, or the user asks for new music, use `music-2.6` to generate a longer standalone instrumental BGM and replace the video audio track. Do not default to ElevenLabs; use ElevenLabs only when the user explicitly requires a strict target duration, and follow the fee-confirmation rule.":
            "Use MiniMax-H3 native audio by default, and write the Apple-style tech BGM direction below directly into the video prompt unless the user explicitly requests silence or a different audio plan.",
        "   - If the current message or current canvas / session already contains materials, state that materials have been detected. Do not ask the user to upload again; only confirm whether to use the current materials.":
            "   - Treat the media connected to the node as the available product materials.",
        "If no product material is available, ask the user to upload it. If material is already available, use it and analyze:":
            "Use the connected product material and analyze:",
        "If the image quality is not usable, stop and give concrete reshoot advice.":
            "If image quality is weak, avoid inventing obscured details and keep the prompt limited to clearly visible product facts.",
        "If the user has not selected a direction, offer 2-3 concise directions, recommend one, and continue after confirmation. If the user says “you decide,” use the recommended one.":
            "If the prompt does not select a direction, infer the strongest concise direction from the product facts and use it consistently.",
        "Generate video directly from the confirmed three independent anchor photos + precise beat text storyboard table. Video style, background, lighting, mood, and pacing follow the selected style. Aspect ratio and size must strictly follow the user-selected setting; if the user chose 16:9, generate 16:9 and do not auto-change to another ratio.":
            "Write the final H3 prompt from the three independent anchor-photo roles and the precise beat text storyboard table. Video style, background, lighting, mood, and pacing follow the selected style. Aspect ratio and size must strictly follow the node setting; if it is 16:9, keep 16:9 and do not change to another ratio.",
        "- Product image too weak: stop, give reshoot guidance, and wait for a better image.":
            "- Product image too weak: avoid inventing product details and restrict the prompt to reliable visible facts.",
        "- Copy too long: compress to 3-5 English words and ask for approval.":
            "- Copy too long: compress it to 3-5 English words.",
        "- If the user provides Chinese copy, translate it into concise English or ask for approval of the English version.":
            "- If the user provides Chinese copy, translate it into concise English while preserving the intended meaning.",
    },
    "music_video_subtitle": {
        "Use this Skill when the user wants to create, revise, audit, or generate music-video prompts or emotional short-film prompts where music, lyrics, typography, references, rhythm, performance, and camera language must be designed together. The workflow adapts MV prompt rules into Hub execution: key creative decisions are confirmed, locked prompts are written to canvas text nodes, and media creation is delegated to Hub agents.":
            "Use this Prompt Guide when the user wants to create, revise, audit, or generate music-video prompts or emotional short-film prompts where music, lyrics, typography, references, rhythm, performance, and camera language must be designed together.",
        "Silently verify before delivery:": "Silently verify before returning the final prompt:",
    },
    "paper_collage": {
        "This Hub-adapted Skill uses Hub-native image, video, audio, and optional postprocess capabilities. It prioritizes style continuity, color harmony, controlled paper texture, stop-motion collage rhythm, and an audio policy that keeps tactile collage SFX by default while explicitly not adding BGM, voiceover, or subtitles unless the user requests them.":
            "This Prompt Guide prioritizes style continuity, color harmony, controlled paper texture, stop-motion collage rhythm, and an audio policy that keeps tactile collage SFX by default while explicitly not adding BGM, voiceover, or subtitles unless requested in the prompt.",
        "2. It is acceptable to ask the user whether they want **voiceover narration/口播**, **BGM**, or **subtitles**, especially for explainers, but present all three as optional add-ons, not defaults.":
            "2. Add **voiceover narration/口播**, **BGM**, or **subtitles** only when explicitly requested in the prompt; all three are optional additions, not defaults.",
        "- Use the approved still as the visual reference / final-frame anchor whenever the selected Hub video model supports it":
            "- Use the resolved still as the visual reference / final-frame anchor",
        "Use `MiniMax-H3` as the default video generation model for this Skill. Do not ask the user to choose a model unless `MiniMax-H3` fails, is unavailable, or cannot satisfy a hard capability requirement. If the user explicitly specified another model, keep that model as primary and adapt parameters only when needed.":
            "Use `MiniMax-H3` as the target model and shape all timing, visual, and audio instructions for H3.",
        "- If generated audio lacks collage SFX but the visual is otherwise strong, ask the user whether to keep it, regenerate with stronger SFX direction, or add/post-sync SFX.":
            "- If the audio plan lacks collage SFX, strengthen the synchronized paper-slide, pop-in, press-flat, rustle, tap, and snap instructions.",
        "- If generated audio contains unwanted BGM or voiceover, remove or regenerate it before final delivery.":
            "- If the prompt could introduce unwanted BGM or voiceover, explicitly forbid them.",
        "After presenting the production plan document, wait for the user to approve, reject, or revise. If the user approves only some numbered items, move only those items forward and revise the rest.": "",
        "## STEP 2: Gate 1 — Production Plan Document Approval": "## STEP 2: Production Plan Document",
        "## STEP 4: Gate 2 — Generate and Approve Still Frames": "## STEP 4: Final Still-Frame Requirements",
        "Generate one final still frame per approved segment. The still must look like the completed last frame of the future animation.":
            "Define one final still frame per segment. The still must look like the completed last frame of the future animation.",
        "After Gate 2 approval, generate one video clip per approved still frame.":
            "Write one video-clip prompt per final still frame.",
        "Before generating any media, create a concise production plan document and stop for user approval. Do not generate stills or videos before the user confirms this document.":
            "Create a concise production plan before writing the final prompt.",
        "Show the generated still frames to the user and stop for approval before video generation. If a still looks too busy, has mismatched color, too many paper layers, too-flat digital edges, or too much aged/brown paper texture, revise the still before video generation.":
            "If a still-frame specification looks too busy, has mismatched color, too many paper layers, overly flat digital edges, or too much aged/brown paper texture, revise the specification before writing the video prompt.",
    },
    "papercraft_stop_motion": {
        "description: For creators explaining science, education, or general knowledge through tactile handmade papercraft visuals. Users provide a topic, core knowledge points, or source material and may specify audience, duration, aspect ratio, and deliverable type. The Skill extracts the learning goal and visual metaphor, proposes creative directions, designs paper characters, layered diorama sets, and props, creates preview concepts plus image and video prompts, and plans storyboards, camera movement, transitions, and sound with staged approvals and review checklists. It outputs a production-ready papercraft stop-motion explainer package, or selected assets such as still prompts, image-series prompts, short-video prompts, or storyboards. Best for cut-paper, pop-up-book, layered diorama, and miniature stop-motion explainers; not for standard 2D cartoons, line doodles, live action, or explainers without a paper-art look.":
            "description: For creators explaining science, education, or general knowledge through tactile handmade papercraft visuals. The Prompt Guide extracts the learning goal and visual metaphor, proposes creative directions, designs paper characters, layered diorama sets, props, preview concepts, storyboards, camera movement, transitions, sound, and review constraints for a production-ready H3 prompt. Best for cut-paper, pop-up-book, layered diorama, and miniature stop-motion explainers; not for standard 2D cartoons, line doodles, live action, or explainers without a paper-art look.",
        "## STEP 8: Plan or Generate 1-3 Visual Preview Images": "## STEP 8: Plan 1-3 Visual Preview Images",
        "Before writing final prompts or storyboards, plan 1 to 3 visual preview images based on the approved creative direction, character design, scene design, and layered staging. If image generation is available and the user wants actual previews, generate them; otherwise provide preview briefs and prompts. These previews are for style and concept confirmation, not final production frames.":
            "Before writing final prompts or storyboards, plan 1 to 3 visual preview images based on the chosen creative direction, character design, scene design, and layered staging. These previews are for style and concept definition, not final production frames.",
        "Use the full phased confirmation workflow only when the user asks for a complete video package, a full production plan, or does not specify a narrower deliverable.": "",
        "After presenting directions, ask the user to choose both the creative direction and the target duration. Duration options should be concise: 15s quick version, 30s standard version, 60s full version, or custom duration. Do not proceed into detailed assets until a duration is chosen.":
            "Choose the creative direction that best fits the prompt and use the duration supplied by the node before defining detailed assets.",
        "After the table, ask the user with a confirmation card: continue to editing rhythm and camera rules, revise storyboard, change duration, or return to visual previews.":
            "After the table, continue to editing rhythm and camera rules only when the storyboard, duration, and visual-preview logic are internally consistent.",
    },
}


REFERENCE_REMOVED_SECTIONS = {
    "3d_animation_short/references/qc-checklist.md": {
        "## Canvas Ordering and Grouping Discipline",
        "## User Choice Card Discipline",
        "## Regeneration and Latest-Asset Discipline",
    },
    "3d_animation_short/references/storyboard-guidelines.md": {
        "### Storyboard approval (both modes)",
    },
}


REFERENCE_OVERRIDES = {
    "3d_animation_short/references/fallback-policy.md": """# H3 Prompt Correction Policy

## Reference-anchor drift

If a shot drifts from the defined `Reference Anchors`—for example a door frame moves to the wrong side, a character exits from the wrong edge, or the lighting direction flips—strengthen the prompt by quoting the exact `Reference Anchors` block from the shot table. Do not accept a prompt that silently mixes corrected and uncorrected spatial states.

If the shot remains unstable, shorten it to six seconds or less, split the dropped duration into an adjacent shot, and re-run the shot-table self-check so the transition and spatial handoff remain explicit.

## Storyboard correction

If a storyboard layout collapses, labels become illegible, panels merge, or character identity drifts, tighten the prompt by explicitly restating the four-quadrant layout, the `[char:…] [scene:…] [shot:…]` labels, and the per-panel content rules. The text storyboard remains authoritative; a visual storyboard must never override its identity, continuity, or timing instructions.
""",
    "3d_animation_short/references/model-selection.md": """# H3 Single-Shot Prompt Preparation

## H3 characteristics

H3 is strong on visual packaging, motion graphics, text and UI clarity, multimodal context understanding, stylized design language, and dialogue-driven beats with native dual-channel audio.

## Prompt binding rules

For every shot, use exactly the matching section from the text storyboard together with the exact character references and exact scene reference named by that shot.

- Preserve the global visual style lock.
- Preserve exact character identity, costume, proportions, colors, and signature props.
- Preserve the scene's fixed continuity landmarks and screen direction.
- Keep per-second actions, camera behavior, dialogue, Foley, sound effects, and music intent explicit.
- Strip all storyboard-only labels (`[char:…]`, `[scene:…]`, `[shot:…]`, `[dur:…]`, `[hook:…]`) from the final video prompt so they cannot appear in-frame.
- The final video must contain only clean full-color animation content and no storyboard borders, arrows, notes, timing marks, or pose ghosts.
- Maintain the aspect ratio, duration, and resolution supplied by the node.

## H3 prompt shaping

For the default stylized 3D direction, emphasize: `Pixar-inspired 3D cartoon rendering, C4D + Octane look, stylized Q-version proportions, warm SSS skin, designed-with-detail hair, strong character design language, clean motion, on-brand color palette`.

H3 follows detailed timing well, so the shot table's per-second directives may be carried into the final prompt with their identity, spatial, performance, and audio anchors intact.
""",
    "3d_animation_short/references/qc-checklist.md": """# H3 Final Prompt Review

## Continuity and audio rules

- Preserve the exact shot order from the standardized shot table.
- Match music to the video's pacing, emotional arc, comedy beats, chase rhythm, and ending tone.
- Duck music under dialogue, non-language reactions, and important sound effects.
- Preserve intended dialogue, Foley, and sound effects unless the prompt explicitly replaces them.
- Do not describe a separate music reset for every shot; maintain one coherent musical arc when music is requested.
- Do not add subtitles or visible text unless explicitly requested.
- Require clean animation visuals with no storyboard traces, including no `[char:…] [scene:…] [shot:…]` labels.

## Final review

Check the final prompt for:

- Character consistency.
- Scene continuity against every `Reference Anchors` entry.
- Emotional-anchor setup and payoff.
- A clear purpose for every shot.
- Intelligible dialogue with exact `<d>...</d>` content preserved.
- Foley and sound-effect timing aligned with the `Audio & Dialogue Track`.
- Balanced music that does not mask dialogue or key sound effects.
- No panel borders, sketch lines, arrows, labels, handwritten notes, timing marks, pose ghosts, storyboard text, or double-binding labels in the visible video.
- No missing shot, weak continuity handoff, stale reference, or contradictory asset description.
""",
}


REFERENCE_EXACT_REPLACEMENTS = {
    "3d_animation_short/references/shot-table-spec.md": {
        "After character cards and scene cards are locked, output standardized video prompts as a shot information table. This step is mandatory and cannot be swapped with storyboard or video generation. Create a canvas table node or markdown table named `标准镜头信息表` or `standard-shot-table`.":
            "After character and scene identities are resolved, output standardized video prompts as a shot information table. This step is mandatory and cannot be swapped with storyboard or final-prompt writing. Use a markdown table named `标准镜头信息表` or `standard-shot-table`.",
        "Then show a user choice card:\n\n- Approve table and run self-check (recommended)\n- Adjust shot continuity\n- Make animation more exaggerated\n- Adjust close-up / extreme-close-up rhythm\n- Adjust Dutch-angle design": "",
        "Before moving to pencil storyboards, run a hard self-check on the approved shot table. If any check fails, revise the table and re-run before asking the user to approve storyboarding.":
            "Before moving to the storyboard structure, run a hard self-check on the shot table. If any check fails, revise the table and re-run the check.",
        "If all six pass, place a `shot-table self-check: passed` stamp at the top of the canvas table node and show the user choice card:\n\n- Approve self-check and draw shot storyboards (recommended)\n- Show self-check details\n- Revise failed checks\n- Re-run self-check":
            "If all six pass, treat the shot table as internally consistent and continue to the storyboard structure.",
        "If any check fails, do not enter Step 6. Return to Step 5, list the failed rows, and only re-show the storyboard approval card after the table is fixed and the self-check passes.":
            "If any check fails, return to Step 5, repair the failed rows, and continue only after the self-check passes.",
    },
    "3d_animation_short/references/storyboard-guidelines.md": {
        "After the Step 5.5 self-check passes, show a storyboard-mode choice card before producing any storyboard artifact:\n\n- **Text storyboards document only (default, recommended)** — one canvas text node containing all shot storyboards as in-document sections. Mirrors the half-narrated-drama storyboard structure: per-shot fields (title / hook / scene / characters / spatial anchors / continuity / performance) plus Pixar's per-panel four-quadrant content + optional ASCII layout. Carries the full quality-control payload at near-zero cost. The video model selected in Step 7 reads this directly as the per-shot rendering reference.\n- **Text storyboards document + multi-panel pencil image (visualization mode, opt-in)** — the text storyboards document is still produced as the authoritative artifact, AND one multi-panel pencil image is generated per shot for human review. Higher cost, useful when the user wants a visual preview before committing to video generation, or when squash-and-stretch / pose silhouette is the main risk and the user wants to pre-check it visually.":
            "After the Step 5.5 self-check passes, use one authoritative text-storyboard document containing all shot storyboards as in-document sections. It mirrors the half-narrated-drama storyboard structure: per-shot fields (title / hook / scene / characters / spatial anchors / continuity / performance) plus Pixar's per-panel four-quadrant content and optional ASCII layout. Optional visual-storyboard descriptions may supplement it for pose and silhouette checks, but they never override the text storyboard.",
        "Generate one canvas text node named `<title> text storyboards` (one document for the whole short). This document is the authoritative rendering reference for Step 7 even when pencil images are also produced. The structure mirrors the half-narrated-drama storyboard — every shot is a section in the same document, so the user can read cross-shot continuity without node-hopping.":
            "Create one text-storyboards document named `<title> text storyboards` for the whole short. This document is the authoritative H3 prompt reference. Every shot is a section in the same document so cross-shot continuity remains explicit.",
        "After all sections are written, place the document on canvas and move directly to Step 7. Do not call any image generation model in default mode.":
            "After all sections are written, use the document as the source for Step 7.",
        "The default single-document form is optimized for reading and cross-shot continuity. When the user flags a specific shot for heavy iteration (typically climax / chase / slapstick beats where the per-panel content needs many rounds of revision), extract that section into a standalone text node so iteration is localized:\n\n- User signal: at any time after Step 6, the user says things like \"let me focus on S05\", \"S05 needs rework\", \"extract S05\", or selects a shot during the storyboard approval choice card.\n- Extraction mechanics:\n  1. Create a new canvas text node named `<title> S05 text storyboard (extracted)`.\n  2. Move the full content of the `## S05` section from the document into the new node.\n  3. In the document, replace the `## S05` section with a one-line placeholder: `> S05 — extracted to standalone node (see `<title> S05 text storyboard (extracted)`)`.\n  4. Step 7 reads from the extracted node for S05; all other shots still read from the document.\n- Re-integration: when the user is satisfied, the standalone node is folded back into the document (replace the placeholder with the latest content) and the standalone node is archived.\n- Multiple extracted shots: each shot gets its own standalone node; the document tracks them with placeholders.\n\nThe extraction mechanism exists because independent nodes are best used by need, not by default — but they remain available whenever iteration pressure is high on a specific shot.":
            "The default single-document form is optimized for reading and cross-shot continuity. When a specific shot needs heavier revision, isolate that shot's section while keeping the single document as the continuity source of truth:\n\n1. Copy the full shot section into an isolated working section.\n2. Keep its shot ID, timing, identity bindings, spatial anchors, and incoming/outgoing continuity unchanged unless the prompt explicitly revises them.\n3. Reintegrate the revised content into the authoritative document before writing the final H3 prompt.",
        "If the user picked the visualization mode in the storyboard-mode choice card, ALSO produce one multi-panel pencil storyboard image per table row on top of the text storyboards document. The text storyboards document remains the authoritative rendering reference; the pencil images are human-review-only.":
            "When visual-storyboard detail is useful, describe one multi-panel pencil storyboard per table row in addition to the text document. The text storyboards document remains authoritative; visual panels are review-only.",
        "If a pencil image storyboard cannot be produced at the required quality (e.g. layout collapses, labels illegible, panels merged, character inconsistency), apply the following escalation before asking the user:":
            "If a pencil-image storyboard specification cannot maintain the required quality—for example the layout collapses, labels become illegible, panels merge, or character identity drifts—apply this correction order:",
        "4. **After three failed attempts on the same shot**: pause and ask the user with a choice card:\n   - Switch to a block-color storyboard (gray boxes for poses, no pencil lines) for the failing shot only.\n   - Drop the pencil image for the failing shot and rely on the text storyboards document alone for that row.\n   - Split the failing shot into two shorter shots in Step 5 and re-run Step 5.5.\n   - Manually supply a reference image to bind instead of generating.":
            "4. **Final fallback**: use a block-color pose layout for that shot, rely on the authoritative text storyboard alone, or split the shot into two shorter shots and re-run Step 5.5. If a connected reference image is available, bind it explicitly instead of inventing one.",
    },
}


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end < 0:
        return "", text
    return text[: end + 5], text[end + 5 :]


def remove_allowed_tools(frontmatter: str) -> str:
    return re.sub(r"(?ms)^allowed-tools:\s*\n(?:^[ \t]*-.*\n)+", "", frontmatter)


def remove_sections(text: str, headings: set[str]) -> str:
    if not headings:
        return text
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    skip_level: int | None = None
    for line in lines:
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line.rstrip("\r\n"))
        if match:
            level = len(match.group(1))
            heading = f"{'#' * level} {match.group(2)}"
            if skip_level is not None and level <= skip_level:
                skip_level = None
            if skip_level is None and heading in headings:
                skip_level = level
                continue
        if skip_level is None:
            output.append(line)
    return "".join(output)


def apply_exact_replacements(text: str, replacements: dict[str, str]) -> str:
    for old, new in replacements.items():
        if old not in text:
            raise RuntimeError(f"Expected official guide text was not found:\n{old[:180]}")
        text = text.replace(old, new)
    return text


def adapt_text(text: str, guide_name: str, removed_sections: set[str], replacements: dict[str, str]) -> str:
    normalized = apply_exact_replacements(text.replace("\r\n", "\n"), replacements)
    frontmatter, body = split_frontmatter(normalized)
    frontmatter = remove_allowed_tools(frontmatter)
    if frontmatter:
        frontmatter = re.sub(r"(?m)^name:\s*.*$", f"name: {guide_name}", frontmatter, count=1)
        frontmatter = re.sub(r"\bThe Skill\b", "The Prompt Guide", frontmatter)
        frontmatter = re.sub(r"\bthe Skill\b", "the Prompt Guide", frontmatter)
        frontmatter = re.sub(r"\bThis Skill\b", "This Prompt Guide", frontmatter)
    body = remove_sections(body, removed_sections)
    body = re.sub(r"\bUse this Skill\b", "Use this Prompt Guide", body)
    body = re.sub(r"\bThis Skill\b", "This Prompt Guide", body)
    body = re.sub(r"\bthe Skill\b", "the Prompt Guide", body)
    body = re.sub(r"\bSkill package\b", "Prompt Guide package", body)
    body = re.sub(r"\n{3,}", "\n\n", body).rstrip() + "\n"
    return frontmatter + body


def copy_and_adapt_guide(destination: str, source: str, guide_name: str) -> None:
    source_dir = SOURCE_ROOT / source
    destination_dir = GUIDES_ROOT / destination
    if not source_dir.is_dir():
        raise FileNotFoundError(source_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    guide_text = (source_dir / "SKILL.md").read_text(encoding="utf-8")
    adapted = adapt_text(
        guide_text,
        guide_name,
        REMOVED_SECTIONS.get(destination, set()),
        EXACT_REPLACEMENTS.get(destination, {}),
    )
    (destination_dir / "guide.md").write_text(adapted, encoding="utf-8", newline="\n")

    source_references = source_dir / "references"
    destination_references = destination_dir / "references"
    if destination_references.exists():
        shutil.rmtree(destination_references)
    if not source_references.is_dir():
        return
    shutil.copytree(source_references, destination_references)
    for path in destination_references.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt"}:
            continue
        relative = path.relative_to(GUIDES_ROOT).as_posix()
        if relative in REFERENCE_OVERRIDES:
            path.write_text(REFERENCE_OVERRIDES[relative].rstrip() + "\n", encoding="utf-8", newline="\n")
            continue
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        text = remove_sections(text, REFERENCE_REMOVED_SECTIONS.get(relative, set()))
        text = apply_exact_replacements(text, REFERENCE_EXACT_REPLACEMENTS.get(relative, {}))
        text = re.sub(r"\bThis Skill\b", "This Prompt Guide", text)
        text = re.sub(r"\bthe Skill\b", "the Prompt Guide", text)
        text = re.sub(r"\bthis Skill\b", "this Prompt Guide", text)
        path.write_text(re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    for destination, (source, guide_name) in GUIDES.items():
        copy_and_adapt_guide(destination, source, guide_name)


if __name__ == "__main__":
    main()
