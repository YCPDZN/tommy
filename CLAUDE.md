# Tommy

A game starring Tommy (no last name), set in Westminster, London.

**Right now Tommy uses the cartoon model** (`USE_GLB = false`, at the user's request "for now"). Setting `USE_GLB = true` brings back **the user's rigged model `assets/tommy.glb`** (from Codex: `Documents\Codex\2026-10-25\ma\outputs\character-rigged.glb`). It's loaded with GLTFLoader and SkeletonUtils (three r128 examples/js from jsdelivr) and attached by `attachGLB(rig)`.
- The model has a photo-projected face and clothes (unlit materials) and a Mixamo-style 64-bone skeleton. All rest rotations are identity, the model faces +z, and it's scaled to 1.82 m.
- `glbAnimate()` poses the bones procedurally: a stride-locked walk/run, an idle with breathing and weight shift, and arms lowered from the A-pose.
- The toon Tommy from `buildTommy()` still exists. It shows only until the file loads, or if it fails. A hand-built "human" version was tried and reverted.
- Artifacts won't serve `.glb`, so the page loads `assets/tommy-glb.txt`: the GLB as base64, decoded with `GLTFLoader.parse`.
  - If `tommy.glb` changes, regenerate the text file: `[Convert]::ToBase64String` of the bytes.
  - Publish with `assets/tommy-glb.txt` in `files`.

## This folder is the project's permanent home

- Keep all project work here: `C:\Users\HOME\Documents\Claude\Projects\Tommy`.
- Uploaded or attached files often come from other folders (Downloads, Desktop, temp folders). Read them from where they are, and copy anything the project needs into this folder. Never move the session or the project to the folder an upload came from.

## What exists so far

- `tommy-night-run.html`: the 3D main menu (no gameplay yet), built with three.js r128 from cdnjs. It's also published as a private Claude artifact: https://claude.ai/artifact/BZAnqDAhc9cMxuwnSb9tJx. Republish from this file to update that link.
  - The visuals are a toon-shaded 3D Tommy on the Embankment, with Big Ben (showing real London time), Parliament, the London Eye and Westminster Bridge traffic.
  - The menu is styled like an open-world crime game (GTA-like), without using any real game's names, logos or fonts.
- **Story Mode** (just "Story Mode", no chapter numbers) opens with the cutscene "The Address". It's in the same file. Prime Minister **Jordan Andreas** (Conservative Party; fictional) speaks outside 10 Downing Street, with press and a police officer.
  - Tommy is **not** at the speech. The cutscene opens in Tommy's flat, where the speech plays live on his TV ("LDN News 24").
  - It cuts between the flat and the broadcast. It ends on his locked bedroom door ("Tommy's Room – Keep Out"), with warm light under it.
  - Tommy is **not** asleep. A woman behind the door teases him: "You're such a naughty man, Tommy" (5 lines in `HER_LINES`). Keep it suggestive, never explicit.
  - Andreas has swept-up grey hair, big round eyes, a dark maroon suit, a white shirt, a blue tie, a gold belt buckle and black trousers.
  - His 10 lines are in `LINES`. The key line is "I am willing to help end the war on crime." Camera shots are in `SHOTS` / `LINE_SHOTS`.
- After the woman's lines comes a "The next day" card, then **free roam** in Tommy's penthouse (`buildFree`).
  - The penthouse sits 110 m up a tower at world (200, 380). The world is in metres: +x east, +z south, Trafalgar Square at the origin.
  - Central London is laid out with roughly real geography: Trafalgar Square (Nelson's Column, lions, fountains, National Gallery, St Martin-in-the-Fields), Admiralty Arch and The Mall, the Victoria Memorial, Buckingham Palace, Whitehall with Horse Guards and the Cenotaph, Parliament Square, Big Ben, the Palace of Westminster, Westminster Abbey, the Thames, Westminster Bridge, the London Eye and County Hall, plus St James's Park and Green Park.
  - Controls: WASD/arrows to move, Shift to run, drag to turn the camera, E to interact, Esc to pause.
  - **Touch screens** (`pointer:coarse`) get a left thumbstick (analogue: a half push walks slower), a RUN toggle and a gold E button. Drag anywhere else to turn the camera; the camera follows one pointer only.
    - On touch screens the minimap moves to the top-right, with Pause under it. Cutscenes advance by tap, and Skip is a button.
  - There's a minimap with landmark blips, and a telescope on the terrace that cycles through the landmarks with facts. The TV shows the morning news.
  - A private **lift** on the penthouse's north wall (E) takes Tommy down to the street. He comes out at "The Embankment Tower" lobby door on the tower's south face, world (198, 391.5), and that door takes him back up.
  - At street level he walks the whole map in world coordinates. Buildings (`cityCol`), landmarks and the Thames block him, except on Westminster Bridge. The minimap switches to a city map.
  - The streets use real road surfaces: tarmac textures with UK markings (double yellows, centre dashes, lane lines on main roads) and a red Mall.
    - Granite kerbs (instanced) are broken at junctions. There are black lamp posts on main roads, and zebra crossings with Belisha beacons. Pavements are York stone slabs.
  - The layout is deliberately tidy. An even 100 m street grid with 10 m side streets runs around the main roads (Whitehall, The Mall, the Strand, Northumberland Ave, Pall Mall, Charing Cross Rd, the Embankment, Bridge St/Westminster Bridge, Parliament Square).
    - Each grid cell holds one 78 m mansion block (or four 34 m blocks next to a main road), at even heights of 21/24/27 m with district materials.
    - Whitehall has a continuous 26 m Portland-stone frontage. Don't go back to random scattered buildings.
    - On Whitehall's west side, between Horse Guards and the Cenotaph, stand the **Cabinet Office (70 Whitehall)** and **Downing Street** (`DS`).
      - Downing Street is a gated cul-de-sac with Numbers 10–12 in black brick on its north side and a constable on the door of No. 10.
      - It is **inaccessible**: steel gates block it, guarded by three armed police (caps, body armour, carbines). E at the gate gets a "move along" line (`GUARD_LINES`).
      - Both are landmarks on the minimap (`10`, `CO`) and in the telescope.
      - Five civil servants (`servants`) come and go through the Cabinet Office door on staggered loops. They wear suits and lanyards and carry a red despatch box, briefcases or folders.
        - They wait for Tommy and block him.
        - They're flagged `invulnerable` ("unattacked", at the user's request), so any future combat, police or traffic must leave them alone.
  - **Street life** (`life` in `buildFree`): about 64 cars, black cabs and red double-deckers drive on the left along `roads` and brake for Tommy. Buses stay on main roads. About 100 pedestrians walk the pavements, sidestep each other and Tommy, and never overlap.
    - Everything is pooled within `LIFE_R` of Tommy and recycled out of sight. Cars and people block Tommy.
    - Pedestrians are the cutscene's cartoon extras: `figure()` sits at `buildScene` level and is shared. 24 looks are baked once into merged, vertex-coloured meshes (one per moving part) and reused, so the crowd stays cheap.
  - **Portcullis House** (`PH`) stands on the corner of Bridge Street and the Embankment, opposite Big Ben.
    - It's sandstone and bronze, with a bronze colonnade along Bridge Street, a pyramid roof and 14 bronze chimneys.
    - **Westminster tube station** (`TUBE`) has entrances under it: in the Bridge Street colonnade and on the Embankment face. They have red-ring/blue-bar "WESTMINSTER" signs and a sign post on the corner.
    - Walking up to an entrance shows "Circle, District and Jubilee lines". The trains don't run yet.
    - Both are minimap (`PC`, `U`) and telescope landmarks.
  - `assets/water.jpg` (the user's water image) textures the Thames and the St James's Park lake, drifting with a ripple normal map.
  - `assets/tree-sheet.jpg` (the user's bark and leaf sheet) is cut at load time: the bark panel becomes the trunk texture, and the leafy branch is chroma-keyed into leaf cards. Trees are instanced and planted in even rows (The Mall, the Embankment, Northumberland Ave) and on a gently jittered lattice in the parks.
  - **Anti-flicker rules:**
    - The renderer uses `logarithmicDepthBuffer`, and the camera's far plane is 9000.
    - Sky domes use `depthTest:false` + `renderOrder:-1`.
    - Overlapping flat surfaces must never be coplanar: N-S side streets at y .05, E-W at .062, main roads cycling .08/.088/.096, zebras at road y + .014, Tommy's street shadow at .12.
  - Publish the artifact with `assets/water.jpg` and `assets/tree-sheet.jpg` in `files`.
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
