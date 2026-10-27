# Tommy

A game starring Tommy (no last name), set in Westminster, London.

**Tommy wears his own cartoon model, `assets/tommy-toon.glb`** (the user's "Tommy.glb" from `Documents\Tommy - The GTA Game`), and **the police officer on the door of No. 10 in the cutscene is PC Stephen Marsh** (`assets/stephen-marsh.glb`, from "Stephen Marsh.glb").
- Both are three.js-exported cartoon models built from separate parts with named pivots (Torso, Head, LeftArm, RightArm, LeftLeg, RightLeg) at the shoulders and hips, facing +z, with no skeleton.
- `wearChar(rig, name)` in `buildScene` loads `assets/<name>-glb.txt` (base64; artifacts won't serve .glb), toon-shades it, scales it to the toon rig's height, and swaps the rig's body, torso, arms, legs and head for the model's pivots. So `idle()` and the walk animate it unchanged.
  - Props on the old head and arms (`userData.prop`: the seasonal hats and the sparkler) move across to the model.
  - The toon rigs from `buildTommy()` / `figure()` show until the files load, or if they fail.
- If either model changes, copy it in again and regenerate its `-glb.txt` with `[Convert]::ToBase64String`. Publish with `assets/tommy-toon-glb.txt` and `assets/stephen-marsh-glb.txt` in `files`; the itch build includes them.

**The rigged Tripo model is off** (`USE_GLB = false`). Setting `USE_GLB = true` brings back **the user's model `assets/tommy.glb`**: "tommy model 2.glb" from `Documents\Tommy - The GTA Game`, a Tripo export. It's loaded with GLTFLoader and SkeletonUtils (three r128 examples/js from jsdelivr) and attached by `attachGLB(rig)`.
- Tripo's rig was unusable: the bones had no rest transforms, the template skeleton faced +x, and nearly every vertex was weighted to the hips. `build/rig-glb.py` (run with `py -I`) re-rigs it:
  - it turns the skeleton to face +z, gives the bones pure translations with matching bind matrices, and strips the `mixamorig:` prefix;
  - it recomputes the skin weights from each vertex's distance to the bone segments (best 4, legs kept apart).
  - Rerun it on the original file if the model changes, then regenerate `tommy-glb.txt`.
- The previous Codex model is kept as `assets/tommy-old.glb`.
- The model has lit PBR materials (base colour, roughness/metal and normal maps) and casts shadows. All rest rotations are identity, the model faces +z, and it's scaled to 1.82 m.
- The seasonal hats and the sparkler hang off the toon rig, which is hidden while the model shows, so they don't appear on the model yet.
- `glbAnimate()` poses the bones procedurally: a stride-locked walk/run, an idle with breathing and weight shift, and arms lowered from the A-pose.
- The toon Tommy from `buildTommy()` still exists. It shows only until the file loads, or if it fails. A hand-built "human" version was tried and reverted.
- Artifacts won't serve `.glb`, so the page loads `assets/tommy-glb.txt`: the GLB as base64, decoded with `GLTFLoader.parse`.
  - If `tommy.glb` changes, regenerate the text file: `[Convert]::ToBase64String` of the bytes.
  - Publish with `assets/tommy-glb.txt` in `files`.

## Setting (alternate history)

- The game is set in the present day in an alternate history: the Conservatives beat Labour under Keir Starmer at the 2024 general election, and are still in power.
- Prime Minister **Jordan Andreas** (fictional) is **Rishi Sunak's successor** as Conservative leader and PM.
- Real politicians (Sunak, Starmer) are only mentioned as background. Fictional characters carry the story.

## This folder is the project's permanent home

- Keep all project work here: `C:\Users\HOME\Documents\Claude\Projects\Tommy`.
- Uploaded or attached files often come from other folders (Downloads, Desktop, temp folders). Read them from where they are, and copy anything the project needs into this folder. Never move the session or the project to the folder an upload came from.

## What exists so far

- `tommy-night-run.html`: the 3D main menu (no gameplay yet), built with three.js r128 from cdnjs. It's also published as a private Claude artifact: https://claude.ai/artifact/BZAnqDAhc9cMxuwnSb9tJx. Republish from this file to update that link.
  - The visuals are a toon-shaded 3D Tommy on the Embankment, with Big Ben (showing real London time), Parliament, the London Eye and Westminster Bridge traffic, under the real London sky (see below).
  - The menu is styled like an open-world crime game (GTA-like), without using any real game's names, logos or fonts.
  - **The menu follows the real London sky.** It's no longer night-only.
    - **Time of day:** `sunPosition()` computes the sun over Westminster. The phase is set by sun elevation: day ≥ 6°; dawn or dusk from −4° to 6°, by azimuth (morning or evening); twilight from −12° to −4°; night below −12°.
    - **Weather:** `fetchWeather()` reads live London weather from Open-Meteo (no key; credited in Credits, CC BY 4.0) every 15 minutes, mapped by WMO code in `weatherOf()`. If the fetch fails, the sky still follows the sun.
    - **Scene:** `atmosphere()`/`stepAtm()` in `buildScene` ease between five `PRESET` looks, then apply the weather on top:
      - cloud cover greys the sky and dims the sun;
      - fog thickens the air;
      - rain falls as streaks and makes the paving wet and glossy;
      - snow falls as flakes;
      - storms add lightning flashes.
      - The menu scene looks west across the river (north is +x), so the real sun sets behind Parliament.
    - **UI:** `body.phase-*` shifts the purple accent (`--accent`, `--accent-deep`, `--accent-light`). `body.wx-*` adds rain, snow or fog effects, storm flashes and an overcast dullness to the banner.
      - The HUD shows a weather icon plus "Phase · Weather · °C" under the date.
  - **Special seasons on the menu** (`seasonNow()`, by the London date; `setSeason()` in `buildScene`): Christmas, Halloween, Easter and Bonfire Night.
    - **Christmas** (1 Dec – 6 Jan, Twelfth Night): it snows day and night whatever the real weather ("Christmas snow"). Free roam keeps the real weather (`SKY.wxKind`).
      - Snow settles on the paving, the wall, the bollards and the phone box.
      - There's a decorated tree with a star and spiral lights, fairy lights strung between the lamps, and a Santa hat on Tommy.
      - The UI gets fairy lights along the banner and a snow cap on the logo plate.
    - **Halloween** (31 Oct):
      - Jack-o'-lanterns stand on the wall and beside Tommy, and two flocks of bats fly (round Big Ben and over the river).
      - The sky is orange and purple with ground mist and a big orange moon. Tommy wears a witch's hat.
      - The UI accent turns pumpkin orange, bats fly across the banner, and the HUD shows a pumpkin icon with "Halloween".
    - **Easter** (Good Friday to Easter Monday; Easter Sunday by the Gregorian computus in `seasonNow`):
      - Decorated eggs sit on the wall, on the paving and in a basket by Tommy. Planters of daffodils and tulips line the wall.
      - Pastel bunting hangs between the lamps, blossom petals drift down, and Tommy wears bunny ears.
      - The UI gets pastel colours, bunting on the banner and an egg icon.
    - **Bonfire Night** (5 Nov): a bonfire with flickering flames, a firelight and smoke stands where the Christmas tree goes, and Tommy holds up a sparkler.
      - After dark (when `lights` > .3), a pool of rockets bursts into coloured sparks over the river, to the right of the menu panel.
      - The UI accent turns fiery red and gold, firework bursts play on the banner, and the HUD shows a firework icon.
    - All four seasons keep the real time of day and greet the player once in the feed toast (`SEASONS`).
  - The UI accent is **purple** (`--accent` #A35CF0 / `--accent-deep` #5A27A8, at the user's request). It's used across the menu, subtitles, telescope panel, RUN button and minimap arrow. Tommy's shirt stays blue.
- **Story Mode** (just "Story Mode", no chapter numbers) opens with the cutscene "The Address". It's in the same file. **The PM's cutscene is always at night** (its own fixed scenes, exposure 1.15), whatever the real sky (user's rule). Prime Minister **Jordan Andreas** (Conservative Party; fictional) speaks outside 10 Downing Street, with press and a police officer.
  - Tommy is **not** at the speech. The cutscene opens in Tommy's flat, where the speech plays live on his TV ("LDN News 24").
  - It cuts between the flat and the broadcast. It ends on his locked bedroom door ("Tommy's Room – Keep Out"), with warm light under it.
  - Tommy is **not** asleep. A seductive, dominatrix-style woman behind the door bosses him about, ending with "I want you to rock my world" (5 lines in `HER_LINES`). Keep it suggestive, never explicit.
    - After all 5 of her lines, Tommy has 10 lines of his own: an OG, rude "sigma male" who swears at her, not replies to hers.
      - **Tommy is an anti-hero who protects London, not a villain who wants it** (user's rule). He's been fighting crime on his own and means to clean up the streets. He talks to her conversationally, calls her a hoe and throws her out. He never says "silence" (user's rule). (10 lines in `TOMMY_LINES`, cyan subtitles). His voice clips would be `audio/TOMMY1-10.mp3` (not recorded yet; lines without a clip are timed by length).
  - Andreas has swept-up grey hair, big round eyes, a dark maroon suit, a white shirt, a blue tie, a gold belt buckle and black trousers.
  - His 10 lines are in `LINES`. The key line is "I am willing to help end the war on crime." Camera shots are in `SHOTS` / `LINE_SHOTS`.
- After the woman's lines comes a "The next day" card, then **free roam** in Tommy's home (`buildFree`).
  - **Naming (user's rule):** in anything the player sees, it's **"Tommy's apartment complex"** (his home is "the apartment"), never "penthouse". The code and these notes still say penthouse (`ph`, `P0`, the `tommy-save` marker), which is fine.
  - The penthouse sits 110 m up a tower at world (200, 380). The world is in metres: +x east, +z south, Trafalgar Square at the origin.
  - Central London is laid out with roughly real geography: Trafalgar Square (Nelson's Column, lions, fountains, National Gallery, St Martin-in-the-Fields), Admiralty Arch and The Mall, the Victoria Memorial, Buckingham Palace, Whitehall with Horse Guards and the Cenotaph, Parliament Square, Big Ben, the Palace of Westminster, Westminster Abbey, the Thames, Westminster Bridge, the London Eye and County Hall, plus St James's Park and Green Park.
  - Controls: WASD/arrows to move, Shift to run, drag to turn the camera, E to interact, Esc to pause.
  - **Touch screens** (`pointer:coarse`) get a left thumbstick (analogue: a half push walks slower), a RUN toggle and a gold E button. Drag anywhere else to turn the camera; the camera follows one pointer only.
    - On touch screens the minimap moves to the top-right, with Pause under it. Cutscenes advance by tap, and Skip is a button.
  - The penthouse's inside walls (north, east and the bedroom partition) use **the same slate-blue striped wallpaper as Tommy's flat in the cutscene** (`wallpaper`, at true scale via `boxUV`), with white skirting. The ceiling stays white. Keep the two consistent.
  - There's a minimap with landmark blips, and a telescope on the terrace that cycles through the landmarks with facts. The TV shows the morning news.
    - The minimap is a dark open-world-style street map, north up, with a purple (`--accent`) rim and N/E/S/W letters.
      - Side streets are grey, main roads bright, The Mall red. Parks are green, the Thames and the lake blue, Horse Guards and Trafalgar Square plazas, buildings slate (`MAP` in `buildFree`).
      - Blips are colour-coded: government purple (10, CO, HP, PC), sights gold, the Eye teal, the Tube as a roundel. Off-map blips are spread along the rim (`rimSpread`).
      - Tommy is an accent arrow under a light cone showing the camera's view. The penthouse view is a coloured floor plan with the TV, bed, lift and telescope.
  - A private **lift** on the penthouse's north wall (E) takes Tommy down to the street. He comes out at "The Embankment Tower" lobby door on the tower's south face, world (198, 391.5), and that door takes him back up.
  - At street level he walks the whole map in world coordinates. Buildings (`cityCol`), landmarks and the Thames block him, except on Westminster Bridge. The minimap switches to a city map.
  - The streets use real road surfaces: tarmac textures with UK markings (double yellows, centre dashes, lane lines on main roads) and a red Mall.
    - Granite kerbs (instanced) are broken at junctions. There are black lamp posts on main roads, and zebra crossings with Belisha beacons. Pavements are York stone slabs.
  - The layout is deliberately tidy. An even 100 m street grid with 10 m side streets runs around the main roads (Whitehall, The Mall, the Strand, Northumberland Ave, Pall Mall, Charing Cross Rd, the Embankment, Bridge St/Westminster Bridge, Parliament Square).
    - Each grid cell holds one 78 m mansion block (or four 34 m blocks next to a main road), at even heights of 21/24/27 m with district materials.
    - Whitehall has a continuous 26 m Portland-stone frontage. Don't go back to random scattered buildings. (Soho has its own, finer tidy grid; see below.)
    - On Whitehall's west side, between Horse Guards and the Cenotaph, stand the **Cabinet Office (70 Whitehall)** and **Downing Street** (`DS`).
      - Downing Street is a gated cul-de-sac with Numbers 10–12 in black brick on its north side and a constable on the door of No. 10.
      - It is **inaccessible**: steel gates block it, guarded by three armed police (caps, body armour, carbines). E at the gate gets a "move along" line (`GUARD_LINES`).
      - Both are landmarks on the minimap (`10`, `CO`) and in the telescope.
      - Five civil servants (`servants`) come and go through the Cabinet Office door on staggered loops. They wear suits and lanyards and carry a red despatch box, briefcases or folders.
        - They wait for Tommy and block him.
        - They're flagged `invulnerable` ("unattacked", at the user's request), so any future combat, police or traffic must leave them alone.
  - **Soho** (north of Trafalgar Square, `inSoho()`):
    - Boundaries: Oxford Street (z −1000), Regent Street (Piccadilly Circus (−465,−277) to Oxford Circus (−1010,−1000), `regentX`), Charing Cross Road (x 0, extended north to St Giles Circus), and Coventry Street / Leicester Square to the south.
    - Shaftesbury Avenue runs diagonally to Cambridge Circus (0,−700), and Piccadilly and Haymarket meet at the Circus.
    - The map now reaches z −1150, and the generic grid runs from z −1100.
    - It has **its own tidy grid** of 8 m streets (XS/ZS). Carnaby Street (x −635) is pedestrian-only (`ped`, no cars). Gerrard Street (z −380) is Chinatown; Old Compton Street is z −560.
    - The streets are lined with narrow frontages built by `frontage()`:
      - Each has a brick or stucco facade with sash windows and a made-up shop at street level (`sohoFacade`: café, bar, records…). Signs and windows glow at night (`sohoMats`).
      - Frontages are merged per material into 300 m chunks. Rows face the two diagonals; Regent Street is Portland stone, and Shaftesbury Avenue has three theatres with made-up shows.
    - Landmarks:
      - Piccadilly Circus: a tarmac disc, the Eros fountain, and a building with animated made-up adverts (`sohoTick`, every 4 s).
      - Leicester Square: a garden with railings and trees, and "The Regal" cinema.
      - Chinatown: gates at both ends of Gerrard Street, and red lanterns (`sohoLit`).
      - Rainbow bunting on Old Compton Street.
      - Carnaby Street's neon arch.
      - Soho Square: a garden with the mock-Tudor hut.
      - Centre Point (117 m) at (28,−960).
      - All are telescope and minimap landmarks (PI, LS, CT, SS, CS, CP).
    - Collision is a bucketed index (`colIndex`, 50 m cells) over `cityCol` AABBs plus rotated footprints (`obbs`).
    - Through the telescope the camera clips everything within 25 m (`camera.near`), so terrace plants never block a landmark.
  - **Street life** (`life` in `buildFree`): about 64 cars, black cabs and red double-deckers drive on the left along `roads` and brake for Tommy. Buses stay on main roads. About 100 pedestrians walk the pavements, sidestep each other and Tommy, and never overlap.
    - Everything is pooled within `LIFE_R` of Tommy and recycled out of sight. Cars and people block Tommy.
    - **No traffic softlocks:** a car that moves into Tommy pushes him to its nearest side (`life.pushOut`, never into a wall). If he's still caught inside a car or person (`hitsMoving`), only static collisions (`hitsStatic`) block his steps, so he can always walk out.
    - Pedestrians are the cutscene's cartoon extras: `figure()` sits at `buildScene` level and is shared. 24 looks are baked once into merged, vertex-coloured meshes (one per moving part) and reused, so the crowd stays cheap.
  - **Portcullis House** (`PH`) stands on the corner of Bridge Street and the Embankment, opposite Big Ben.
    - It's sandstone and bronze, with a bronze colonnade along Bridge Street, a pyramid roof and 14 bronze chimneys.
    - **Westminster tube station** (`TUBE`) has entrances under it: in the Bridge Street colonnade and on the Embankment face. They have red-ring/blue-bar "WESTMINSTER" signs and a sign post on the corner.
    - Walking up to an entrance shows "Circle, District and Jubilee lines". The trains don't run yet.
    - Both are minimap (`PC`, `U`) and telescope landmarks.
  - `assets/water.jpg` (the user's water image) textures the Thames and the St James's Park lake, drifting with a ripple normal map.
  - `assets/tree-sheet.jpg` (the user's bark and leaf sheet) is cut at load time: the bark panel becomes the trunk texture, and the leafy branch is chroma-keyed into leaf cards. Trees are instanced and planted in even rows (The Mall, the Embankment, Northumberland Ave) and on a gently jittered lattice in the parks.
  - **Graphics (realistic world, cartoon characters, at the user's choice):**
    - **Sun shadows:** a PCF-soft shadow box follows Tommy, snapped to shadow-map texels (`followSun`). `SUN_DIR` is set from the real sun or moon (`setLightDir`).
      - Lit solid meshes cast and receive. Flat ground layers, glass, unlit materials and the kerbs (`userData.noCast`) don't cast. The leaf cards do (`userData.cast`).
    - **Sky:** a shader with a sun glow and drifting fbm clouds (`skyShader`). The same sky, encoded via `linearToOutputTexel`, is baked by PMREM into `fsc.environment` for reflections.
      - `envMapIntensity` is about .45 on matt materials, .6 on facades and 1 on metal, paint and glass.
    - **Facades** (`facadeOf`) use 256 px tiles with roughness/metalness and bump maps, so the glass is glossy and the windows are recessed with sills. `GLASS` buildings are curtain walls.
      - Every `building()` gets instanced trims: a plinth, a string course at 3 m and a cornice.
    - **Exposure** follows the sky: free roam is .8 by day and 1.15 at night; the menu is .95 by day and 1.15 at night; the cutscene is always 1.15. Pavements are mid-grey York stone.
    - **Graphics Quality** has three levels:
      - Low: pixel ratio 1, no shadows, so the blob shadow under Tommy returns.
      - High: up to 2× resolution, 2048 shadow map over ±75 m.
      - Ultra: up to 3× resolution, 4096 shadow map over ±110 m.
  - **Anti-flicker rules:**
    - The renderer uses `logarithmicDepthBuffer`, and the camera's far plane is 9000.
    - Sky domes use `depthTest:false` + `renderOrder:-1`.
    - Overlapping flat surfaces must never be coplanar: N-S side streets at y .05, E-W at .062, main roads cycling .08/.088/.096, zebras at road y + .014, Tommy's street shadow at .12.
  - Publish the artifact with `assets/water.jpg` and `assets/tree-sheet.jpg` in `files`.
  - **The tutorial is always set in the day** (user's rule). The free roam after "The next day", which is all of free roam for now, uses a fixed mid-morning sun (el 38°, az 118°, `tutorialSky`) under the live weather, whatever the real time.
    - `free.setTutorial(false)` switches free roam to the real time of day, for story parts after the tutorial.
  - **Free roam's sky system** (it follows the real London sky once the tutorial is over; the same `SKY` state as the menu): `skyTarget()`/`skyStep()` in `buildFree`.
    - It eases between five `FREE_SKY` looks, sets the sun to its real position (+x east, +z south) and applies the live weather.
      - Cloud cover greys the sky and hides the sun, stars and moon. Fog, rain and snow close the distance in.
      - Rain streaks and snowflakes wrap in a 40 m box round the camera. They're hidden inside the penthouse.
      - Rain makes the roads and pavements glossy (`wetMats`). Storms flash.
    - The shadow light is the sun, kept at least 10° up, or a fixed moon (`MOON_DIR`) at night. The sky shader draws stars and the moon. Reflections are re-baked by PMREM (`bakeEnv`) after each change, not every frame.
    - At night (`lights`):
      - About a third of facade windows glow (`facadeOf` emissive maps), and Parliament is floodlit.
      - Big Ben's stone and the London Eye glow (`floodMats`).
      - Lamp heads light up and throw additive pools of light (y .118).
      - A soft light follows Tommy, and two lights warm the penthouse.
  - Reaching the penthouse saves progress (`tommy-save` in localStorage), which unlocks Continue in the menu.
- `audio/menu-theme.mp3` is the user's main menu theme ("TOMMY MAIN MENU THEME.mp3"). It loops on the menu at Music Volume, starts on the first click or key press (browser rule), and stops immediately when Story Mode or Continue is picked.
- `audio/`: also holds the user's own voice recordings. `INTRO1-10.mp3` are Jordan Andreas's 10 lines, and `GF1-5.mp3` are the woman's 5 lines (originals in `Documents\Tommy - The GTA Game`).
  - Each cutscene line lasts as long as its clip. TV lines get a "telly speaker" filter, and the woman's lines are muffled through the door.
  - Publish the artifact with these files in `files` (`audio/NAME.mp3`). Subtitles are the written lines in `LINES` / `HER_LINES`.
- `build/wrap.ps1`: wraps the page into a full HTML document at `build/game.html` for local preview.
- `.claude/launch.json`: a local preview server (`tommy`, port 8766) serving `build/`. If the preview pane serves stale content, run `py -m http.server 8766 --directory build` and open `http://localhost:8766/game.html`.

## GitHub

- Private repo: https://github.com/YCPDZN/tommy (branch `main`), so the user can work on the go, for example with Claude Code on the web.
- Commit and push after meaningful changes. Build outputs (zip, exe, `build/game.html`, `build/audio`, `build/assets`) are gitignored.
- The user's GitHub organisation is deliberately not involved.

## Decisions so far

- **`Tommy-itch.zip`** is the itch.io HTML upload, built by `build\make-itch.ps1`. It holds `index.html`, `audio/` and `assets/water.jpg` + `tree-sheet.jpg`, with forward-slash paths. Rebuild it after game changes.
- **The exe was removed again** at the user's request. Its builder still exists (`build\make-exe.ps1` makes `Tommy.exe`); only run it if asked.
  - It's a C# launcher (`build\launcher\TommyLauncher.cs`, compiled with the Windows .NET Framework `csc.exe`). It embeds `build\game.html`, `audio\*.mp3`, `assets\water.jpg` and `assets\tree-sheet.jpg`, and unpacks them to `%LOCALAPPDATA%\Tommy\game`.
  - It serves them from a tiny web server on 127.0.0.1, because file:// pages can't fetch audio or read image pixels, and opens a chromeless Edge app window. The exe exits when that window closes, so Quit Game closes it.
  - It needs internet for three.js and the fonts. The itch.io package is still removed.
- The running/jumping game mechanic was removed. Gameplay beyond the opening cutscene hasn't been designed yet.
