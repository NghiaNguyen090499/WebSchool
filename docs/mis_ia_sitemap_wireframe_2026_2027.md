# MIS 2026-2027 IA Blueprint (Sitemap + Wireframe Content)

## 1) Product Direction
- Positioning: Pioneer school for the "Creative Economy Era".
- Core message: Shift from Knowledge Economy to Creative Economy.
- Education model:
  - Teacher = "Knowledge Architect".
  - Student = "CEO of the Mind", technology leader, AI co-creator.
- UI/UX style:
  - Futuristic, clean, high-tech, human-centric.
  - Card-based layout, short copy, strong visual hierarchy.
  - Interactive content blocks over long paragraphs.

## 2) Global Sitemap (Public Website)

```text
/
|- /about-mis
|- /levels
|  |- /levels/preparation        (Mam non + Tien Tieu hoc)
|  |- /levels/primary            (Tieu hoc)
|  |- /levels/lower-secondary    (THCS)
|  |- /levels/upper-secondary    (THPT)
|- /edtech-ecosystem
|- /parent-portal
|- /admissions
|- /news-events
|- /contact
`- /en/... (optional locale mirror)
```

## 3) Navigation Model
- Top nav:
  - Home
  - Levels
  - EdTech Ecosystem
  - Parent Portal
  - Admissions
  - Contact
- Sticky CTA:
  - "Book Consultation"
  - "Visit Campus"
- Mobile nav:
  - Accordion by level with direct module links.

## 4) Homepage Wireframe

### 4.1 Block Structure
1. Hero: "Knowledge Economy -> Creative Economy"
2. Philosophy Split: Teacher vs Student role transformation
3. Level Navigator Cards (Preparation / Primary / THCS / THPT)
4. AI + Creative Economy Value Strip
5. Featured Projects (student outputs)
6. EdTech Ecosystem teaser
7. Parent Portal teaser (AI-Track)
8. Admissions CTA + Contact CTA

### 4.2 Homepage Wireframe (ASCII)
```text
[HEADER]
[HERO: Big Statement + CTA1 + CTA2]
[PHILOSOPHY SPLIT: Teacher = Architect | Student = Tech Leader]
[LEVEL CARDS x4]
[WHY MIS: AI-integrated | Creative Economy | Global Citizen]
[STUDENT PROJECT CAROUSEL]
[EDTECH TOOLCHAIN PREVIEW]
[PARENT AI-TRACK PREVIEW]
[ADMISSIONS FINAL CTA]
[FOOTER]
```

## 5) Level Page Template (Reusable)

Use one shared template with data-driven blocks.

1. Hero (concept + level promise)
2. Learning Outcomes (3-5 cards)
3. Module Grid (subject modules)
4. Project/Portfolio Block
5. AI Tools Used (logo chips)
6. Language Track Block (if applicable)
7. Parent Insight (how progress is measured)
8. CTA strip

## 6) Preparation Level (Mam non + Tien Tieu hoc)

### 6.1 Page Goal
- "Step-in platform for AI era learning behavior."

### 6.2 Content Blocks
1. Hero: "The Preparation"
2. Module: Digital Familiarity
  - Living things vs machines
  - Device safety basics
3. Module: Foundational Thinking
  - Number and shape recognition
  - Drag-drop logic games
4. Module: Creative Expression
  - Drawing with AI (AutoDraw)
  - Music and emotion activities
5. Parent confidence block
6. CTA: Trial class booking

### 6.3 Card Suggestions
- Card icon set:
  - `fa-seedling` (growth)
  - `fa-shield-heart` (safety)
  - `fa-puzzle-piece` (logic)
  - `fa-palette` (creativity)

## 7) Primary Level (Khai pha & Cam thu so)

### 7.1 Concept
- Gamification-first learning.

### 7.2 Content Blocks
1. Hero: "Learn by Playing, Think by Building"
2. Module: Practical Math
  - Market modeling, time reading
  - Tool references: DeepSeek Math, Nexta Tablet
3. Module: Language Growth
  - English: Cambridge Movers/Flyers
  - Chinese: YCT 1-3
  - Storytelling and song-based learning
4. Module: Technology Foundations
  - Scratch Junior
  - 10-finger typing
  - IC3 Spark pathway
5. Mini project gallery
6. CTA strip

### 7.3 UI Notes
- Gamified progress chips per module.
- "Unlock next challenge" interaction pattern.

## 8) THCS Level (Tu duy he thong & Sang tao so)

### 8.1 Concept
- Critical thinking + debate + digital production.

### 8.2 Content Blocks
1. Hero: "System Thinking and Digital Creation"
2. Module: Math & Science
  - Big Data basics
  - 3D geometry with GeoGebra
  - Intro Python
3. Module: Literature
  - Script writing
  - School magazine
  - Mind-map thinking
4. Real-world Projects
  - Infographic
  - Digital Math Handbook
  - Deepfake/Fake-news warning project
5. Language Track
  - IELTS 4.0-6.0+
  - HSK 1-3
6. Debate showcase block
7. CTA strip

### 8.3 Icon/Logo Suggestions
- Python, GeoGebra, data chart, debate mic, shield-check.

## 9) THPT Level (Dinh huong nghe nghiep & Chuyen sau)

### 9.1 Concept
- Master technology, build future pathway.

### 9.2 Content Blocks
1. Hero: "Career-Ready in the Creative Economy"
2. STEM + AI Module
  - Data Science
  - Digital Finance
  - Machine Learning model training
3. Digital Portfolio Module
  - Student project archive
  - University application-ready profile
4. Advanced Language Module
  - Academic Writing
  - IELTS 6.5-8.0+
  - HSK 4-6
  - Scholarship strategy
5. University/Career pathway cards
6. CTA strip

### 9.3 Feature Requirement
- Portfolio card states:
  - Draft
  - Published
  - Mentor-reviewed
  - Application-ready

## 10) EdTech Ecosystem Page

### 10.1 Goal
- Explain the MIS technology stack in one place.

### 10.2 Content Blocks
1. Hero: "Technology that powers human growth"
2. Tool Grid (interactive cards):
  - Azota: exam management, AI-assisted grading
  - Nexta: smart classroom, personalized tablets
  - iCorrect + Doubao: 24/7 speaking assistant
  - VR/AR: virtual lab, space exploration
3. "How data flows" visual map (student -> teacher -> parent)
4. Safety & ethics block
5. CTA: Request campus demo

## 11) Parent Portal Page

### 11.1 Goal
- Build parent trust through transparent real-time progress.

### 11.2 Content Blocks
1. Hero: "Parent Portal powered by AI-Track"
2. AI-Track Dashboard Preview
  - Real-time learning progress
  - Skill heatmap (not only scores)
3. Personalized Competency Report
  - Problem-solving
  - Collaboration
  - Critical thinking
  - Communication
4. Recommended next actions
5. CTA: Parent account onboarding

### 11.3 Feature Notes
- Do not present only score chart.
- Show "skill trajectory + evidence artifacts".

## 12) Content-Block Data Model (for CMS/JSON)

```json
{
  "page_key": "levels_primary",
  "year": "2026-2027",
  "hero": {
    "title": "Primary - Explore and Feel Digital Learning",
    "subtitle": "Gamified pathways for creative problem solving",
    "cta_primary": "Book Consultation",
    "cta_secondary": "View Modules"
  },
  "blocks": [
    {
      "type": "module_grid",
      "title": "Practical Math",
      "items": [
        {
          "title": "Market Math Simulation",
          "tools": ["DeepSeek Math", "Nexta Tablet"],
          "icon": "python"
        }
      ]
    }
  ],
  "metadata": {
    "keywords": ["AI-integrated", "Creative Economy", "Global Citizen"],
    "source": "MIS 2026-2027 strategy"
  }
}
```

## 13) Interaction Guidelines
- Keep sections scannable:
  - 1 headline + 1 short descriptor + card set.
- Use tabs for module switching by grade bands.
- Use micro-interaction:
  - hover reveal for tools
  - progress animation in AI-Track preview
  - timeline scroll for level pathways
- Accessibility:
  - color contrast AA
  - keyboard-focusable interactive cards
  - icon + text labels, never icon-only semantics

## 14) Suggested Asset List
- AI and STEM logos/icons:
  - Python
  - GeoGebra
  - DeepSeek
  - Nexta
  - Azota
  - VR/AR symbols
- Photo themes:
  - collaboration
  - maker projects
  - classroom technology
  - mentoring moments

## 15) Delivery Recommendation
- Phase 1 (2-3 weeks):
  - Implement sitemap routes + shared level page template.
  - Build Home + 4 level pages + EdTech + Parent Portal skeleton.
- Phase 2:
  - Add AI-Track interactive mock dashboard.
  - Add Digital Portfolio gallery filter and detail pages.
- Phase 3:
  - Integrate analytics events for module interaction and CTA tracking.
