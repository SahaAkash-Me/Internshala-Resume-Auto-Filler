"""
╔══════════════════════════════════════════════════════════════╗
║   INTERNSHALA RESUME AUTO-FILLER — AKASH SAHA (v8 FINAL)   ║
╚══════════════════════════════════════════════════════════════╝
HOW TO RUN:
    1. Set your PASSWORD below
    2. cd Downloads
    3. python internshala_resume_filler.py
"""

import time
from playwright.sync_api import sync_playwright

# ════════════════════════════════════════════
#  🔐  YOUR CREDENTIALS
# ════════════════════════════════════════════
EMAIL    = "random@mail.com"
PASSWORD = "Enter Your Password Here"   # ← CHANGE THIS

# ════════════════════════════════════════════
#  📋  RESUME CONTENT
# ════════════════════════════════════════════

CAREER_OBJECTIVE = (
    "Analytics professional with 4.5+ years in Fraud Detection, KYC Compliance, "
    "and Data Analysis at Amazon and Wipro. Built a SQL Data Warehouse using ETL "
    "pipelines. Targeting a Data Analyst role."
)  # 192 chars ✅

# Job descriptions as bullet points (each item = one bullet)
AMAZON_BULLETS = [
    "Screened 1000+ seller accounts monthly for fraud patterns, boosting enforcement accuracy by 20%",
    "Wrote SQL queries to flag suspicious activity and irregular pricing",
    "Built spam resolution model cutting manual processing time by 35%",
    "Drove 10+ process changes as Process Improvement POC, reducing errors by 20%",
    "Ran 8-10 live KYC video sessions daily across 4 markets with 98% decision accuracy",
    "Trained 60+ colleagues across 3 sites. Received Make A Difference Award",
]

WIPRO_BULLETS = [
    "Handled 40+ daily infrastructure damage cases for UK telecom sites (Openreach)",
    "Built Excel tracking dashboards cutting data entry errors by 18%",
    "Maintained SLA delivery above 95% every month across all operational streams",
    "Managed escalations from 5+ Operations teams with 90%+ customer satisfaction scores",
    "Created manual Excel reporting workflows during outages — zero downtime across 3 incidents",
]

PROJECT_BULLETS = [
    "Built end-to-end SQL Server data warehouse using Medallion Architecture (Bronze, Silver, Gold layers)",
    "Designed ETL pipelines to ingest raw CRM and ERP CSV files with full audit trail",
    "Created Star Schema with 15+ analytical SQL views for KPI tracking and business queries",
]

ACCOMPLISHMENTS = (
    "Cut error rates by 20% at Amazon via audit cycles. Trained 60+ staff across 3 countries. "
    "Drove 10+ process changes saving time. Received Make A Difference Award. "
    "Maintained 95%+ SLA at Wipro. Achieved 98% KYC accuracy."
)  # 218 chars ✅

SKILLS_TO_ADD = [
    "MySQL", "DAX", "Data Warehousing", "Data Cleaning",
    "Root Cause Analysis", "Stakeholder Management",
    "Data Analysis", "Business Intelligence",
    "Data Visualization", "Microsoft Excel", "Statistics", "ETL",
]


# ════════════════════════════════════════════
#  🛠  UTILITIES
# ════════════════════════════════════════════
def wait(s=1.5):
    time.sleep(s)

def log(msg):
    print(f"  {msg}")

def close_modal(page):
    try:
        for sel in ['.close', 'button[data-dismiss="modal"]', 'button.close']:
            try:
                for btn in page.locator(sel).all():
                    if btn.is_visible():
                        btn.click()
                        wait(0.5)
                        return
            except Exception:
                pass
        page.keyboard.press("Escape")
        wait(0.8)
    except Exception:
        pass

def click_update_or_save(page):
    """Click Update or Save button — Internshala uses 'Update' for job edits."""
    for sel in [
        'button:has-text("Update")',
        'input[value="Update"]',
        'button:has-text("Save")',
        'button[type="submit"]',
        'input[type="submit"]',
        '.btn-primary',
    ]:
        try:
            for btn in page.locator(sel).all():
                if btn.is_visible():
                    btn.click()
                    log("✅ Clicked Update/Save")
                    wait(2.5)
                    return True
        except Exception:
            continue
    log("⚠️  Update/Save button not found")
    return False

def click_pencil_near(page, keyword):
    """Click the pencil edit icon near a keyword using JS."""
    result = page.evaluate(f"""
        () => {{
            const walker = document.createTreeWalker(
                document.body, NodeFilter.SHOW_TEXT, null, false
            );
            while (walker.nextNode()) {{
                const node = walker.currentNode;
                if (!node.textContent.trim().includes('{keyword}')) continue;
                let el = node.parentElement;
                for (let i = 0; i < 10; i++) {{
                    if (!el || el === document.body) break;
                    const triggers = el.querySelectorAll(
                        'a.edit_link, a[data-toggle="modal"], button[data-toggle="modal"], ' +
                        'i.fa-pencil, i.fa-edit, .edit-btn, span.glyphicon-pencil'
                    );
                    for (const t of triggers) {{
                        const clickable = t.closest('a, button') || t;
                        if (clickable.offsetParent !== null) {{
                            clickable.click();
                            return 'success';
                        }}
                    }}
                    el = el.parentElement;
                }}
            }}
            return 'not found';
        }}
    """)
    return result

def wait_for_modal(page, timeout=8):
    """Wait until the Job Details modal is fully open."""
    for _ in range(timeout * 2):
        time.sleep(0.5)
        try:
            # Check if modal is visible by looking for the Update button
            for sel in ['button:has-text("Update")', 'button:has-text("Save")',
                        '.modal.in', '.modal.show']:
                items = page.locator(sel).all()
                for item in items:
                    if item.is_visible():
                        return True
        except Exception:
            pass
    return False

def fill_rich_text_bullets(page, bullets):
    """
    Fill Internshala's rich text bullet editor.
    The editor is a contenteditable div below the formatting buttons.
    Each bullet point is typed on a new line.
    """
    # Wait for modal to open
    if not wait_for_modal(page, timeout=8):
        log("⚠️  Modal did not open in time")
        return False

    wait(1)

    # Try to find the contenteditable div (the actual typing area)
    filled = page.evaluate(f"""
        () => {{
            // Find all contenteditable divs
            const editors = document.querySelectorAll(
                'div[contenteditable="true"], ' +
                '[role="textbox"], ' +
                '.ql-editor, ' +
                '.note-editable, ' +
                '.fr-element'
            );

            for (const editor of editors) {{
                if (editor.offsetParent === null) continue; // skip hidden

                // Clear existing content
                editor.focus();
                editor.innerHTML = '';

                // Build bullet HTML
                const bullets = {str(bullets).replace("'", '"')};
                const ul = document.createElement('ul');
                bullets.forEach(text => {{
                    const li = document.createElement('li');
                    li.textContent = text;
                    ul.appendChild(li);
                }});
                editor.appendChild(ul);

                // Trigger React/Vue change events
                editor.dispatchEvent(new Event('input', {{bubbles: true}}));
                editor.dispatchEvent(new Event('change', {{bubbles: true}}));

                return 'filled with ' + bullets.length + ' bullets';
            }}
            return 'editor not found';
        }}
    """)

    log(f"  JS fill result: {filled}")

    if "filled" in filled:
        wait(0.5)
        return True

    # Fallback: click into editor and type manually
    log("  Trying keyboard fallback...")
    try:
        # Find the contenteditable div
        editor = page.locator(
            'div[contenteditable="true"], [role="textbox"], .ql-editor'
        ).first

        if editor.is_visible(timeout=3000):
            editor.click()
            wait(0.3)

            # Select all and delete
            page.keyboard.press("Control+a")
            wait(0.1)
            page.keyboard.press("Delete")
            wait(0.2)

            # Type each bullet
            for i, bullet in enumerate(bullets):
                page.keyboard.type(bullet, delay=15)
                if i < len(bullets) - 1:
                    page.keyboard.press("Enter")
                    wait(0.1)

            log(f"  ✅ Typed {len(bullets)} bullets via keyboard")
            wait(0.5)
            return True

    except Exception as e:
        log(f"  ⚠️  Keyboard fallback failed: {e}")

    return False

def fill_simple_textarea(page, text):
    """Fill a simple textarea (for Career Objective, Accomplishments)."""
    for _ in range(12):
        time.sleep(0.5)
        try:
            for ta in page.locator("textarea").all():
                if ta.is_visible():
                    ta.click()
                    wait(0.2)
                    ta.press("Control+a")
                    ta.fill(text)
                    log(f"✅ Filled textarea ({len(text)} chars)")
                    return True
        except Exception:
            pass
    log("⚠️  Textarea not found")
    return False


# ════════════════════════════════════════════
#  🔑  LOGIN
# ════════════════════════════════════════════
def login(page):
    print("\n━━━ STEP 1: LOGIN ━━━━━━━━━━━━━━━━━━━━━━━━━")
    page.goto("https://internshala.com/login/student")
    wait(2)
    try:
        page.locator('input[type="email"]').first.fill(EMAIL)
        wait(0.3)
        page.locator('input[type="password"]').first.fill(PASSWORD)
        wait(0.3)
        page.locator('button[type="submit"]').first.click()
        wait(3)
        log("✅ Login submitted")
    except Exception as e:
        log(f"❌ Login error: {e}")


# ════════════════════════════════════════════
#  🎯  CAREER OBJECTIVE
# ════════════════════════════════════════════
def fill_career_objective(page):
    print("\n━━━ STEP 2: CAREER OBJECTIVE ━━━━━━━━━━━━━━")
    try:
        page.locator("text=Add your career objective").first.click(timeout=4000)
        log("✅ Clicked Add career objective")
    except Exception:
        result = click_pencil_near(page, "CAREER OBJECTIVE")
        log(f"  Pencil JS: {result}")
    wait(2.5)
    if fill_simple_textarea(page, CAREER_OBJECTIVE):
        click_update_or_save(page)


# ════════════════════════════════════════════
#  🏆  ACCOMPLISHMENTS
# ════════════════════════════════════════════
def fill_accomplishments(page):
    print("\n━━━ STEP 3: ACCOMPLISHMENTS ━━━━━━━━━━━━━━━")
    try:
        page.locator("text=Add accomplishment/ additional detail").first.click(timeout=5000)
        log("✅ Clicked Add accomplishment")
        wait(2.5)
        if fill_simple_textarea(page, ACCOMPLISHMENTS[:245]):
            click_update_or_save(page)
    except Exception as e:
        log(f"⚠️  Accomplishments error: {e}")


# ════════════════════════════════════════════
#  💼  WORK EXPERIENCE
# ════════════════════════════════════════════
def update_work_experience(page):
    print("\n━━━ STEP 4: WORK EXPERIENCE ━━━━━━━━━━━━━━━")

    jobs = [
        {
            "keyword" : "Fraud Inveatisgation Specialist",
            "label"   : "Amazon",
            "bullets" : AMAZON_BULLETS,
        },
        {
            "keyword" : "Case Manager",
            "label"   : "Wipro",
            "bullets" : WIPRO_BULLETS,
        },
    ]

    for job in jobs:
        log(f"Editing: {job['label']}")

        # Scroll to the entry
        try:
            page.locator(f"text={job['keyword']}").first.scroll_into_view_if_needed()
            wait(0.5)
        except Exception:
            pass

        # Click the pencil icon
        result = click_pencil_near(page, job["keyword"])
        log(f"  Pencil JS: {result}")

        if result == "not found":
            log(f"  ⚠️  Pencil not found for {job['label']}")
            continue

        # Wait for modal + fill bullets
        if fill_rich_text_bullets(page, job["bullets"]):
            click_update_or_save(page)
            log(f"✅ {job['label']} updated successfully")
        else:
            log(f"⚠️  Could not fill {job['label']} description")
            close_modal(page)

        wait(1)


# ════════════════════════════════════════════
#  🚀  PROJECT
# ════════════════════════════════════════════
def update_project(page):
    print("\n━━━ STEP 5: PROJECT ━━━━━━━━━━━━━━━━━━━━━━━")

    try:
        page.locator("text=Data Warehouse Architecture Project").first.scroll_into_view_if_needed()
        wait(0.5)
    except Exception:
        pass

    result = click_pencil_near(page, "Data Warehouse Architecture Project")
    log(f"  Pencil JS: {result}")

    if result == "not found":
        log("  ⚠️  Pencil not found for project")
        return

    if fill_rich_text_bullets(page, PROJECT_BULLETS):
        click_update_or_save(page)
        log("✅ Project updated successfully")
    else:
        log("⚠️  Could not fill project description")
        close_modal(page)


# ════════════════════════════════════════════
#  🏅  SKILLS
# ════════════════════════════════════════════
def fill_skills(page):
    print("\n━━━ STEP 6: SKILLS ━━━━━━━━━━━━━━━━━━━━━━━")
    existing = page.inner_text("body").lower()
    added = 0

    for skill in SKILLS_TO_ADD:
        if skill.lower() in existing:
            log(f"⏭  Already exists: {skill}")
            continue

        log(f"Adding: {skill}")
        try:
            page.locator("text=Add skill").first.click(timeout=5000)
            wait(1.5)

            inp = page.locator(
                'input[placeholder="e.g. Adobe Photoshop"], '
                'input[placeholder*="Adobe"], '
                'input[placeholder*="skill" i]'
            ).first
            inp.wait_for(state="visible", timeout=4000)
            inp.click()
            wait(0.3)
            inp.type(skill, delay=100)
            wait(2.5)

            clicked = False
            for sel in [
                f'ul.ui-autocomplete li:has-text("{skill}")',
                f'.ui-autocomplete li:has-text("{skill}")',
                f'ul[role="listbox"] li:has-text("{skill}")',
                f'.autocomplete-suggestions div:has-text("{skill}")',
            ]:
                try:
                    opt = page.locator(sel).first
                    if opt.is_visible(timeout=1500):
                        opt.click()
                        clicked = True
                        log(f"  ✅ Dropdown selected")
                        wait(0.8)
                        break
                except Exception:
                    continue

            if not clicked:
                try:
                    for item in page.locator("ul.ui-autocomplete li").all():
                        if item.is_visible() and skill.lower() in item.inner_text().lower():
                            item.click()
                            clicked = True
                            log(f"  ✅ Fallback selected")
                            wait(0.8)
                            break
                except Exception:
                    pass

            if not clicked:
                log(f"  ⚠️  '{skill}' not in dropdown — skipping")
                close_modal(page)
                continue

            for btn_sel in ['button:has-text("Add")', 'input[value="Add"]',
                            'button[type="submit"]', '.btn-primary']:
                try:
                    btn = page.locator(btn_sel).first
                    if btn.is_visible(timeout=1500):
                        btn.click()
                        log(f"  ✅ Saved: {skill}")
                        wait(1.5)
                        break
                except Exception:
                    continue

            added += 1
            existing = page.inner_text("body").lower()

        except Exception as e:
            log(f"  ⚠️  Failed '{skill}': {e}")
            close_modal(page)

    log(f"\n  Skills done — added {added} new skills.")


# ════════════════════════════════════════════
#  🎬  MAIN
# ════════════════════════════════════════════
def main():
    print("""
╔══════════════════════════════════════════════╗
║  INTERNSHALA RESUME FILLER v8 — Akash Saha  ║
╚══════════════════════════════════════════════╝""")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        try:
            login(page)

            input("""
  ⏸  PAUSED — Check the browser window.
     Solve any CAPTCHA / OTP if shown.
     Press ENTER when you are logged in ... """)

            page.goto("https://internshala.com/student/resume?detail_source=resume_direct")
            wait(3)

            fill_career_objective(page)
            fill_accomplishments(page)
            update_work_experience(page)
            update_project(page)
            fill_skills(page)

            print("""
╔══════════════════════════════════════════════╗
║  ✅ ALL DONE! Check your resume in browser. ║
╚══════════════════════════════════════════════╝""")
            input("\n  Press ENTER to close browser ...")

        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("  Press ENTER to close ...")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
